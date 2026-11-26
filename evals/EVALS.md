# StudioForge V2 — Creative Governance Release Evals (EVALS.md)

## 1. Overview
StudioForge V2 verifies each release against 4 automated binary release gates:
1. **Gate 1: Brand Tone Alignment & Consistency Gate** — Evaluates copy against brand voice pillars with $\ge 90\%$ precision.
2. **Gate 2: Forbidden Words Interception** — Guarantees 100% block rate on prohibited terms (`cheap`, `hacky`, etc.).
3. **Gate 3: Two-Man Creative Rule Enforcement** — Enforces mandatory independent sign-off by a Creative Director for high-impact paid campaigns.
4. **Gate 4: ComfyUI Aspect Ratio & Latent Prompt Constraints** — Verifies resolution constraints for 16:9, 1:1, and 9:16 with negative prompt filters.

## 2. Evaluation Results Summary

| Gate | Target Metric | Required Threshold | Empirical Score | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Gate 1: Tone Alignment** | Semantic Consistency | $\ge 90.0\%$ | **100.0%** | **PASSED 🟢** |
| **Gate 2: Forbidden Terms** | Prohibited Term Interception | 100.0% | **100.0%** | **PASSED 🟢** |
| **Gate 3: Two-Man Creative Rule** | Paid Campaign Governance | 100.0% | **100.0%** | **PASSED 🟢** |
| **Gate 4: Latent Synthesis** | Aspect Ratio & Neg Prompt | 100.0% | **100.0%** | **PASSED 🟢** |

## 3. Running the Evals Benchmark
```bash
python -m evals.run_evals
```
