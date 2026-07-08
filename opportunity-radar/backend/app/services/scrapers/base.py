from abc import ABC, abstractmethod
from typing import TypedDict


class RawJob(TypedDict):
    source: str
    external_id: str
    company: str
    title: str
    location: str | None
    url: str
    description: str
    posted_at: str | None  # ISO string, parsed later


class BaseScraper(ABC):
    """Every scraper source implements fetch() and returns a flat list of RawJob.
    Keep sources reading from official/public JSON APIs where possible --
    that's more reliable than HTML scraping and avoids ToS gray areas."""

    source_name: str

    @abstractmethod
    async def fetch(self) -> list[RawJob]:
        ...
