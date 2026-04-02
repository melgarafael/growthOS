"""Tests for GrowthOS brand voice configuration loader."""

from pathlib import Path

import pytest
import yaml

from growthOS_shared.config import (
    AntiSlopConfig,
    AutonomyConfig,
    PlatformConfig,
    load_brand_voice,
)

FIXTURES_DIR = Path(__file__).parent / "fixtures"

VALID_CONFIG = {
    "brand": {
        "name": "TestBrand",
        "tone": ["professional", "friendly"],
        "tagline": "Test tagline",
        "avoid": ["synergy"],
        "personality": "Helpful and direct",
        "industry": "SaaS",
    },
    "platforms": {
        "twitter": {
            "enabled": True,
            "tone_override": "concise_witty",
            "max_length": 280,
        },
        "linkedin": {
            "enabled": True,
            "max_length": 3000,
            "hashtags": True,
            "post_types": ["article", "post"],
        },
        "reddit": {
            "enabled": False,
            "tone_override": "authentic_casual",
            "max_length": 10000,
        },
    },
    "anti_slop": {
        "enabled": True,
        "banned_phrases": ["game-changer", "revolutionary"],
        "style_rules": ["Use active voice"],
        "custom_banned": ["our proprietary"],
    },
    "autonomy": {
        "level": "semi",
        "require_preview": True,
        "dry_run_default": True,
        "kill_switch": True,
    },
}


@pytest.fixture
def valid_yaml_file(tmp_path: Path) -> Path:
    """Write a valid config YAML and return its path."""
    p = tmp_path / "brand-voice.yaml"
    p.write_text(yaml.dump(VALID_CONFIG), encoding="utf-8")
    return p


@pytest.fixture
def minimal_yaml_file(tmp_path: Path) -> Path:
    """Write a minimal valid config (only required fields)."""
    minimal = {"brand": {"name": "MinBrand", "tone": ["casual"]}}
    p = tmp_path / "brand-voice.yaml"
    p.write_text(yaml.dump(minimal), encoding="utf-8")
    return p


# ── Valid YAML parsing ──────────────────────────────────────────────


class TestValidParsing:
    def test_full_config_loads(self, valid_yaml_file: Path) -> None:
        config = load_brand_voice(str(valid_yaml_file))
        assert config.brand.name == "TestBrand"
        assert config.brand.tone == ["professional", "friendly"]
        assert config.brand.tagline == "Test tagline"

    def test_minimal_config_loads(self, minimal_yaml_file: Path) -> None:
        config = load_brand_voice(str(minimal_yaml_file))
        assert config.brand.name == "MinBrand"
        assert config.brand.tone == ["casual"]
        assert config.autonomy.level == "semi"  # default

    def test_platforms_parsed(self, valid_yaml_file: Path) -> None:
        config = load_brand_voice(str(valid_yaml_file))
        assert "twitter" in config.platforms
        assert config.platforms["twitter"].max_length == 280
        assert config.platforms["linkedin"].hashtags is True

    def test_anti_slop_parsed(self, valid_yaml_file: Path) -> None:
        config = load_brand_voice(str(valid_yaml_file))
        assert config.anti_slop.enabled is True
        assert "game-changer" in config.anti_slop.banned_phrases

    def test_autonomy_parsed(self, valid_yaml_file: Path) -> None:
        config = load_brand_voice(str(valid_yaml_file))
        assert config.autonomy.level == "semi"
        assert config.autonomy.kill_switch is True


# ── Missing required fields ─────────────────────────────────────────


class TestMissingRequiredFields:
    def test_missing_brand_name(self, tmp_path: Path) -> None:
        p = tmp_path / "bad.yaml"
        p.write_text(yaml.dump({"brand": {"tone": ["casual"]}}), encoding="utf-8")
        with pytest.raises(Exception):  # Pydantic ValidationError
            load_brand_voice(str(p))

    def test_empty_brand_name(self, tmp_path: Path) -> None:
        p = tmp_path / "bad.yaml"
        p.write_text(
            yaml.dump({"brand": {"name": "  ", "tone": ["casual"]}}),
            encoding="utf-8",
        )
        with pytest.raises(Exception, match="brand.name"):
            load_brand_voice(str(p))

    def test_missing_tone(self, tmp_path: Path) -> None:
        p = tmp_path / "bad.yaml"
        p.write_text(yaml.dump({"brand": {"name": "X"}}), encoding="utf-8")
        with pytest.raises(Exception):
            load_brand_voice(str(p))

    def test_empty_tone_list(self, tmp_path: Path) -> None:
        p = tmp_path / "bad.yaml"
        p.write_text(
            yaml.dump({"brand": {"name": "X", "tone": []}}),
            encoding="utf-8",
        )
        with pytest.raises(Exception, match="tone"):
            load_brand_voice(str(p))

    def test_missing_brand_section_entirely(self, tmp_path: Path) -> None:
        p = tmp_path / "bad.yaml"
        p.write_text(yaml.dump({"platforms": {}}), encoding="utf-8")
        with pytest.raises(Exception):
            load_brand_voice(str(p))

    def test_file_not_found(self) -> None:
        with pytest.raises(FileNotFoundError, match="Brand voice config not found"):
            load_brand_voice("/nonexistent/path/brand-voice.yaml")

    def test_invalid_yaml_format(self, tmp_path: Path) -> None:
        p = tmp_path / "bad.yaml"
        p.write_text("just a string", encoding="utf-8")
        with pytest.raises(ValueError, match="expected YAML mapping"):
            load_brand_voice(str(p))


# ── Platform override merging ───────────────────────────────────────


class TestPlatformOverrides:
    def test_get_platform_exists(self, valid_yaml_file: Path) -> None:
        config = load_brand_voice(str(valid_yaml_file))
        twitter = config.get_platform("twitter")
        assert twitter is not None
        assert twitter.tone_override == "concise_witty"

    def test_get_platform_not_found(self, valid_yaml_file: Path) -> None:
        config = load_brand_voice(str(valid_yaml_file))
        assert config.get_platform("tiktok") is None

    def test_get_enabled_platforms(self, valid_yaml_file: Path) -> None:
        config = load_brand_voice(str(valid_yaml_file))
        enabled = config.get_enabled_platforms()
        assert "twitter" in enabled
        assert "linkedin" in enabled
        assert "reddit" not in enabled  # disabled in fixture

    def test_platform_defaults(self) -> None:
        p = PlatformConfig()
        assert p.enabled is True
        assert p.tone_override is None
        assert p.max_length is None
        assert p.hashtags is False

    def test_tone_override_null_means_inherit(self, valid_yaml_file: Path) -> None:
        config = load_brand_voice(str(valid_yaml_file))
        linkedin = config.get_platform("linkedin")
        assert linkedin is not None
        assert linkedin.tone_override is None  # inherits brand tone


# ── Anti-slop phrase matching ───────────────────────────────────────


class TestAntiSlop:
    def test_is_banned_exact(self) -> None:
        slop = AntiSlopConfig(banned_phrases=["game-changer"], custom_banned=[])
        assert slop.is_banned("game-changer") is True

    def test_is_banned_case_insensitive(self) -> None:
        slop = AntiSlopConfig(banned_phrases=["Game-Changer"], custom_banned=[])
        assert slop.is_banned("GAME-CHANGER") is True

    def test_is_banned_substring_match(self) -> None:
        slop = AntiSlopConfig(banned_phrases=["game-changer"], custom_banned=[])
        assert slop.is_banned("This is a real game-changer for us") is True

    def test_is_banned_custom_phrases(self) -> None:
        slop = AntiSlopConfig(banned_phrases=[], custom_banned=["our proprietary"])
        assert slop.is_banned("Check out our proprietary tech") is True

    def test_not_banned(self) -> None:
        slop = AntiSlopConfig(banned_phrases=["game-changer"], custom_banned=[])
        assert slop.is_banned("This is a practical improvement") is False

    def test_empty_banned_list(self) -> None:
        slop = AntiSlopConfig(banned_phrases=[], custom_banned=[])
        assert slop.is_banned("anything goes") is False

    def test_full_config_anti_slop(self, valid_yaml_file: Path) -> None:
        config = load_brand_voice(str(valid_yaml_file))
        assert config.anti_slop.is_banned("This is revolutionary!") is True
        assert config.anti_slop.is_banned("This is practical") is False


# ── Autonomy level validation ──────────────────────────────────────


class TestAutonomyValidation:
    def test_valid_levels(self) -> None:
        for level in ("manual", "semi", "auto"):
            a = AutonomyConfig(level=level)
            assert a.level == level

    def test_invalid_level(self) -> None:
        with pytest.raises(Exception, match="autonomy.level"):
            AutonomyConfig(level="yolo")

    def test_defaults(self) -> None:
        a = AutonomyConfig()
        assert a.level == "semi"
        assert a.require_preview is True
        assert a.dry_run_default is True
        assert a.kill_switch is True


# ── Environment variable override ──────────────────────────────────


class TestEnvVarOverride:
    def test_env_var_path(self, valid_yaml_file: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GROWTHOS_BRAND_VOICE_PATH", str(valid_yaml_file))
        config = load_brand_voice()
        assert config.brand.name == "TestBrand"

    def test_explicit_path_overrides_env(
        self, valid_yaml_file: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        other = tmp_path / "other.yaml"
        other.write_text(
            yaml.dump({"brand": {"name": "Other", "tone": ["bold"]}}),
            encoding="utf-8",
        )
        monkeypatch.setenv("GROWTHOS_BRAND_VOICE_PATH", str(valid_yaml_file))
        config = load_brand_voice(str(other))
        assert config.brand.name == "Other"

    def test_env_var_file_not_found(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GROWTHOS_BRAND_VOICE_PATH", "/nonexistent/config.yaml")
        with pytest.raises(FileNotFoundError):
            load_brand_voice()


# ── Example file validation ────────────────────────────────────────


class TestExampleFile:
    def test_example_file_is_valid(self) -> None:
        """Ensure brand-voice.example.yaml parses without errors."""
        example_path = Path(__file__).parent.parent.parent / "brand-voice.example.yaml"
        if not example_path.exists():
            pytest.skip("brand-voice.example.yaml not found")
        config = load_brand_voice(str(example_path))
        assert config.brand.name == "MyProduct"
        assert len(config.anti_slop.banned_phrases) >= 15
        assert config.autonomy.level == "semi"
