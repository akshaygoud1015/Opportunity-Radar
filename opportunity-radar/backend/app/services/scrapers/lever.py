import httpx

from app.services.scrapers.base import BaseScraper, RawJob

# Public API. Docs: https://github.com/lever/postings-api
LEVER_URL = "https://api.lever.co/v0/postings/{company}?mode=json"


class LeverScraper(BaseScraper):
    source_name = "lever"

    def __init__(self, companies: list[str]):
        self.companies = companies

    async def fetch(self) -> list[RawJob]:
        jobs: list[RawJob] = []
        async with httpx.AsyncClient(timeout=20.0) as client:
            for company in self.companies:
                try:
                    resp = await client.get(LEVER_URL.format(company=company))
                    resp.raise_for_status()
                except httpx.HTTPError:
                    continue

                for item in resp.json():
                    categories = item.get("categories", {})
                    jobs.append(
                        RawJob(
                            source=self.source_name,
                            external_id=item["id"],
                            company=company,
                            title=item.get("text", ""),
                            location=categories.get("location"),
                            url=item.get("hostedUrl", ""),
                            description=item.get("descriptionPlain", item.get("description", "")),
                            posted_at=None,
                        )
                    )
        return jobs
