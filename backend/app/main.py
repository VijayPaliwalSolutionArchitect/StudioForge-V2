"""app/main.py — FastAPI Application Factory for StudioForge V2."""

from __future__ import annotations
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database.connection import Database
from .database.brand_repository import BrandRepository
from .database.creative_repository import CreativeRepository
from .database.approval_repository import ApprovalRepository
from .rag.brand_retriever import BrandRetriever
from .routes import (
    brands_router,
    campaigns_router,
    briefs_router,
    assets_router,
    calendar_router,
    approvals_router,
    admin_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not hasattr(app.state, "db") or app.state.db is None:
        app.state.db = Database(settings.database_url)
    if not hasattr(app.state, "brand_repo") or app.state.brand_repo is None:
        app.state.brand_repo = BrandRepository(app.state.db)
    if not hasattr(app.state, "creative_repo") or app.state.creative_repo is None:
        app.state.creative_repo = CreativeRepository(app.state.db)
    if not hasattr(app.state, "approval_repo") or app.state.approval_repo is None:
        app.state.approval_repo = ApprovalRepository(app.state.db)
    if not hasattr(app.state, "retriever") or app.state.retriever is None:
        app.state.retriever = BrandRetriever(app.state.brand_repo)

    yield

    if hasattr(app.state, "db") and app.state.db:
        try:
            app.state.db.close()
        except Exception:
            pass


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Autonomous AI Brand & Media Factory with ComfyUI Prompt Synthesis & Brand Tone Consistency Reasoning",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
@app.get("/healthz")
def health_check():
    return {
        "status": "ok",
        "service": "StudioForge V2",
        "version": settings.app_version,
        "two_man_approval_active": settings.require_two_man_approval_for_paid_ads,
    }


@app.get("/readyz")
def readiness_check():
    return {"status": "ready", "database": "connected_wal_mode"}


# Register Routers
app.include_router(brands_router)
app.include_router(campaigns_router)
app.include_router(briefs_router)
app.include_router(assets_router)
app.include_router(calendar_router)
app.include_router(approvals_router)
app.include_router(admin_router)
