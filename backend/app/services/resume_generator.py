import json
import subprocess
import uuid
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from app.data.profile import PROFILE
from app.schemas import SkillMatchResult

TEMPLATES_DIR = Path(__file__).parent.parent / "templates"
SKILL_BANK_PATH = Path(__file__).parent.parent / "data" / "master_skill_bank.json"
OUTPUT_DIR = Path(__file__).parent.parent.parent / "generated"
OUTPUT_DIR.mkdir(exist_ok=True)

# Jinja's default delimiters clash with LaTeX braces, so swap to block/variable
# markers that don't collide with LaTeX syntax.
_env = Environment(
    loader=FileSystemLoader(str(TEMPLATES_DIR)),
    block_start_string="((*", block_end_string="*))",
    variable_start_string="(((", variable_end_string=")))",
    comment_start_string="((#", comment_end_string="#))",
    trim_blocks=True,
    lstrip_blocks=True,
)


def _load_skill_bank() -> dict[str, list[str]]:
    return json.loads(SKILL_BANK_PATH.read_text())


def _reorder_categories_by_relevance(
    skill_bank: dict[str, list[str]], matched_skills: list[str]
) -> dict[str, list[str]]:
    """Categories containing a matched skill float to the top -- keeps the
    reader's eye on what's relevant to this specific job first."""
    matched_set = {s.lower() for s in matched_skills}

    def relevance(item: tuple[str, list[str]]) -> int:
        _, skills = item
        return -sum(1 for s in skills if s.lower() in matched_set)

    return dict(sorted(skill_bank.items(), key=relevance))


def generate_document(
    doc_type: str,
    match_result: SkillMatchResult,
    headline: str = "Software Engineer",
    summary: str | None = None,
) -> Path:
    """Renders and compiles a resume or CV PDF. doc_type is 'resume' or 'cv'.
    Returns the path to the generated PDF."""

    if doc_type not in ("resume", "cv"):
        raise ValueError("doc_type must be 'resume' or 'cv'")

    skill_bank = _load_skill_bank()
    ordered_bank = _reorder_categories_by_relevance(skill_bank, match_result.matched_skills)

    default_summary = (
        "Software Engineer with a Master of Science in Computer Science "
        "(GPA 3.9/4.0) and hands-on experience building and deploying "
        "full-stack web applications, REST APIs, and AI-powered systems."
    )

    context = {
        **PROFILE,
        "headline": headline,
        "summary": summary or default_summary,
        "skills_by_category": ordered_bank,
        "matched_skills": match_result.matched_skills,
    }

    template = _env.get_template(f"{doc_type}.tex.jinja")
    tex_source = template.render(**context)

    run_id = uuid.uuid4().hex[:8]
    tex_path = OUTPUT_DIR / f"{doc_type}_{run_id}.tex"
    tex_path.write_text(tex_source)

    # tectonic bundles its own TeX packages and fetches what it needs on first
    # run -- no system-wide texlive install required, but it does need
    # internet access the first time it sees a new package.
    result = subprocess.run(
        ["tectonic", str(tex_path), "--outdir", str(OUTPUT_DIR)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"tectonic failed to compile {tex_path.name}:\n{result.stderr}")

    return OUTPUT_DIR / f"{doc_type}_{run_id}.pdf"
