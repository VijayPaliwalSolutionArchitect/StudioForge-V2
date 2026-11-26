"""backend/tests/test_two_man_creative_approvals.py — Two-Man Rule Creative Director approval tests."""

def test_list_pending_approvals(client):
    res = client.get("/api/v1/approvals/pending")
    assert res.status_code == 200
    apps = res.json()
    assert isinstance(apps, list)


def test_resolve_approval_by_creative_director(client):
    # First create a brief requiring approval
    res = client.post("/api/v1/briefs", json={
        "campaign_id": "camp-fleet-launch-2026",
        "brand_id": "brand-shivam-itcs",
        "concept_title": "Super Bowl Autonomous AI Ad",
        "core_idea": "Authoritative presentation of sovereign enterprise infrastructure",
    })
    brief_data = res.json()
    approval_id = brief_data["approval"]["id"]

    # Approve with CREATIVE_DIRECTOR clearance
    resolve_res = client.post(f"/api/v1/approvals/{approval_id}/resolve", json={
        "decision": "APPROVED",
        "approver": "creative-lead@shivamitcs.com",
        "approver_role": "CREATIVE_DIRECTOR",
        "review_notes": "Visually stunning and 100% on-brand",
    })
    assert resolve_res.status_code == 200
    assert resolve_res.json()["decision"] == "APPROVED"


def test_resolve_approval_unauthorized_role_403(client):
    # Create brief
    res = client.post("/api/v1/briefs", json={
        "campaign_id": "camp-fleet-launch-2026",
        "brand_id": "brand-shivam-itcs",
        "concept_title": "Another Paid Brief",
        "core_idea": "Precision sovereign engineering without compromise",
    })
    approval_id = res.json()["approval"]["id"]

    # Attempt resolving with unauthorized role
    resolve_res = client.post(f"/api/v1/approvals/{approval_id}/resolve", json={
        "decision": "APPROVED",
        "approver": "junior-intern@shivamitcs.com",
        "approver_role": "INTERN",
    })
    assert resolve_res.status_code == 403
    assert "Forbidden" in resolve_res.json()["detail"]


def test_resolve_approval_rejection_marks_brief_rejected(client):
    res = client.post("/api/v1/briefs", json={
        "campaign_id": "camp-fleet-launch-2026",
        "brand_id": "brand-shivam-itcs",
        "concept_title": "Subpar Visual Direction",
        "core_idea": "Sovereign autonomy lacking adequate contrast",
    })
    brief_id = res.json()["brief"]["id"]
    approval_id = res.json()["approval"]["id"]

    client.post(f"/api/v1/approvals/{approval_id}/resolve", json={
        "decision": "REJECTED",
        "approver": "director@shivamitcs.com",
        "approver_role": "CREATIVE_DIRECTOR",
        "review_notes": "Lighting is off, reshoot required",
    })

    # Verify brief is marked REJECTED
    briefs = client.get("/api/v1/briefs").json()
    b = next(item for item in briefs if item["id"] == brief_id)
    assert b["status"] == "REJECTED"


def test_resolve_non_existent_approval_404(client):
    res = client.post("/api/v1/approvals/appr-ghost-999/resolve", json={
        "decision": "APPROVED",
        "approver": "director@shivamitcs.com",
        "approver_role": "CREATIVE_DIRECTOR",
    })
    assert res.status_code == 404
