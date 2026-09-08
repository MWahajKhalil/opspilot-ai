from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    print("Starting up...")
    yield
    print("Shutting down...")
    
app = FastAPI(lifespan=lifespan)



@app.get("/health")
async def health_check():
    return {"status": "ok"}



