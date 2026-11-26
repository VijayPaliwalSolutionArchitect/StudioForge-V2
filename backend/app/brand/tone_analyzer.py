"""app/brand/tone_analyzer.py — Brand Tone Reasoner & Semantic Consistency Scorer."""

from __future__ import annotations
import re
from typing import Dict, List, Tuple, Any


class BrandToneAnalyzer:
    """Evaluates marketing copy and visual prompts against brand guidelines."""

    @classmethod
    def analyze_tone(
        cls,
        text: str,
        tone_of_voice: str,
        forbidden_words: List[str],
        primary_color_hex: str = "#06b6d4"
    ) -> Dict[str, Any]:
        text_lower = text.lower()
        violations: List[str] = []

        # 1. Scan for Forbidden Words
        for word in forbidden_words:
            pattern = rf"\b{re.escape(word.lower())}\b"
            if re.search(pattern, text_lower):
                violations.append(f"Forbidden term detected: '{word}'")

        # 2. Tone Pillar Scoring
        # Positive tone keywords
        pillars = [p.strip().lower() for p in tone_of_voice.split(",") if p.strip()]
        matched_pillars = []
        for pillar in pillars:
            # Check if root of pillar or synonyms exist
            if pillar in text_lower or any(token in text_lower for token in pillar.split()):
                matched_pillars.append(pillar)

        # Baseline alignment score
        base_score = 85.0
        if matched_pillars:
            base_score += len(matched_pillars) * 5.0

        # Penalize for forbidden words (40 pts penalty per violation)
        penalty = len(violations) * 40.0
        final_score = max(0.0, min(100.0, base_score - penalty))

        passed = final_score >= 75.0 and len(violations) == 0

        return {
            "brand_alignment_score": round(final_score, 1),
            "passed_brand_check": passed,
            "violations": violations,
            "matched_pillars": matched_pillars,
            "tone_evaluated": tone_of_voice,
            "recommended_action": "APPROVE" if passed else "REJECT_OFF_BRAND",
        }
