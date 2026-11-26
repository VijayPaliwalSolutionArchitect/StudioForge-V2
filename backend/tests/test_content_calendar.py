"""backend/tests/test_content_calendar.py — Content calendar & multi-channel scheduling tests."""

def test_schedule_calendar_item(client):
    briefs = client.get("/api/v1/briefs").json()
    brief_id = briefs[0]["id"]

    res = client.post("/api/v1/calendar", json={
        "brief_id": brief_id,
        "brand_id": "brand-shivam-itcs",
        "channel": "LINKEDIN",
        "scheduled_for": "2026-12-01T10:00:00Z",
        "copy_text": "Autonomous AI is transforming enterprise infrastructure. Zero data egress, maximum velocity.",
    })
    assert res.status_code == 200
    data = res.json()
    assert data["channel"] == "LINKEDIN"
    assert data["status"] == "SCHEDULED"


def test_list_calendar_items(client):
    res = client.get("/api/v1/calendar")
    assert res.status_code == 200
    items = res.json()
    assert len(items) >= 1


def test_schedule_calendar_invalid_brief_404(client):
    res = client.post("/api/v1/calendar", json={
        "brief_id": "brief-ghost-999",
        "brand_id": "brand-shivam-itcs",
        "channel": "TWITTER",
        "scheduled_for": "2026-12-01T12:00:00Z",
        "copy_text": "Post that should fail.",
    })
    assert res.status_code == 404


def test_schedule_multiple_channels(client):
    briefs = client.get("/api/v1/briefs").json()
    brief_id = briefs[0]["id"]

    for ch in ["TWITTER", "YOUTUBE"]:
        res = client.post("/api/v1/calendar", json={
            "brief_id": brief_id,
            "brand_id": "brand-shivam-itcs",
            "channel": ch,
            "scheduled_for": "2026-12-02T15:00:00Z",
            "copy_text": f"Sovereign Fleet update on {ch}.",
        })
        assert res.status_code == 200
        assert res.json()["channel"] == ch
