"""app/routes/brands.py — Brand identity management endpoints."""

from __future__ import annotations
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from ..database.brand_repository import BrandRepository

router = APIRouter(prefix="/api/v1/brands", tags=["brands"])


class CreateBrandRequest(BaseModel):
    name: str = Field(..., min_length=2)
    industry: str
    tone_of_voice: str
    tagline: Optional[str] = ""
    primary_color_hex: Optional[str] = "#06b6d4"
    secondary_color_hex: Optional[str] = "#3b82f6"
    forbidden_words: Optional[List[str]] = Field(default_factory=list)
    target_personas: Optional[List[str]] = Field(default_factory=list)


def get_brand_repo(request: Request) -> BrandRepository:
    return request.app.state.brand_repo


@router.get("")
def list_brands(brand_repo: BrandRepository = Depends(get_brand_repo)):
    return brand_repo.list_brands()


@router.post("")
def create_brand(req: CreateBrandRequest, brand_repo: BrandRepository = Depends(get_brand_repo)):
    return brand_repo.create_brand(
        name=req.name,
        industry=req.industry,
        tone_of_voice=req.tone_of_voice,
        tagline=req.tagline or "",
        primary_color_hex=req.primary_color_hex or "#06b6d4",
        secondary_color_hex=req.secondary_color_hex or "#3b82f6",
        forbidden_words=req.forbidden_words,
        target_personas=req.target_personas,
    )


@router.get("/{brand_id}")
def get_brand(brand_id: str, brand_repo: BrandRepository = Depends(get_brand_repo)):
    b = brand_repo.get_brand(brand_id)
    if not b:
        raise HTTPException(status_code=404, detail="Brand not found")
    return b
