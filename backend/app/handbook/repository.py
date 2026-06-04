"""Data-access layer for the module handbook domain."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.handbook.schemas import HandbookEntryData
from app.models.handbook import ModuleHandbookEntry, ModuleSkillMapping


class HandbookRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_latest_entries(
        self,
        university_id: str | None = None,
    ) -> list[ModuleHandbookEntry]:
        """Return all entries for the newest handbook version for each university.

        If *university_id* is given, restrict to that university.
        """
        # Find the latest version string per university (lexicographic max).
        if university_id:
            version_q = (
                select(
                    ModuleHandbookEntry.handbook_version,
                )
                .where(ModuleHandbookEntry.university_id == university_id)
                .order_by(ModuleHandbookEntry.handbook_version.desc())
                .limit(1)
                .scalar_subquery()
            )
            q = (
                select(ModuleHandbookEntry)
                .where(ModuleHandbookEntry.university_id == university_id)
                .where(ModuleHandbookEntry.handbook_version == version_q)
                .options(selectinload(ModuleHandbookEntry.skill_mappings))
            )
        else:
            # Without a university filter, return *all* entries from all latest versions.
            # For large deployments this should be paginated; acceptable for now.
            from sqlalchemy import func

            version_subq = (
                select(
                    ModuleHandbookEntry.university_id,
                    func.max(ModuleHandbookEntry.handbook_version).label("max_version"),
                )
                .group_by(ModuleHandbookEntry.university_id)
                .subquery()
            )
            q = (
                select(ModuleHandbookEntry)
                .join(
                    version_subq,
                    (ModuleHandbookEntry.university_id == version_subq.c.university_id)
                    & (ModuleHandbookEntry.handbook_version == version_subq.c.max_version),
                )
                .options(selectinload(ModuleHandbookEntry.skill_mappings))
            )

        result = await self._session.scalars(q)
        return list(result.all())

    async def get_by_id(self, entry_id: int) -> ModuleHandbookEntry | None:
        return await self._session.get(
            ModuleHandbookEntry,
            entry_id,
            options=[selectinload(ModuleHandbookEntry.skill_mappings)],
        )

    async def list_versions(self) -> list[dict]:
        """Return summary rows: (university_id, handbook_version, count)."""
        from sqlalchemy import func

        rows = await self._session.execute(
            select(
                ModuleHandbookEntry.university_id,
                ModuleHandbookEntry.handbook_version,
                func.count(ModuleHandbookEntry.id).label("module_count"),
            ).group_by(
                ModuleHandbookEntry.university_id,
                ModuleHandbookEntry.handbook_version,
            )
        )
        return [
            {
                "university_id": r.university_id,
                "handbook_version": r.handbook_version,
                "module_count": r.module_count,
            }
            for r in rows
        ]

    async def upsert_entry(self, data: HandbookEntryData) -> ModuleHandbookEntry:
        """Insert or update a handbook entry keyed by (university_id, handbook_version, module_code)."""
        existing = None
        if data.module_code:
            existing = await self._session.scalar(
                select(ModuleHandbookEntry)
                .where(ModuleHandbookEntry.university_id == data.university_id)
                .where(ModuleHandbookEntry.handbook_version == data.handbook_version)
                .where(ModuleHandbookEntry.module_code == data.module_code)
            )

        if existing is None:
            entry = ModuleHandbookEntry(
                university_id=data.university_id,
                handbook_version=data.handbook_version,
                module_code=data.module_code,
                module_title=data.module_title,
                module_title_en=data.module_title_en,
                description=data.description,
                learning_outcomes=data.learning_outcomes,
                contents=data.contents,
                prerequisites=data.prerequisites,
                ects=data.ects,
                level=data.level,
                language=data.language,
            )
            self._session.add(entry)
        else:
            entry = existing
            entry.module_title = data.module_title
            entry.module_title_en = data.module_title_en
            entry.description = data.description
            entry.learning_outcomes = data.learning_outcomes
            entry.contents = data.contents
            entry.prerequisites = data.prerequisites
            entry.ects = data.ects
            entry.level = data.level
            entry.language = data.language

        await self._session.flush()
        return entry

    async def save_skill_mappings(
        self, mappings: list[ModuleSkillMapping]
    ) -> None:
        for m in mappings:
            self._session.add(m)
        await self._session.flush()

    async def commit(self) -> None:
        await self._session.commit()
