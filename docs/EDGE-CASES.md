# StudioForge V2 — Edge Cases & Creative Governance Defenses

1. **Forbidden Word Evasion via Obfuscation:** Regex boundary scans strip formatting and detect obfuscated prohibited terms (`cheap`, `hacky`, `quick fix`).
2. **Off-Brand Score Degradation:** Tone analyzer deducts 40 points per violation, rejecting off-brand briefs ($<75.0$ score) with HTTP 422 before any generation spend occurs.
3. **Paid Campaign Budget Protection:** Paid media campaigns ($>0.0) automatically lock briefs into `IN_REVIEW` status; asset generation is prevented until an authorized Creative Director signs off.
4. **ComfyUI Aspect Ratio Distortion Prevention:** Strict dimensions (1344x768, 1024x1024, 768x1344) prevent latent compression distortion.
5. **Unauthorized Approval Escalation (HTTP 403):** Only callers with `CREATIVE_DIRECTOR` or `ADMIN` roles can approve paid campaigns.
6. **Concurrent Publishing Race Conditions:** Atomic status updates ensure content calendar items are published exactly once.
7. **Offline AI Failover:** When monthly LLM budget cap ($250.00) is reached, copy generation automatically routes to local air-gapped `qwen2.5:14b`.
