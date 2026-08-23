from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.urls import router, redirect_router
from app.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP: runs before the first request
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield  # <-- app is alive and serving requests here

    # SHUTDOWN: runs after the last request
    await engine.dispose()


app = FastAPI(title="Url Shortener app", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Content-Type"],
)

app.include_router(router)
app.include_router(redirect_router)
