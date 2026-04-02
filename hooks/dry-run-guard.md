---
name: dry-run-guard
description: PreToolUse guard that intercepts ALL external MCP calls when dry-run mode is active — simulates execution without real API calls
hooks:
  - type: PreToolUse
    tool_name: mcp__growthOS-social-publish__*
  - type: PreToolUse
    tool_name: mcp__growthOS-social-discover__*
  - type: PreToolUse
    tool_name: mcp__growthOS-obsidian-vault__*
---

# Dry Run Guard Hook

Fires before any GrowthOS MCP tool call. When dry-run mode is active, intercepts ALL external calls — simulates the operation, logs what would happen, and returns a synthetic result without making real API calls.

## Activation Conditions

Dry-run mode is active when **either** condition is true:

1. **Config-based:** `dry_run_default: true` in `brand-voice.yaml` → `autonomy.dry_run_default`
2. **Parameter-based:** The tool call includes `dry_run: true` as an explicit argument

```python
from growthOS_shared.config import load_brand_voice

config = load_brand_voice()
config_dry_run = config.get("autonomy", {}).get("dry_run_default", False)

# Check both config and explicit parameter
tool_dry_run = tool_input.get("dry_run", False)
is_dry_run = config_dry_run or tool_dry_run
```

If neither condition is met, **allow the call through unchanged**.

## Logic

1. **Check activation** — evaluate `is_dry_run` as defined above.

2. **If not dry-run:** ALLOW the tool call to proceed. Exit hook.

3. **If dry-run is active:** BLOCK the real API call and:

   a. **Identify the MCP server** from the tool name:
      - `mcp__growthOS-social-publish__*` → server: `social-publish`
      - `mcp__growthOS-social-discover__*` → server: `social-discover`
      - `mcp__growthOS-obsidian-vault__*` → server: `obsidian-vault`

   b. **Log the simulated call** with `[DRY RUN]` prefix:
      ```
      [DRY RUN] Would call: {tool_name}
      [DRY RUN] Server: {server}
      [DRY RUN] Parameters:
        - platform: {platform}
        - content: {content[:100]}...
        - media_urls: {media_urls}
      [DRY RUN] Result: Simulated success (no API call made)
      ```

   c. **Generate a synthetic response** that mimics the real tool's return shape:

      ### social-publish tools
      ```json
      {
        "status": "dry_run",
        "platform": "{platform}",
        "message": "[DRY RUN] Post simulated — no content was published",
        "simulated_id": "dry-run-{timestamp}",
        "content_hash": "{hash}",
        "char_count": {len},
        "would_publish": true
      }
      ```

      ### social-discover tools
      ```json
      {
        "status": "dry_run",
        "message": "[DRY RUN] Discovery simulated — no external API was called",
        "simulated_results": [],
        "query": "{original query}"
      }
      ```

      ### obsidian-vault tools
      ```json
      {
        "status": "dry_run",
        "message": "[DRY RUN] Vault operation simulated — no files were written",
        "path": "{target path}",
        "operation": "{tool_name}"
      }
      ```

   d. **Write to audit trail** for traceability:
      ```python
      from growthOS_shared.audit_logger import AuditLogger

      logger = AuditLogger()
      logger.log_action(
          action=tool_name,
          platform=platform or "system",
          content_hash=content_hash if content else "",
          user="system",
          status="dry_run",
          metadata={
              "dry_run_source": "config" if config_dry_run else "parameter",
              "simulated": True,
              "original_params": sanitized_params,
          },
      )
      ```

   e. **Return the synthetic response** to the caller instead of the real tool result.

## Output Format

All dry-run output MUST be prefixed with `[DRY RUN]` for clear visual distinction:

```
[DRY RUN] ─────────────────────────────────────────
  Tool:     mcp__growthOS-social-publish__publish_post
  Server:   social-publish
  Platform: twitter
  Content:  "Excited to announce our new feature..."
  Length:   142/280 chars
  Media:    0 attachments
  Result:   ✅ Simulated success (no API call made)
────────────────────────────────────────────────────
```

## Interaction with Other Hooks

- **preview-before-publish:** The preview hook checks `dry_run` and skips gating for dry-run calls. The dry-run-guard handles simulation independently. If both fire, dry-run-guard takes precedence (blocks the call before preview can gate it).
- **audit-logger:** The PostToolUse audit-logger will NOT fire for blocked calls because the tool never executes. The dry-run-guard writes its own audit entry to maintain the trail.
- **circuit-breaker:** Dry-run calls do not affect circuit breaker state — no real failures can occur.

## Edge Cases

- **Missing brand-voice.yaml:** Default to `dry_run_default: false` — only honor explicit `dry_run: true` parameter.
- **Nested tool calls:** If a dry-run tool call triggers another MCP call internally, the guard catches that too (each MCP call fires its own PreToolUse event).
- **Vault writes during dry-run:** Even `obsidian-vault` writes are simulated. The draft-save from `preview-before-publish` is an exception — that hook calls the vault directly and handles its own dry-run logic.
- **Parameter sanitization:** Before logging `original_params`, redact any field matching `*_token`, `*_secret`, `*_key`, `*_password`, `authorization`, `cookie` (same rules as audit-logger).
