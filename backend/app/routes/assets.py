"""app/routes/assets.py — Creative asset generation & ComfyUI synthesis endpoints."""

from __future__ import annotations
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from ..database.creative_repository import CreativeRepository
from ..creative.asset_generator import AssetGenerator
from ..config import settings

router = APIRouter(prefix="/api/v1/assets", tags=["assets"])


class GenerateAssetRequest(BaseModel):
    brief_id: str
    asset_type: Optional[str] = "IMAGE"
    model: Optional[str] = "flux-1-schnell"


def get_creative_repo(request: Request) -> CreativeRepository:
    return request.app.state.creative_repo


@router.get("")
def list_assets(brief_id: Optional[str] = None, creative_repo: CreativeRepository = Depends(get_creative_repo)):
    return creative_repo.list_assets(brief_id=brief_id)


@router.post("/generate")
def generate_asset(req: GenerateAssetRequest, creative_repo: CreativeRepository = Depends(get_creative_repo)):
    brief = creative_repo.get_brief(req.brief_id)
    if not brief:
        raise HTTPException(status_code=404, detail="Creative brief not found")

    # If brief is in review, assert it cannot be published directly without approval
    if brief["status"] == "REJECTED":
        raise HTTPException(status_code=400, detail="Cannot generate assets for a rejected brief")

    meta = AssetGenerator.generate_asset_metadata(
        brief_title=brief["title"],
        aspect_ratio=brief["aspect_ratio"],
        model=req.model or settings.default_image_model,
    )

    asset = creative_repo.create_asset(
        brief_id=brief["id"],
        brand_id=brief["brand_id"],
        asset_type=req.asset_type or "IMAGE",
        content_url_or_text=meta["asset_url"],
        resolution=meta["resolution"],
        comfyui_prompt_id=meta["comfyui_prompt_id"],
        comfyui_seed=meta["comfyui_seed"],
    )

    return {
        "asset": asset,
        "generation_metadata": meta,
    }
