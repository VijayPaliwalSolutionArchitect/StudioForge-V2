# StudioForge V2 — Testing Methodology & Verification Guide

## 1. Overview
The automated test suite verifies 41 pytest unit and integration tests and 4 release evals gates.

## 2. Test Execution
```bash
# Run Pytest Suite:
cd backend
python -m pytest tests/ -v

# Run Hard Release Evals Gate:
cd ..
python -m evals.run_evals
```

## 3. Test Coverage Summary
* `test_brand_guidelines_and_forbidden_words.py`: 5 tests
* `test_prompt_synthesizer.py`: 5 tests
* `test_campaigns_and_briefs.py`: 6 tests
* `test_two_man_creative_approvals.py`: 5 tests
* `test_asset_generation_comfyui.py`: 4 tests
* `test_content_calendar.py`: 4 tests
* `test_brand_retriever_rag.py`: 4 tests
* `test_ai_model_budget_router.py`: 4 tests
* `test_probes_and_admin_stats.py`: 4 tests
* **Total: 41 Passed (100%)**
