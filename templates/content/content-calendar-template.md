---
title: ""
scheduled_date: 2026-01-01
platform: linkedin
content_type: social
status: draft
author: ""
tags: []
---

# {{title}}

## Content

_Write your content here._

## Notes

- **Platform:** {{platform}}
- **Scheduled:** {{scheduled_date}}
- **Type:** {{content_type}}

## Dataview Queries

### All scheduled content
```dataview
TABLE scheduled_date, platform, status, content_type
FROM "content-calendar"
WHERE status = "scheduled"
SORT scheduled_date ASC
```

### Failed items needing attention
```dataview
TABLE scheduled_date, platform, status
FROM "content-calendar"
WHERE status = "failed"
SORT scheduled_date ASC
```

### Content by platform
```dataview
TABLE scheduled_date, status, content_type
FROM "content-calendar"
WHERE platform = "linkedin"
SORT scheduled_date ASC
```

### This week's calendar
```dataview
TABLE scheduled_date, platform, status, content_type
FROM "content-calendar"
WHERE scheduled_date >= date(today) AND scheduled_date <= date(today) + dur(7 days)
SORT scheduled_date ASC
```

---

## Frontmatter Field Reference

| Field            | Type     | Values                                              | Dataview filterable |
|------------------|----------|-----------------------------------------------------|---------------------|
| `title`          | string   | Free text                                           | Yes                 |
| `scheduled_date` | date     | `YYYY-MM-DD` or `YYYY-MM-DDTHH:MM`                 | Yes                 |
| `platform`       | string   | `linkedin`, `twitter`, `reddit`, `instagram`, etc.  | Yes                 |
| `content_type`   | string   | `social`, `article`, `carousel`, `thread`, `video`  | Yes                 |
| `status`         | string   | `draft`, `scheduled`, `publishing`, `published`, `failed` | Yes           |
| `author`         | string   | Free text                                           | Yes                 |
| `tags`           | list     | YAML list of strings                                | Yes                 |
