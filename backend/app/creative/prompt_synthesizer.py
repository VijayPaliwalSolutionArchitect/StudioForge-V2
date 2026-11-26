"""app/creative/prompt_synthesizer.py — Headless ComfyUI / SD / Flux visual prompt synthesizer."""

from __future__ import annotations
from typing import Dict, Any, List


class VisualPromptSynthesizer:
    """Translates creative concepts into latent diffusion prompts with brand color grading."""

    ASPECT_RATIOS = {
        "16:9": {"width": 1344, "height": 768, "channel": "YouTube / Desktop Banner"},
        "1:1": {"width": 1024, "height": 1024, "channel": "Instagram / LinkedIn Post"},
        "9:16": {"width": 768, "height": 1344, "channel": "TikTok / YouTube Shorts / Reels"},
    }

    DEFAULT_NEGATIVE_PROMPT = (
        "blurry, distorted, low quality, oversaturated, amateur, watermark, signature, "
        "grainy, deformed fingers, extra limbs, ugly, text artifacts"
    )

    @classmethod
    def synthesize_prompt(
        cls,
        concept: str,
        primary_color_hex: str = "#06b6d4",
        secondary_color_hex: str = "#3b82f6",
        aspect_ratio: str = "16:9",
        style_preset: str = "cinematic_enterprise"
    ) -> Dict[str, Any]:
        dimensions = cls.ASPECT_RATIOS.get(aspect_ratio, cls.ASPECT_RATIOS["16:9"])

        # Construct visual prompt with volumetric lighting and brand color grading
        positive_prompt = (
            f"Hyper-detailed, commercial grade photograph of {concept}. "
            f"Atmospheric volumetric lighting, premium corporate aesthetic, "
            f"subtle color grading with glowing cyber accents matching {primary_color_hex} and deep indigo {secondary_color_hex}. "
            f"8k resolution, shot on Hasselblad H6D-100c, 85mm f/1.4 lens, razor sharp focus, cinematic depth of field."
        )

        return {
            "positive_prompt": positive_prompt,
            "negative_prompt": cls.DEFAULT_NEGATIVE_PROMPT,
            "aspect_ratio": aspect_ratio,
            "width": dimensions["width"],
            "height": dimensions["height"],
            "target_channel": dimensions["channel"],
            "sampler_settings": {
                "sampler_name": "euler_ancestral",
                "scheduler": "karras",
                "steps": 28,
                "cfg_scale": 7.0,
            }
        }
