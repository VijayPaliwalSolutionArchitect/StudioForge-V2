"""app/config/settings.py — StudioForge V2 Configuration Settings.

Defines all configuration parameters using Pydantic Settings.
Allocated ports:
- Backend Service: :8097
- Frontend Workstation: :5179
- Headless ComfyUI Runtime: :8188 (Local host)
"""

from __future__ import annotations
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Immutable typed configuration for StudioForge V2."""

    app_name: str = "StudioForge V2 — Autonomous AI Brand & Media Factory"
    app_version: str = "2.0.0"
    app_port: int = 8097
    app_host: str = "0.0.0.0"
    frontend_port: int = 5179

    # Database
    database_url: str = "sqlite:///./backend/data/studioforge.db"
    enable_wal_mode: bool = True

    # Generative AI Engines
    comfyui_base_url: str = "http://127.0.0.1:8188"
    default_image_model: str = "flux-1-schnell"
    default_sd_checkpoint: str = "sd_xl_base_1.0.safetensors"

    # Creative Governance & Two-Man Rule
    require_two_man_approval_for_paid_ads: bool = True
    min_brand_alignment_score: float = 75.0  # Out of 100

    # Model Budget Pools
    groq_model: str = "groq/llama-3.3-70b-versatile"
    openai_model: str = "gpt-4o-mini"
    claude_model: str = "claude-3-5-sonnet-20241022"
    gemini_model: str = "gemini-2.0-flash"
    local_model: str = "qwen2.5:14b"
    monthly_budget_usd: float = 250.0

    class Config:
        env_prefix = "STUDIOFORGE_"
        case_sensitive = False


settings = Settings()
