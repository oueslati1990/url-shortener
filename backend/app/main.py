import logging
from fastapi import FastAPI

app = FastAPI(title="Url Shoretener")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
