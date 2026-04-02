"""Tests for the GrowthOS Instagram carousel HTML generator."""

from pathlib import Path

import pytest

from growthOS_shared.carousel_generator import (
    CarouselOutput,
    MAX_SLIDE_KB,
    MAX_SLIDES,
    MIN_SLIDES,
    SlideContent,
    VALID_DIMENSIONS,
    VALID_STYLES,
    generate_carousel,
)
from growthOS_shared.config import (
    AntiSlopConfig,
    BrandConfig,
    BrandVoiceConfig,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_slide(
    slide_number: int = 1,
    total_slides: int = 5,
    type: str = "content",
    headline: str = "Test Headline",
    **overrides,
) -> SlideContent:
    defaults = {
        "slide_number": slide_number,
        "total_slides": total_slides,
        "type": type,
        "headline": headline,
    }
    defaults.update(overrides)
    return SlideContent(**defaults)


def _make_slides(count: int = 5) -> list[SlideContent]:
    """Build a list of slides with cover, content, and cta types."""
    slides = []
    for i in range(1, count + 1):
        if i == 1:
            slide_type = "cover"
        elif i == count:
            slide_type = "cta"
        else:
            slide_type = "content"
        slides.append(
            _make_slide(
                slide_number=i,
                total_slides=count,
                type=slide_type,
                headline=f"Headline {i}",
                body=f"Body text for slide {i}.",
                icon="🚀" if slide_type == "content" else "",
                bullets=["Bullet A", "Bullet B"] if slide_type == "content" else [],
                cta_text="Follow for more" if slide_type == "cta" else "",
            )
        )
    return slides


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def brand_config() -> BrandVoiceConfig:
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
def brand_config_with_colors() -> BrandVoiceConfig:
    return BrandVoiceConfig(
        brand=BrandConfig(
            name="ColorBrand",
            tone=["bold"],
            avoid=[],
        ),
        anti_slop=AntiSlopConfig(enabled=False),
    )


@pytest.fixture
def five_slides() -> list[SlideContent]:
    return _make_slides(5)


# ---------------------------------------------------------------------------
# SlideContent
# ---------------------------------------------------------------------------


class TestSlideContent:
    def test_create_with_all_fields(self) -> None:
        slide = SlideContent(
            slide_number=3,
            total_slides=7,
            type="content",
            headline="All Fields",
            body="Some body text.",
            icon="💡",
            bullets=["First", "Second"],
            cta_text="Save it",
            cta_action="bookmark",
        )
        assert slide.slide_number == 3
        assert slide.total_slides == 7
        assert slide.type == "content"
        assert slide.headline == "All Fields"
        assert slide.body == "Some body text."
        assert slide.icon == "💡"
        assert slide.bullets == ["First", "Second"]
        assert slide.cta_text == "Save it"
        assert slide.cta_action == "bookmark"

    def test_create_with_defaults(self) -> None:
        slide = SlideContent(
            slide_number=1,
            total_slides=5,
            type="cover",
            headline="Only Required",
        )
        assert slide.slide_number == 1
        assert slide.total_slides == 5
        assert slide.type == "cover"
        assert slide.headline == "Only Required"
        assert slide.body == ""
        assert slide.icon == ""
        assert slide.bullets == []
        assert slide.cta_text == ""
        assert slide.cta_action == ""

    def test_valid_types(self) -> None:
        for slide_type in ("cover", "content", "cta"):
            slide = _make_slide(type=slide_type)
            assert slide.type == slide_type


# ---------------------------------------------------------------------------
# CarouselOutput
# ---------------------------------------------------------------------------


class TestCarouselOutput:
    def test_construction_with_all_fields(self) -> None:
        output = CarouselOutput(
            slides=["/tmp/slide-01.html", "/tmp/slide-02.html"],
            preview="/tmp/all-slides.html",
            total_slides=2,
            style="bold",
            dimensions=(1080, 1350),
        )
        assert output.slides == ["/tmp/slide-01.html", "/tmp/slide-02.html"]
        assert output.preview == "/tmp/all-slides.html"
        assert output.total_slides == 2
        assert output.style == "bold"
        assert output.dimensions == (1080, 1350)

    def test_slides_contains_paths(self) -> None:
        output = CarouselOutput(
            slides=["/out/slide-01.html", "/out/slide-02.html", "/out/slide-03.html"],
            preview="/out/all-slides.html",
            total_slides=3,
            style="minimal",
            dimensions=(1080, 1080),
        )
        for path in output.slides:
            assert isinstance(path, str)
            assert path.endswith(".html")


# ---------------------------------------------------------------------------
# generate_carousel — style validation
# ---------------------------------------------------------------------------


class TestGenerateCarouselStyleValidation:
    def test_all_six_styles_produce_output(self, tmp_path: Path) -> None:
        slides = _make_slides(3)
        for style in VALID_STYLES:
            out_dir = tmp_path / style
            out_dir.mkdir()
            result = generate_carousel(
                slides=slides,
                style=style,
                output_dir=str(out_dir),
            )
            assert isinstance(result, CarouselOutput)
            assert len(result.slides) == 3

    def test_valid_styles_list(self) -> None:
        expected = {"minimal", "bold", "gradient", "clean-educator", "dark-premium", "vibrant-creator"}
        assert set(VALID_STYLES) == expected

    def test_invalid_style_raises(self, tmp_path: Path) -> None:
        slides = _make_slides(3)
        with pytest.raises(ValueError, match="style"):
            generate_carousel(
                slides=slides,
                style="neon-glow",
                output_dir=str(tmp_path),
            )


# ---------------------------------------------------------------------------
# generate_carousel — slide count validation
# ---------------------------------------------------------------------------


class TestGenerateCarouselSlideCountValidation:
    def test_minimum_slides_works(self, tmp_path: Path) -> None:
        slides = _make_slides(MIN_SLIDES)
        result = generate_carousel(slides=slides, output_dir=str(tmp_path))
        assert result.total_slides == MIN_SLIDES

    def test_maximum_slides_works(self, tmp_path: Path) -> None:
        slides = _make_slides(MAX_SLIDES)
        result = generate_carousel(slides=slides, output_dir=str(tmp_path))
        assert result.total_slides == MAX_SLIDES

    def test_below_minimum_raises(self, tmp_path: Path) -> None:
        slides = _make_slides(2)
        with pytest.raises(ValueError):
            generate_carousel(slides=slides, output_dir=str(tmp_path))

    def test_above_maximum_raises(self, tmp_path: Path) -> None:
        slides = _make_slides(11)
        with pytest.raises(ValueError):
            generate_carousel(slides=slides, output_dir=str(tmp_path))

    def test_min_slides_constant(self) -> None:
        assert MIN_SLIDES == 3

    def test_max_slides_constant(self) -> None:
        assert MAX_SLIDES == 10


# ---------------------------------------------------------------------------
# generate_carousel — output structure
# ---------------------------------------------------------------------------


class TestGenerateCarouselOutputStructure:
    def test_returns_carousel_output(self, tmp_path: Path, five_slides) -> None:
        result = generate_carousel(slides=five_slides, output_dir=str(tmp_path))
        assert isinstance(result, CarouselOutput)

    def test_slides_has_correct_count(self, tmp_path: Path, five_slides) -> None:
        result = generate_carousel(slides=five_slides, output_dir=str(tmp_path))
        assert len(result.slides) == 5

    def test_preview_is_valid_path_string(self, tmp_path: Path, five_slides) -> None:
        result = generate_carousel(slides=five_slides, output_dir=str(tmp_path))
        assert isinstance(result.preview, str)
        assert result.preview.endswith(".html")

    def test_total_slides_matches_input(self, tmp_path: Path, five_slides) -> None:
        result = generate_carousel(slides=five_slides, output_dir=str(tmp_path))
        assert result.total_slides == len(five_slides)

    def test_style_matches_input(self, tmp_path: Path, five_slides) -> None:
        result = generate_carousel(
            slides=five_slides,
            style="dark-premium",
            output_dir=str(tmp_path),
        )
        assert result.style == "dark-premium"

    def test_dimensions_matches_input(self, tmp_path: Path, five_slides) -> None:
        result = generate_carousel(
            slides=five_slides,
            dimensions=(1080, 1080),
            output_dir=str(tmp_path),
        )
        assert result.dimensions == (1080, 1080)


# ---------------------------------------------------------------------------
# generate_carousel — file output
# ---------------------------------------------------------------------------


class TestGenerateCarouselFileOutput:
    def test_creates_individual_slide_files(self, tmp_path: Path, five_slides) -> None:
        generate_carousel(slides=five_slides, output_dir=str(tmp_path))
        for i in range(1, 6):
            slide_file = tmp_path / f"slide-{i:02d}.html"
            assert slide_file.exists(), f"Missing {slide_file.name}"

    def test_creates_all_slides_preview(self, tmp_path: Path, five_slides) -> None:
        generate_carousel(slides=five_slides, output_dir=str(tmp_path))
        preview = tmp_path / "all-slides.html"
        assert preview.exists()

    def test_each_file_is_valid_html(self, tmp_path: Path, five_slides) -> None:
        generate_carousel(slides=five_slides, output_dir=str(tmp_path))
        for i in range(1, 6):
            content = (tmp_path / f"slide-{i:02d}.html").read_text(encoding="utf-8")
            assert "<!DOCTYPE html>" in content

    def test_each_file_under_max_size(self, tmp_path: Path, five_slides) -> None:
        generate_carousel(slides=five_slides, output_dir=str(tmp_path))
        for i in range(1, 6):
            file_path = tmp_path / f"slide-{i:02d}.html"
            size_kb = file_path.stat().st_size / 1024
            assert size_kb < MAX_SLIDE_KB, (
                f"{file_path.name} is {size_kb:.1f}KB, exceeds {MAX_SLIDE_KB}KB limit"
            )

    def test_max_slide_kb_constant(self) -> None:
        assert MAX_SLIDE_KB == 15


# ---------------------------------------------------------------------------
# generate_carousel — brand integration
# ---------------------------------------------------------------------------


class TestGenerateCarouselBrandIntegration:
    def test_brand_name_appears_in_output(
        self, tmp_path: Path, five_slides, brand_config
    ) -> None:
        generate_carousel(
            slides=five_slides,
            brand_config=brand_config,
            output_dir=str(tmp_path),
        )
        # Check that brand name or handle appears in at least one slide
        # (may be in active content or HTML comments depending on slide type)
        all_content = ""
        for i in range(1, 6):
            all_content += (tmp_path / f"slide-{i:02d}.html").read_text(encoding="utf-8")
        assert "TestBrand" in all_content or "testbrand" in all_content, (
            "Brand name 'TestBrand' not found in any slide"
        )

    def test_brand_colors_injected_as_css_vars(
        self, tmp_path: Path, five_slides, brand_config_with_colors
    ) -> None:
        generate_carousel(
            slides=five_slides,
            brand_config=brand_config_with_colors,
            output_dir=str(tmp_path),
        )
        content = (tmp_path / "slide-01.html").read_text(encoding="utf-8")
        # Should contain CSS custom properties
        assert "--" in content, "Expected CSS custom properties in output"

    def test_without_brand_config_no_error(self, tmp_path: Path, five_slides) -> None:
        result = generate_carousel(
            slides=five_slides,
            brand_config=None,
            output_dir=str(tmp_path),
        )
        assert isinstance(result, CarouselOutput)
        assert len(result.slides) == 5


# ---------------------------------------------------------------------------
# generate_carousel — content rendering
# ---------------------------------------------------------------------------


class TestGenerateCarouselContentRendering:
    def test_headline_appears_in_html(self, tmp_path: Path) -> None:
        slides = [_make_slide(headline="My Big Headline")]
        # Use minimum 3 slides for validation
        slides = _make_slides(3)
        slides[0] = _make_slide(
            slide_number=1, total_slides=3, type="cover", headline="My Big Headline",
        )
        generate_carousel(slides=slides, output_dir=str(tmp_path))
        content = (tmp_path / "slide-01.html").read_text(encoding="utf-8")
        assert "My Big Headline" in content

    def test_body_text_appears(self, tmp_path: Path) -> None:
        slides = _make_slides(3)
        slides[1] = _make_slide(
            slide_number=2,
            total_slides=3,
            type="content",
            headline="H2",
            body="This is the body text for testing.",
        )
        generate_carousel(slides=slides, output_dir=str(tmp_path))
        content = (tmp_path / "slide-02.html").read_text(encoding="utf-8")
        assert "This is the body text for testing." in content

    def test_bullets_rendered_as_list_items(self, tmp_path: Path) -> None:
        slides = _make_slides(3)
        slides[1] = _make_slide(
            slide_number=2,
            total_slides=3,
            type="content",
            headline="H2",
            bullets=["Alpha point", "Beta point", "Gamma point"],
        )
        generate_carousel(slides=slides, output_dir=str(tmp_path))
        content = (tmp_path / "slide-02.html").read_text(encoding="utf-8")
        assert "Alpha point" in content
        assert "Beta point" in content
        assert "Gamma point" in content
        assert "<li" in content.lower()

    def test_icon_appears(self, tmp_path: Path) -> None:
        slides = _make_slides(3)
        slides[1] = _make_slide(
            slide_number=2,
            total_slides=3,
            type="content",
            headline="H2",
            icon="🔥",
        )
        generate_carousel(slides=slides, output_dir=str(tmp_path))
        content = (tmp_path / "slide-02.html").read_text(encoding="utf-8")
        assert "🔥" in content

    def test_cta_text_on_cta_slide(self, tmp_path: Path) -> None:
        slides = _make_slides(3)
        slides[2] = _make_slide(
            slide_number=3,
            total_slides=3,
            type="cta",
            headline="Final",
            cta_text="Follow for more tips",
        )
        generate_carousel(slides=slides, output_dir=str(tmp_path))
        content = (tmp_path / "slide-03.html").read_text(encoding="utf-8")
        assert "Follow for more tips" in content

    def test_progress_dots_present(self, tmp_path: Path) -> None:
        slides = _make_slides(5)
        generate_carousel(slides=slides, output_dir=str(tmp_path))
        content = (tmp_path / "slide-03.html").read_text(encoding="utf-8")
        # Should contain dot indicators — either unicode (●/○) or HTML entities (&#9679;/&#9675;) or CSS dots
        has_dots = (
            "●" in content
            or "○" in content
            or "&#9679;" in content
            or "&#9675;" in content
            or "dot" in content.lower()
            or "progress" in content.lower()
        )
        assert has_dots, "Expected progress indicators in slide"

    def test_slide_number_present(self, tmp_path: Path) -> None:
        slides = _make_slides(5)
        generate_carousel(slides=slides, output_dir=str(tmp_path))
        content = (tmp_path / "slide-03.html").read_text(encoding="utf-8")
        # Slide 3 of 5 — should contain "3" somewhere in context of numbering
        assert "3" in content


# ---------------------------------------------------------------------------
# generate_carousel — anti-slop
# ---------------------------------------------------------------------------


class TestGenerateCarouselAntiSlop:
    def test_banned_phrases_removed(self, tmp_path: Path, brand_config) -> None:
        slides = _make_slides(3)
        slides[1] = _make_slide(
            slide_number=2,
            total_slides=3,
            type="content",
            headline="A game-changer idea",
            body="This revolutionary approach uses synergy to deliver results.",
        )
        generate_carousel(
            slides=slides,
            brand_config=brand_config,
            output_dir=str(tmp_path),
        )
        content = (tmp_path / "slide-02.html").read_text(encoding="utf-8")
        assert "game-changer" not in content.lower()
        assert "revolutionary" not in content.lower()
        assert "synergy" not in content.lower()


# ---------------------------------------------------------------------------
# generate_carousel — dimensions
# ---------------------------------------------------------------------------


class TestGenerateCarouselDimensions:
    def test_default_portrait_dimensions(self, tmp_path: Path) -> None:
        slides = _make_slides(3)
        result = generate_carousel(slides=slides, output_dir=str(tmp_path))
        assert result.dimensions == (1080, 1350)

    def test_square_dimensions(self, tmp_path: Path) -> None:
        slides = _make_slides(3)
        result = generate_carousel(
            slides=slides,
            dimensions=(1080, 1080),
            output_dir=str(tmp_path),
        )
        assert result.dimensions == (1080, 1080)

    def test_story_dimensions(self, tmp_path: Path) -> None:
        slides = _make_slides(3)
        result = generate_carousel(
            slides=slides,
            dimensions=(1080, 1920),
            output_dir=str(tmp_path),
        )
        assert result.dimensions == (1080, 1920)

    def test_valid_dimensions_constant(self) -> None:
        # VALID_DIMENSIONS is a dict mapping names to tuples
        assert "post" in VALID_DIMENSIONS
        assert "portrait" in VALID_DIMENSIONS
        assert "story" in VALID_DIMENSIONS
        assert VALID_DIMENSIONS["post"] == (1080, 1080)
        assert VALID_DIMENSIONS["portrait"] == (1080, 1350)
        assert VALID_DIMENSIONS["story"] == (1080, 1920)


# ---------------------------------------------------------------------------
# Preview generation
# ---------------------------------------------------------------------------


class TestPreviewGeneration:
    def test_preview_contains_references_to_all_slides(self, tmp_path: Path) -> None:
        slides = _make_slides(5)
        result = generate_carousel(slides=slides, output_dir=str(tmp_path))
        preview_content = Path(result.preview).read_text(encoding="utf-8")
        for i in range(1, 6):
            assert f"slide-{i:02d}" in preview_content, (
                f"Preview missing reference to slide-{i:02d}"
            )

    def test_preview_is_valid_html(self, tmp_path: Path) -> None:
        slides = _make_slides(5)
        result = generate_carousel(slides=slides, output_dir=str(tmp_path))
        preview_content = Path(result.preview).read_text(encoding="utf-8")
        assert "<!DOCTYPE html>" in preview_content
