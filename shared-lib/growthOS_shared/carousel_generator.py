"""Instagram carousel HTML generator for GrowthOS.

Produces individual slide HTML files and a preview grid,
with embedded CSS, zero external dependencies, and exact
Instagram dimensions (1080x1350 default).
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

from growthOS_shared.config import BrandVoiceConfig


TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates" / "carousels"
VALID_STYLES = (
    "minimal",
    "bold",
    "gradient",
    "clean-educator",
    "dark-premium",
    "vibrant-creator",
)
VALID_DIMENSIONS = {
    "post": (1080, 1080),
    "portrait": (1080, 1350),
    "story": (1080, 1920),
}
MAX_SLIDE_KB = 15
MAX_SLIDES = 10
MIN_SLIDES = 3


@dataclass
class SlideContent:
    """Content for a single carousel slide."""

    slide_number: int
    total_slides: int
    type: str  # "cover" | "content" | "cta"
    headline: str
    body: str = ""
    icon: str = ""  # emoji
    bullets: list[str] = field(default_factory=list)
    cta_text: str = ""
    cta_action: str = ""


@dataclass
class CarouselOutput:
    """Result of carousel generation."""

    slides: list[str]  # paths of individual slide HTML files
    preview: str  # path of all-slides.html preview
    total_slides: int
    style: str
    dimensions: tuple[int, int]


def _load_template(style: str) -> str:
    """Load an HTML template file by style name."""
    if style not in VALID_STYLES:
        raise ValueError(
            f"Unknown style '{style}'. Choose from: {', '.join(VALID_STYLES)}"
        )
    template_path = TEMPLATES_DIR / f"{style}.html"
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    return template_path.read_text(encoding="utf-8")


def _apply_anti_slop(text: str, brand_config: BrandVoiceConfig) -> str:
    """Remove banned phrases from text based on brand voice anti-slop config."""
    if not brand_config.anti_slop.enabled:
        return text
    all_banned = brand_config.anti_slop.banned_phrases + brand_config.anti_slop.custom_banned
    result = text
    for phrase in all_banned:
        lower = result.lower()
        idx = lower.find(phrase.lower())
        while idx != -1:
            result = result[:idx] + result[idx + len(phrase) :]
            lower = result.lower()
            idx = lower.find(phrase.lower())
    return result


def _generate_progress_dots(current: int, total: int) -> str:
    """Generate progress indicator dots for carousel navigation.

    Returns HTML span elements: filled dot for current slide, empty for others.
    """
    dots = []
    for i in range(1, total + 1):
        if i == current:
            dots.append('<span class="dot dot-active">&#9679;</span>')
        else:
            dots.append('<span class="dot">&#9675;</span>')
    return " ".join(dots)


def _render_bullets(bullets: list[str]) -> str:
    """Render a list of strings as HTML list items."""
    if not bullets:
        return ""
    items = "\n".join(f"        <li>{bullet}</li>" for bullet in bullets)
    return f'<ul class="slide-bullets">\n{items}\n      </ul>'


def _apply_brand_colors(html: str, brand_config: BrandVoiceConfig) -> str:
    """Inject brand colors as CSS custom properties.

    Extracts tone-based colors from brand config and injects them into the
    HTML as CSS custom property overrides in a <style> block.
    """
    tone = brand_config.brand.tone[0] if brand_config.brand.tone else "professional"
    tone_lower = tone.lower()

    color_map = {
        "professional": {"--accent-color": "#2563eb", "--text-primary": "#1a1a2e"},
        "corporate": {"--accent-color": "#1e40af", "--text-primary": "#0f172a"},
        "bold": {"--accent-color": "#dc2626", "--text-primary": "#111827"},
        "disruptive": {"--accent-color": "#f59e0b", "--text-primary": "#111827"},
        "innovative": {"--accent-color": "#8b5cf6", "--text-primary": "#1e1b4b"},
        "modern": {"--accent-color": "#06b6d4", "--text-primary": "#164e63"},
        "casual": {"--accent-color": "#f97316", "--text-primary": "#1c1917"},
        "friendly": {"--accent-color": "#22c55e", "--text-primary": "#14532d"},
        "educational": {"--accent-color": "#3b82f6", "--text-primary": "#1e3a5f"},
        "helpful": {"--accent-color": "#0ea5e9", "--text-primary": "#0c4a6e"},
        "premium": {"--accent-color": "#d4af37", "--text-primary": "#0a0a0a"},
        "luxury": {"--accent-color": "#c9a96e", "--text-primary": "#1a1a1a"},
    }

    overrides = color_map.get(tone_lower, {})
    if not overrides:
        return html

    css_vars = "\n".join(f"      {prop}: {value};" for prop, value in overrides.items())
    style_block = f"\n    <style>\n    :root {{\n{css_vars}\n    }}\n    </style>"

    # Insert before closing </head> tag
    return html.replace("</head>", f"{style_block}\n  </head>")


def _render_slide(
    template: str,
    slide: SlideContent,
    brand_config: Optional[BrandVoiceConfig],
    dimensions: tuple[int, int],
) -> str:
    """Render a single slide by replacing template placeholders."""
    brand_name = ""
    brand_handle = ""
    if brand_config:
        brand_name = brand_config.brand.name
        brand_handle = f"@{brand_name.lower().replace(' ', '')}"

    slide_type_class = f"slide-{slide.type}"

    replacements = {
        "{{headline}}": slide.headline,
        "{{body}}": slide.body,
        "{{icon}}": slide.icon,
        "{{bullets}}": _render_bullets(slide.bullets),
        "{{progress_dots}}": _generate_progress_dots(slide.slide_number, slide.total_slides),
        "{{slide_number}}": str(slide.slide_number),
        "{{total_slides}}": str(slide.total_slides),
        "{{brand_name}}": brand_name,
        "{{brand_handle}}": brand_handle,
        "{{cta_text}}": slide.cta_text,
        "{{cta_action}}": slide.cta_action,
        "{{slide_type_class}}": slide_type_class,
        "{{slide_width}}": str(dimensions[0]),
        "{{slide_height}}": str(dimensions[1]),
    }

    html = template
    for placeholder, value in replacements.items():
        html = html.replace(placeholder, value)

    # Apply brand colors and anti-slop if brand config provided
    if brand_config:
        html = _apply_brand_colors(html, brand_config)
        html = _apply_anti_slop(html, brand_config)

    return html


def _generate_preview(slide_paths: list[str], style: str) -> str:
    """Generate all-slides.html preview with a responsive grid of all slides."""
    iframe_items = []
    for i, path in enumerate(slide_paths, 1):
        filename = Path(path).name
        iframe_items.append(
            f'      <div class="preview-item">\n'
            f'        <div class="preview-label">Slide {i}</div>\n'
            f'        <iframe src="{filename}" class="preview-frame"></iframe>\n'
            f"      </div>"
        )

    iframes_html = "\n".join(iframe_items)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Carousel Preview — {style}</title>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: #f0f0f0;
      padding: 2rem;
    }}
    h1 {{
      text-align: center;
      margin-bottom: 2rem;
      color: #333;
      font-size: 1.5rem;
    }}
    .preview-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
      gap: 1.5rem;
      max-width: 1400px;
      margin: 0 auto;
    }}
    .preview-item {{
      background: #fff;
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}
    .preview-label {{
      padding: 0.5rem 1rem;
      font-weight: 600;
      font-size: 0.85rem;
      color: #666;
      border-bottom: 1px solid #eee;
    }}
    .preview-frame {{
      width: 100%;
      aspect-ratio: 1080 / 1350;
      border: none;
      display: block;
    }}
  </style>
</head>
<body>
  <h1>Carousel Preview &mdash; {style}</h1>
  <div class="preview-grid">
{iframes_html}
  </div>
</body>
</html>"""


def _get_output_dir(output_dir: Optional[str]) -> Path:
    """Resolve or create the output directory for carousel files."""
    if output_dir:
        path = Path(output_dir)
    else:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        path = Path(".growthOS") / "output" / "carousels" / timestamp

    path.mkdir(parents=True, exist_ok=True)
    return path


def generate_carousel(
    slides: list[SlideContent],
    style: str = "clean-educator",
    brand_config: Optional[BrandVoiceConfig] = None,
    dimensions: tuple[int, int] = (1080, 1350),
    output_dir: Optional[str] = None,
) -> CarouselOutput:
    """Generate a complete Instagram carousel as individual HTML slide files.

    Args:
        slides: List of SlideContent dataclasses defining each slide.
        style: Template style name. One of: minimal, bold, gradient,
               clean-educator, dark-premium, vibrant-creator.
        brand_config: Optional BrandVoiceConfig for brand colors and anti-slop.
        dimensions: Slide dimensions as (width, height). Default is portrait 1080x1350.
        output_dir: Output directory path. Defaults to .growthOS/output/carousels/{timestamp}/.

    Returns:
        CarouselOutput with paths to individual slides and preview file.

    Raises:
        ValueError: If style is invalid, slide count is out of range,
                    or a generated slide exceeds the size limit.
        FileNotFoundError: If the template file does not exist.
    """
    # Validate style
    if style not in VALID_STYLES:
        raise ValueError(
            f"Unknown style '{style}'. Choose from: {', '.join(VALID_STYLES)}"
        )

    # Validate slide count
    if len(slides) < MIN_SLIDES:
        raise ValueError(
            f"Carousel requires at least {MIN_SLIDES} slides, got {len(slides)}."
        )
    if len(slides) > MAX_SLIDES:
        raise ValueError(
            f"Carousel allows at most {MAX_SLIDES} slides, got {len(slides)}."
        )

    # Validate dimensions
    if dimensions not in VALID_DIMENSIONS.values():
        valid_dims = ", ".join(f"{k}: {v}" for k, v in VALID_DIMENSIONS.items())
        raise ValueError(
            f"Invalid dimensions {dimensions}. Valid options: {valid_dims}"
        )

    template = _load_template(style)
    out_dir = _get_output_dir(output_dir)

    slide_paths: list[str] = []

    for slide in slides:
        html = _render_slide(template, slide, brand_config, dimensions)

        # Validate size constraint
        size_kb = len(html.encode("utf-8")) / 1024
        if size_kb > MAX_SLIDE_KB:
            raise ValueError(
                f"Slide {slide.slide_number} is {size_kb:.1f}KB, "
                f"exceeds {MAX_SLIDE_KB}KB limit."
            )

        filename = f"slide-{slide.slide_number:02d}.html"
        filepath = out_dir / filename
        filepath.write_text(html, encoding="utf-8")
        slide_paths.append(str(filepath))

    # Generate preview grid
    preview_html = _generate_preview(slide_paths, style)
    preview_path = out_dir / "all-slides.html"
    preview_path.write_text(preview_html, encoding="utf-8")

    return CarouselOutput(
        slides=slide_paths,
        preview=str(preview_path),
        total_slides=len(slides),
        style=style,
        dimensions=dimensions,
    )


def list_carousel_styles() -> list[str]:
    """Return list of available carousel template style names."""
    return list(VALID_STYLES)
