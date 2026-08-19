from fastapi import FastAPI
from app.routers.urls import router as urls_router

app = FastAPI(title="Url Shortener app")

app.include_router(urls_router)
