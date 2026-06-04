"""skill_computation

Revision ID: 0010
Revises: 0009
Create Date: 2026-06-04
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "0010"
down_revision: Union[str, None] = "0009"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# ---------------------------------------------------------------------------
# Seed taxonomy: (name, category, aliases)
# ---------------------------------------------------------------------------
_SEED_SKILLS: list[tuple[str, str, list[str]]] = [
    # programming
    ("algorithms", "programming", ["algorithmen", "algorithm design", "algorithmik", "datenstrukturen und algorithmen"]),
    ("data structures", "programming", ["datenstrukturen", "data structures and algorithms"]),
    ("programming languages", "programming", ["programmiersprachen", "compiler construction", "compilerbau"]),
    ("object-oriented programming", "programming", ["objektorientierte programmierung", "oop", "object oriented"]),
    ("functional programming", "programming", ["funktionale programmierung", "functional"]),
    ("software testing", "engineering", ["softwarequalität", "testen", "qualitätssicherung", "testing", "test engineering"]),
    ("agile methods", "engineering", ["agile", "scrum", "kanban", "softwareprozess", "software process"]),
    ("software engineering", "engineering", ["softwaretechnik", "se", "software development", "software-engineering"]),
    ("software architecture", "engineering", ["softwarearchitektur", "entwurfsmuster", "design patterns", "architecture"]),
    ("devops", "engineering", ["ci/cd", "deployment", "continuous integration", "versionierung", "git"]),
    # mathematics
    ("linear algebra", "mathematics", ["lineare algebra", "la", "matrix algebra", "vector spaces"]),
    ("calculus", "mathematics", ["analysis", "differential calculus", "integral calculus", "differentialrechnung"]),
    ("statistics", "mathematics", ["statistik", "statistical methods", "stochastik", "wahrscheinlichkeitsrechnung"]),
    ("probability theory", "mathematics", ["wahrscheinlichkeitstheorie", "probability", "probabilistic methods"]),
    ("discrete mathematics", "mathematics", ["diskrete mathematik", "combinatorics", "graph theory", "kombinatorik"]),
    ("optimization", "mathematics", ["optimierung", "mathematical optimization", "convex optimization"]),
    ("numerical methods", "mathematics", ["numerische methoden", "numerik", "numerical analysis"]),
    ("logic", "mathematics", ["logik", "formal logic", "mathematical logic", "aussagenlogik"]),
    # theory
    ("machine learning", "theory", ["maschinelles lernen", "ml", "statistical learning", "statistical machine learning"]),
    ("deep learning", "theory", ["deep learning", "neural networks", "neuronale netze", "künstliche neuronale netze"]),
    ("computer vision", "theory", ["bildverarbeitung", "cv", "image processing", "bildanalyse"]),
    ("natural language processing", "theory", ["nlp", "sprachverarbeitung", "text mining", "computational linguistics"]),
    ("reinforcement learning", "theory", ["bestärkendes lernen", "rl", "reward learning"]),
    ("data mining", "theory", ["data mining", "knowledge discovery", "wissensextraktion"]),
    ("theoretical computer science", "theory", ["theoretische informatik", "complexity theory", "automata theory", "computability"]),
    ("formal methods", "theory", ["formale methoden", "formal verification", "model checking"]),
    # systems
    ("operating systems", "systems", ["betriebssysteme", "os", "betriebssystem", "operating system"]),
    ("computer architecture", "systems", ["rechnerarchitektur", "computer organization", "rechnerorganisation", "hardware"]),
    ("computer networks", "systems", ["rechnernetze", "netzwerke", "networking", "networks", "netzwerktechnik"]),
    ("distributed systems", "systems", ["verteilte systeme", "distributed computing", "verteilte programmierung"]),
    ("parallel computing", "systems", ["parallele systeme", "gpu computing", "nebenläufige programmierung", "concurrent programming"]),
    ("embedded systems", "systems", ["eingebettete systeme", "embedded computing", "systemnahe programmierung"]),
    ("cryptography", "systems", ["kryptographie", "kryptografische methoden", "it-sicherheit", "cyber security"]),
    ("cloud computing", "systems", ["cloud", "cloud infrastructure", "serverless", "infrastructure as code"]),
    # data
    ("databases", "data", ["datenbanken", "datenbanksysteme", "sql", "nosql", "dbms", "datenbankmanagement"]),
    ("data engineering", "data", ["data pipelines", "etl", "data warehouse", "big data", "datenhaltung"]),
    ("information retrieval", "data", ["informationsretrieval", "ir", "search engines", "information systems"]),
    ("data visualization", "data", ["datenvisualisierung", "visualization", "explorative datenanalyse"]),
    ("knowledge representation", "data", ["wissensrepräsentation", "ontologies", "semantic web", "knowledge graphs"]),
    # engineering
    ("robotics", "engineering", ["robotik", "robot programming", "autonomous systems", "mechatronik"]),
    ("signal processing", "engineering", ["signalverarbeitung", "digital signal processing", "dsp"]),
    ("human-computer interaction", "engineering", ["mensch-computer-interaktion", "hci", "usability", "ux"]),
    ("computer graphics", "engineering", ["computergrafik", "3d rendering", "graphics programming", "cg"]),
    ("web development", "engineering", ["webentwicklung", "frontend", "backend", "full-stack", "web engineering"]),
    ("mobile development", "engineering", ["mobile apps", "android", "ios", "mobile computing"]),
    # research
    ("scientific computing", "research", ["wissenschaftliches rechnen", "simulation", "computational science"]),
    ("research methods", "research", ["wissenschaftliches arbeiten", "forschungsmethoden", "seminar", "colloquium"]),
    ("project management", "research", ["projektmanagement", "teamarbeit", "softwareprojekt", "team project"]),
]


def upgrade() -> None:
    # ------------------------------------------------------------------
    # 1. Extend the job_type enum with new values
    # ------------------------------------------------------------------
    op.execute("ALTER TYPE job_type ADD VALUE IF NOT EXISTS 'compute_skills'")
    op.execute("ALTER TYPE job_type ADD VALUE IF NOT EXISTS 'ingest_handbook'")

    # ------------------------------------------------------------------
    # 2. module_handbook_entries
    # ------------------------------------------------------------------
    op.create_table(
        "module_handbook_entries",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("university_id", sa.String(50), nullable=False),
        sa.Column("handbook_version", sa.String(50), nullable=False),
        sa.Column("module_code", sa.String(50), nullable=True),
        sa.Column("module_title", sa.String(500), nullable=False),
        sa.Column("module_title_en", sa.String(500), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("learning_outcomes", sa.Text(), nullable=True),
        sa.Column("contents", sa.Text(), nullable=True),
        sa.Column("prerequisites", sa.Text(), nullable=True),
        sa.Column("ects", sa.Numeric(4, 1), nullable=True),
        sa.Column("level", sa.String(20), nullable=True),
        sa.Column("language", sa.String(10), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.UniqueConstraint(
            "university_id", "handbook_version", "module_code",
            name="uq_handbook_entry_code",
        ),
    )
    op.create_index(
        "ix_module_handbook_entries_university_id",
        "module_handbook_entries",
        ["university_id"],
    )

    # ------------------------------------------------------------------
    # 3. skill_tags
    # ------------------------------------------------------------------
    op.create_table(
        "skill_tags",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(100), nullable=False, unique=True),
        sa.Column("category", sa.String(50), nullable=True),
        sa.Column("aliases", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )

    # ------------------------------------------------------------------
    # 4. module_skill_mappings
    # ------------------------------------------------------------------
    op.create_table(
        "module_skill_mappings",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("handbook_entry_id", sa.Integer(), nullable=False),
        sa.Column("skill_tag_id", sa.Integer(), nullable=False),
        sa.Column("relevance", sa.Numeric(3, 2), nullable=False),
        sa.Column("source", sa.String(30), nullable=False, server_default="llm_generated"),
        sa.Column("llm_prompt_version", sa.String(50), nullable=True),
        sa.Column("llm_model", sa.String(100), nullable=True),
        sa.Column("llm_input_hash", sa.String(64), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["handbook_entry_id"], ["module_handbook_entries.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["skill_tag_id"], ["skill_tags.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("handbook_entry_id", "skill_tag_id", name="uq_module_skill_mapping"),
    )
    op.create_index(
        "ix_module_skill_mappings_handbook_entry_id",
        "module_skill_mappings",
        ["handbook_entry_id"],
    )
    op.create_index(
        "ix_module_skill_mappings_skill_tag_id",
        "module_skill_mappings",
        ["skill_tag_id"],
    )

    # ------------------------------------------------------------------
    # 5. skill_computation_runs  (must come before user_skills for FK)
    # ------------------------------------------------------------------
    op.create_table(
        "skill_computation_runs",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("job_id", sa.UUID(), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("handbook_version", sa.String(50), nullable=True),
        sa.Column("university_id", sa.String(50), nullable=True),
        sa.Column("total_courses", sa.SmallInteger(), nullable=True),
        sa.Column("matched_courses", sa.SmallInteger(), nullable=True),
        sa.Column("unmatched_courses", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("warnings", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("config", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["job_id"], ["jobs.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_skill_computation_runs_user_id", "skill_computation_runs", ["user_id"])
    op.create_index("ix_skill_computation_runs_job_id", "skill_computation_runs", ["job_id"])

    # ------------------------------------------------------------------
    # 6. user_skills
    # ------------------------------------------------------------------
    op.create_table(
        "user_skills",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("skill_tag_id", sa.Integer(), nullable=False),
        sa.Column("score", sa.Numeric(5, 4), nullable=False),
        sa.Column("computation_run_id", sa.UUID(), nullable=False),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["skill_tag_id"], ["skill_tags.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["computation_run_id"], ["skill_computation_runs.id"], ondelete="CASCADE"
        ),
        sa.UniqueConstraint("user_id", "skill_tag_id", name="uq_user_skill"),
    )
    op.create_index("ix_user_skills_user_id", "user_skills", ["user_id"])
    op.create_index("ix_user_skills_computation_run_id", "user_skills", ["computation_run_id"])

    # ------------------------------------------------------------------
    # 7. skill_evidence
    # ------------------------------------------------------------------
    op.create_table(
        "skill_evidence",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("user_skill_id", sa.Integer(), nullable=False),
        sa.Column("student_course_id", sa.Integer(), nullable=False),
        sa.Column("handbook_entry_id", sa.Integer(), nullable=True),
        sa.Column("match_method", sa.String(30), nullable=False),
        sa.Column("match_confidence", sa.Numeric(3, 2), nullable=False),
        sa.Column("module_skill_relevance", sa.Numeric(3, 2), nullable=False),
        sa.Column("credits_used", sa.Numeric(4, 1), nullable=True),
        sa.Column("grade_factor", sa.Numeric(3, 2), nullable=True),
        sa.Column("level_factor", sa.Numeric(3, 2), nullable=False),
        sa.Column("recency_factor", sa.Numeric(3, 2), nullable=False),
        sa.Column("raw_contribution", sa.Numeric(7, 4), nullable=False),
        sa.Column("computation_run_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(["user_skill_id"], ["user_skills.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["student_course_id"], ["student_courses.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["handbook_entry_id"], ["module_handbook_entries.id"], ondelete="SET NULL"
        ),
        sa.ForeignKeyConstraint(
            ["computation_run_id"], ["skill_computation_runs.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_skill_evidence_user_skill_id", "skill_evidence", ["user_skill_id"])
    op.create_index("ix_skill_evidence_computation_run_id", "skill_evidence", ["computation_run_id"])

    # ------------------------------------------------------------------
    # 8. Seed initial skill taxonomy
    # ------------------------------------------------------------------
    skill_tags_table = sa.table(
        "skill_tags",
        sa.column("name", sa.String),
        sa.column("category", sa.String),
        sa.column("aliases", postgresql.JSONB),
    )
    op.bulk_insert(
        skill_tags_table,
        [
            {"name": name, "category": category, "aliases": aliases}
            for name, category, aliases in _SEED_SKILLS
        ],
    )


def downgrade() -> None:
    op.drop_table("skill_evidence")
    op.drop_table("user_skills")
    op.drop_table("skill_computation_runs")
    op.drop_table("module_skill_mappings")
    op.drop_table("skill_tags")
    op.drop_table("module_handbook_entries")
    # Note: PostgreSQL does not support removing enum values in-place.
    # compute_skills and ingest_handbook are left in job_type on downgrade.
