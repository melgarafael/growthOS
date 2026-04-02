# A/B Test Plan: [Test Name]

## Metadata

| Field | Value |
|-------|-------|
| **Test ID** | `ABT-[NNN]` |
| **Status** | Draft / Running / Completed / Archived |
| **Created** | [ISO 8601] |
| **Owner** | [name/role] |
| **Page** | [URL or file reference] |
| **Duration** | [start] to [end] |

---

## Hypothesis

**Observation:** [What behavior or metric triggered this test idea]

**Hypothesis statement:** Because we observed `[observation]`, we believe that `[change]` will cause `[expected_outcome]` as measured by `[primary_metric]`.

**Primary metric:** [Single metric that determines success]
**Secondary metrics:** [Supporting metrics to monitor]
**Minimum detectable effect:** [Smallest improvement worth detecting, e.g., 5%]

---

## Variants

### Control

| Field | Value |
|-------|-------|
| **ID** | `control` |
| **File** | `[page-name]-control.html` |
| **Description** | Current version — no changes |

### Variant A

| Field | Value |
|-------|-------|
| **ID** | `variant-a` |
| **File** | `[page-name]-variant-a.html` |
| **Change** | [Specific element changed and how] |
| **Hypothesis** | [Why this specific change should improve the metric] |
| **Expected Impact** | [e.g., +10-15% CTR based on industry benchmarks] |

### Variant B (optional)

| Field | Value |
|-------|-------|
| **ID** | `variant-b` |
| **File** | `[page-name]-variant-b.html` |
| **Change** | [Different change from variant-a] |
| **Hypothesis** | [Reasoning for this variant] |
| **Expected Impact** | [estimated impact] |

---

## Traffic Allocation

| Variant | Allocation |
|---------|-----------|
| Control | 34% |
| Variant A | 33% |
| Variant B | 33% |

**Method:** Equal / Weighted

---

## Success Criteria

```yaml
success_criteria:
  primary_metric: "[metric name]"
  minimum_improvement: "[e.g., 5%]"
  statistical_significance: 0.95
  minimum_sample_per_variant: 100
  minimum_duration_days: 14
```

### Stop Conditions

- Statistical significance reached (p < 0.05)
- Variant clearly losing (>20% worse) — stop early to limit damage
- Duration exceeds 30 days without significance — inconclusive, re-evaluate

---

## Measurement Plan

**Tool:** [GA4 | Plausible | Umami | PostHog]

### Events to Track

| Event | Trigger | Properties |
|-------|---------|------------|
| `page_view` | Page load | `variant`, `source`, `device` |
| `cta_click` | CTA button click | `variant`, `cta_location` |
| `form_submit` | Form submission | `variant`, `form_id` |
| `scroll_depth` | Scroll milestone | `variant`, `depth_percent` |

### Segmentation

- Device type (desktop / mobile / tablet)
- Traffic source (organic / paid / referral / direct)
- New vs. returning visitors

### Reporting Cadence

- [ ] Daily check during first week
- [ ] Weekly summary after stabilization
- [ ] Final report at test conclusion

---

## Results (fill after test completion)

### Raw Data

| Variant | Visitors | Conversions | Rate | Improvement | Significant? |
|---------|----------|-------------|------|-------------|-------------|
| Control | — | — | —% | baseline | — |
| Variant A | — | — | —% | +/- —% | Yes / No |
| Variant B | — | — | —% | +/- —% | Yes / No |

### Decision

**Winner:** [variant-id or inconclusive]
**Action:** [Roll out winner / Iterate / Re-test with changes]
**Learnings:** [What we learned for future tests]

---

## YAML Schema Reference

```yaml
ab_test_plan:
  test_name: "[descriptive-slug]"
  status: "[draft | running | completed | archived]"
  hypothesis:
    observation: "[trigger]"
    change: "[what we're changing]"
    expected_outcome: "[predicted impact]"
    reasoning: "[why we believe this]"
    primary_metric: "[metric]"
    secondary_metrics: []
    minimum_detectable_effect: "[e.g., 5%]"
  control:
    id: "control"
    file: "[page-name]-control.html"
    description: "Current version"
  variants:
    - id: "variant-a"
      change: "[specific change]"
      file: "[page-name]-variant-a.html"
      hypothesis: "[reasoning]"
      expected_impact: "[estimate]"
  traffic_split:
    method: "[equal | weighted]"
    allocation: { control: 34, variant-a: 33, variant-b: 33 }
  duration:
    minimum_days: 14
    minimum_conversions_per_variant: 100
    confidence_level: 0.95
  success_criteria:
    primary_metric: "[metric]"
    minimum_improvement: "[threshold]"
    statistical_significance: 0.95
```
