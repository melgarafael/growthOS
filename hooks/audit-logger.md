---
name: audit-logger
description: Logs all GrowthOS MCP tool calls to an append-only JSONL audit trail for compliance and traceability
hooks:
  - type: PostToolUse
    tool_name: "mcp__growthOS*"
---

# Audit Logger Hook

Fires after every GrowthOS MCP tool call completes. Records the call to an append-only JSONL audit trail using the shared-lib `AuditLogger`.

## Logic

1. **Capture call metadata** from the tool result:
   - `action` — the full tool name (e.g. `mcp__growthOS__social_publish__post_tweet`)
   - `platform` — extract from tool name segment (e.g. `social_publish`, `social_discover`, `obsidian_vault`)
   - `content_hash` — hash of the content payload if present, empty string otherwise
   - `status` — `"success"` if tool returned normally, `"error"` if it threw/returned an error
   - `duration_ms` — elapsed time of the tool call in milliseconds

2. **Redact sensitive fields** before logging. Any field in the tool input or output whose key matches these patterns MUST be replaced with `"[REDACTED]"`:
   - `*_token`
   - `*_secret`
   - `*_key`
   - `*_password`
   - `authorization`
   - `cookie`

   Note: `content_hash` is NOT redacted — it is a non-reversible hash needed for traceability.

3. **Write the audit entry** using `AuditLogger.log_action()`:
   ```python
   from growthOS_shared.audit_logger import AuditLogger

   logger = AuditLogger()  # uses GROWTHOS_AUDIT_DIR env var
   logger.log_action(
       action=tool_name,
       platform=platform,
       content_hash=content_hash,
       user="system",
       status=status,
       metadata={
           "duration_ms": duration_ms,
           "redacted_fields": list_of_redacted_keys,
       },
   )
   ```

4. **Never block the response.** If logging fails (disk full, permissions), catch the error silently — the audit trail is critical but must not break the user's workflow. Log the logging failure to stderr.

## File Format

Output: daily JSONL files at `$GROWTHOS_AUDIT_DIR/audit-YYYY-MM-DD.jsonl` (default `.growthOS/audit/`).

Each line is a self-contained JSON object:
```json
{"timestamp":"2026-04-01T14:30:00Z","action":"mcp__growthOS__social_publish__post_tweet","platform":"social_publish","content_hash":"a1b2c3","user":"system","status":"success","metadata":{"duration_ms":1200,"redacted_fields":["access_token"]}}
```
