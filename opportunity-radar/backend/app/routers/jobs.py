import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import JobPosting
from app.schemas import JobPostingOut, JobPostingDetail

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=list[JobPostingOut])
def list_jobs(
    scrape_run_id: uuid.UUID | None = Query(default=None, description="Filter to one scrape run"),
    entry_level_only: bool = Query(default=False),
    min_visa_score: float = Query(default=0.0, ge=0.0, le=1.0),
    db: Session = Depends(get_db),
):
    q = db.query(JobPosting)
    if scrape_run_id:
        q = q.filter(JobPosting.scrape_run_id == scrape_run_id)
    if entry_level_only:
        q = q.filter(JobPosting.is_entry_level.is_(True))
    if min_visa_score:
        q = q.filter(JobPosting.visa_score >= min_visa_score)

    jobs = q.order_by(JobPosting.visa_score.desc(), JobPosting.created_at.desc()).all()
    return [JobPostingOut.model_validate(j) for j in jobs]


@router.get("/{job_id}", response_model=JobPostingDetail)
def get_job(job_id: uuid.UUID, db: Session = Depends(get_db)):
    job = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job posting not found")
    return JobPostingDetail.model_validate(job)
