"""app/routes/calendar.py — Content calendar & scheduling endpoints."""

from __future__ import annotations
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from ..database.creative_repository import CreativeRepository

router = APIRouter(prefix="/api/v1/calendar", tags=["calendar"])


class ScheduleItemRequest(BaseModel):
    brief_id: str
    brand_id: str
    channel: str = Field(..., description="LINKEDIN, TWITTER, INSTAGRAM, YOUTUBE")
    scheduled_for: str = Field(..., description="ISO datetime string")
    copy_text: str = Field(..., min_length=5)


def get_creative_repo(request: Request) -> CreativeRepository:
    return request.app.state.creative_repo


@router.get("")
def list_calendar(creative_repo: CreativeRepository = Depends(get_creative_repo)):
    return creative_repo.list_calendar()


@router.post("")
def schedule_calendar_item(req: ScheduleItemRequest, creative_repo: CreativeRepository = Depends(get_creative_repo)):
    brief = creative_repo.get_brief(req.brief_id)
    if not brief:
        raise HTTPException(status_code=404, detail="Creative brief not found")

    return creative_repo.schedule_item(
        brief_id=req.brief_id,
        brand_id=req.brand_id,
        channel=req.channel,
        scheduled_for=req.scheduled_for,
        copy_text=req.copy_text,
    )
