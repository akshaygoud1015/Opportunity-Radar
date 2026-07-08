# OpportunityRadar

A job-search agent: run it whenever you want (no scheduler), it pulls entry-level
listings from public job board APIs, scores them for likely visa sponsorship, and
lets you generate a tailored LaTeX resume or CV for any listing in one click --
using only skills you actually have.

## Architecture

```
frontend (Next.js)  <-->  backend (FastAPI)  <-->  Postgres
                                |
                                +--> scrapers (Greenhouse, Lever, RemoteOK)
                                +--> Claude API (skill extraction, tool use)
                                +--> LaTeX (Jinja2 templates -> tectonic -> PDF)
```

- **No daily scheduler.** Everything runs when you click "Run scrape" in the dashboard.
- **Skill matching is a one-way gate.** The tailoring pipeline can only ever
  surface skills already in your `master_skill_bank.json` -- it will never
  invent a skill you don't have. Skills the job wants that you're missing are
  shown separately as "gaps," purely so you know what's worth learning.

## Project layout

```
backend/
  app/
    main.py                 FastAPI app, mounts routers + static PDF serving
    config.py                Settings (env-driven)
    database.py              SQLAlchemy engine/session
    models.py                 ScrapeRun, JobPosting, MasterSkill, TailoredResume
    schemas.py                 Pydantic request/response models
    routers/
      scrape.py                POST /scrape/run
      jobs.py                    GET /jobs, GET /jobs/{id}
      skills.py                   POST /skills/extract/{job_id}
      resume.py                    POST /resume/tailor
    services/
      scrapers/                    One class per job board source
      filters.py                    Entry-level + visa-likelihood heuristics
      skill_extraction.py            Claude tool-use call -> structured skills
      skill_matcher.py                Matches extracted skills to your bank
      resume_generator.py              Jinja2 -> LaTeX -> tectonic -> PDF
    templates/
      resume.tex.jinja                 One-page resume template
      cv.tex.jinja                      Longer CV template
    data/
      profile.py                        Your durable resume content (edit this)
      master_skill_bank.json             Ground-truth skill list
  scripts/
    load_h1b_sponsors.py                 Starting point for real sponsor data

frontend/
  app/page.tsx              Dashboard: scrape button + job table
  components/
    ScrapeButton.tsx           Triggers POST /scrape/run
    JobTable.tsx                 Lists jobs, opens TailorModal per row
    TailorModal.tsx                Extract -> show matched/gap skills -> generate PDF
  lib/api.ts                 Typed fetch client for the backend
```

## Running it locally

### With Docker Compose (recommended)

```bash
cp backend/.env.example backend/.env
# edit backend/.env and add your ANTHROPIC_API_KEY

docker compose up --build
```

- Frontend: http://localhost:3000
- Backend docs: http://localhost:8000/docs

### Without Docker

Backend:
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # fill in ANTHROPIC_API_KEY, point DATABASE_URL at a local Postgres
uvicorn app.main:app --reload
```

Frontend:
```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

You'll also need Postgres running locally, and `tectonic` installed
(https://tectonic-typesetting.github.io/) if you're not using the Docker image,
since it handles LaTeX compilation without a full texlive install.

## What's stubbed vs. real

- **Scrapers** (Greenhouse, Lever, RemoteOK) hit real public APIs -- these work
  out of the box, but `settings.greenhouse_boards` / `lever_companies` in
  `config.py` are seeded with placeholder company slugs. Swap in real ones
  (the slug is whatever appears in `boards.greenhouse.io/<slug>` or
  `jobs.lever.co/<slug>`).
- **Visa scoring** is a keyword heuristic plus an empty `KNOWN_SPONSORS` set --
  see `scripts/load_h1b_sponsors.py` for how to populate it from real DOL
  disclosure data (the same kind of data h1bgrader.com surfaces).
- **Skill extraction** calls the real Claude API -- needs `ANTHROPIC_API_KEY` set.
- **Resume generation** renders real LaTeX and compiles with `tectonic` -- fully
  functional once tectonic is available (bundled in the backend Docker image).
- **Database migrations** use `Base.metadata.create_all()` for simplicity.
  Swap in Alembic once the schema stabilizes and you need to evolve it safely.

## Suggested next steps

1. Seed `config.py` with real Greenhouse/Lever company slugs you actually want to track.
2. Build the real `known_sponsors` set from DOL H-1B data.
3. Add authentication if you ever deploy this somewhere other than localhost --
   right now there's no auth layer since it's assumed to be single-user, local.
4. Consider adding a `scripts/` seed command to backfill `MasterSkill` rows into
   the DB from `master_skill_bank.json` if you want skills queryable via the API
   rather than just read from the JSON file directly.
