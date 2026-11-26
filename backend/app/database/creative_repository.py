"""app/database/creative_repository.py — Campaigns, creative briefs, assets, and calendar repository."""

from __future__ import annotations
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from .connection import Database


class CreativeRepository:
    """Manages marketing campaigns, briefs, ComfyUI visual assets, and content calendar events."""

    def __init__(self, db: Database):
        self.db = db

    # Campaigns
    def list_campaigns(self, brand_id: Optional[str] = None) -> List[Dict[str, Any]]:
        if brand_id:
            cursor = self.db.execute("SELECT * FROM campaigns WHERE brand_id = ? ORDER BY created_at DESC", (brand_id,))
        else:
            cursor = self.db.execute("SELECT * FROM campaigns ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]

    def create_campaign(
        self,
        brand_id: str,
        name: str,
        objective: str = "AWARENESS",
        budget_usd: float = 0.0,
        is_paid: bool = False,
        start_date: str = "2026-11-26",
    ) -> Dict[str, Any]:
        camp_id = f"camp-{uuid.uuid4().hex[:8]}"
        now = datetime.now(timezone.utc).isoformat()
        with self.db._conn:
            self.db.execute(
                """
                INSERT INTO campaigns (id, brand_id, name, objective, budget_usd, is_paid_campaign, status, start_date, created_at)
                VALUES (?, ?, ?, ?, ?, ?, 'ACTIVE', ?, ?)
                """,
                (camp_id, brand_id, name, objective, budget_usd, 1 if is_paid else 0, start_date, now)
            )
        cursor = self.db.execute("SELECT * FROM campaigns WHERE id = ?", (camp_id,))
        return dict(cursor.fetchone())

    # Creative Briefs
    def create_brief(
        self,
        campaign_id: str,
        brand_id: str,
        title: str,
        hook: str,
        core_message: str,
        call_to_action: str,
        target_channels: List[str],
        visual_prompt: str,
        negative_prompt: str = "",
        aspect_ratio: str = "16:9",
        brand_alignment_score: float = 90.0,
    ) -> Dict[str, Any]:
        brief_id = f"brief-{uuid.uuid4().hex[:8]}"
        now = datetime.now(timezone.utc).isoformat()
        with self.db._conn:
            self.db.execute(
                """
                INSERT INTO creative_briefs (id, campaign_id, brand_id, title, hook, core_message, call_to_action, target_channels_json, visual_prompt, negative_prompt, aspect_ratio, brand_alignment_score, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'DRAFT', ?, ?)
                """,
                (
                    brief_id,
                    campaign_id,
                    brand_id,
                    title,
                    hook,
                    core_message,
                    call_to_action,
                    json.dumps(target_channels),
                    visual_prompt,
                    negative_prompt,
                    aspect_ratio,
                    brand_alignment_score,
                    now,
                    now,
                )
            )
        return self.get_brief(brief_id)

    def get_brief(self, brief_id: str) -> Optional[Dict[str, Any]]:
        cursor = self.db.execute("SELECT * FROM creative_briefs WHERE id = ?", (brief_id,))
        row = cursor.fetchone()
        if not row:
            return None
        item = dict(row)
        item["target_channels"] = json.loads(item["target_channels_json"])
        return item

    def list_briefs(self, campaign_id: Optional[str] = None) -> List[Dict[str, Any]]:
        if campaign_id:
            cursor = self.db.execute("SELECT * FROM creative_briefs WHERE campaign_id = ? ORDER BY created_at DESC", (campaign_id,))
        else:
            cursor = self.db.execute("SELECT * FROM creative_briefs ORDER BY created_at DESC")
        results = []
        for row in cursor.fetchall():
            item = dict(row)
            item["target_channels"] = json.loads(item["target_channels_json"])
            results.append(item)
        return results

    def update_brief_status(self, brief_id: str, status: str) -> bool:
        now = datetime.now(timezone.utc).isoformat()
        with self.db._conn:
            cursor = self.db.execute(
                "UPDATE creative_briefs SET status = ?, updated_at = ? WHERE id = ?",
                (status, now, brief_id)
            )
            return cursor.rowcount > 0

    # Assets
    def create_asset(
        self,
        brief_id: str,
        brand_id: str,
        asset_type: str,
        content_url_or_text: str,
        resolution: str = "1024x1024",
        comfyui_prompt_id: Optional[str] = None,
        comfyui_seed: Optional[int] = None,
    ) -> Dict[str, Any]:
        asset_id = f"asset-{uuid.uuid4().hex[:8]}"
        now = datetime.now(timezone.utc).isoformat()
        with self.db._conn:
            self.db.execute(
                """
                INSERT INTO assets (id, brief_id, brand_id, asset_type, content_url_or_text, resolution, comfyui_prompt_id, comfyui_seed, brand_check_passed, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, ?)
                """,
                (asset_id, brief_id, brand_id, asset_type, content_url_or_text, resolution, comfyui_prompt_id, comfyui_seed, now)
            )
        cursor = self.db.execute("SELECT * FROM assets WHERE id = ?", (asset_id,))
        return dict(cursor.fetchone())

    def list_assets(self, brief_id: Optional[str] = None) -> List[Dict[str, Any]]:
        if brief_id:
            cursor = self.db.execute("SELECT * FROM assets WHERE brief_id = ? ORDER BY created_at DESC", (brief_id,))
        else:
            cursor = self.db.execute("SELECT * FROM assets ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]

    # Calendar
    def schedule_item(self, brief_id: str, brand_id: str, channel: str, scheduled_for: str, copy_text: str) -> Dict[str, Any]:
        cal_id = f"cal-{uuid.uuid4().hex[:8]}"
        now = datetime.now(timezone.utc).isoformat()
        with self.db._conn:
            self.db.execute(
                """
                INSERT INTO calendar_items (id, brief_id, brand_id, channel, scheduled_for, copy_text, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, 'SCHEDULED', ?)
                """,
                (cal_id, brief_id, brand_id, channel.upper(), scheduled_for, copy_text, now)
            )
        cursor = self.db.execute("SELECT * FROM calendar_items WHERE id = ?", (cal_id,))
        return dict(cursor.fetchone())

    def list_calendar(self) -> List[Dict[str, Any]]:
        cursor = self.db.execute("SELECT * FROM calendar_items ORDER BY scheduled_for ASC")
        return [dict(row) for row in cursor.fetchall()]
