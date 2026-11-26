# StudioForge V2 — Technical Architecture & Creative Pipeline

## 1. Executive Summary
StudioForge V2 is an enterprise-grade autonomous AI brand and media factory orchestrating deterministic brand tone reasoning, ComfyUI latent diffusion prompt synthesis, multi-channel social scheduling, and Two-Man Rule creative approvals.

```
+---------------------------------------------------------------------------------------+
|                                   React 18 Workstation                                |
|   [ Creative Briefs ]   [ Brand Guidelines ]   [ Campaigns ]   [ Content Calendar ]   |
+-------------------------------------------+-------------------------------------------+
                                            | REST / JSON (Port 8097)
+-------------------------------------------v-------------------------------------------+
|                          FastAPI Creative Engine (:8097)                              |
+-------------------------------------------+-------------------------------------------+
         |                                  |                                  |
+--------v---------+             +----------v----------+             +---------v--------+
| Tone Analyzer    |             | Visual Prompt Syn   |             | 5-Pool Router    |
| - Pillar Scoring |             | - Aspect Ratio Grid |             | - Groq / Claude  |
| - Forbidden Scnr |             | - Negative Prompts  |             | - Local Qwen     |
| - Min 75.0 Gate  |             | - Brand Hex Grading |             | - Budget Ledger  |
+--------+---------+             +----------+----------+             +---------+--------+
         |                                  |                                  |
+--------v----------------------------------v----------------------------------v--------+
|                           Persistent SQLite WAL Engine                                |
|    brands | campaigns | creative_briefs | assets | calendar_items | approvals         |
+---------------------------------------------------------------------------------------+
```

## 2. Headless ComfyUI & Aspect Ratio Constraints
Visual prompts are synthesized with strict latent constraints:
* **16:9 Landscape:** 1344x768 (YouTube, Desktop Display Ads)
* **1:1 Square:** 1024x1024 (Instagram, LinkedIn Feed)
* **9:16 Vertical:** 768x1344 (Instagram Reels, TikTok, YouTube Shorts)
Every prompt automatically injects negative token exclusion guards and brand hex palette accents.
