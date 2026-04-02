# Analytics Tracking Plan: [Project Name]

## Metadata

| Field | Value |
|-------|-------|
| **Version** | 1.0 |
| **Last Updated** | [ISO 8601] |
| **Analytics Tool** | GA4 / Plausible / Umami |
| **Product Type** | SaaS / Ecommerce / Content / Marketplace |
| **Privacy Requirements** | GDPR / CCPA / None |

---

## KPIs

| KPI | Definition | Target | Events Used | Dashboard |
|-----|-----------|--------|-------------|-----------|
| [KPI name] | [How it's calculated] | [Target + timeframe] | [event_1, event_2] | [location] |
| [KPI name] | [How it's calculated] | [Target + timeframe] | [event_1] | [location] |

---

## Event Taxonomy

### Naming Convention

- All event names use `snake_case`
- Format: `[category]_[action]` (e.g., `cta_click`, `form_submit`, `page_scroll`)
- Categories: `engagement`, `conversion`, `navigation`, `error`

### Events

#### Conversion Events

| Event | Description | Trigger | Category | Properties | KPI |
|-------|------------|---------|----------|------------|-----|
| `signup_complete` | User completes registration | Form submit success | conversion | `method`, `source` | Signup Rate |
| `cta_click` | Primary CTA clicked | Button click | conversion | `location`, `variant`, `cta_text` | CTR |
| `purchase_complete` | Transaction finished | Payment success | conversion | `value`, `currency`, `items` | Revenue |

#### Engagement Events

| Event | Description | Trigger | Category | Properties | KPI |
|-------|------------|---------|----------|------------|-----|
| `page_view` | Page loaded | Page load | engagement | `page_path`, `referrer`, `device_type` | Traffic |
| `scroll_depth` | Scroll milestone reached | Scroll 25/50/75/100% | engagement | `depth_percent`, `page_path` | Engagement |
| `time_on_page` | Engagement timer | 30s, 60s, 120s milestones | engagement | `duration_seconds`, `page_path` | Time on Site |
| `video_play` | Video started | Play button click | engagement | `video_id`, `video_title` | Video Engagement |

#### Navigation Events

| Event | Description | Trigger | Category | Properties | KPI |
|-------|------------|---------|----------|------------|-----|
| `nav_click` | Navigation link clicked | Link click | navigation | `destination`, `nav_section` | — |
| `search_performed` | Site search used | Search submit | navigation | `query`, `results_count` | Search Usage |
| `outbound_click` | External link clicked | Link click | navigation | `url`, `link_text` | — |

#### Error Events

| Event | Description | Trigger | Category | Properties | KPI |
|-------|------------|---------|----------|------------|-----|
| `form_error` | Form validation failed | Submit with errors | error | `form_id`, `error_field`, `error_type` | Error Rate |
| `page_error` | Page failed to load | Error response | error | `status_code`, `page_path` | Uptime |

---

## Global Properties

### Sent with every event

| Property | Type | Description |
|----------|------|-------------|
| `page_path` | string | URL path of the current page |
| `referrer` | string | Traffic source |
| `device_type` | string | `desktop` / `mobile` / `tablet` |
| `utm_source` | string | Campaign source (from URL params) |
| `utm_medium` | string | Campaign medium |
| `utm_campaign` | string | Campaign name |

### User Properties (when authenticated)

| Property | Type | Description |
|----------|------|-------------|
| `user_id` | string | Hashed user identifier |
| `user_segment` | string | Segment classification |
| `account_age_days` | number | Days since registration |

---

## Implementation Snippets

### Google Analytics 4

```html
<!-- GA4 Base -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');

  // Track custom event
  function trackEvent(name, params) {
    gtag('event', name, params);
  }

  // Example: CTA click
  document.querySelector('[data-track="cta_click"]').addEventListener('click', function() {
    trackEvent('cta_click', {
      location: this.dataset.trackLocation || 'unknown',
      variant: this.dataset.trackVariant || 'default'
    });
  });
</script>
```

### Plausible Analytics

```html
<!-- Plausible (privacy-friendly, no cookies) -->
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.js"></script>
<script>
  // Track custom event
  function trackEvent(name, props) {
    plausible(name, {props: props});
  }

  // Example: CTA click
  document.querySelector('[data-track="cta_click"]').addEventListener('click', function() {
    trackEvent('cta_click', {
      location: this.dataset.trackLocation || 'unknown'
    });
  });
</script>
```

### Umami Analytics

```html
<!-- Umami (self-hosted, GDPR-compliant) -->
<script async src="https://your-umami.com/script.js" data-website-id="YOUR-WEBSITE-ID"></script>
<script>
  // Track custom event
  function trackEvent(name, data) {
    umami.track(name, data);
  }

  // Example: CTA click
  document.querySelector('[data-track="cta_click"]').addEventListener('click', function() {
    trackEvent('cta_click', {
      location: this.dataset.trackLocation || 'unknown'
    });
  });
</script>
```

### Data Attribute Pattern

```html
<!-- Use data-track attributes for declarative tracking -->
<button data-track="cta_click" data-track-location="hero" data-track-variant="primary">
  Get Started
</button>

<form data-track="form_submit" data-track-form="signup">
  <!-- fields -->
</form>

<section data-track-scroll="features" data-track-threshold="50">
  <!-- content -->
</section>
```

### Universal Tracker (auto-binds data-track elements)

```javascript
// Auto-bind all data-track elements
document.querySelectorAll('[data-track]').forEach(function(el) {
  var eventName = el.dataset.track;
  var eventType = el.tagName === 'FORM' ? 'submit' : 'click';

  el.addEventListener(eventType, function(e) {
    var props = {};
    for (var key in this.dataset) {
      if (key.startsWith('track') && key !== 'track') {
        props[key.replace('track', '').toLowerCase()] = this.dataset[key];
      }
    }
    trackEvent(eventName, props);
  });
});
```

---

## Validation Checklist

- [ ] All conversion events have corresponding KPIs
- [ ] Event names follow `snake_case` convention
- [ ] All properties have types and descriptions
- [ ] Implementation snippet matches chosen analytics tool
- [ ] Privacy requirements addressed (consent banner if GDPR/CCPA)
- [ ] No PII (personally identifiable information) in event properties
- [ ] Scroll depth tracking configured for key pages
- [ ] UTM parameter capture implemented
- [ ] Error events configured for forms and page loads
- [ ] Events tested in development before deploy

---

## YAML Schema Reference

```yaml
tracking_plan:
  project: "[project name]"
  version: "1.0"
  last_updated: "[ISO 8601]"
  analytics_tool: "[GA4 | Plausible | Umami]"
  events:
    - name: "[event_name]"
      description: "[what this captures]"
      trigger: "[user action]"
      category: "[engagement | conversion | navigation | error]"
      properties:
        - name: "[property_name]"
          type: "[string | number | boolean]"
          description: "[what it captures]"
          required: true
          example: "[sample value]"
      kpi_contribution: "[which KPI]"
  properties:
    global:
      - name: string
        type: string
        description: string
    user:
      - name: string
        type: string
        description: string
  kpis:
    - name: "[KPI name]"
      definition: "[calculation]"
      target: "[target + timeframe]"
      events_used: "[events]"
      dashboard_location: "[where to find]"
  implementation_snippets:
    GA4: "[snippet]"
    Plausible: "[snippet]"
    Umami: "[snippet]"
```
