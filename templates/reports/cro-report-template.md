# CRO Report: [Page/Funnel Name]

## Metadata

| Field | Value |
|-------|-------|
| **Report ID** | `CRO-[NNN]` |
| **Analysis Date** | [ISO 8601] |
| **Analyst** | Growth Engineer |
| **Page/Funnel** | [URL or funnel name] |
| **Funnel Goal** | [Ultimate conversion action] |
| **Baseline Conversion Rate** | [current rate or unknown] |

---

## Executive Summary

[2-3 sentences: what was analyzed, key findings, and the expected impact of top recommendations]

---

## Funnel Definition

### Stages

| # | Stage | Description | URL Pattern | Success Action |
|---|-------|------------|-------------|----------------|
| 1 | [name] | [description] | [url] | [action to proceed] |
| 2 | [name] | [description] | [url] | [action to proceed] |
| 3 | [name] | [description] | [url] | [action to proceed] |
| 4 | [name] | [description] | [url] | [final conversion] |

### Funnel Visualization

```
[Stage 1] ──── [Stage 2] ──── [Stage 3] ──── [Stage 4]
  100%           ??%            ??%            ??%
         -??%           -??%           -??%
```

---

## Drop-Off Analysis

### Stage Metrics

| Stage | Traffic | Conv. to Next | Drop-Off Rate | Severity |
|-------|---------|--------------|---------------|----------|
| [Stage 1] | [n] | [%] | [%] | [critical/high/medium/low] |
| [Stage 2] | [n] | [%] | [%] | [critical/high/medium/low] |
| [Stage 3] | [n] | [%] | [%] | [critical/high/medium/low] |

**Severity thresholds:** >80% = Critical | 60-80% = High | 40-60% = Medium | <40% = Low

### Identified Drop-Off Causes

#### [Stage A] to [Stage B] — [drop-off %] drop-off ([severity])

| # | Cause | Evidence | Affected Segment |
|---|-------|----------|-----------------|
| 1 | [friction point] | [data or heuristic] | [all / mobile / new users] |
| 2 | [friction point] | [data or heuristic] | [segment] |

#### [Stage B] to [Stage C] — [drop-off %] drop-off ([severity])

| # | Cause | Evidence | Affected Segment |
|---|-------|----------|-----------------|
| 1 | [friction point] | [data or heuristic] | [segment] |

---

## CRO Audit Checklist

### Above the Fold
- [ ] Clear value proposition visible immediately
- [ ] Single primary CTA (no competing actions)
- [ ] CTA visible without scrolling
- [ ] Headline is benefit-focused

### Trust & Proof
- [ ] Social proof present and specific
- [ ] Risk reversal stated
- [ ] Trust badges or security indicators present

### Content & Copy
- [ ] Copy is scannable (short paragraphs, bullets)
- [ ] Benefits > features ratio
- [ ] Anti-slop compliant
- [ ] Urgency/scarcity used appropriately

### Technical Performance
- [ ] Page loads in <2s (LCP)
- [ ] No layout shifts (CLS < 0.1)
- [ ] Mobile responsive and thumb-friendly
- [ ] Images optimized

### Conversion Architecture
- [ ] Single clear conversion path
- [ ] Form fields minimized
- [ ] Error states are helpful
- [ ] Success state confirms action

---

## Recommendations (ICE-Scored)

### ICE Scoring Reference

| Score | Impact | Confidence | Ease |
|-------|--------|------------|------|
| 10 | Transforms the metric | Proven by data/research | Minutes to implement |
| 7-9 | Major improvement | Strong evidence | Hours to implement |
| 4-6 | Moderate improvement | Some evidence | Days to implement |
| 1-3 | Minor improvement | Gut feeling | Weeks to implement |

**Formula:** ICE Total = Impact x Confidence x Ease (max 1000)

### Priority Recommendations (Top 5, sorted by ICE)

#### #1: [Title] — ICE: [total]

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Impact** | [1-10] | [why this score] |
| **Confidence** | [1-10] | [evidence level] |
| **Ease** | [1-10] | [implementation effort] |
| **ICE Total** | **[I x C x E]** | |

- **Stage:** [which funnel stage]
- **Drop-off cause:** [which identified cause]
- **Change:** [specific change to implement]
- **Expected improvement:** [e.g., +15% conversion at this stage]
- **Test plan:** [how to validate — usually A/B test]

---

#### #2: [Title] — ICE: [total]

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| **Impact** | [1-10] | [why] |
| **Confidence** | [1-10] | [evidence] |
| **Ease** | [1-10] | [effort] |
| **ICE Total** | **[I x C x E]** | |

- **Stage:** [stage]
- **Drop-off cause:** [cause]
- **Change:** [change]
- **Expected improvement:** [estimate]
- **Test plan:** [validation approach]

---

#### #3-5: [Repeat pattern above]

---

## Action Plan

### Quick Wins (ICE Ease >= 8)

| # | Recommendation | ICE Total | Next Step | Owner | Deadline |
|---|---------------|-----------|-----------|-------|----------|
| 1 | [title] | [score] | [action] | [who] | [when] |

### Test Queue (requires A/B testing)

| # | Recommendation | ICE Total | Test Design | Est. Duration |
|---|---------------|-----------|-------------|---------------|
| 1 | [title] | [score] | [control vs variant] | [days] |

### Backlog (lower priority)

| # | Recommendation | ICE Total | Reason for Deferral |
|---|---------------|-----------|-------------------|
| 1 | [title] | [score] | [why not now] |

---

## Success Metrics

| Metric | Baseline | Target | Measurement Period |
|--------|----------|--------|-------------------|
| Overall funnel conversion | [current] | [target] | [timeframe] |
| [Stage X] conversion | [current] | [target] | [timeframe] |
| [Key metric] | [current] | [target] | [timeframe] |

---

## YAML Schema Reference

```yaml
funnel_analysis:
  funnel_name: "[name]"
  analysis_date: "[ISO 8601]"
  total_entry_traffic: "[number]"
  stages:
    - name: "[stage name]"
      traffic: "[visitors]"
      conversion_to_next: "[percentage]"
      drop_off_rate: "[percentage]"
  drop_offs:
    - stage_transition: "[Stage A -> Stage B]"
      drop_off_rate: "[percentage]"
      severity: "[critical | high | medium | low]"
      identified_causes:
        - cause: "[friction point]"
          evidence: "[data or heuristic]"
          affected_segment: "[all | mobile | new_users]"
  recommendations:
    - id: "REC-001"
      title: "[title]"
      stage: "[funnel stage]"
      drop_off_cause: "[cause]"
      change_description: "[what to change]"
      ice_score:
        impact: "[1-10]"
        confidence: "[1-10]"
        ease: "[1-10]"
        total: "[I x C x E]"
      expected_improvement: "[estimate]"
      implementation_effort: "[hours/days]"
      test_plan: "[validation approach]"
  action_plan:
    quick_wins: []
    test_queue: []
    backlog: []
  success_metrics:
    - metric: "[name]"
      baseline: "[current]"
      target: "[goal]"
      measurement_period: "[timeframe]"
```
