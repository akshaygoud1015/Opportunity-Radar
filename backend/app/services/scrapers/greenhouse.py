import httpx

from app.services.scrapers.base import BaseScraper, RawJob

# Public, unauthenticated API -- no scraping/ToS gray area.
# Docs: https://developers.greenhouse.io/job-board.html
GREENHOUSE_URL = "https://boards-api.greenhouse.io/v1/boards/{board}/jobs?content=true"


class GreenhouseScraper(BaseScraper):
    source_name = "greenhouse"

    def __init__(self, board_tokens: list[str]):
        # board_tokens are the company slugs used in Greenhouse's public job board
        # URLs, e.g. "idealist" from boards.greenhouse.io/idealist
        self.board_tokens = board_tokens

    async def fetch(self) -> list[RawJob]:
        jobs: list[RawJob] = []
        async with httpx.AsyncClient(timeout=20.0) as client:
            for board in self.board_tokens:
                try:
                    resp = await client.get(GREENHOUSE_URL.format(board=board))
                    resp.raise_for_status()
                except httpx.HTTPError:
                    # One bad board shouldn't kill the whole run.
                    continue

                for item in resp.json().get("jobs", []):
                    jobs.append(
                        RawJob(
                            source=self.source_name,
                            external_id=str(item["id"]),
                            company=board,
                            title=item.get("title", ""),
                            location=(item.get("location") or {}).get("name"),
                            url=item.get("absolute_url", ""),
                            description=item.get("content", ""),
                            posted_at=item.get("updated_at"),
                        )
                    )
        return jobs
