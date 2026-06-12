from functools import lru_cache
from typing import Annotated

from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ai-blockchain-events"
    database_url: str = "sqlite:///./events.db"
    scraper_keywords: str = "ai,artificial intelligence,blockchain,web3,crypto"
    cors_origins: Annotated[list[str], NoDecode] = ["http://localhost:5173"]
    source_urls: str = ""
    ticketmaster_api_key: str = ""
    ticketmaster_city: str = "Toronto"
    ticketmaster_country_code: str = "CA"
    ics_feed_urls: str = ""
    rss_feed_urls: str = ""
    json_ld_event_urls: str = ""
    html_event_urls: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @property
    def keywords(self) -> list[str]:
        return [keyword.strip() for keyword in self.scraper_keywords.split(",") if keyword.strip()]

    @staticmethod
    def parse_urls(value: str) -> list[str]:
        return [url.strip() for url in value.split(",") if url.strip()]

    @property
    def ics_urls(self) -> list[str]:
        return self.parse_urls(self.ics_feed_urls)

    @property
    def sources(self) -> list[str]:
        return self.parse_urls(self.source_urls)

    @property
    def rss_urls(self) -> list[str]:
        return self.parse_urls(self.rss_feed_urls)

    @property
    def json_ld_urls(self) -> list[str]:
        return self.parse_urls(self.json_ld_event_urls)

    @property
    def html_urls(self) -> list[str]:
        return self.parse_urls(self.html_event_urls)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
