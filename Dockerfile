# GrowthOS — Multi-stage Docker build for MCP servers
# Each target produces a minimal image for one MCP server

# ─── Base stage: shared dependencies ───────────────────────
FROM python:3.11-slim AS base

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r growthos && useradd -r -g growthos -d /app -s /sbin/nologin growthos

# Install shared library first (changes less often)
COPY shared-lib/ shared-lib/
COPY pyproject.toml .
RUN pip install --no-cache-dir -e shared-lib/

# ─── MCP Social Publish ───────────────────────────────────
FROM base AS mcp-social-publish

COPY mcp-servers/mcp-social-publish/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY --chown=growthos:growthos mcp-servers/mcp-social-publish/ mcp-servers/mcp-social-publish/

USER growthos
EXPOSE 8001

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8001/health || exit 1

CMD ["python", "-m", "mcp-servers.mcp-social-publish.server"]

# ─── MCP Social Discover ──────────────────────────────────
FROM base AS mcp-social-discover

COPY mcp-servers/mcp-social-discover/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY --chown=growthos:growthos mcp-servers/mcp-social-discover/ mcp-servers/mcp-social-discover/

USER growthos
EXPOSE 8002

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8002/health || exit 1

CMD ["python", "-m", "mcp-servers.mcp-social-discover.server"]

# ─── MCP Obsidian Vault ───────────────────────────────────
FROM base AS mcp-obsidian-vault

COPY mcp-servers/mcp-obsidian-vault/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY --chown=growthos:growthos mcp-servers/mcp-obsidian-vault/ mcp-servers/mcp-obsidian-vault/

USER growthos
EXPOSE 8003

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8003/health || exit 1

CMD ["python", "-m", "mcp-servers.mcp-obsidian-vault.server"]
