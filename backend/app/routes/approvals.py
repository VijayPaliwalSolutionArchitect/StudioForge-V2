"""app/routes/approvals.py — Two-Man Rule Creative Director approval endpoints."""

from __future__ import annotations
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field

from ..database.approval_repository import ApprovalRepository
from ..database.creative_repository import CreativeRepository

router = APIRouter(prefix="/api/v1/approvals", tags=["approvals"])


class ResolveApprovalRequest(BaseModel):
    decision: str = Field(..., description="'APPROVED' or 'REJECTED'")
    approver: str = Field(..., description="Creative Director email or username")
    approver_role: Optional[str] = "CREATIVE_DIRECTOR"
    review_notes: Optional[str] = ""


def get_approval_repo(request: Request) -> ApprovalRepository:
    return request.app.state.approval_repo


def get_creative_repo(request: Request) -> CreativeRepository:
    return request.app.state.creative_repo


@router.get("/pending")
def list_pending_approvals(approval_repo: ApprovalRepository = Depends(get_approval_repo)):
    return approval_repo.list_pending_approvals()


@router.post("/{approval_id}/resolve")
def resolve_approval(
    approval_id: str,
    req: ResolveApprovalRequest,
    approval_repo: ApprovalRepository = Depends(get_approval_repo),
    creative_repo: CreativeRepository = Depends(get_creative_repo)
):
    if req.decision not in ["APPROVED", "REJECTED"]:
        raise HTTPException(status_code=400, detail="Decision must be 'APPROVED' or 'REJECTED'")

    # Enforce role clearance (must be CREATIVE_DIRECTOR or ADMIN)
    if req.approver_role not in ["CREATIVE_DIRECTOR", "ADMIN"]:
        raise HTTPException(status_code=403, detail="Forbidden: Two-Man approval requires CREATIVE_DIRECTOR clearance")

    res = approval_repo.resolve_approval(
        approval_id=approval_id,
        approver=req.approver,
        approver_role=req.approver_role,
        decision=req.decision,
        review_notes=req.review_notes or "",
    )
    if not res:
        raise HTTPException(status_code=404, detail="Approval request not found")

    # Update brief status
    brief_status = "APPROVED" if req.decision == "APPROVED" else "REJECTED"
    creative_repo.update_brief_status(res["brief_id"], brief_status)

    return res
