"""app/routes/briefs.py — Creative brief generation with Brand Tone validation & ComfyUI prompts."""

from __future__ import annotations
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from ..database.creative_repository import CreativeRepository
from ..database.brand_repository import BrandRepository
from ..database.approval_repository import ApprovalRepository
from ..brand.tone_analyzer import BrandToneAnalyzer
from ..creative.prompt_synthesizer import VisualPromptSynthesizer
from ..config import settings

router = APIRouter(prefix="/api/v1/briefs", tags=["briefs"])


class GenerateBriefRequest(BaseModel):
    campaign_id: str
    brand_id: str
    concept_title: str = Field(..., min_length=3)
    core_idea: str = Field(..., min_length=5)
    target_channels: Optional[List[str]] = Field(default_factory=lambda: ["linkedin", "x_twitter"])
    aspect_ratio: Optional[str] = "16:9"
    requested_by: Optional[str] = "producer@shivamitcs.com"


def get_creative_repo(request: Request) -> CreativeRepository:
    return request.app.state.creative_repo


def get_brand_repo(request: Request) -> BrandRepository:
    return request.app.state.brand_repo


def get_approval_repo(request: Request) -> ApprovalRepository:
    return request.app.state.approval_repo


@router.get("")
def list_briefs(campaign_id: Optional[str] = None, creative_repo: CreativeRepository = Depends(get_creative_repo)):
    return creative_repo.list_briefs(campaign_id=campaign_id)


@router.post("")
def generate_creative_brief(
    req: GenerateBriefRequest,
    creative_repo: CreativeRepository = Depends(get_creative_repo),
    brand_repo: BrandRepository = Depends(get_brand_repo),
    approval_repo: ApprovalRepository = Depends(get_approval_repo)
):
    brand = brand_repo.get_brand(req.brand_id)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    # 1. Evaluate Tone & Brand Alignment
    tone_result = BrandToneAnalyzer.analyze_tone(
        text=f"{req.concept_title} {req.core_idea}",
        tone_of_voice=brand["tone_of_voice"],
        forbidden_words=brand["forbidden_words"],
        primary_color_hex=brand["primary_color_hex"],
    )

    if not tone_result["passed_brand_check"]:
        violations_msg = "; ".join(tone_result["violations"]) or "Brand tone alignment score below 75%"
        raise HTTPException(
            status_code=422,
            detail=f"Brand Guard Rejection: {violations_msg} (Score: {tone_result['brand_alignment_score']})"
        )

    # 2. Synthesize ComfyUI Visual Prompt
    visual_spec = VisualPromptSynthesizer.synthesize_prompt(
        concept=req.core_idea,
        primary_color_hex=brand["primary_color_hex"],
        secondary_color_hex=brand["secondary_color_hex"],
        aspect_ratio=req.aspect_ratio or "16:9",
    )

    hook = f"How {brand['name']} is redefining autonomous enterprise velocity"
    cta = "Deploy sovereign AI across your infrastructure today"

    # 3. Store Brief
    brief = creative_repo.create_brief(
        campaign_id=req.campaign_id,
        brand_id=req.brand_id,
        title=req.concept_title,
        hook=hook,
        core_message=req.core_idea,
        call_to_action=cta,
        target_channels=req.target_channels or ["linkedin"],
        visual_prompt=visual_spec["positive_prompt"],
        negative_prompt=visual_spec["negative_prompt"],
        aspect_ratio=req.aspect_ratio or "16:9",
        brand_alignment_score=tone_result["brand_alignment_score"],
    )

    # 4. Check if campaign requires Two-Man Creative Approval
    campaigns = creative_repo.list_campaigns(brand_id=req.brand_id)
    camp = next((c for c in campaigns if c["id"] == req.campaign_id), None)
    requires_approval = bool(camp and camp.get("is_paid_campaign") and settings.require_two_man_approval_for_paid_ads)

    approval_info = None
    if requires_approval:
        approval_info = approval_repo.request_approval(
            brief_id=brief["id"],
            campaign_id=req.campaign_id,
            requested_by=req.requested_by or "producer@shivamitcs.com",
            requester_role="CREATIVE_PRODUCER",
        )
        creative_repo.update_brief_status(brief["id"], "IN_REVIEW")
        brief["status"] = "IN_REVIEW"

    return {
        "brief": brief,
        "visual_spec": visual_spec,
        "tone_result": tone_result,
        "requires_two_man_approval": requires_approval,
        "approval": approval_info,
    }
