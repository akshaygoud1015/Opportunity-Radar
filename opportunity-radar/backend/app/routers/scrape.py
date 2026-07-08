from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import ScrapeRun, JobPosting
from app.schemas import ScrapeRunResult, ScrapeRunOut, JobPostingOut
from app.services.filters import is_entry_level, visa_score
from app.services.scrapers import GreenhouseScraper, LeverScraper, RemoteOkScraper

router = APIRouter(prefix="/scrape", tags=["scrape"])

# TODO: replace with a real set built from DOL H-1B disclosure data, the kind
# h1bgrader.com surfaces -- see scripts/load_h1b_sponsors.py for a starting point.
KNOWN_SPONSORS: set[str] = set()


@router.post("/run", response_model=ScrapeRunResult)
async def run_scrape(db: Session = Depends(get_db)):
    """Manually triggered scrape -- no scheduler. Pulls from every configured
    source, applies entry-level + visa heuristics, and stores results under a
    new ScrapeRun so the dashboard can show 'this run's listings' as a group.
    """
    scrape_run = ScrapeRun(status="running", sources={})
    db.add(scrape_run)
    db.commit()
    db.refresh(scrape_run)

    scrapers = [
        GreenhouseScraper(settings.greenhouse_boards),
        LeverScraper(settings.lever_companies),
    ]
    if settings.remoteok_enabled:
        scrapers.append(RemoteOkScraper())

    source_counts: dict[str, int] = {}
    saved_jobs: list[JobPosting] = []

    for scraper in scrapers:
        raw_jobs = await scraper.fetch()
        count = 0
        for raw in raw_jobs:
            # Dedup: skip if we already have this exact (source, external_id) pair.
            exists = (
                db.query(JobPosting)
                .filter_by(source=raw["source"], external_id=raw["external_id"])
                .first()
            )
            if exists:
                continue

            posting = JobPosting(
                scrape_run_id=scrape_run.id,
                source=raw["source"],
                external_id=raw["external_id"],
                company=raw["company"],
                title=raw["title"],
                location=raw["location"],
                url=raw["url"],
                description=raw["description"],
                is_entry_level=is_entry_level(raw["title"], raw["description"]),
                visa_score=visa_score(raw["description"], raw["company"], KNOWN_SPONSORS),
            )
            db.add(posting)
            saved_jobs.append(posting)
            count += 1

        source_counts[scraper.source_name] = count

    scrape_run.status = "completed"
    scrape_run.finished_at = datetime.now(timezone.utc)
    scrape_run.sources = source_counts
    db.commit()
    db.refresh(scrape_run)

    return ScrapeRunResult(
        scrape_run=ScrapeRunOut.model_validate(scrape_run, from_attributes=True).model_copy(
            update={"job_count": len(saved_jobs)}
        ),
        jobs=[JobPostingOut.model_validate(j) for j in saved_jobs],
    )
