import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class JobPostingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    source: str
    company: str
    title: str
    location: str | None
    url: str
    is_entry_level: bool
    visa_score: float
    posted_at: datetime | None
    created_at: datetime


class JobPostingDetail(JobPostingOut):
    description: str
    extracted_skills: dict | None


class ScrapeRunOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    started_at: datetime
    finished_at: datetime | None
    status: str
    sources: dict
    job_count: int = 0


class ScrapeRunResult(BaseModel):
    scrape_run: ScrapeRunOut
    jobs: list[JobPostingOut]


class SkillExtractionResult(BaseModel):
    required_skills: list[str]
    nice_to_have_skills: list[str]


class SkillMatchResult(BaseModel):
    matched_skills: list[str]  # skills you have that the job wants -- safe to feature/reorder
    gap_skills: list[str]      # skills the job wants that you don't have -- never added to resume


class TailorRequest(BaseModel):
    job_posting_id: uuid.UUID
    doc_type: str = "resume"  # "resume" | "cv"


class TailorResponse(BaseModel):
    pdf_url: str
    matched_skills: list[str]
    gap_skills: list[str]
