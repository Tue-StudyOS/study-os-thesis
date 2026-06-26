#!/usr/bin/env python3
"""Regenerate skill Markdown indexes from OpenAlex.

This script is intentionally standalone: it imports no backend modules and
requires no database, Docker service, FastAPI app, or third-party package.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
RESEARCHERS_INDEX = REPO_ROOT / "skills/find-university-chairs/references/researchers/INDEX.md"
CHAIRS_INDEX = REPO_ROOT / "skills/find-university-chairs/references/chairs/INDEX.md"
PAPERS_DIR = REPO_ROOT / "skills/find-recent-papers/references/papers"
OPENALEX_API = "https://api.openalex.org"
DEFAULT_EXCLUDED_TYPES = {"book", "book-chapter", "editorial", "erratum", "letter", "paratext"}


@dataclass(frozen=True)
class BuildConfig:
    """Locations of one faculty's Markdown tree.

    Defaults point at the bundled Tuebingen data, but every path is
    overridable so the same builder can assemble or validate the tree for
    any other faculty without code changes.
    """

    researchers_index: Path = RESEARCHERS_INDEX
    chairs_index: Path = CHAIRS_INDEX
    papers_dir: Path = PAPERS_DIR

    @property
    def researchers_dir(self) -> Path:
        return self.researchers_index.parent

    @property
    def paper_index(self) -> Path:
        return self.papers_dir / "INDEX.md"

    @property
    def topic_dir(self) -> Path:
        return self.papers_dir / "by-topic"

    @property
    def year_dir(self) -> Path:
        return self.papers_dir / "by-year"


DEFAULT_CONFIG = BuildConfig()


@dataclass(frozen=True)
class Researcher:
    slug: str
    name: str
    role: str
    chair_slug: str
    openalex_author_id: str
    keywords: list[str]
    last_updated: str


@dataclass(frozen=True)
class Paper:
    title: str
    year: str
    authors: str
    source: str
    doi: str
    openalex: str
    url: str
    abstract: str
    keywords: list[str]
    researcher_slug: str
    researcher_name: str
    chair_slug: str
    work_type: str


def slugify(value: str) -> str:
    text = value.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-") or "unknown"


def markdown_cell(value: str | int | None) -> str:
    text = "" if value is None else str(value)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = text.replace("\\", "\\\\").replace("|", "\\|")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def markdown_text(value: str | None) -> str:
    text = "" if value is None else str(value)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text.strip()


def split_table_row(line: str) -> list[str]:
    cells: list[str] = []
    current: list[str] = []
    escaped = False
    for char in line.strip().strip("|"):
        if escaped:
            current.append(char)
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == "|":
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    cells.append("".join(current).strip())
    return cells


def read_table(path: Path) -> list[dict[str, str]]:
    """Parse a GitHub-flavored Markdown table into header-keyed row dicts.

    Rows are keyed by (lower-cased) column name rather than position, so a
    faculty may add or reorder columns without breaking the readers or the
    referential-integrity validator. The first table row is treated as the
    header; the `|---|` separator row is skipped.
    """
    if not path.exists():
        raise FileNotFoundError(f"index missing: {path}")

    header: list[str] | None = None
    rows: list[dict[str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = split_table_row(line)
        if cells and all(set(cell) <= {"-", ":"} for cell in cells if cell):
            continue  # separator row: |---|:--:|
        if header is None:
            header = [cell.strip().lower() for cell in cells]
            continue
        rows.append({name: (cells[index].strip() if index < len(cells) else "") for index, name in enumerate(header)})
    return rows


def _split_slugs(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def read_researchers(path: Path = RESEARCHERS_INDEX) -> list[Researcher]:
    rows: list[Researcher] = []
    for row in read_table(path):
        slug = row.get("slug", "")
        openalex_author_id = row.get("openalex_author_id", "")
        if not slug or not openalex_author_id:
            continue
        rows.append(
            Researcher(
                slug=slug,
                name=row.get("name", ""),
                role=row.get("role", ""),
                chair_slug=row.get("chair_slug", ""),
                openalex_author_id=openalex_author_id,
                keywords=_split_slugs(row.get("keywords", "")),
                last_updated=row.get("last_updated", ""),
            )
        )
    return rows


def read_chair_slugs(path: Path = CHAIRS_INDEX) -> set[str]:
    return {row["slug"] for row in read_table(path) if row.get("slug")}


def read_chair_researcher_links(path: Path = CHAIRS_INDEX) -> dict[str, list[str]]:
    return {row["slug"]: _split_slugs(row.get("researchers", "")) for row in read_table(path) if row.get("slug")}


def read_paper_links(path: Path) -> list[dict[str, object]]:
    papers: list[dict[str, object]] = []
    for row in read_table(path):
        title = row.get("title", "")
        if not title:
            continue
        papers.append(
            {
                "title": title,
                "researchers": _split_slugs(row.get("researchers", "")),
                "chairs": _split_slugs(row.get("chairs", "")),
            }
        )
    return papers


def validate_researcher_index(researchers: list[Researcher], chair_slugs: set[str]) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    openalex_pattern = re.compile(r"^(https://openalex\.org/)?A\d+$")
    for researcher in researchers:
        if researcher.slug in seen:
            errors.append(f"duplicate researcher slug: {researcher.slug}")
        seen.add(researcher.slug)
        if researcher.chair_slug not in chair_slugs:
            errors.append(f"{researcher.slug} references missing chair {researcher.chair_slug}")
        if not openalex_pattern.fullmatch(researcher.openalex_author_id):
            errors.append(f"{researcher.slug} has invalid OpenAlex author id {researcher.openalex_author_id}")
    return errors


def validate_references(config: BuildConfig = DEFAULT_CONFIG) -> list[str]:
    """Faculty-agnostic referential-integrity check over a Markdown tree.

    Confirms that every cross-reference resolves: researcher -> chair,
    chair -> researcher, and paper -> researcher / chair. It reads tables by
    column name, so faculty-specific extra columns do not affect it. Returns a
    list of human-readable errors (empty when the tree is internally consistent).
    """
    researchers = read_researchers(config.researchers_index)
    chair_slugs = read_chair_slugs(config.chairs_index)
    researcher_slugs = {researcher.slug for researcher in researchers}

    errors = validate_researcher_index(researchers, chair_slugs)

    for chair_slug, member_slugs in read_chair_researcher_links(config.chairs_index).items():
        for member in member_slugs:
            if member not in researcher_slugs:
                errors.append(f"chair {chair_slug} lists missing researcher {member}")

    if config.paper_index.exists():
        for paper in read_paper_links(config.paper_index):
            for slug in paper["researchers"]:
                if slug not in researcher_slugs:
                    errors.append(f"paper '{paper['title']}' references missing person {slug}")
            for slug in paper["chairs"]:
                if slug not in chair_slugs:
                    errors.append(f"paper '{paper['title']}' references missing chair {slug}")
    return errors


def request_json(url: str, mailto: str | None, retries: int = 3, backoff_seconds: float = 1.0) -> dict[str, Any]:
    parsed = urllib.parse.urlparse(url)
    query = dict(urllib.parse.parse_qsl(parsed.query))
    if mailto:
        query["mailto"] = mailto
    final_url = urllib.parse.urlunparse(parsed._replace(query=urllib.parse.urlencode(query)))
    request = urllib.request.Request(final_url, headers={"User-Agent": "study-os-thesis-skill-indexer/1.0"})

    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code not in {429, 500, 502, 503, 504} or attempt == retries:
                break
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = exc
            if attempt == retries:
                break
        time.sleep(backoff_seconds * attempt)

    raise RuntimeError(f"OpenAlex request failed after {retries} attempts: {final_url}") from last_error


def abstract_from_inverted_index(value: Any) -> str:
    if not isinstance(value, dict):
        return ""
    positions: list[tuple[int, str]] = []
    for word, indexes in value.items():
        if isinstance(indexes, list):
            positions.extend((int(index), str(word)) for index in indexes)
    return " ".join(word for _index, word in sorted(positions))


def paper_from_work(work: dict[str, Any], researcher: Researcher) -> Paper:
    authorships = work.get("authorships") or []
    author_names = []
    for authorship in authorships[:8]:
        author = authorship.get("author") or {}
        if author.get("display_name"):
            author_names.append(str(author["display_name"]))

    primary_location = work.get("primary_location") or {}
    source = primary_location.get("source") or {}
    doi = str(work.get("doi") or "")
    openalex = str(work.get("id") or "")
    url = str(primary_location.get("landing_page_url") or doi or openalex)
    title = str(work.get("title") or "Untitled paper")
    year = str(work.get("publication_year") or "")
    abstract = abstract_from_inverted_index(work.get("abstract_inverted_index"))
    concepts = work.get("concepts") or []
    keywords = [str(item.get("display_name")) for item in concepts[:5] if item.get("display_name")]

    return Paper(
        title=title,
        year=year,
        authors=", ".join(author_names),
        source=str(source.get("display_name") or ""),
        doi=doi,
        openalex=openalex,
        url=url,
        abstract=abstract,
        keywords=keywords or researcher.keywords,
        researcher_slug=researcher.slug,
        researcher_name=researcher.name,
        chair_slug=researcher.chair_slug,
        work_type=str(work.get("type") or ""),
    )


def paper_is_usable(paper: Paper, since_year: int, excluded_types: set[str]) -> bool:
    if not paper.title or not paper.openalex:
        return False
    if paper.work_type in excluded_types:
        return False
    if paper.year and paper.year.isdigit() and int(paper.year) < since_year:
        return False
    return True


def fetch_papers(researcher: Researcher, max_results: int, since_year: int, mailto: str | None, retries: int) -> list[Paper]:
    author_id = researcher.openalex_author_id.rsplit("/", maxsplit=1)[-1]
    filters = f"author.id:{author_id},from_publication_date:{since_year}-01-01"
    query = urllib.parse.urlencode({"filter": filters, "sort": "publication_date:desc", "per-page": str(max_results)})
    data = request_json(f"{OPENALEX_API}/works?{query}", mailto, retries=retries)
    papers = [paper_from_work(work, researcher) for work in data.get("results", [])]
    return [paper for paper in papers if paper_is_usable(paper, since_year, DEFAULT_EXCLUDED_TYPES)][:max_results]


def load_fixture_papers(path: Path, researchers: list[Researcher], since_year: int) -> dict[str, list[Paper]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    by_slug = {researcher.slug: researcher for researcher in researchers}
    result: dict[str, list[Paper]] = {}
    for slug, works in data.items():
        researcher = by_slug.get(slug)
        if researcher is None:
            continue
        papers = [paper_from_work(work, researcher) for work in works]
        result[slug] = [paper for paper in papers if paper_is_usable(paper, since_year, DEFAULT_EXCLUDED_TYPES)]
    return result


def paper_key(paper: Paper) -> str:
    if paper.doi:
        return paper.doi.lower()
    if paper.openalex:
        return paper.openalex.lower()
    return re.sub(r"\W+", "", paper.title.lower())


def dedupe_papers(papers: list[Paper]) -> list[Paper]:
    seen: set[str] = set()
    deduped: list[Paper] = []
    for paper in papers:
        candidates = [paper.doi.lower(), paper.openalex.lower(), re.sub(r"\W+", "", paper.title.lower())]
        candidates = [candidate for candidate in candidates if candidate]
        if any(candidate in seen for candidate in candidates):
            continue
        seen.update(candidates)
        deduped.append(paper)
    return deduped


def format_paper_block(paper: Paper) -> str:
    thesis_angle = "Use this paper as evidence for a thesis conversation; refine the angle with the supervisor."
    return "\n".join(
        [
            f"### {markdown_text(paper.title)}",
            f"- Year: {markdown_text(paper.year)}",
            f"- Authors: {markdown_text(paper.authors)}",
            f"- Source: {markdown_text(paper.source)}",
            f"- DOI: {markdown_text(paper.doi)}",
            f"- OpenAlex: {markdown_text(paper.openalex)}",
            f"- URL: {markdown_text(paper.url)}",
            f"- Keywords: {markdown_text('; '.join(paper.keywords))}",
            f"- Thesis angle: {thesis_angle}",
            f"- Abstract: {markdown_text(paper.abstract)}",
        ]
    )


def write_researcher_profile(researcher: Researcher, papers: list[Paper], today: str, researchers_dir: Path) -> None:
    lines = [
        f"# {researcher.name}",
        "",
        "## Metadata",
        f"- Role: {researcher.role}",
        f"- Chair: {researcher.chair_slug}",
        "- Website:",
        f"- OpenAlex author id: {researcher.openalex_author_id}",
        f"- Last updated: {today}",
        "",
        "## Research Areas",
        f"- Keywords: {'; '.join(researcher.keywords)}",
        "",
        "## Selected Recent Papers",
    ]
    if papers:
        lines.extend(format_paper_block(paper) + "\n" for paper in papers)
    else:
        lines.append("- No recent papers matched the current selection rules.")
    lines.extend(
        [
            "",
            "## Caveats",
            "- Affiliation uncertainty: Verify against official university pages before contacting.",
            "- Missing data: Generated from OpenAlex metadata; source pages may have richer context.",
        ]
    )
    (researchers_dir / f"{researcher.slug}.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_paper_indexes(papers: list[Paper], today: str, config: BuildConfig = DEFAULT_CONFIG) -> None:
    config.papers_dir.mkdir(parents=True, exist_ok=True)
    config.topic_dir.mkdir(parents=True, exist_ok=True)
    config.year_dir.mkdir(parents=True, exist_ok=True)

    rows = ["# Paper Index", "", f"Last updated: {today}", "", "| title | year | researchers | chairs | keywords | doi | openalex | updated |", "|---|---|---|---|---|---|---|---|"]
    for paper in papers:
        rows.append(
            "| "
            + " | ".join(
                [
                    markdown_cell(paper.title),
                    markdown_cell(paper.year),
                    markdown_cell(paper.researcher_slug),
                    markdown_cell(paper.chair_slug),
                    markdown_cell("; ".join(paper.keywords)),
                    markdown_cell(paper.doi),
                    markdown_cell(paper.openalex),
                    markdown_cell(today),
                ]
            )
            + " |"
        )
    config.paper_index.write_text("\n".join(rows) + "\n", encoding="utf-8")

    by_year: dict[str, list[Paper]] = {}
    by_topic: dict[str, list[Paper]] = {}
    for paper in papers:
        by_year.setdefault(paper.year or "unknown", []).append(paper)
        for keyword in paper.keywords[:3]:
            by_topic.setdefault(slugify(keyword), []).append(paper)

    for year, year_papers in by_year.items():
        content = [f"# Papers From {year}", "", f"Last updated: {today}", ""]
        content.extend(format_paper_block(paper) + "\n" for paper in year_papers)
        (config.year_dir / f"{year}.md").write_text("\n".join(content).rstrip() + "\n", encoding="utf-8")

    for topic, topic_papers in by_topic.items():
        content = [f"# Papers For {topic}", "", f"Last updated: {today}", ""]
        content.extend(format_paper_block(paper) + "\n" for paper in topic_papers)
        (config.topic_dir / f"{topic}.md").write_text("\n".join(content).rstrip() + "\n", encoding="utf-8")

    topic_index = ["# Topic Paper Index", "", "| topic | file | paper_count | last_updated |", "|---|---|---|---|"]
    topic_index.extend(f"| {markdown_cell(topic)} | {markdown_cell(topic + '.md')} | {len(items)} | {today} |" for topic, items in sorted(by_topic.items()))
    (config.topic_dir / "INDEX.md").write_text("\n".join(topic_index) + "\n", encoding="utf-8")

    year_index = ["# Year Paper Index", "", "| year | file | paper_count | last_updated |", "|---|---|---|---|"]
    year_index.extend(f"| {markdown_cell(year)} | {markdown_cell(year + '.md')} | {len(items)} | {today} |" for year, items in sorted(by_year.items(), reverse=True))
    (config.year_dir / "INDEX.md").write_text("\n".join(year_index) + "\n", encoding="utf-8")


def write_summary(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def main_with_args(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-results", type=int, default=10)
    parser.add_argument("--since-year", type=int, default=dt.date.today().year - 3)
    parser.add_argument("--mailto", default="")
    parser.add_argument("--fixture", type=Path)
    parser.add_argument("--summary-file", type=Path, default=Path("openalex-update-summary.md"))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--researchers-index", type=Path, default=RESEARCHERS_INDEX, help="researcher INDEX.md for the target faculty")
    parser.add_argument("--chairs-index", type=Path, default=CHAIRS_INDEX, help="chair INDEX.md for the target faculty")
    parser.add_argument("--papers-dir", type=Path, default=PAPERS_DIR, help="output directory for the paper tree")
    parser.add_argument("--validate-only", action="store_true", help="check referential integrity of the tree and exit without fetching")
    args = parser.parse_args(argv)

    config = BuildConfig(
        researchers_index=args.researchers_index,
        chairs_index=args.chairs_index,
        papers_dir=args.papers_dir,
    )

    if args.validate_only:
        errors = validate_references(config)
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 2 if errors else 0

    researchers = read_researchers(config.researchers_index)
    chair_slugs = read_chair_slugs(config.chairs_index)
    validation_errors = validate_references(config)
    if validation_errors:
        for error in validation_errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 2

    if not researchers:
        summary = f"No researchers with OpenAlex IDs found in {config.researchers_index}"
        print(summary)
        write_summary(args.summary_file, summary)
        return 0

    papers_by_researcher: dict[str, list[Paper]]
    if args.fixture:
        papers_by_researcher = load_fixture_papers(args.fixture, researchers, args.since_year)
    else:
        papers_by_researcher = {}
        failures: list[str] = []
        for researcher in researchers:
            try:
                papers_by_researcher[researcher.slug] = fetch_papers(researcher, args.max_results, args.since_year, args.mailto or None, args.retries)
            except RuntimeError as exc:
                failures.append(f"{researcher.slug}: {exc}")
                papers_by_researcher[researcher.slug] = []
            time.sleep(0.2)
        if failures:
            print("\n".join(f"WARNING: {failure}" for failure in failures), file=sys.stderr)

    unique_papers = dedupe_papers([paper for papers in papers_by_researcher.values() for paper in papers])
    today = dt.date.today().isoformat()
    summary = f"Updated {len(researchers)} researchers and {len(unique_papers)} unique papers."

    if args.dry_run:
        summary = f"Would update {len(researchers)} researchers and {len(unique_papers)} unique papers."
        print(summary)
        write_summary(args.summary_file, summary)
        return 0

    for researcher in researchers:
        write_researcher_profile(researcher, papers_by_researcher.get(researcher.slug, []), today, config.researchers_dir)
    write_paper_indexes(unique_papers, today, config)
    write_summary(args.summary_file, summary)
    print(summary)
    return 0


def main() -> int:
    return main_with_args()


if __name__ == "__main__":
    sys.exit(main())
