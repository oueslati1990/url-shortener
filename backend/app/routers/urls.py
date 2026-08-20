from fastapi import APIRouter, HTTPException, status

from app.shemas import URLResponse, URLCreate
from app import store
from app.config import settings

router = APIRouter(prefix="/api/urls", tags=["urls"])


@router.post("/", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
def shorten_url(payload: URLCreate):
    original_url = str(payload.original_url)
    try:
        code = store.generate_code(settings.short_code_length)
        store.save(code, original_url)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    return URLResponse(
        short_code=code,
        short_url=f"{settings.base_url}/{code}",
        original_url=original_url,
    )


@router.get("/", response_model=list[URLResponse])
def list_all():
    all_entries = store.list_all_entries()
    return [
        URLResponse(
            short_code=e["short_code"],
            original_url=e["original_url"],
            short_url=f"{settings.base_url}/{e["short_code"]}",
        )
        for e in all_entries
    ]
