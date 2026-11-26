"""backend/tests/test_campaigns_and_briefs.py — Campaign CRUD & creative brief generation tests."""

def test_list_campaigns(client):
    res = client.get("/api/v1/campaigns")
    assert res.status_code == 200
    camps = res.json()
    assert len(camps) >= 1
    assert any(c["id"] == "camp-fleet-launch-2026" for c in camps)


def test_create_new_campaign(client):
    res = client.post("/api/v1/campaigns", json={
        "brand_id": "brand-shivam-itcs",
        "name": "Q1 Defense Infiltration",
        "objective": "LEAD_GEN",
        "budget_usd": 25000.0,
        "is_paid": True,
        "start_date": "2027-01-01",
    })
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "Q1 Defense Infiltration"
    assert data["is_paid_campaign"] == 1


def test_generate_creative_brief_success(client):
    res = client.post("/api/v1/briefs", json={
        "campaign_id": "camp-fleet-launch-2026",
        "brand_id": "brand-shivam-itcs",
        "concept_title": "Autonomous Fleet Sovereign Power",
        "core_idea": "Sovereign AI agents executing mission-critical workflows with zero cloud data egress",
        "aspect_ratio": "16:9",
    })
    assert res.status_code == 200
    data = res.json()
    brief = data["brief"]
    assert brief["title"] == "Autonomous Fleet Sovereign Power"
    assert brief["brand_alignment_score"] >= 75.0
    assert "visual_spec" in data
    # Because camp-fleet-launch-2026 is paid, it requires Two-Man approval
    assert data["requires_two_man_approval"] is True
    assert brief["status"] == "IN_REVIEW"


def test_generate_creative_brief_rejects_off_brand_forbidden_words(client):
    res = client.post("/api/v1/briefs", json={
        "campaign_id": "camp-fleet-launch-2026",
        "brand_id": "brand-shivam-itcs",
        "concept_title": "Get Rich with Quick Fix AI",
        "core_idea": "A cheap hacky quick fix that guarantees profit overnight",
    })
    assert res.status_code == 422
    assert "Brand Guard Rejection" in res.json()["detail"]


def test_list_briefs_endpoint(client):
    res = client.get("/api/v1/briefs")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_create_campaign_invalid_brand_404(client):
    res = client.post("/api/v1/campaigns", json={
        "brand_id": "non-existent-brand-id",
        "name": "Ghost Campaign",
    })
    assert res.status_code == 404
