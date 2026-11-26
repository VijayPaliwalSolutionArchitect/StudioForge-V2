"""app/database/brand_repository.py — Brand identity & guideline repository."""

from __future__ import annotations
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from .connection import Database


class BrandRepository:
    """Manages brand identities, color palettes, tone pillars, and forbidden terms."""

    def __init__(self, db: Database):
        self.db = db

    def list_brands(self) -> List[Dict[str, Any]]:
        cursor = self.db.execute("SELECT * FROM brands ORDER BY created_at DESC")
        results = []
        for row in cursor.fetchall():
            item = dict(row)
            item["forbidden_words"] = json.loads(item["forbidden_words_json"])
            item["target_personas"] = json.loads(item["target_personas_json"])
            results.append(item)
        return results

    def get_brand(self, brand_id: str) -> Optional[Dict[str, Any]]:
        cursor = self.db.execute("SELECT * FROM brands WHERE id = ? OR name = ?", (brand_id, brand_id))
        row = cursor.fetchone()
        if not row:
            return None
        item = dict(row)
        item["forbidden_words"] = json.loads(item["forbidden_words_json"])
        item["target_personas"] = json.loads(item["target_personas_json"])
        return item

    def create_brand(
        self,
        name: str,
        industry: str,
        tone_of_voice: str,
        tagline: str = "",
        primary_color_hex: str = "#06b6d4",
        secondary_color_hex: str = "#3b82f6",
        forbidden_words: Optional[List[str]] = None,
        target_personas: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        brand_id = f"brand-{uuid.uuid4().hex[:8]}"
        now = datetime.now(timezone.utc).isoformat()
        with self.db._conn:
            self.db.execute(
                """
                INSERT INTO brands (id, name, industry, tone_of_voice, tagline, primary_color_hex, secondary_color_hex, forbidden_words_json, target_personas_json, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    brand_id,
                    name,
                    industry,
                    tone_of_voice,
                    tagline,
                    primary_color_hex,
                    secondary_color_hex,
                    json.dumps(forbidden_words or []),
                    json.dumps(target_personas or []),
                    now,
                    now,
                )
            )
        return self.get_brand(brand_id)
