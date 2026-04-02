"""Landing page HTML generator for GrowthOS.

Produces single-file HTML landing pages with embedded CSS,
zero external dependencies, responsive design, and SEO meta tags.
"""

from pathlib import Path
from typing import Optional

from growthOS_shared.config import BrandVoiceConfig


TEMPLATES_DIR = Path(__file__).parent.parent.parent / "templates" / "landing-pages"
VALID_STYLES = ("minimal", "bold", "gradient")
MAX_OUTPUT_KB = 100


def _load_template(style: str) -> str:
    """Load an HTML template file by style name."""
    if style not in VALID_STYLES:
        raise ValueError(f"Unknown style '{style}'. Choose from: {', '.join(VALID_STYLES)}")
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
            result = result[:idx] + result[idx + len(phrase):]
            lower = result.lower()
            idx = lower.find(phrase.lower())
    return result


def _build_tone_suffix(brand_config: BrandVoiceConfig) -> str:
    """Build a tone descriptor string from brand config."""
    tones = brand_config.brand.tone
    if not tones:
        return ""
    if len(tones) == 1:
        return tones[0]
    return ", ".join(tones[:-1]) + f" & {tones[-1]}"


def generate_landing_page(
    product_name: str,
    description: str,
    style: str = "minimal",
    brand_config: Optional[BrandVoiceConfig] = None,
    *,
    headline: Optional[str] = None,
    cta_text: str = "Get Started",
    cta_url: str = "#",
    features: Optional[list[dict[str, str]]] = None,
    testimonial_text: Optional[str] = None,
    testimonial_author: str = "Happy Customer",
) -> str:
    """Generate a complete single-file HTML landing page.

    Args:
        product_name: The product/brand name.
        description: Short product description (used for hero + meta).
        style: Template style — "minimal", "bold", or "gradient".
        brand_config: Optional BrandVoiceConfig for tone/anti-slop filtering.
        headline: Hero headline. Defaults to product_name.
        cta_text: Call-to-action button text.
        cta_url: CTA link destination.
        features: List of dicts with 'title' and 'desc' keys (up to 4).
        testimonial_text: Social proof quote text.
        testimonial_author: Attribution for the testimonial.

    Returns:
        Complete HTML string ready to save to a file.

    Raises:
        ValueError: If style is unknown or output exceeds 100KB.
    """
    template = _load_template(style)

    if headline is None:
        headline = product_name

    if features is None:
        features = [
            {"title": "Fast", "desc": f"{product_name} delivers results quickly."},
            {"title": "Reliable", "desc": "Built for consistency you can count on."},
            {"title": "Simple", "desc": "No complexity. Just what you need."},
            {"title": "Secure", "desc": "Your data stays yours. Always."},
        ]

    # Pad to 4 features if fewer provided
    while len(features) < 4:
        features.append({"title": "", "desc": ""})

    if testimonial_text is None:
        testimonial_text = f"{product_name} helped us ship faster and with more confidence."

    meta_description = description[:160]
    if brand_config:
        _build_tone_suffix(brand_config)

    replacements = {
        "{{product_name}}": product_name,
        "{{headline}}": headline,
        "{{description}}": description,
        "{{meta_description}}": meta_description,
        "{{cta_text}}": cta_text,
        "{{cta_url}}": cta_url,
        "{{features_heading}}": "Why " + product_name,
        "{{feature_1_title}}": features[0].get("title", ""),
        "{{feature_1_desc}}": features[0].get("desc", ""),
        "{{feature_2_title}}": features[1].get("title", ""),
        "{{feature_2_desc}}": features[1].get("desc", ""),
        "{{feature_3_title}}": features[2].get("title", ""),
        "{{feature_3_desc}}": features[2].get("desc", ""),
        "{{feature_4_title}}": features[3].get("title", ""),
        "{{feature_4_desc}}": features[3].get("desc", ""),
        "{{social_proof_heading}}": "Trusted by Teams",
        "{{testimonial_text}}": testimonial_text,
        "{{testimonial_author}}": testimonial_author,
        "{{cta_heading}}": "Ready to start?",
        "{{cta_description}}": f"Join teams already using {product_name}.",
        "{{footer_text}}": f"\u00a9 2026 {product_name}. All rights reserved.",
    }

    html = template
    for placeholder, value in replacements.items():
        html = html.replace(placeholder, value)

    # Apply anti-slop filtering if brand config provided
    if brand_config:
        html = _apply_anti_slop(html, brand_config)

    # Validate size constraint
    size_kb = len(html.encode("utf-8")) / 1024
    if size_kb > MAX_OUTPUT_KB:
        raise ValueError(
            f"Generated page is {size_kb:.1f}KB, exceeds {MAX_OUTPUT_KB}KB limit."
        )

    return html


def list_available_styles() -> list[str]:
    """Return list of available template style names."""
    return list(VALID_STYLES)
