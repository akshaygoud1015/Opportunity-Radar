from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import JobPosting, TailoredResume
from app.schemas import TailorRequest, TailorResponse, SkillMatchResult
from app.services.resume_generator import generate_document

router = APIRouter(prefix="/resume", tags=["resume"])


@router.post("/tailor", response_model=TailorResponse)
def tailor_resume(request: TailorRequest, db: Session = Depends(get_db)):
    job = db.query(JobPosting).filter(JobPosting.id == request.job_posting_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job posting not found")
    if not job.extracted_skills:
        raise HTTPException(
            status_code=400,
            detail="Run POST /skills/extract/{job_id} for this job before tailoring a resume.",
        )

    match_result = SkillMatchResult(
        matched_skills=job.extracted_skills["matched_skills"],
        gap_skills=job.extracted_skills["gap_skills"],
    )

    headline = "Software Engineer" if request.doc_type == "resume" else "Software Engineer / Researcher"
    pdf_path = generate_document(request.doc_type, match_result, headline=headline)

    record = TailoredResume(
        job_posting_id=job.id,
        doc_type=request.doc_type,
        matched_skills={"matched": match_result.matched_skills, "gaps": match_result.gap_skills},
        pdf_path=str(pdf_path),
    )
    db.add(record)
    db.commit()

    return TailorResponse(
        pdf_url=f"/generated/{pdf_path.name}",
        matched_skills=match_result.matched_skills,
        gap_skills=match_result.gap_skills,
    )
