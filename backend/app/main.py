from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import bucketlist, destinations
from app.database import create_db_and_tables
from app.services.seed_service import seed_if_empty


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    seed_if_empty()
    yield


app = FastAPI(
    title="Travel Bucket List",
    description="Reise-Bucketlist mit Weltkarte",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(destinations.router, prefix="/api")
app.include_router(bucketlist.router, prefix="/api")


@app.get("/api/health")
def health():
    return {"status": "ok"}
