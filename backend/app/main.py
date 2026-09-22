from contextlib import asynccontextmanager

from fastapi import FastAPI
import httpx
from app.api.device import router as device_router



@asynccontextmanager
async def lifespan(app):
    print("Starting up...")
    timeout = httpx.Timeout(10.0, connect=5.0)
    
    async with httpx.AsyncClient(timeout=timeout) as http_client:
        app.state.http_client = http_client
        yield
    print("Shutting down...")
    

app = FastAPI(lifespan=lifespan)
app.include_router(device_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}



