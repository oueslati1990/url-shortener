import datetime
from pydantic import BaseModel, HttpUrl


class URLCreate(BaseModel):
    original_url: HttpUrl


class URLResponse(BaseModel):
    id: int
    short_code: str
    short_url: str
    original_url: str
    clicks: int
    created_at: datetime
