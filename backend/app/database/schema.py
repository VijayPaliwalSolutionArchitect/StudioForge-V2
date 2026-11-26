"""app/database/schema.py — Relational Database Schema DDL for StudioForge V2.

Tables:
1. `brands` — Brand identities, core values, forbidden words, and mandatory hex color codes.
2. `campaigns` — Marketing campaigns tied to brand identities with target channels and budgets.
3. `creative_briefs` — AI-assisted briefs with target audience, visual prompts, and copy variants.
4. `assets` — Generated image/copy media assets with aspect ratio, resolution, and ComfyUI seed.
5. `calendar_items` — Scheduled publishing events for social channels (LinkedIn, X, Instagram, YouTube).
6. `creative_approvals` — Two-Man Rule approval queue for high-impact paid advertising campaigns.
7. `audit_logs` — Immutable audit trail of all generation, approval, and publishing events.
"""

DDL_STATEMENTS = [
    # 1. Brands Table
    """
    CREATE TABLE IF NOT EXISTS brands (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        industry TEXT NOT NULL,
        tone_of_voice TEXT NOT NULL,       -- e.g. 'Authoritative, Futuristic, Empathetic'
        tagline TEXT,
        primary_color_hex TEXT NOT NULL,    -- e.g. '#06b6d4'
        secondary_color_hex TEXT NOT NULL,  -- e.g. '#3b82f6'
        forbidden_words_json TEXT NOT NULL, -- JSON array of prohibited strings
        target_personas_json TEXT NOT NULL, -- JSON array of ICP target personas
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );
    """,

    # 2. Campaigns Table
    """
    CREATE TABLE IF NOT EXISTS campaigns (
        id TEXT PRIMARY KEY,
        brand_id TEXT NOT NULL,
        name TEXT NOT NULL,
        objective TEXT NOT NULL,            -- AWARENESS, LEAD_GEN, PRODUCT_LAUNCH, CONVERSION
        budget_usd REAL NOT NULL DEFAULT 0.0,
        is_paid_campaign INTEGER NOT NULL DEFAULT 0,
        status TEXT NOT NULL DEFAULT 'ACTIVE', -- PLANNING, ACTIVE, COMPLETED, PAUSED
        start_date TEXT NOT NULL,
        end_date TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY (brand_id) REFERENCES brands(id) ON DELETE CASCADE
    );
    """,

    # 3. Creative Briefs Table
    """
    CREATE TABLE IF NOT EXISTS creative_briefs (
        id TEXT PRIMARY KEY,
        campaign_id TEXT NOT NULL,
        brand_id TEXT NOT NULL,
        title TEXT NOT NULL,
        hook TEXT NOT NULL,
        core_message TEXT NOT NULL,
        call_to_action TEXT NOT NULL,
        target_channels_json TEXT NOT NULL, -- e.g. ['linkedin', 'x_twitter', 'instagram']
        visual_prompt TEXT NOT NULL,        -- Headless ComfyUI synthesis prompt
        negative_prompt TEXT NOT NULL,
        aspect_ratio TEXT NOT NULL DEFAULT '16:9', -- 16:9, 1:1, 9:16
        brand_alignment_score REAL NOT NULL DEFAULT 0.0,
        status TEXT NOT NULL DEFAULT 'DRAFT', -- DRAFT, IN_REVIEW, APPROVED, REJECTED
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY (campaign_id) REFERENCES campaigns(id) ON DELETE CASCADE,
        FOREIGN KEY (brand_id) REFERENCES brands(id) ON DELETE CASCADE
    );
    """,

    # 4. Creative Assets Table
    """
    CREATE TABLE IF NOT EXISTS assets (
        id TEXT PRIMARY KEY,
        brief_id TEXT NOT NULL,
        brand_id TEXT NOT NULL,
        asset_type TEXT NOT NULL,            -- IMAGE, COPY_VARIANT, VIDEO_STORYBOARD
        content_url_or_text TEXT NOT NULL,
        resolution TEXT NOT NULL DEFAULT '1024x1024',
        comfyui_prompt_id TEXT,
        comfyui_seed INTEGER,
        brand_check_passed INTEGER NOT NULL DEFAULT 1,
        created_at TEXT NOT NULL,
        FOREIGN KEY (brief_id) REFERENCES creative_briefs(id) ON DELETE CASCADE,
        FOREIGN KEY (brand_id) REFERENCES brands(id) ON DELETE CASCADE
    );
    """,

    # 5. Content Calendar Items Table
    """
    CREATE TABLE IF NOT EXISTS calendar_items (
        id TEXT PRIMARY KEY,
        brief_id TEXT NOT NULL,
        brand_id TEXT NOT NULL,
        channel TEXT NOT NULL,              -- LINKEDIN, TWITTER, INSTAGRAM, YOUTUBE
        scheduled_for TEXT NOT NULL,
        copy_text TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'SCHEDULED', -- SCHEDULED, PUBLISHED, CANCELLED
        created_at TEXT NOT NULL,
        FOREIGN KEY (brief_id) REFERENCES creative_briefs(id) ON DELETE CASCADE,
        FOREIGN KEY (brand_id) REFERENCES brands(id) ON DELETE CASCADE
    );
    """,

    # 6. Two-Man Rule Creative Approvals Table
    """
    CREATE TABLE IF NOT EXISTS creative_approvals (
        id TEXT PRIMARY KEY,
        brief_id TEXT NOT NULL,
        campaign_id TEXT NOT NULL,
        requested_by TEXT NOT NULL,
        requester_role TEXT NOT NULL DEFAULT 'CREATIVE_PRODUCER',
        approver TEXT,
        approver_role TEXT,
        decision TEXT NOT NULL DEFAULT 'PENDING', -- PENDING, APPROVED, REJECTED
        review_notes TEXT,
        created_at TEXT NOT NULL,
        resolved_at TEXT,
        FOREIGN KEY (brief_id) REFERENCES creative_briefs(id) ON DELETE CASCADE
    );
    """,

    # 7. Immutable Audit Logs Table
    """
    CREATE TABLE IF NOT EXISTS audit_logs (
        id TEXT PRIMARY KEY,
        timestamp TEXT NOT NULL,
        brand_id TEXT,
        actor TEXT NOT NULL,
        action TEXT NOT NULL,
        resource_id TEXT,
        status TEXT NOT NULL,
        details TEXT
    );
    """
]
