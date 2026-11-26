"""app/database/approval_repository.py — Two-Man Rule Creative Director approval queue."""

from __future__ import annotations
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from .connection import Database


class ApprovalRepository:
    """Manages Two-Man Rule approvals for high-stakes paid advertising campaigns."""

    def __init__(self, db: Database):
        self.db = db

    def request_approval(self, brief_id: str, campaign_id: str, requested_by: str, requester_role: str = "CREATIVE_PRODUCER") -> Dict[str, Any]:
        app_id = f"appr-{uuid.uuid4().hex[:8]}"
        now = datetime.now(timezone.utc).isoformat()
        with self.db._conn:
            self.db.execute(
                """
                INSERT INTO creative_approvals (id, brief_id, campaign_id, requested_by, requester_role, decision, created_at)
                VALUES (?, ?, ?, ?, ?, 'PENDING', ?)
                """,
                (app_id, brief_id, campaign_id, requested_by, requester_role, now)
            )
        cursor = self.db.execute("SELECT * FROM creative_approvals WHERE id = ?", (app_id,))
        return dict(cursor.fetchone())

    def list_pending_approvals(self) -> List[Dict[str, Any]]:
        cursor = self.db.execute("SELECT * FROM creative_approvals WHERE decision = 'PENDING' ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]

    def resolve_approval(self, approval_id: str, approver: str, approver_role: str, decision: str, review_notes: str = "") -> Optional[Dict[str, Any]]:
        now = datetime.now(timezone.utc).isoformat()
        with self.db._conn:
            self.db.execute(
                """
                UPDATE creative_approvals
                SET approver = ?, approver_role = ?, decision = ?, review_notes = ?, resolved_at = ?
                WHERE id = ?
                """,
                (approver, approver_role, decision, review_notes, now, approval_id)
            )
        cursor = self.db.execute("SELECT * FROM creative_approvals WHERE id = ?", (approval_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
