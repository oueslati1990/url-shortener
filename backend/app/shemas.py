import datetime
from pydantic import BaseModel, HttpUrl


class URLCreate(BaseModel):
    original_url: HttpUrl


class URLResponse(BaseModel):
    id: int
    short_code: str
    short_url: str
    original_url: str
    click_count: int
    created_at: datetime

    model_config = {"from_attributes": True}
