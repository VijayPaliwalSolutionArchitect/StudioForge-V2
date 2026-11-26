"""app/routes/campaigns.py — Marketing campaign endpoints."""

from __future__ import annotations
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from ..database.creative_repository import CreativeRepository
from ..database.brand_repository import BrandRepository

router = APIRouter(prefix="/api/v1/campaigns", tags=["campaigns"])


class CreateCampaignRequest(BaseModel):
    brand_id: str
    name: str = Field(..., min_length=2)
    objective: Optional[str] = "AWARENESS"
    budget_usd: Optional[float] = 0.0
    is_paid: Optional[bool] = False
    start_date: Optional[str] = "2026-11-26"


def get_creative_repo(request: Request) -> CreativeRepository:
    return request.app.state.creative_repo


def get_brand_repo(request: Request) -> BrandRepository:
    return request.app.state.brand_repo


@router.get("")
def list_campaigns(brand_id: Optional[str] = None, creative_repo: CreativeRepository = Depends(get_creative_repo)):
    return creative_repo.list_campaigns(brand_id=brand_id)


@router.post("")
def create_campaign(
    req: CreateCampaignRequest,
    creative_repo: CreativeRepository = Depends(get_creative_repo),
    brand_repo: BrandRepository = Depends(get_brand_repo)
):
    brand = brand_repo.get_brand(req.brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    return creative_repo.create_campaign(
        brand_id=req.brand_id,
        name=req.name,
        objective=req.objective or "AWARENESS",
        budget_usd=req.budget_usd or 0.0,
        is_paid=req.is_paid or False,
        start_date=req.start_date or "2026-11-26",
    )
