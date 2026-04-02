"""Brand voice configuration loader for GrowthOS."""

import os
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel, Field, field_validator


class PlatformConfig(BaseModel):
    """Configuration for a single social media platform."""

    enabled: bool = True
    tone_override: Optional[str] = None
    max_length: Optional[int] = None
    hashtags: bool = False
    threads: bool = False
    post_types: list[str] = Field(default_factory=list)


class AntiSlopConfig(BaseModel):
    """Anti-slop filter configuration to prevent generic AI marketing language."""

    enabled: bool = True
    banned_phrases: list[str] = Field(default_factory=list)
    style_rules: list[str] = Field(default_factory=list)
    custom_banned: list[str] = Field(default_factory=list)

    def is_banned(self, phrase: str) -> bool:
        """Check if a phrase matches any banned phrase (case-insensitive)."""
        phrase_lower = phrase.lower()
        all_banned = self.banned_phrases + self.custom_banned
        return any(banned.lower() in phrase_lower for banned in all_banned)


class AutonomyConfig(BaseModel):
    """Autonomy level configuration for GrowthOS operations."""

    level: str = "semi"
    require_preview: bool = True
    dry_run_default: bool = True
    kill_switch: bool = True

    @field_validator("level")
    @classmethod
    def validate_level(cls, v: str) -> str:
        allowed = {"manual", "semi", "auto"}
        if v not in allowed:
            raise ValueError(f"autonomy.level must be one of {allowed}, got '{v}'")
        return v


class BrandConfig(BaseModel):
    """Core brand identity configuration."""

    name: str
    tagline: str = ""
    tone: list[str]
    avoid: list[str] = Field(default_factory=list)
    personality: str = ""
    industry: str = ""

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("brand.name is required and cannot be empty")
        return v

    @field_validator("tone")
    @classmethod
    def tone_not_empty(cls, v: list[str]) -> list[str]:
        if not v:
            raise ValueError("brand.tone requires at least one tone descriptor")
        return v


class BrandVoiceConfig(BaseModel):
    """Root configuration model for GrowthOS brand voice."""

    brand: BrandConfig
    platforms: dict[str, PlatformConfig] = Field(default_factory=dict)
    anti_slop: AntiSlopConfig = Field(default_factory=AntiSlopConfig)
    autonomy: AutonomyConfig = Field(default_factory=AutonomyConfig)

    def get_platform(self, name: str) -> Optional[PlatformConfig]:
        """Get platform config by name, returns None if not found."""
        return self.platforms.get(name)

    def get_enabled_platforms(self) -> dict[str, PlatformConfig]:
        """Return only enabled platforms."""
        return {k: v for k, v in self.platforms.items() if v.enabled}


def _resolve_config_path(path: Optional[str] = None) -> Path:
    """Resolve the brand voice config file path.

    Priority:
    1. Explicit path argument
    2. GROWTHOS_BRAND_VOICE_PATH environment variable
    3. Default: brand-voice.yaml in plugin root
    """
    if path:
        return Path(path)

    env_path = os.environ.get("GROWTHOS_BRAND_VOICE_PATH")
    if env_path:
        return Path(env_path)

    return Path(__file__).parent.parent.parent / "brand-voice.yaml"


def load_brand_voice(path: Optional[str] = None) -> BrandVoiceConfig:
    """Load and validate brand voice configuration from YAML.

    Args:
        path: Optional explicit path to the config file.

    Returns:
        Validated BrandVoiceConfig instance.

    Raises:
        FileNotFoundError: If the config file doesn't exist.
        ValueError: If the config is invalid.
    """
    config_path = _resolve_config_path(path)

    if not config_path.exists():
        raise FileNotFoundError(
            f"Brand voice config not found at {config_path}. "
            "Copy brand-voice.example.yaml to brand-voice.yaml and customize it."
        )

    raw = yaml.safe_load(config_path.read_text(encoding="utf-8"))

    if not isinstance(raw, dict):
        raise ValueError(f"Invalid config format in {config_path}: expected YAML mapping")

    return BrandVoiceConfig(**raw)
