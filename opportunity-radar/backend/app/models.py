import uuid
from datetime import datetime

from sqlalchemy import String, Text, Float, Boolean, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ScrapeRun(Base):
    """One manually triggered scrape. Groups the jobs pulled during that run."""

    __tablename__ = "scrape_runs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="running")  # running | completed | failed
    sources: Mapped[dict] = mapped_column(JSONB, default=dict)  # e.g. {"greenhouse": 12, "lever": 4}

    jobs: Mapped[list["JobPosting"]] = relationship(back_populates="scrape_run")


class JobPosting(Base):
    __tablename__ = "job_postings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    scrape_run_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("scrape_runs.id"))

    source: Mapped[str] = mapped_column(String(30))  # greenhouse | lever | remoteok
    external_id: Mapped[str] = mapped_column(String(255))  # id from the source, used for dedup
    company: Mapped[str] = mapped_column(String(255))
    title: Mapped[str] = mapped_column(String(255))
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    url: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
    posted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    is_entry_level: Mapped[bool] = mapped_column(Boolean, default=False)
    visa_score: Mapped[float] = mapped_column(Float, default=0.0)  # 0-1 heuristic likelihood

    extracted_skills: Mapped[dict | None] = mapped_column(JSONB, nullable=True)  # filled after tailoring

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    scrape_run: Mapped["ScrapeRun"] = relationship(back_populates="jobs")

    __table_args__ = ()


class MasterSkill(Base):
    """Akshay's ground-truth skill bank -- the tailoring pipeline may only ever
    surface a subset of these, never invent skills outside this table."""

    __tablename__ = "master_skills"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    category: Mapped[str] = mapped_column(String(50))  # e.g. "Languages", "Databases", "AI/ML"


class TailoredResume(Base):
    """Record of a generated resume/CV so you can look back at what was sent where."""

    __tablename__ = "tailored_resumes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_posting_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job_postings.id"))
    doc_type: Mapped[str] = mapped_column(String(10))  # "resume" | "cv"
    matched_skills: Mapped[dict] = mapped_column(JSONB)  # {"matched": [...], "gaps": [...]}
    pdf_path: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
