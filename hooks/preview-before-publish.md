---
name: preview-before-publish
description: PreToolUse guard that intercepts publish actions — shows formatted content preview and requires user confirmation based on autonomy level
hooks:
  - type: PreToolUse
    tool_name: mcp__growthOS-social-publish__publish_post
---

# Preview Before Publish Hook

Fires before any `publish_post` call to the social-publish MCP server. Enforces the autonomy policy from `brand-voice.yaml` by gating real publishes behind user confirmation.

## Logic

1. **Load autonomy config** from `brand-voice.yaml`:
   ```python
   from growthOS_shared.config import load_brand_voice

   config = load_brand_voice()
   autonomy = config.get("autonomy", {})
   level = autonomy.get("level", "manual")  # manual | semi | auto
   ```

2. **Extract call parameters** from the intercepted tool input:
   - `platform` — target platform (twitter, linkedin, reddit, etc.)
   - `content` — the post text
   - `media_urls` — attached media (if any)
   - `dry_run` — whether this is already a dry-run call

3. **Skip if dry_run is True.** Dry-run calls are safe — let them pass without gating (the `dry-run-guard` hook handles dry-run simulation separately).

4. **Format a platform-specific preview** for the user:

   ### Twitter
   ```
   ┌─ 🐦 Twitter Preview ────────────────────────┐
   │ {content}                                     │
   │                                               │
   │ Characters: {len}/280  {⚠️ OVER LIMIT if >280}│
   │ Media: {count} attachment(s)                  │
   └───────────────────────────────────────────────┘
   ```

   ### LinkedIn
   ```
   ┌─ 💼 LinkedIn Preview ───────────────────────┐
   │ {content}                                    │
   │                                              │
   │ Characters: {len}/3000                       │
   │ Hashtags: {extracted hashtags}               │
   │ Media: {count} attachment(s)                 │
   └──────────────────────────────────────────────┘
   ```

   ### Reddit
   ```
   ┌─ 🔶 Reddit Preview ────────────────────────┐
   │ {content}                                    │
   │                                              │
   │ Characters: {len}/10000                      │
   └──────────────────────────────────────────────┘
   ```

   ### Threads
   ```
   ┌─ 🧵 Threads Preview ───────────────────────┐
   │ {content}                                    │
   │                                              │
   │ Characters: {len}/500                        │
   │ Media: {count} attachment(s)                 │
   └──────────────────────────────────────────────┘
   ```

   ### GitHub
   ```
   ┌─ 🐙 GitHub Preview ────────────────────────┐
   │ {content}                                    │
   │                                              │
   │ Characters: {len}                            │
   └──────────────────────────────────────────────┘
   ```

   ### Generic (any other platform)
   ```
   ┌─ 📢 {Platform} Preview ────────────────────┐
   │ {content}                                    │
   │                                              │
   │ Characters: {len}                            │
   │ Media: {count} attachment(s)                 │
   └──────────────────────────────────────────────┘
   ```

5. **Apply autonomy policy:**

   ### `manual` or `semi` — BLOCK and require confirmation
   - Display the formatted preview
   - Show the prompt:
     ```
     ⚠️ Publish to {platform}? (autonomy: {level})
        [Y] Publish now  |  [N] Cancel and save as draft
     ```
   - **On user confirmation (Y):** ALLOW the tool call to proceed
   - **On user decline (N):** BLOCK the tool call and execute the draft-save flow (step 6)

   ### `auto` — LOG and allow
   - Display the formatted preview with header:
     ```
     ℹ️ [AUTO-PUBLISH] Publishing to {platform} (autonomy: auto)
     ```
   - Log the preview to the audit trail:
     ```python
     from growthOS_shared.audit_logger import AuditLogger

     logger = AuditLogger()
     logger.log_action(
         action="preview_before_publish",
         platform=platform,
         content_hash=content_hash,
         user="system",
         status="auto_approved",
         metadata={"autonomy": "auto", "char_count": len(content)},
     )
     ```
   - ALLOW the tool call to proceed

6. **Draft-save on decline:** When the user declines publishing, save the content as a draft in the Obsidian vault:
   ```python
   # Call the obsidian-vault MCP to save as draft
   # Tool: mcp__growthOS-obsidian-vault__save_note
   save_note(
       path="GrowthOS/Drafts/{platform}/{date}-blocked-draft.md",
       content=draft_template,
       metadata={
           "status": "blocked",
           "platform": platform,
           "blocked_at": timestamp,
           "reason": "user_declined_preview",
           "content_hash": content_hash,
       },
   )
   ```

   Draft template:
   ```markdown
   ---
   status: blocked
   platform: {platform}
   blocked_at: {ISO timestamp}
   reason: user_declined_preview
   content_hash: {hash}
   ---

   # Blocked Draft — {platform}

   {original content}

   ---
   *Blocked by preview-before-publish hook. Edit and re-queue when ready.*
   ```

   Confirm to user:
   ```
   📝 Draft saved to GrowthOS/Drafts/{platform}/{date}-blocked-draft.md
      Status: blocked | Re-queue when ready.
   ```

## Platform Character Limits Reference

| Platform     | Max Length | Source                    |
|-------------|-----------|---------------------------|
| Twitter     | 280       | brand-voice.yaml          |
| LinkedIn    | 3000      | brand-voice.yaml          |
| Reddit      | 10000     | brand-voice.yaml          |
| Threads     | 500       | brand-voice.yaml          |
| GitHub      | unlimited | brand-voice.yaml          |
| YouTube     | 5000      | brand-voice.yaml          |
| Instagram   | 2200      | brand-voice.yaml          |

## Edge Cases

- **Missing autonomy config:** Default to `manual` (safest option).
- **Unknown platform:** Use generic preview format, no character limit warning.
- **Content exceeds platform limit:** Show ⚠️ warning in preview but do NOT auto-block — let the user decide.
- **Vault save fails:** Log error to stderr, still BLOCK the publish (safety > convenience).
