from fastapi import APIRouter, HTTPException

from app.shemas import URLResponse, URLCreate
from app import store
from app.config import settings

router = APIRouter(prefix="/api/urls", tags=["urls"])


@router.post("/", response_model=URLResponse, status_code=201)
def shorten_url(payload: URLCreate):
    code = store.generate_code(settings.short_code_length)
    result = store.save(code, payload.original_url)
    if not result:
        raise HTTPException(
            status_code=400, detail="An issue happened when creating the short url"
        )
    return URLResponse(**result, short_url=f"{settings.base_url}/{code}")
