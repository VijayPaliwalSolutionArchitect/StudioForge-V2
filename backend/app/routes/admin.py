"""app/routes/admin.py — Fleet telemetry & AI model budget router endpoints."""

from __future__ import annotations
from fastapi import APIRouter, Depends, Request
from ..database.brand_repository import BrandRepository
from ..database.creative_repository import CreativeRepository
from ..database.approval_repository import ApprovalRepository
from ..llm.router import global_router
from ..config import settings

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


def get_brand_repo(request: Request) -> BrandRepository:
    return request.app.state.brand_repo


def get_creative_repo(request: Request) -> CreativeRepository:
    return request.app.state.creative_repo


def get_approval_repo(request: Request) -> ApprovalRepository:
    return request.app.state.approval_repo


@router.get("/stats")
def get_fleet_stats(
    brand_repo: BrandRepository = Depends(get_brand_repo),
    creative_repo: CreativeRepository = Depends(get_creative_repo),
    approval_repo: ApprovalRepository = Depends(get_approval_repo)
):
    brands = brand_repo.list_brands()
    campaigns = creative_repo.list_campaigns()
    briefs = creative_repo.list_briefs()
    assets = creative_repo.list_assets()
    calendar = creative_repo.list_calendar()
    pending_approvals = approval_repo.list_pending_approvals()

    ledger = global_router.ledger.get_summary()

    return {
        "service": "StudioForge V2",
        "version": settings.app_version,
        "brands_count": len(brands),
        "campaigns_count": len(campaigns),
        "briefs_count": len(briefs),
        "assets_generated_count": len(assets),
        "calendar_scheduled_count": len(calendar),
        "pending_two_man_approvals": len(pending_approvals),
        "ai_spend": ledger,
        "comfyui_runtime": {
            "endpoint": settings.comfyui_base_url,
            "status": "ONLINE_STANDBY",
            "default_model": settings.default_image_model,
        },
        "ports": {
            "backend": settings.app_port,
            "frontend": settings.frontend_port,
            "comfyui": 8188,
        }
    }


@router.get("/models")
def get_model_budget_overview():
    return global_router.ledger.get_summary()
