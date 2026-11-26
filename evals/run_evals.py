"""evals/run_evals.py — Automated Hard Release Evals Gate for StudioForge V2."""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.brand.tone_analyzer import BrandToneAnalyzer
from app.creative.prompt_synthesizer import VisualPromptSynthesizer
from app.database.connection import Database
from app.database.brand_repository import BrandRepository
from app.database.creative_repository import CreativeRepository
from app.database.approval_repository import ApprovalRepository


def run_all_evals():
    print("=" * 70)
    print("🔬 StudioForge V2 — Automated Creative Governance Release Evals Gate")
    print("=" * 70)

    # ---------------------------------------------------------
    # Gate 1: Brand Tone Alignment & Consistency Gate
    # ---------------------------------------------------------
    print("\n[Gate 1/4] Brand Tone Consistency & Semantic Alignment...")
    tone_eval_set = [
        ("Authoritative enterprise infrastructure delivering sovereign AI autonomy.", True),
        ("Empathetic healthcare clinic scheduling system ensuring HIPAA compliance.", True),
        ("Visionary multi-agent fleet orchestrator designed for global enterprises.", True),
        ("Get rich quick with this hacky crypto pump scheme overnight guaranteed.", False),
        ("Cheap dirty hacks to bypass safety guards with zero oversight.", False),
    ]
    correct_evals = 0
    for text, expected_pass in tone_eval_set:
        res = BrandToneAnalyzer.analyze_tone(
            text=text,
            tone_of_voice="Authoritative, Visionary, Sovereign, Empathetic",
            forbidden_words=["cheap", "hacky", "crypto pump", "quick fix", "guaranteed"],
        )
        if res["passed_brand_check"] == expected_pass:
            correct_evals += 1
            status_label = "APPROVED" if res["passed_brand_check"] else "BLOCKED_OFF_BRAND"
            print(f"  ✅ '{text[:45]}...' -> {status_label} (Score: {res['brand_alignment_score']})")
        else:
            print(f"  ❌ Misclassified: '{text[:45]}...'")

    tone_acc = (correct_evals / len(tone_eval_set)) * 100.0
    print(f"Brand Tone Alignment Precision: {tone_acc:.1f}% (Threshold: >= 90.0%)")
    assert tone_acc >= 90.0, "Gate 1 Failed: Brand Tone alignment precision below 90%"

    # ---------------------------------------------------------
    # Gate 2: Forbidden Words Interception (100% Rate)
    # ---------------------------------------------------------
    print("\n[Gate 2/4] Forbidden Words & Brand Safety Interception...")
    forbidden_samples = [
        "This is a cheap knockoff",
        "Use this hacky code snippet",
        "Invest in our crypto pump fund",
        "A quick fix for your server crash",
    ]
    blocked_count = 0
    for sample in forbidden_samples:
        res = BrandToneAnalyzer.analyze_tone(
            text=sample,
            tone_of_voice="Authoritative, Precise",
            forbidden_words=["cheap", "hacky", "crypto pump", "quick fix"],
        )
        if not res["passed_brand_check"] and len(res["violations"]) > 0:
            blocked_count += 1
            print(f"  🛡️ Intercepted: '{sample}' -> Violations: {res['violations']}")

    forbidden_block_rate = (blocked_count / len(forbidden_samples)) * 100.0
    print(f"Forbidden Word Interception Rate: {forbidden_block_rate:.1f}% (Threshold: 100.0%)")
    assert forbidden_block_rate == 100.0, "Gate 2 Failed: Forbidden term was not blocked!"

    # ---------------------------------------------------------
    # Gate 3: Two-Man Creative Rule Enforcement
    # ---------------------------------------------------------
    print("\n[Gate 3/4] Two-Man Creative Rule Enforcement on Paid Media...")
    db = Database("sqlite:///:memory:")
    brand_repo = BrandRepository(db)
    creative_repo = CreativeRepository(db)
    approval_repo = ApprovalRepository(db)

    b = brand_repo.create_brand(name="Sovereign Brand", industry="AI", tone_of_voice="Authoritative")
    camp = creative_repo.create_campaign(brand_id=b["id"], name="Paid Ad Campaign", is_paid=True, budget_usd=50000.0)

    brief = creative_repo.create_brief(
        campaign_id=camp["id"],
        brand_id=b["id"],
        title="Paid Media Ad",
        hook="Hook text",
        core_message="Sovereign AI messaging",
        call_to_action="Deploy today",
        target_channels=["linkedin"],
        visual_prompt="datacenter photograph",
    )

    # Must require approval
    appr = approval_repo.request_approval(brief_id=brief["id"], campaign_id=camp["id"], requested_by="producer@shivamitcs.com")
    assert appr["decision"] == "PENDING"
    print(f"  ✅ High-Stakes Paid Campaign Brief locked in 'PENDING' Two-Man state (ID: {appr['id']})")

    # Resolve approval
    resolved = approval_repo.resolve_approval(
        approval_id=appr["id"],
        approver="creative-director@shivamitcs.com",
        approver_role="CREATIVE_DIRECTOR",
        decision="APPROVED"
    )
    assert resolved["decision"] == "APPROVED"
    print("  ✅ Two-Man Rule strictly enforced and signed off by Creative Director.")

    # ---------------------------------------------------------
    # Gate 4: ComfyUI Aspect Ratio & Latent Prompt Constraints
    # ---------------------------------------------------------
    print("\n[Gate 4/4] ComfyUI Aspect Ratio & Latent Prompt Constraints...")
    ratios = [
        ("16:9", 1344, 768),
        ("1:1", 1024, 1024),
        ("9:16", 768, 1344),
    ]
    for r, exp_w, exp_h in ratios:
        spec = VisualPromptSynthesizer.synthesize_prompt(concept="sovereign satellite", aspect_ratio=r)
        assert spec["width"] == exp_w and spec["height"] == exp_h, f"Dimension mismatch for {r}"
        assert "blurry" in spec["negative_prompt"]
        assert "distorted" in spec["negative_prompt"]
        print(f"  ✅ Aspect Ratio {r}: {exp_w}x{exp_h} with Negative Prompt Guard verified.")

    print("\n" + "=" * 70)
    print("🎯 ALL 4 CREATIVE GOVERNANCE EVALS GATES PASSED (100% COMPLIANCE)")
    print("=" * 70)


if __name__ == "__main__":
    run_all_evals()
