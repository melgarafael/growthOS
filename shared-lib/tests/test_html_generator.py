"""Tests for the GrowthOS landing page HTML generator."""

import pytest

from growthOS_shared.html_generator import (
    VALID_STYLES,
    _apply_anti_slop,
    _build_tone_suffix,
    _load_template,
    generate_landing_page,
    list_available_styles,
)
from growthOS_shared.config import (
    AntiSlopConfig,
    BrandConfig,
    BrandVoiceConfig,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def brand_config():
    return BrandVoiceConfig(
        brand=BrandConfig(
            name="TestBrand",
            tone=["professional", "friendly"],
            avoid=["synergy"],
        ),
        anti_slop=AntiSlopConfig(
            enabled=True,
            banned_phrases=["game-changer", "revolutionary"],
            custom_banned=["synergy"],
        ),
    )


@pytest.fixture
def brand_config_no_slop():
    return BrandVoiceConfig(
        brand=BrandConfig(
            name="TestBrand",
            tone=["casual"],
        ),
        anti_slop=AntiSlopConfig(enabled=False),
    )


# ---------------------------------------------------------------------------
# Template loading
# ---------------------------------------------------------------------------

class TestLoadTemplate:
    def test_loads_all_valid_styles(self):
        for style in VALID_STYLES:
            html = _load_template(style)
            assert "<!DOCTYPE html>" in html
            assert "{{product_name}}" in html

    def test_invalid_style_raises(self):
        with pytest.raises(ValueError, match="Unknown style"):
            _load_template("neon")

    def test_template_has_required_sections(self):
        for style in VALID_STYLES:
            html = _load_template(style)
            assert "hero" in html
            assert "features" in html
            assert "social-proof" in html
            assert "cta" in html
            assert "footer" in html

    def test_template_has_seo_tags(self):
        for style in VALID_STYLES:
            html = _load_template(style)
            assert 'og:title' in html
            assert 'og:description' in html
            assert 'twitter:card' in html
            assert 'meta name="description"' in html

    def test_no_external_dependencies(self):
        for style in VALID_STYLES:
            html = _load_template(style)
            assert "http://" not in html
            assert "https://" not in html
            assert "<script" not in html


# ---------------------------------------------------------------------------
# Anti-slop filter
# ---------------------------------------------------------------------------

class TestAntiSlop:
    def test_removes_banned_phrases(self, brand_config):
        text = "This is a game-changer for your workflow."
        result = _apply_anti_slop(text, brand_config)
        assert "game-changer" not in result

    def test_case_insensitive(self, brand_config):
        text = "This is REVOLUTIONARY technology."
        result = _apply_anti_slop(text, brand_config)
        assert "revolutionary" not in result.lower()

    def test_removes_custom_banned(self, brand_config):
        text = "Leverage the synergy of our platform."
        result = _apply_anti_slop(text, brand_config)
        assert "synergy" not in result

    def test_disabled_filter_passes_through(self, brand_config_no_slop):
        text = "This is a game-changer."
        result = _apply_anti_slop(text, brand_config_no_slop)
        assert result == text


# ---------------------------------------------------------------------------
# Tone suffix builder
# ---------------------------------------------------------------------------

class TestBuildToneSuffix:
    def test_single_tone(self, brand_config_no_slop):
        assert _build_tone_suffix(brand_config_no_slop) == "casual"

    def test_multiple_tones(self, brand_config):
        result = _build_tone_suffix(brand_config)
        assert result == "professional & friendly"

    def test_three_tones(self):
        cfg = BrandVoiceConfig(
            brand=BrandConfig(name="X", tone=["bold", "fun", "clear"]),
        )
        assert _build_tone_suffix(cfg) == "bold, fun & clear"


# ---------------------------------------------------------------------------
# Full generation
# ---------------------------------------------------------------------------

class TestGenerateLandingPage:
    def test_generates_valid_html(self):
        html = generate_landing_page("Acme", "Build better software.")
        assert "<!DOCTYPE html>" in html
        assert "Acme" in html
        assert "Build better software." in html

    def test_all_styles_generate(self):
        for style in VALID_STYLES:
            html = generate_landing_page("Acme", "Test desc.", style=style)
            assert "<!DOCTYPE html>" in html

    def test_under_100kb(self):
        for style in VALID_STYLES:
            html = generate_landing_page("Acme", "Test desc.", style=style)
            assert len(html.encode("utf-8")) < 100 * 1024

    def test_custom_cta(self):
        html = generate_landing_page(
            "Acme", "Desc", cta_text="Sign Up Now", cta_url="https://acme.dev",
        )
        assert "Sign Up Now" in html
        assert "https://acme.dev" in html

    def test_custom_features(self):
        features = [
            {"title": "Alpha", "desc": "First feature."},
            {"title": "Beta", "desc": "Second feature."},
        ]
        html = generate_landing_page("Acme", "Desc", features=features)
        assert "Alpha" in html
        assert "Beta" in html

    def test_custom_testimonial(self):
        html = generate_landing_page(
            "Acme", "Desc",
            testimonial_text="Amazing product!",
            testimonial_author="Jane Doe",
        )
        assert "Amazing product!" in html
        assert "Jane Doe" in html

    def test_brand_config_integration(self, brand_config):
        html = generate_landing_page(
            "Acme", "A game-changer for devs.",
            brand_config=brand_config,
        )
        assert "game-changer" not in html

    def test_meta_description_truncated(self):
        long_desc = "A" * 200
        html = generate_landing_page("Acme", long_desc)
        # meta description should be truncated to 160 chars
        assert 'content="' + "A" * 160 + '"' in html

    def test_no_external_urls_in_output(self):
        html = generate_landing_page("Acme", "Test.")
        # Only the CTA url should be the default "#"
        lines = [line for line in html.split("\n") if "http" in line.lower()]
        # No CDN or external resources
        for line in lines:
            assert "cdn" not in line.lower()
            assert "fonts.googleapis" not in line.lower()

    def test_responsive_viewport_tag(self):
        for style in VALID_STYLES:
            html = generate_landing_page("Acme", "Test.", style=style)
            assert 'width=device-width' in html

    def test_custom_headline(self):
        html = generate_landing_page("Acme", "Desc", headline="Ship Faster")
        assert "Ship Faster" in html

    def test_invalid_style_raises(self):
        with pytest.raises(ValueError, match="Unknown style"):
            generate_landing_page("Acme", "Desc", style="neon")

    def test_default_headline_is_product_name(self):
        html = generate_landing_page("SuperApp", "Desc")
        assert ">SuperApp<" in html


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

class TestListStyles:
    def test_returns_all_styles(self):
        styles = list_available_styles()
        assert set(styles) == {"minimal", "bold", "gradient"}
