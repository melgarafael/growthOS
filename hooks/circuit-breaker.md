---
name: circuit-breaker
description: Implements circuit breaker pattern for GrowthOS MCP tool calls — prevents cascading failures by temporarily blocking calls to failing services
hooks:
  - type: PostToolUse
    tool_name: "mcp__growthOS*"
---

# Circuit Breaker Hook

Fires after every GrowthOS MCP tool call. Tracks failures per MCP tool and opens the circuit when a service is consistently failing, preventing cascading failures and wasted API calls.

## State Machine

Uses the shared-lib `CircuitBreaker` with per-tool instances:

```
CLOSED  ──(3 consecutive failures)──▸  OPEN
OPEN    ──(after 60s timeout)───────▸  HALF_OPEN
HALF_OPEN ──(1 success)─────────────▸  CLOSED
HALF_OPEN ──(1 failure)─────────────▸  OPEN
```

## Logic

1. **Identify the MCP tool** from the tool call name (e.g. `mcp__growthOS__social_publish__post_tweet`). Group by MCP server prefix:
   - `mcp__growthOS__social_publish__*` → breaker key: `social_publish`
   - `mcp__growthOS__social_discover__*` → breaker key: `social_discover`
   - `mcp__growthOS__obsidian_vault__*` → breaker key: `obsidian_vault`

2. **Check circuit state** before allowing the call result to propagate:
   - If circuit is **OPEN**: return a clear error message instead of attempting the call:
     ```
     ⚠️ Service temporarily unavailable. Circuit breaker active for [breaker_key]. Retry after [remaining_seconds]s.
     ```
   - If circuit is **HALF_OPEN**: allow the probe call through (max 1).

3. **Record outcome** after the tool call:
   - **Success** → call `circuit_breaker._on_success()` to reset failure count
   - **Failure/Error** → call `circuit_breaker._on_failure()` to increment failure count

4. **Configuration** (from shared-lib defaults):
   ```python
   from growthOS_shared.circuit_breaker import CircuitBreaker

   # One breaker per MCP server
   breakers = {
       "social_publish": CircuitBreaker(failure_threshold=3, recovery_timeout=60, half_open_max=1),
       "social_discover": CircuitBreaker(failure_threshold=3, recovery_timeout=60, half_open_max=1),
       "obsidian_vault": CircuitBreaker(failure_threshold=3, recovery_timeout=60, half_open_max=1),
   }
   ```

5. **State persistence**: Circuit state is in-memory per session. A fresh Claude Code session starts with all circuits CLOSED. This is intentional — transient failures should not persist across sessions.

## Error Messages

When circuit is OPEN, provide actionable feedback:

```
⚠️ Circuit breaker OPEN for social_publish (3 consecutive failures).
   Last failure: 45s ago. Will allow retry in 15s.
   Tip: Check API credentials and rate limits for this service.
```

When circuit transitions to HALF_OPEN:

```
ℹ️ Circuit breaker for social_publish entering HALF_OPEN — allowing 1 probe call.
```

When probe succeeds and circuit closes:

```
✅ Circuit breaker for social_publish CLOSED — service recovered.
```
