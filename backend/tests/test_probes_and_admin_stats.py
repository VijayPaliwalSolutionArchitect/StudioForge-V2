"""backend/tests/test_probes_and_admin_stats.py — Health probes & fleet stats tests."""

def test_health_endpoint(client):
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert data["service"] == "StudioForge V2"
    assert data["two_man_approval_active"] is True


def test_healthz_endpoint(client):
    res = client.get("/healthz")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_readyz_endpoint(client):
    res = client.get("/readyz")
    assert res.status_code == 200
    assert res.json()["status"] == "ready"


def test_admin_stats_metrics(client):
    res = client.get("/api/v1/admin/stats")
    assert res.status_code == 200
    data = res.json()
    assert data["service"] == "StudioForge V2"
    assert data["brands_count"] >= 1
    assert data["campaigns_count"] >= 1
    assert data["ports"]["backend"] == 8097
    assert data["ports"]["frontend"] == 5179
    assert data["ports"]["comfyui"] == 8188
