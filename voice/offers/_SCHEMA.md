# Product/Offer Knowledge Schema

Template for documenting any product or offer. This file is consumed by the Sales Page System during the Discovery phase. If a matching offer file exists, the system loads it and asks the user for confirmation before proceeding.

---

## How to Use

1. Copy this template to `{product-slug}.md` in this directory
2. Fill in all sections (the discovery skill will guide you interactively)
3. The system will load this file automatically in future sales page builds

---

```markdown
---
name: "{Product Name}"
slug: "{product-slug}"
version: 1
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: draft | validated | active
---

# {Product Name}

## Promise
<!-- What transformation does this product deliver? One sentence. -->
**Core Promise:** 

<!-- What is the before/after? -->
**Before:** 
**After:** 

## Deliverables
<!-- What exactly does the person receive? Be specific. -->

### Core Deliverables
- [ ] 

### Bonus / Additional
- [ ] 

### Access Details
- **Format:** [course | community | software | service | hybrid]
- **Duration:** [lifetime | X months | subscription]
- **Platform:** 

## Benefits
<!-- What changes in their life? Think functional, emotional, social. -->

### Functional Benefits (what it does)
- 

### Emotional Benefits (how it makes them feel)
- 

### Social Benefits (how others perceive them)
- 

## Guarantees
<!-- What reduces perceived risk? -->

### Primary Guarantee
- **Type:** [money-back | trial | result-guarantee | satisfaction]
- **Duration:** 
- **Conditions:** 

### Secondary Trust Signals
- 

## Target Audience

### Primary Persona
- **Who:** 
- **Age Range:** 
- **Pain Level:** [1-10]
- **Awareness Level:** [unaware | problem-aware | solution-aware | product-aware | most-aware]
- **Budget Sensitivity:** [low | medium | high]

### Secondary Persona
- **Who:** 
- **Difference from primary:** 

## Objections
<!-- What stops people from buying? List the top objections and how to handle each. -->

| # | Objection | Response Strategy |
|---|-----------|-------------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

## Competitors
<!-- Who/what are they comparing you to? -->

| Competitor | Their Promise | Our Advantage |
|-----------|---------------|---------------|
| | | |

## Pricing
- **Main Price:** 
- **Installments:** 
- **Anchor Price:** [optional — "was $X, now $Y"]
- **Payment Methods:** 

## USP (Unique Selling Proposition)
<!-- Why should they buy THIS, from YOU, RIGHT NOW? -->
**In one sentence:** 

## Social Proof Available
- [ ] Testimonials (count: )
- [ ] Case studies (count: )
- [ ] Media mentions
- [ ] Certifications
- [ ] User count / metrics
- [ ] Before/after results

## Voice & Tone for This Product
<!-- Override brand defaults if needed -->
- **Tone:** [same as brand | override: ...]
- **Formality:** [casual | professional | mix]
- **Urgency Level:** [low | medium | high]

## Notes
<!-- Anything else the sales page should know -->

```
