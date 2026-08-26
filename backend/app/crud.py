import string
import random
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import URL
from app.config import settings

ALPHABET = string.ascii_letters + string.digits


def _generate_code(length: int) -> str:
    return "".join(random.choices(ALPHABET, k=length))


async def create_url(db: AsyncSession, original_url: str) -> URL:
    for _ in range(5):
        code = _generate_code(settings.short_code_length)
        existing = await db.scalar(select(URL).where(URL.short_code == code))
        if not existing:
            url = URL(original_url=original_url, short_code=code)
            db.add(url)
            await db.commit()
            await db.refresh(url)
            return url
    raise RuntimeError("Could not generate a unique short code after 5 attempts")


async def get_by_code(db: AsyncSession, code: str) -> URL | None:
    return await db.scalar(select(URL).where(URL.short_code == code))


async def list_urls(db: AsyncSession, limit: int = 50) -> list[URL]:
    result = await db.execute(
        select(URL).order_by(URL.created_at.desc()).limit(limit=limit)
    )
    return list(result.scalars().all())


async def increment_clicks(db: AsyncSession, url: URL) -> None:
    url.click_count += 1
    await db.commit()
