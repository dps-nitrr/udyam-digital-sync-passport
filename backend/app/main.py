import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import settings
from backend.app.db import init_db
from backend.app.routers import (
    registry,
    advisor,
    quote,
    consent,
    kyc,
    orders,
    backoffice,
    metrics,
    privacy
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize database and load CSV registries
    init_db()
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    yield
    # Shutdown

app = FastAPI(
    title="Sync Passport — GSTIN-First SMB Onboarding API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
origins = [
    settings.CORS_ORIGIN,
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(registry.router)
app.include_router(advisor.router)
app.include_router(quote.router)
app.include_router(consent.router)
app.include_router(kyc.router)
app.include_router(orders.router)
app.include_router(backoffice.router)
app.include_router(metrics.router)
app.include_router(privacy.router)

@app.get("/")
def root():
    return {
        "service": "Sync Passport SMB Onboarding API",
        "status": "operational",
        "demo_today": settings.DEMO_TODAY,
        "docs_url": "/docs"
    }

@app.get("/api/health")
def health():
    return {"status": "ok"}
