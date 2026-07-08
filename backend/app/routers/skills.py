import json
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import JobPosting
from app.schemas import SkillMatchResult
from app.services.skill_extraction import SkillExtractor
from app.services.skill_matcher import match_skills

router = APIRouter(prefix="/skills", tags=["skills"])

SKILL_BANK_PATH = Path(__file__).parent.parent / "data" / "master_skill_bank.json"


def _flat_skill_bank() -> list[str]:
    categories: dict[str, list[str]] = json.loads(SKILL_BANK_PATH.read_text())
    return [skill for skills in categories.values() for skill in skills]


@router.post("/extract/{job_id}", response_model=SkillMatchResult)
def extract_and_match(job_id: uuid.UUID, db: Session = Depends(get_db)):
    """Runs the job description through Claude to extract required skills,
    then matches against your master skill bank. Only matched (truthful)
    skills are ever eligible to appear on a generated resume -- gap_skills
    are informational only.
    """
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job posting not found")

    extractor = SkillExtractor()
    extraction = extractor.extract(job.description)
    match_result = match_skills(extraction, _flat_skill_bank())

    job.extracted_skills = {
        "required_skills": extraction.required_skills,
        "nice_to_have_skills": extraction.nice_to_have_skills,
        "matched_skills": match_result.matched_skills,
        "gap_skills": match_result.gap_skills,
    }
    db.commit()

    return match_result
