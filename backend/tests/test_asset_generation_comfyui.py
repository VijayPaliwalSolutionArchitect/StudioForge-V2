"""backend/tests/test_asset_generation_comfyui.py — ComfyUI asset generation tests."""

def test_generate_asset_for_brief(client):
    # Create brief
    brief_res = client.post("/api/v1/briefs", json={
        "campaign_id": "camp-fleet-launch-2026",
        "brand_id": "brand-shivam-itcs",
        "concept_title": "Asset Generation Target",
        "core_idea": "Sovereign datacenter server rack glow",
        "aspect_ratio": "16:9",
    })
    brief_id = brief_res.json()["brief"]["id"]

    # Generate asset
    gen_res = client.post("/api/v1/assets/generate", json={
        "brief_id": brief_id,
        "asset_type": "IMAGE",
        "model": "flux-1-schnell",
    })
    assert gen_res.status_code == 200
    data = gen_res.json()
    assert "asset" in data
    assert data["asset"]["resolution"] == "1344x768"
    assert "comfyui_prompt_id" in data["generation_metadata"]


def test_list_assets_endpoint(client):
    res = client.get("/api/v1/assets")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_generate_asset_non_existent_brief_404(client):
    res = client.post("/api/v1/assets/generate", json={
        "brief_id": "brief-non-existent-999",
    })
    assert res.status_code == 404


def test_generate_asset_rejected_brief_400(client):
    # Create brief and reject it
    b_res = client.post("/api/v1/briefs", json={
        "campaign_id": "camp-fleet-launch-2026",
        "brand_id": "brand-shivam-itcs",
        "concept_title": "To Be Rejected",
        "core_idea": "Sovereign concepts to reject",
    })
    brief_id = b_res.json()["brief"]["id"]
    approval_id = b_res.json()["approval"]["id"]

    client.post(f"/api/v1/approvals/{approval_id}/resolve", json={
        "decision": "REJECTED",
        "approver": "director@shivamitcs.com",
        "approver_role": "CREATIVE_DIRECTOR",
    })

    # Try generating asset on rejected brief
    res = client.post("/api/v1/assets/generate", json={"brief_id": brief_id})
    assert res.status_code == 400
    assert "Cannot generate assets for a rejected brief" in res.json()["detail"]
