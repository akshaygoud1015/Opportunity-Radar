from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://opportunityradar:opportunityradar@db:5432/opportunityradar"
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-4-6"

    # Companies/sources to query on each manual scrape run.
    greenhouse_boards: list[str] = ["idealist", "khanacademy"]
    lever_companies: list[str] = ["netlify"]
    remoteok_enabled: bool = True

    class Config:
        env_file = ".env"


settings = Settings()
