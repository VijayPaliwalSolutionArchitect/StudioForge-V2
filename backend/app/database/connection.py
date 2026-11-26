"""app/database/connection.py — SQLite WAL mode database connection & initial seeder."""

from __future__ import annotations
import sqlite3
import os
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from .schema import DDL_STATEMENTS


class Database:
    """Manages transactional SQLite connection with WAL mode and seed data."""

    def __init__(self, db_url: str = "sqlite:///./backend/data/studioforge.db"):
        if db_url.startswith("sqlite:///"):
            self.db_path = db_url.replace("sqlite:///", "")
        else:
            self.db_path = db_url

        if self.db_path != ":memory:":
            db_dir = os.path.dirname(self.db_path)
            if db_dir:
                os.makedirs(db_dir, exist_ok=True)

        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row

        if self.db_path != ":memory:":
            self._conn.execute("PRAGMA journal_mode=WAL;")
        self._conn.execute("PRAGMA foreign_keys=ON;")

        self._initialize_schema()
        self._seed_default_data()

    def _initialize_schema(self):
        with self._conn:
            for ddl in DDL_STATEMENTS:
                self._conn.execute(ddl)

    def _seed_default_data(self):
        now = datetime.now(timezone.utc).isoformat()
        with self._conn:
            # 1. Seed Default Brand: Shivam ITCS Autonomous AI Fleet
            self._conn.execute(
                """
                INSERT OR IGNORE INTO brands (id, name, industry, tone_of_voice, tagline, primary_color_hex, secondary_color_hex, forbidden_words_json, target_personas_json, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "brand-shivam-itcs",
                    "Shivam ITCS",
                    "Enterprise Autonomous AI Systems",
                    "Authoritative, Precise, Sovereign, Visionary",
                    "Sovereign Enterprise AI Fleet Systems That Scale Without Cloud Leaks",
                    "#06b6d4",
                    "#3b82f6",
                    json.dumps(["cheap", "hacky", "crypto pump", "quick fix", "guaranteed profit"]),
                    json.dumps(["Chief Technology Officers", "VP of Engineering", "General Counsel", "Head of ITSM"]),
                    now,
                    now,
                )
            )

            # 2. Seed Flagship Q4 Campaign
            self._conn.execute(
                """
                INSERT OR IGNORE INTO campaigns (id, brand_id, name, objective, budget_usd, is_paid_campaign, status, start_date, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "camp-fleet-launch-2026",
                    "brand-shivam-itcs",
                    "Sovereign Fleet Global Launch",
                    "LEAD_GEN",
                    15000.0,
                    1,
                    "ACTIVE",
                    "2026-11-01",
                    now,
                )
            )

    def execute(self, sql: str, params: tuple = ()) -> sqlite3.Cursor:
        return self._conn.execute(sql, params)

    def commit(self):
        self._conn.commit()

    def close(self):
        try:
            self._conn.close()
        except Exception:
            pass
