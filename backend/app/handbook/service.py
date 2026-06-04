"""Business logic for handbook ingestion."""

from __future__ import annotations

import logging

from app.config import Settings
from app.handbook.parser import DoclingHandbookParser
from app.handbook.repository import HandbookRepository
from app.handbook.schemas import HandbookIngestResult
from app.llm.port import LLMPort

_logger = logging.getLogger(__name__)


class HandbookService:
    """Orchestrates handbook PDF parsing and DB persistence.

    Tag generation (LLM-based) happens lazily during skill computation, not
    here.  This service only cares about getting module entries into the DB.
    """

    def __init__(
        self,
        handbook_repo: HandbookRepository,
        llm_client: LLMPort,
        settings: Settings,
    ) -> None:
        self._repo = handbook_repo
        self._llm = llm_client
        self._settings = settings

    async def ingest_pdf(
        self,
        pdf_bytes: bytes,
        university_id: str,
        handbook_version: str,
    ) -> HandbookIngestResult:
        parser = DoclingHandbookParser(self._llm, self._settings)
        parsed_entries = await parser.parse(pdf_bytes, university_id, handbook_version)

        ingested = 0
        skipped = 0
        warnings: list[str] = []

        for data in parsed_entries:
            if not data.module_title or len(data.module_title.strip()) < 2:
                skipped += 1
                warnings.append(f"Skipped entry with empty/short title: {data.module_title!r}")
                continue
            try:
                await self._repo.upsert_entry(data)
                ingested += 1
            except Exception as exc:
                skipped += 1
                warnings.append(f"Failed to persist '{data.module_title}': {exc}")
                _logger.warning("HandbookService: upsert failed for %r: %s", data.module_title, exc)

        await self._repo.commit()
        _logger.info(
            "HandbookService: ingestion done — %d ingested, %d skipped (university=%s version=%s)",
            ingested,
            skipped,
            university_id,
            handbook_version,
        )

        return HandbookIngestResult(
            university_id=university_id,
            handbook_version=handbook_version,
            modules_ingested=ingested,
            modules_skipped=skipped,
            warnings=warnings,
        )
