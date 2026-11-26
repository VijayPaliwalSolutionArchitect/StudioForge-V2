"""backend/tests/test_brand_guidelines_and_forbidden_words.py — Brand identity & tone reasoning tests."""

from app.brand.tone_analyzer import BrandToneAnalyzer


def test_list_seeded_brands(client):
    res = client.get("/api/v1/brands")
    assert res.status_code == 200
    brands = res.json()
    assert len(brands) >= 1
    assert any(b["id"] == "brand-shivam-itcs" for b in brands)


def test_create_custom_brand(client):
    res = client.post("/api/v1/brands", json={
        "name": "Aether Dynamics",
        "industry": "Aerospace & Satellites",
        "tone_of_voice": "Visionary, Scientific, Inspiring",
        "primary_color_hex": "#0ea5e9",
        "secondary_color_hex": "#6366f1",
        "forbidden_words": ["cheap", "untested"],
        "target_personas": ["Defense Procurement Leads"],
    })
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "Aether Dynamics"
    assert "cheap" in data["forbidden_words"]


def test_tone_analyzer_passes_on_brand_content():
    analysis = BrandToneAnalyzer.analyze_tone(
        text="Sovereign enterprise autonomous systems architected with precision.",
        tone_of_voice="Authoritative, Precise, Sovereign",
        forbidden_words=["cheap", "hacky"],
    )
    assert analysis["passed_brand_check"] is True
    assert analysis["brand_alignment_score"] >= 75.0
    assert len(analysis["violations"]) == 0


def test_tone_analyzer_rejects_forbidden_words():
    analysis = BrandToneAnalyzer.analyze_tone(
        text="Get our cheap hacky solution for a quick fix today!",
        tone_of_voice="Authoritative, Precise",
        forbidden_words=["cheap", "hacky", "quick fix"],
    )
    assert analysis["passed_brand_check"] is False
    assert len(analysis["violations"]) >= 2
    assert analysis["brand_alignment_score"] < 50.0


def test_get_brand_by_id(client):
    res = client.get("/api/v1/brands/brand-shivam-itcs")
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "Shivam ITCS"
    assert data["primary_color_hex"] == "#06b6d4"
