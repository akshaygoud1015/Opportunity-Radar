"""Lightweight heuristics run on every scraped posting before it hits the DB.

These are intentionally simple keyword heuristics, not a trained classifier --
good enough to triage a day's postings, not a substitute for reading the
actual listing before you apply.
"""

ENTRY_LEVEL_KEYWORDS = [
    "entry level", "entry-level", "junior", "new grad", "graduate",
    "associate", "early career", "0-2 years", "0-1 years", "i (level 1)",
]

SENIOR_EXCLUDE_KEYWORDS = [
    "senior", "sr.", "staff", "principal", "lead", "director", "manager",
    "10+ years", "8+ years", "7+ years",
]

# Keyword signals in the JD text itself that suggest openness to sponsorship.
VISA_POSITIVE_KEYWORDS = [
    "visa sponsorship available", "will sponsor", "h-1b sponsorship",
    "opt", "cpt", "sponsorship available", "international candidates welcome",
]

# Explicit red flags -- if present, treat visa_score as near zero regardless
# of anything else.
VISA_NEGATIVE_KEYWORDS = [
    "no sponsorship", "not able to sponsor", "must be authorized to work",
    "u.s. citizens only", "us citizenship required", "unable to sponsor",
]


def is_entry_level(title: str, description: str) -> bool:
    text = f"{title} {description}".lower()
    if any(kw in text for kw in SENIOR_EXCLUDE_KEYWORDS):
        return False
    return any(kw in text for kw in ENTRY_LEVEL_KEYWORDS)


def visa_score(description: str, company: str, known_sponsors: set[str]) -> float:
    """Returns a 0-1 heuristic likelihood of visa sponsorship.

    known_sponsors should be populated from DOL H-1B disclosure data (the
    kind of data h1bgrader.com surfaces) -- see scripts/load_h1b_sponsors.py
    for a starting point on building that set yourself.
    """
    text = description.lower()

    if any(kw in text for kw in VISA_NEGATIVE_KEYWORDS):
        return 0.0

    score = 0.0
    if any(kw in text for kw in VISA_POSITIVE_KEYWORDS):
        score += 0.6
    if company.strip().lower() in known_sponsors:
        score += 0.4

    return min(score, 1.0)
