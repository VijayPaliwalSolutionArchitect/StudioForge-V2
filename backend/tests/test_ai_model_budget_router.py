"""backend/tests/test_ai_model_budget_router.py — 5-Pool model router tests."""

from app.llm.router import ModelRouter


def test_model_router_tracks_spend():
    router = ModelRouter()
    res = router.route_copywriting(pool="balanced", prompt="Create ad copy for sovereign AI")
    assert "generated_copy" in res
    assert res["pool"] == "balanced"
    assert res["cost_usd"] > 0
    assert router.ledger.total_calls == 1


def test_model_router_all_pools():
    router = ModelRouter()
    for pool in ["fast", "high_reasoning", "creative", "offline_airgap"]:
        res = router.route_copywriting(pool=pool, prompt="Test prompt")
        assert res["pool"] == pool


def test_model_router_budget_hard_cap_fallback():
    router = ModelRouter()
    # Artificially breach budget
    router.ledger.total_spend = 300.0
    assert router.ledger.is_budget_exceeded() is True

    # Call should fall back to offline_airgap
    res = router.route_copywriting(pool="high_reasoning", prompt="Expensive call")
    assert res["pool"] == "offline_airgap"


def test_model_router_summary():
    router = ModelRouter()
    router.route_copywriting(pool="fast", prompt="test")
    summary = router.ledger.get_summary()
    assert summary["total_calls"] >= 1
    assert "budget_remaining_usd" in summary
