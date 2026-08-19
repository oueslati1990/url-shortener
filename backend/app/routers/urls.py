from fastapi import APIRouter, HTTPException

from app.shemas import URLResponse, URLCreate
from app import store
from app.config import settings

router = APIRouter(prefix="/api/urls", tags=["urls"])


@router.post("/", response_model=URLResponse, status_code=201)
def shorten_url(payload: URLCreate):
    try:
        code = store.generate_code(settings.short_code_length)
        store.save(code, payload.original_url)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    return URLResponse(
        short_code=code,
        short_url=f"{settings.base_url}/{code}",
        original_url=payload.original_url,
    )
