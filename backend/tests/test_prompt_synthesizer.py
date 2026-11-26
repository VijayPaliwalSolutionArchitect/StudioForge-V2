"""backend/tests/test_prompt_synthesizer.py — ComfyUI / SD / Flux prompt synthesizer tests."""

from app.creative.prompt_synthesizer import VisualPromptSynthesizer


def test_synthesize_prompt_16_9_aspect_ratio():
    spec = VisualPromptSynthesizer.synthesize_prompt(
        concept="autonomous server datacenter running AI agents",
        primary_color_hex="#06b6d4",
        secondary_color_hex="#3b82f6",
        aspect_ratio="16:9",
    )
    assert spec["aspect_ratio"] == "16:9"
    assert spec["width"] == 1344
    assert spec["height"] == 768
    assert "#06b6d4" in spec["positive_prompt"]
    assert "blurry" in spec["negative_prompt"]


def test_synthesize_prompt_1_1_square_aspect_ratio():
    spec = VisualPromptSynthesizer.synthesize_prompt(
        concept="executive boardroom AI dashboard",
        aspect_ratio="1:1",
    )
    assert spec["width"] == 1024
    assert spec["height"] == 1024
    assert "Instagram / LinkedIn Post" in spec["target_channel"]


def test_synthesize_prompt_9_16_vertical_reels():
    spec = VisualPromptSynthesizer.synthesize_prompt(
        concept="mobile phone streaming AI agent telemetry",
        aspect_ratio="9:16",
    )
    assert spec["width"] == 768
    assert spec["height"] == 1344
    assert "Reels" in spec["target_channel"]


def test_negative_prompt_includes_standard_exclusions():
    spec = VisualPromptSynthesizer.synthesize_prompt(concept="modern drone")
    neg = spec["negative_prompt"].lower()
    assert "watermark" in neg
    assert "distorted" in neg
    assert "deformed fingers" in neg


def test_sampler_settings_present():
    spec = VisualPromptSynthesizer.synthesize_prompt(concept="neural network chip")
    sampler = spec["sampler_settings"]
    assert sampler["sampler_name"] == "euler_ancestral"
    assert sampler["steps"] == 28
