import httpx

from app.services.scrapers.base import BaseScraper, RawJob

# Public API, no key required. https://remoteok.com/api
REMOTEOK_URL = "https://remoteok.com/api"


class RemoteOkScraper(BaseScraper):
    source_name = "remoteok"

    async def fetch(self) -> list[RawJob]:
        jobs: list[RawJob] = []
        # RemoteOK asks for a descriptive User-Agent -- be a good citizen.
        headers = {"User-Agent": "OpportunityRadar/1.0 (personal job search tool)"}
        async with httpx.AsyncClient(timeout=20.0, headers=headers) as client:
            try:
                resp = await client.get(REMOTEOK_URL)
                resp.raise_for_status()
            except httpx.HTTPError:
                return jobs

            data = resp.json()
            # First element is metadata, not a job -- skip it.
            for item in data[1:]:
                if not isinstance(item, dict) or "id" not in item:
                    continue
                jobs.append(
                    RawJob(
                        source=self.source_name,
                        external_id=str(item["id"]),
                        company=item.get("company", ""),
                        title=item.get("position", item.get("title", "")),
                        location=item.get("location"),
                        url=item.get("url", ""),
                        description=item.get("description", ""),
                        posted_at=item.get("date"),
                    )
                )
        return jobs
