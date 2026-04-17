# Sales Page Pipeline State Schema

This document defines the state object that travels through the 8-phase pipeline. Each phase reads the previous state, adds its output, and passes forward.

## State File Location

During a build, state is persisted at:
```
growthOS/output/sales-pages/{project-slug}/state.json
```

## Schema

```json
{
  "$schema": "sales-page-pipeline-state-v1",
  "project": {
    "slug": "string — unique project identifier",
    "name": "string — human-readable project name",
    "created": "ISO 8601 date",
    "updated": "ISO 8601 date",
    "current_phase": "discovery | research | briefing | visual-design | narrative | fusion | build | qa",
    "status": "in-progress | paused | completed | failed"
  },

  "phase_1_discovery": {
    "status": "pending | in-progress | approved | revision-requested",
    "offer_file": "path to offers/*.md file used or created",
    "offer_source": "existing | new | hybrid",
    "product_name": "string",
    "promise": "string — core transformation promise",
    "deliverables": ["array of deliverable strings"],
    "benefits": {
      "functional": ["array"],
      "emotional": ["array"],
      "social": ["array"]
    },
    "guarantees": {
      "primary": "string",
      "trust_signals": ["array"]
    },
    "audience": {
      "primary_persona": "string",
      "awareness_level": "unaware | problem-aware | solution-aware | product-aware | most-aware",
      "pain_level": "1-10"
    },
    "objections": [
      {"objection": "string", "response": "string"}
    ],
    "competitors": [
      {"name": "string", "their_promise": "string", "our_advantage": "string"}
    ],
    "pricing": {
      "main_price": "string",
      "anchor_price": "string | null",
      "installments": "string | null"
    },
    "usp": "string",
    "social_proof": {
      "testimonials_count": "number",
      "case_studies_count": "number",
      "has_metrics": "boolean",
      "has_media": "boolean"
    },
    "voice_overrides": {
      "tone": "string | null",
      "formality": "string | null",
      "urgency": "low | medium | high"
    },
    "approved_at": "ISO 8601 | null",
    "preview_url": "localhost URL where briefing was shown"
  },

  "phase_2_research": {
    "status": "pending | in-progress | approved | revision-requested",
    "competitor_analysis": [
      {
        "name": "string",
        "url": "string",
        "strengths": ["array"],
        "weaknesses": ["array"],
        "design_notes": "string"
      }
    ],
    "audience_insights": {
      "language_patterns": ["phrases the audience uses"],
      "pain_points_validated": ["array"],
      "desires_validated": ["array"],
      "where_they_hang_out": ["platforms/communities"]
    },
    "reference_sites_selected": ["array of design-intelligence/references/sites/*.md files to use"],
    "patterns_selected": ["array of design-intelligence/references/patterns/*.md patterns to apply"],
    "techniques_selected": ["array of techniques to implement"],
    "approved_at": "ISO 8601 | null",
    "preview_url": "localhost URL where research dashboard was shown"
  },

  "phase_3_briefing": {
    "status": "pending | in-progress | approved | revision-requested",
    "briefing_document": "path to generated briefing HTML",
    "key_decisions": {
      "page_objective": "string — one clear goal",
      "primary_cta": "string — the main action",
      "secondary_cta": "string | null",
      "estimated_sections": "number",
      "target_scroll_depth": "percentage"
    },
    "approved_at": "ISO 8601 | null",
    "preview_url": "localhost URL where briefing was presented"
  },

  "phase_4_visual_design": {
    "status": "pending | in-progress | approved | revision-requested",
    "archetype_selected": "tech-elite | ai-native | clean-authority | cinematic | conversion-machine | builder-maker | luxury-minimal",
    "design_tokens": {
      "colors": {
        "background": "hex",
        "foreground": "hex",
        "accent_primary": "hex",
        "accent_secondary": "hex | null",
        "surface": "hex",
        "muted": "hex"
      },
      "typography": {
        "display_font": "string",
        "body_font": "string",
        "mono_font": "string",
        "scale": "array of clamp() values"
      },
      "spacing": {
        "base": "px value",
        "scale": "array of values",
        "section_gap": "px value"
      },
      "borders": {
        "radius_small": "px",
        "radius_medium": "px",
        "radius_large": "px"
      },
      "motion": {
        "micro": "ms",
        "transition": "ms",
        "reveal": "ms",
        "cinematic": "ms",
        "easing": "cubic-bezier string"
      }
    },
    "hero_pattern": "string — which hero style from references/patterns/hero-sections.md",
    "animation_strategy": "minimal | moderate | cinematic",
    "scroll_technique": "none | css-scroll-driven | canvas-frame-sequence | gsap-scrolltrigger",
    "design_references_used": ["array of reference file paths that justified decisions"],
    "psychology_principles_applied": ["array from theory/ files"],
    "approved_at": "ISO 8601 | null",
    "preview_url": "localhost URL where design system was presented"
  },

  "phase_5_narrative": {
    "status": "pending | in-progress | approved | revision-requested",
    "framework_used": "aida | pas | story-bridge | custom",
    "sections": [
      {
        "id": "string — section identifier",
        "type": "hero | problem | solution | features | social-proof | objection-handler | pricing | cta | faq | guarantee | footer",
        "headline": "string",
        "subheadline": "string | null",
        "body_copy": "string",
        "cta_text": "string | null",
        "cta_action": "string | null",
        "social_proof_element": "string | null",
        "estimated_scroll_position": "percentage"
      }
    ],
    "copywriting_skill_used": "boolean — was growthOS-copywriting invoked",
    "anti_slop_validated": "boolean",
    "voice_alignment_checked": "boolean — checked against GOLDEN-DOC if applicable",
    "approved_at": "ISO 8601 | null",
    "preview_url": "localhost URL where narrative wireframe was shown"
  },

  "phase_6_fusion": {
    "status": "pending | in-progress | approved | revision-requested",
    "mockup_file": "path to fusion mockup HTML",
    "design_narrative_conflicts_resolved": ["array of conflicts and resolutions"],
    "approved_at": "ISO 8601 | null",
    "preview_url": "localhost URL where mockup was presented"
  },

  "phase_7_build": {
    "status": "pending | in-progress | approved | revision-requested",
    "output_file": "path to final HTML file",
    "techniques_implemented": ["array of techniques actually used"],
    "performance": {
      "file_size_kb": "number",
      "estimated_lcp": "ms",
      "estimated_fcp": "ms",
      "lighthouse_score": "number | null"
    },
    "seo": {
      "title_tag": "string",
      "meta_description": "string",
      "og_tags": "boolean",
      "structured_data": "boolean",
      "semantic_html": "boolean"
    },
    "accessibility": {
      "wcag_level": "A | AA | AAA",
      "focus_states": "boolean",
      "alt_texts": "boolean",
      "semantic_headings": "boolean"
    },
    "preview_url": "localhost URL for live page"
  },

  "phase_8_qa": {
    "status": "pending | in-progress | pass | fail | concerns",
    "playwright_tests": {
      "total": "number",
      "passed": "number",
      "failed": "number",
      "report_file": "path"
    },
    "visual_checks": {
      "responsive_tested": ["array of viewports tested"],
      "screenshots": ["array of screenshot paths"],
      "issues_found": ["array of visual issues"]
    },
    "performance_audit": {
      "lighthouse_score": "number",
      "core_web_vitals": {
        "lcp": "ms",
        "fid": "ms",
        "cls": "number"
      }
    },
    "bugs_fixed": "number",
    "final_verdict": "pass | fail | concerns",
    "report_preview_url": "localhost URL where QA report was shown"
  },

  "metadata": {
    "total_phases_completed": "number (0-8)",
    "total_revisions": "number",
    "design_intelligence_files_consulted": ["array of file paths"],
    "skills_invoked": ["array of skill names used"],
    "build_duration_minutes": "number | null"
  }
}
```

## Preview Server Convention

Each phase that presents visual output writes an HTML file to:
```
growthOS/output/sales-pages/{project-slug}/previews/phase-{N}-{phase-name}.html
```

The preview server serves these at:
```
http://localhost:8061/sales-page/{project-slug}/phase/{N}
```

## State Transitions

```
discovery → research → briefing → visual-design → narrative → fusion → build → qa
     ↑           ↑          ↑            ↑             ↑          ↑        ↑
     └───────────┴──────────┴────────────┴─────────────┴──────────┴────────┘
                              (any phase can loop back for revision)
```

Each phase transition requires `status: "approved"` on the previous phase.
Revision resets the phase status to `"revision-requested"` and increments `metadata.total_revisions`.
