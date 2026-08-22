from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.shemas import URLResponse, URLCreate
from app import crud
from database import get_db
from app.config import settings

router = APIRouter(prefix="/api/urls", tags=["urls"])


@router.post("/", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
async def shorten_url(payload: URLCreate, db: AsyncSession = Depends(get_db)):
    original_url = str(payload.original_url)
    try:
        url = await crud.create_url(db=db, original_url=original_url)
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {**url.__dict__, "short_url": f"{settings.base_url}/{url.short_code}"}


@router.get("/", response_model=list[URLResponse])
def list_all():
    all_entries = store.list_all_entries()
    return [
        URLResponse(
            short_code=e["short_code"],
            original_url=e["original_url"],
            short_url=f"{settings.base_url}/{e['short_code']}",
        )
        for e in all_entries
    ]


redirect_router = APIRouter(tags=["redirect"])


@redirect_router.get("/{code}")
def redirect_to_original(code: str):
    original = store.find(code)
    if not original:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="url not found !"
        )
    return RedirectResponse(original, status_code=status.HTTP_302_FOUND)
