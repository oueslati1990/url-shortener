from fastapi import FastAPI
from app.routers.urls import router, redirect_router

app = FastAPI(title="Url Shortener app")

app.include_router(router)
app.include_router(redirect_router)
