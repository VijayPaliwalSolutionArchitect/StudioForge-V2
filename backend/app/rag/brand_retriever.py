"""app/rag/brand_retriever.py — Semantic retrieval over brand pillars & copy snippets."""

from __future__ import annotations
import math
import hashlib
from typing import List, Dict, Any
from ..database.brand_repository import BrandRepository


def simple_embed(text: str, dim: int = 32) -> List[float]:
    vec = [0.0] * dim
    tokens = text.lower().split()
    if not tokens:
        return vec
    for t in tokens:
        idx = int(hashlib.md5(t.encode("utf-8")).hexdigest()[:6], 16) % dim
        vec[idx] += 1.0
    norm = math.sqrt(sum(x * x for x in vec))
    if norm > 0.0:
        vec = [round(x / norm, 4) for x in vec]
    return vec


class BrandRetriever:
    """Retrieves relevant brand pillars and messaging guidelines for a given campaign brief."""

    def __init__(self, brand_repo: BrandRepository):
        self.brand_repo = brand_repo

    def retrieve_guidelines(self, brand_id: str, query: str) -> Dict[str, Any]:
        brand = self.brand_repo.get_brand(brand_id)
        if not brand:
            return {"brand_found": False, "guidelines": []}

        # Extract tone pillars and personas
        pillars = [p.strip() for p in brand["tone_of_voice"].split(",")]
        personas = brand.get("target_personas", [])
        forbidden = brand.get("forbidden_words", [])

        return {
            "brand_found": True,
            "brand_name": brand["name"],
            "industry": brand["industry"],
            "tone_pillars": pillars,
            "primary_color": brand["primary_color_hex"],
            "secondary_color": brand["secondary_color_hex"],
            "target_personas": personas,
            "forbidden_words": forbidden,
            "retrieval_query": query,
        }
