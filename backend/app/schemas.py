from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EventBase(BaseModel):
    source: str
    source_id: str
    title: str
    url: str
    location: str | None = None
    starts_at: datetime | None = None
    description: str | None = None


class EventCreate(EventBase):
    pass


class EventRead(EventBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SourceRun(BaseModel):
    name: str
    method: str
    configured: bool
    status: str
    events_found: int = 0
    error: str | None = None


class ScrapeResult(BaseModel):
    scanned: int
    created: int
    updated: int
    sources: list[SourceRun] = Field(default_factory=list)


class SourceInfo(BaseModel):
    name: str
    method: str
    configured: bool
    description: str


class SourceDiagnostic(BaseModel):
    url: str
    status: str
    detected_format: str | None = None
    linked_sources: list[str] = Field(default_factory=list)
    events_found: int = 0
    error: str | None = None
