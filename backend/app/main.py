from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.device import router as device_router


@asynccontextmanager
async def lifespan(app):
    print("Starting up...")
    yield
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)
app.include_router(device_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
