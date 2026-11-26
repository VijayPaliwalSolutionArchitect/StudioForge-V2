# StudioForge V2 — API Reference Specification

All endpoints are hosted on `http://127.0.0.1:8097`.

---

## 1. Creative Briefs & Synthesis

### `POST /api/v1/briefs`
Synthesizes an AI creative brief, runs real-time Brand Tone validation, constructs ComfyUI visual prompts, and triggers Two-Man approvals if paid.

#### Request Body
```json
{
  "campaign_id": "camp-fleet-launch-2026",
  "brand_id": "brand-shivam-itcs",
  "concept_title": "Autonomous Fleet Launch",
  "core_idea": "Sovereign enterprise autonomous AI systems delivering high assurance velocity without cloud leaks",
  "aspect_ratio": "16:9",
  "target_channels": ["linkedin", "x_twitter"]
}
```

#### Response (200 OK)
```json
{
  "brief": {
    "id": "brief-a1b2c3d4",
    "title": "Autonomous Fleet Launch",
    "brand_alignment_score": 95.0,
    "status": "IN_REVIEW"
  },
  "visual_spec": {
    "positive_prompt": "Hyper-detailed, commercial grade photograph...",
    "negative_prompt": "blurry, distorted...",
    "width": 1344,
    "height": 768
  },
  "requires_two_man_approval": true
}
```

---

## 2. Other Core Endpoints

* `GET /api/v1/brands` — List active brand guidelines.
* `POST /api/v1/campaigns` — Provision marketing campaigns.
* `POST /api/v1/assets/generate` — Render media assets via ComfyUI.
* `POST /api/v1/calendar` — Schedule multi-channel publication.
* `POST /api/v1/approvals/{id}/resolve` — Two-Man Rule Creative Director clearance.
