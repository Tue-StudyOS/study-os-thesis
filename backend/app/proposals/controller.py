from fastapi import APIRouter

from app.auth.deps import CurrentUserDep
from app.models import Thesis
from app.proposals.constants import PROPOSALS_API_PREFIX, PROPOSALS_API_TAG
from app.proposals.deps import ProposalServiceDep
from app.theses.schemas import ThesisOut

router = APIRouter(prefix=PROPOSALS_API_PREFIX, tags=[PROPOSALS_API_TAG])


@router.get("/mine", response_model=list[ThesisOut])
async def list_my_proposals(
    current_user: CurrentUserDep,
    proposal_service: ProposalServiceDep,
) -> list[Thesis]:
    """Return all AI-generated proposals for the currently logged-in student."""
    return await proposal_service.list_my_proposals(current_user.id)
