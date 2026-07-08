from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.routers import scrape, jobs, skills, resume

app = FastAPI(title="OpportunityRadar", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scrape.router)
app.include_router(jobs.router)
app.include_router(skills.router)
app.include_router(resume.router)

GENERATED_DIR = Path(__file__).parent.parent / "generated"
GENERATED_DIR.mkdir(exist_ok=True)
app.mount("/generated", StaticFiles(directory=str(GENERATED_DIR)), name="generated")


@app.on_event("startup")
def on_startup():
    # Scaffold-simple table creation. Swap for Alembic migrations once the
    # schema stabilizes.
    Base.metadata.create_all(bind=engine)


@app.get("/health")
def health():
    return {"status": "ok"}
