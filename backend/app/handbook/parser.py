"""Handbook PDF parser using IBM Docling for hierarchical structure extraction.

Two-phase approach:
  Phase 1 (deterministic): Docling converts the PDF into a hierarchical document.
      Heading patterns detect per-module section boundaries.
  Phase 2 (LLM-assisted): An LLM extracts structured fields from each module
      section for ambiguous content (ECTS from prose text, level classification,
      description/outcomes/contents extraction from unstructured text).

Docling is intentionally imported *lazily* inside the async method so that the
API server process (which never calls this code) does not pay the ~200 MB model
load overhead.
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import re
from typing import Any

from app.config import Settings
from app.handbook.schemas import HandbookEntryData
from app.llm.port import LLMPort

_logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# LLM prompt for per-module structured extraction
# ---------------------------------------------------------------------------

_MODULE_EXTRACT_PROMPT = """\
You receive raw text from one section of a university module handbook.
Extract the following fields and return a single JSON object.

Fields to extract:
- "module_code": alphanumeric module identifier (e.g. "IN0001"), or null if absent
- "module_title": German module title (full, including Roman numerals if present)
- "module_title_en": English title if present, else null
- "description": 1-4 sentence summary of the module
- "learning_outcomes": what students will be able to do after completing the module
- "contents": list of main topics covered, as a single string
- "prerequisites": required prior knowledge or modules, or null
- "ects": credit points as a number (e.g. 6.0), or null if not found
- "level": "bachelor", "master", or "phd" — infer from context; null if unclear
- "language": "de" if German, "en" if English, null if unclear

Rules:
- If a field is not present, use null.
- Do NOT invent information not present in the text.
- Return ONLY the JSON object, no markdown, no explanation.

Module section text:
"""


def _compute_input_hash(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


class DoclingHandbookParser:
    """Parse a Modulhandbuch PDF into structured ModuleHandbookEntry data.

    Uses Docling for layout-aware PDF conversion and an LLM for field extraction.
    """

    # Heading patterns that typically mark the start of a new module section.
    # Matches strings like:
    #   "IN0001 Einführung in die Informatik"
    #   "MA0902 Analysis für Informatik I"
    #   "Module: Maschinelles Lernen"
    #   "Modul: Algorithmen und Datenstrukturen"
    _MODULE_HEADING_RE = re.compile(
        r"^(?:[A-Z]{1,4}\d{3,6}[a-z]?\s+.{3,}|(?:Module?|Modul)\s*:?\s*.{3,})$",
        re.IGNORECASE,
    )

    def __init__(self, llm_client: LLMPort, settings: Settings) -> None:
        self._llm = llm_client
        self._settings = settings

    async def parse(
        self,
        document_bytes: bytes,
        university_id: str,
        handbook_version: str,
    ) -> list[HandbookEntryData]:
        """Parse *document_bytes* and return one ``HandbookEntryData`` per module."""
        _logger.info(
            "HandbookParser: starting PDF conversion (university=%s version=%s bytes=%d)",
            university_id,
            handbook_version,
            len(document_bytes),
        )

        # Phase 1: Docling structural parsing — runs sync in a thread pool.
        raw_sections = await asyncio.get_event_loop().run_in_executor(
            None, self._convert_and_split, document_bytes
        )
        _logger.info(
            "HandbookParser: Docling extracted %d candidate sections", len(raw_sections)
        )

        # Phase 2: LLM-assisted field extraction per section.
        entries: list[HandbookEntryData] = []
        for i, section_text in enumerate(raw_sections):
            try:
                entry = await self._extract_fields(section_text)
                entry.university_id = university_id
                entry.handbook_version = handbook_version
                entries.append(entry)
            except Exception as exc:
                _logger.warning(
                    "HandbookParser: failed to extract section %d/%d: %s",
                    i + 1,
                    len(raw_sections),
                    exc,
                )

        _logger.info(
            "HandbookParser: extracted %d module entries", len(entries)
        )
        return entries

    # ------------------------------------------------------------------
    # Phase 1 helpers
    # ------------------------------------------------------------------

    def _convert_and_split(self, pdf_bytes: bytes) -> list[str]:
        """Convert the PDF with Docling and split into per-module text chunks."""
        try:
            from docling.document_converter import DocumentConverter
        except ImportError as exc:
            raise RuntimeError(
                "docling is not installed. Add 'docling>=2.97' to pyproject.toml."
            ) from exc

        import io

        converter = DocumentConverter()
        result = converter.convert_from_stream(io.BytesIO(pdf_bytes), mime_type="application/pdf")
        doc = result.document

        # Export to Markdown — Docling preserves heading hierarchy in Markdown.
        markdown_text: str = doc.export_to_markdown()

        return self._split_markdown_by_modules(markdown_text)

    def _split_markdown_by_modules(self, markdown: str) -> list[str]:
        """Split a Markdown document at module-heading boundaries.

        Strategy: look for H2/H3 headings whose content matches the module
        heading pattern.  Each match starts a new module chunk.
        Falls back to splitting on any H2 if no module headings are found.
        """
        lines = markdown.splitlines()
        chunks: list[str] = []
        current: list[str] = []

        def _is_module_heading(line: str) -> bool:
            stripped = line.lstrip("#").strip()
            return bool(self._MODULE_HEADING_RE.match(stripped))

        heading_re = re.compile(r"^#{1,4}\s+")

        for line in lines:
            if heading_re.match(line) and _is_module_heading(line):
                if current:
                    text = "\n".join(current).strip()
                    if len(text) > 80:  # skip trivially short chunks
                        chunks.append(text)
                current = [line]
            else:
                current.append(line)

        if current:
            text = "\n".join(current).strip()
            if len(text) > 80:
                chunks.append(text)

        # Fallback: if no module headings detected, try splitting on any H2.
        if not chunks:
            _logger.warning(
                "HandbookParser: no module headings detected; falling back to H2 splits"
            )
            for line in lines:
                if re.match(r"^##\s+", line):
                    if current:
                        text = "\n".join(current).strip()
                        if len(text) > 80:
                            chunks.append(text)
                    current = [line]
                else:
                    current.append(line)
            if current:
                text = "\n".join(current).strip()
                if len(text) > 80:
                    chunks.append(text)

        return chunks

    # ------------------------------------------------------------------
    # Phase 2 helpers
    # ------------------------------------------------------------------

    async def _extract_fields(self, section_text: str) -> HandbookEntryData:
        """Send one module section to the LLM for structured field extraction."""
        prompt = _MODULE_EXTRACT_PROMPT + section_text[:4000]  # guard context length
        try:
            response = await self._llm.chat(
                model=self._settings.effective_extract_model,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0},
            )
        except Exception as exc:
            _logger.warning("HandbookParser: LLM call failed: %s", exc)
            return self._fallback_parse(section_text)

        content: str = (response.get("message", {}) or {}).get("content", "") or ""
        content = content.strip()
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        content = content.strip()

        try:
            data: Any = json.loads(content)
        except json.JSONDecodeError:
            _logger.warning(
                "HandbookParser: LLM returned non-JSON for section starting with: %s",
                section_text[:100],
            )
            return self._fallback_parse(section_text)

        return HandbookEntryData(
            module_code=data.get("module_code"),
            module_title=data.get("module_title") or self._extract_title_heuristic(section_text),
            module_title_en=data.get("module_title_en"),
            description=data.get("description"),
            learning_outcomes=data.get("learning_outcomes"),
            contents=data.get("contents"),
            prerequisites=data.get("prerequisites"),
            ects=self._parse_float(data.get("ects")),
            level=data.get("level") if data.get("level") in ("bachelor", "master", "phd") else None,
            language=data.get("language"),
        )

    def _fallback_parse(self, section_text: str) -> HandbookEntryData:
        """Minimal parsing when the LLM fails: extract title from first heading."""
        title = self._extract_title_heuristic(section_text)
        return HandbookEntryData(
            module_title=title,
            description=section_text[:500] if len(section_text) > 20 else None,
        )

    @staticmethod
    def _extract_title_heuristic(text: str) -> str:
        first_line = text.splitlines()[0].lstrip("#").strip()
        return first_line[:500] if first_line else "Unknown Module"

    @staticmethod
    def _parse_float(value: Any) -> float | None:
        if value is None:
            return None
        try:
            return float(value)
        except (TypeError, ValueError):
            return None
