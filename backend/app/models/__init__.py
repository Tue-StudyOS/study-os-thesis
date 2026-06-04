from app.models.chair import Chair, ChairDocument, ChairDocumentKind
from app.models.chat import ChatMessage, ChatSession, MessageRole
from app.models.handbook import ModuleHandbookEntry, ModuleSkillMapping
from app.models.job import Job, JobStatus, JobType
from app.models.skill import SkillComputationRun, SkillEvidence, SkillTag, UserSkill
from app.models.student import Student, StudentCourse
from app.models.thesis import EMBEDDING_DIM, Thesis, ThesisDifficulty, ThesisSource
from app.models.user import User, UserRole

__all__ = [
    "EMBEDDING_DIM",
    "Chair",
    "ChairDocument",
    "ChairDocumentKind",
    "ChatMessage",
    "ChatSession",
    "Job",
    "JobStatus",
    "JobType",
    "MessageRole",
    "ModuleHandbookEntry",
    "ModuleSkillMapping",
    "SkillComputationRun",
    "SkillEvidence",
    "SkillTag",
    "Student",
    "StudentCourse",
    "Thesis",
    "ThesisDifficulty",
    "ThesisSource",
    "User",
    "UserRole",
    "UserSkill",
]
