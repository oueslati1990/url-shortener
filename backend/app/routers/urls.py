from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.shemas import URLResponse, URLCreate
from app import crud
from app.database import get_db
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
async def list_all(db: AsyncSession = Depends(get_db)):
    urls = await crud.list_urls(db)
    return [
        {**u.__dict__, "short_url": f"{settings.base_url}/{u.short_code}"} for u in urls
    ]


redirect_router = APIRouter(tags=["redirect"])


@redirect_router.get("/{code}")
async def redirect_to_original(code: str, db: AsyncSession = Depends(get_db)):
    url = await crud.get_by_code(code=code, db=db)
    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="url not found !"
        )
    return RedirectResponse(url.original_url, status_code=status.HTTP_302_FOUND)
