"""app/creative/asset_generator.py — ComfyUI workflow dispatcher & simulated asset generator."""

from __future__ import annotations
import uuid
import random
from typing import Dict, Any


class AssetGenerator:
    """Dispatches generation requests to local ComfyUI instance or synthesizes media descriptors."""

    @classmethod
    def generate_asset_metadata(
        cls,
        brief_title: str,
        aspect_ratio: str,
        model: str = "flux-1-schnell"
    ) -> Dict[str, Any]:
        seed = random.randint(100000000, 999999999)
        prompt_id = f"comfy-{uuid.uuid4().hex[:12]}"
        resolutions = {"16:9": "1344x768", "1:1": "1024x1024", "9:16": "768x1344"}
        resolution = resolutions.get(aspect_ratio, "1024x1024")

        return {
            "comfyui_prompt_id": prompt_id,
            "comfyui_seed": seed,
            "resolution": resolution,
            "model_checkpoint": model,
            "asset_url": f"/static/generated/{prompt_id}.png",
            "render_time_ms": round(random.uniform(420.0, 950.0), 1),
            "status": "COMPLETED",
        }
