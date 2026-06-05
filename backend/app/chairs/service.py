"""Business logic for research chairs."""

import logging


from app.chairs.repository import ChairRepository
from app.chairs.schemas import ChairCreate, ChairPatch
from app.config import Settings
from app.exceptions import NotFoundException
from app.llm.port import LLMPort
from app.models.chair import Chair, ChairDocumentKind

_logger = logging.getLogger(__name__)


def _split_professor_title_and_name(title: str | None, name: str) -> tuple[str | None, str]:
    """Split a combined input like "Prof. Dr. Georg Martius" into (title, name).

    We preserve the title separately (no data loss) and keep `name` canonical
    for scraping/matching.
    """

    s = (name or "").strip()
    if not s:
        return (title.strip() if title else None), s

    import re

    # Repeated leading titles (case-insensitive), e.g. "Prof. Dr.", "Professor Dr.-Ing.".
    m = re.match(r"^\s*((?:(?:Professor|Prof)\.?\s*|Dr(?:\.-Ing\.)?\.?\s*)+)", s, flags=re.IGNORECASE)
    parsed_title = m.group(1).strip() if m else None
    parsed_name = s[m.end() :].strip() if m else s

    out_title = title or parsed_title
    if out_title is not None:
        out_title = out_title.strip() or None
    return out_title, parsed_name


class ChairService:
    def __init__(
        self,
        chair_repo: ChairRepository,
        embed_client: LLMPort,
        settings: Settings,
    ) -> None:
        self._chair_repo = chair_repo
        self._ollama = embed_client
        self._settings = settings

    # ------------------------------------------------------------------
    # Chair CRUD
    # ------------------------------------------------------------------

    async def create_chair(self, data: ChairCreate, *, embed: bool = True) -> Chair:
        professor_title, professor_name = _split_professor_title_and_name(data.professor_title, data.professor_name)
        _logger.info("Creating chair: name=%r professor=%r", data.name, professor_name)
        chair = await self._chair_repo.create(
            name=data.name,
            short_description=data.short_description,
            professor_title=professor_title,
            professor_name=professor_name,
            professor_user_id=data.professor_user_id,
            website_url=data.website_url,
        )
        if embed:
            _logger.info("Chair created: id=%d — embedding description document", chair.id)
            embedding = await self._embed_text(data.short_description)
            await self._chair_repo.add_document(
                chair_id=chair.id,
                kind=ChairDocumentKind.description,
                content=data.short_description,
                embedding=embedding,
            )
        await self._chair_repo.commit()
        _logger.info("Chair id=%d committed to DB", chair.id)
        return await self._chair_repo.get_by_id(chair.id, load_documents=True)  # type: ignore[return-value]

    async def get_chair(self, chair_id: int) -> Chair:
        chair = await self._chair_repo.get_by_id(chair_id, load_documents=True)
        if chair is None:
            raise NotFoundException("Chair", chair_id)
        return chair

    async def list_chairs(self) -> list[Chair]:
        return await self._chair_repo.list()

    async def update_chair(self, chair_id: int, data: ChairPatch) -> Chair:
        chair = await self._chair_repo.get_by_id(chair_id)
        if chair is None:
            raise NotFoundException("Chair", chair_id)
        updates = data.model_dump(exclude_none=True)

        if "professor_name" in updates or "professor_title" in updates:
            professor_title, professor_name = _split_professor_title_and_name(
                updates.get("professor_title"),
                str(updates.get("professor_name") or chair.professor_name),
            )
            updates["professor_title"] = professor_title
            updates["professor_name"] = professor_name

        chair = await self._chair_repo.update(chair, **updates)
        await self._chair_repo.commit()
        return await self._chair_repo.get_by_id(chair_id, load_documents=True)  # type: ignore[return-value]

    async def delete_chair(self, chair_id: int) -> None:
        chair = await self._chair_repo.get_by_id(chair_id)
        if chair is None:
            raise NotFoundException("Chair", chair_id)
        await self._chair_repo.delete(chair)
        await self._chair_repo.commit()

    # ------------------------------------------------------------------
    # Document management
    # ------------------------------------------------------------------

    async def delete_document(self, chair_id: int, doc_id: int) -> None:
        doc = await self._chair_repo.get_document(doc_id)
        if doc is None or doc.chair_id != chair_id:
            raise NotFoundException("ChairDocument", doc_id)
        await self._chair_repo.delete_document(doc)
        await self._chair_repo.commit()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    async def _embed_text(self, text: str) -> list[float] | None:
        _logger.info("Embedding text: model=%s text_len=%d", self._settings.ollama_embed_model, len(text))
        try:
            vec = await self._ollama.embed(self._settings.ollama_embed_model, text)
            _logger.info("Embedding done: dim=%d", len(vec))
            return vec
        except Exception as exc:
            _logger.warning("Embedding failed, document stored without embedding: %s", exc)
            return None
