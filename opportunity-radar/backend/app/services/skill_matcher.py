"""Matches a job's extracted skills against your master skill bank.

This is the honesty boundary of the whole pipeline: matched_skills can be
surfaced/reordered on a generated resume, gap_skills must NEVER be added --
they're purely informational, so you can see what's worth learning next.
"""

from app.schemas import SkillExtractionResult, SkillMatchResult

# Common aliases so "JS" matches "JavaScript", "Postgres" matches "PostgreSQL", etc.
# Extend this as you notice more job postings phrasing your own skills differently.
SKILL_ALIASES: dict[str, str] = {
    "js": "javascript",
    "ts": "typescript",
    "postgres": "postgresql",
    "psql": "postgresql",
    "node": "node.js",
    "nodejs": "node.js",
    "react.js": "react",
    "reactjs": "react",
    "next.js": "nextjs",
    "sklearn": "scikit-learn",
    "gcp": "google cloud platform",
}


def _normalize(skill: str) -> str:
    s = skill.strip().lower()
    return SKILL_ALIASES.get(s, s)


def match_skills(
    extraction: SkillExtractionResult, master_skill_bank: list[str]
) -> SkillMatchResult:
    bank_normalized = {_normalize(s): s for s in master_skill_bank}

    requested = extraction.required_skills + extraction.nice_to_have_skills

    matched: list[str] = []
    gaps: list[str] = []
    seen = set()

    for skill in requested:
        norm = _normalize(skill)
        if norm in seen:
            continue
        seen.add(norm)

        if norm in bank_normalized:
            matched.append(bank_normalized[norm])  # use your own casing, e.g. "PostgreSQL"
        else:
            gaps.append(skill)

    return SkillMatchResult(matched_skills=matched, gap_skills=gaps)
