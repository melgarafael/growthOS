# GrowthOS Scripts

Utilitários locais que compõem o pipeline de conteúdo. Todos rodam no seu Mac, sem cloud.

## `export-carousel.mjs` — HTML → PNG exporter

Abre um arquivo `carousels-vN.html`, captura cada `.slide` em PNG 1080×1080 retina.

```bash
node growthOS/scripts/export-carousel.mjs growthOS/design-system/carousels-v3.html

# Exporta só 1 carrossel específico:
node growthOS/scripts/export-carousel.mjs growthOS/design-system/carousels-v3.html --carousel c04

# Custom output directory:
node growthOS/scripts/export-carousel.mjs growthOS/design-system/carousels-v3.html --out /tmp/test
```

**Dependência:** Playwright (`npm install playwright` ou reuse do MCP).
**Output:** `growthOS/output/carousels/{stem}/{cid}/slides/{cid}-sNN.png`

## `asset-indexer.py` — Asset library indexer (com Claude Vision)

Indexa assets dropados em `growthOS/assets/{logos,screenshots,icons,photos}/`. Extrai paleta via Pillow e **chama Claude Vision** pra gerar análise semântica (o que o asset mostra, onde usar, brand fit score).

```bash
# Indexa 1 arquivo (roda vision se ANTHROPIC_API_KEY tiver setado)
.venv/bin/python growthOS/scripts/asset-indexer.py growthOS/assets/logos/openclaw.png

# Sem vision (só paleta + tags)
.venv/bin/python growthOS/scripts/asset-indexer.py growthOS/assets/logos/openclaw.png --no-vision

# Reindexa tudo (só arquivos novos passam por vision — cache via sha256)
.venv/bin/python growthOS/scripts/asset-indexer.py --reindex

# Force re-vision mesmo arquivos cached
.venv/bin/python growthOS/scripts/asset-vision.py --all --force
```

**Output:** sidecar `.meta.yaml` em `assets/_meta/` com os blocos:
- `asset/path/type/tags/palette/voice_fit` (extraídos local)
- `vision:` — bloco semântico gerado por Claude:
  - `subject`, `visual_type`, `dominant_elements`, `mood`
  - `brand_fit_score` (0-1), `brand_fit_reason`
  - `best_placement[]` — `{slide_type, position, size, reason}`
  - `suggested_topics[]`, `do_not_use_when[]`
  - `contrast_considerations`, `text_overlay_ok`, `crop_hint`, `accessibility_alt`
  - `_cached_hash` (sha256) + `_model` + `_analyzed_at`

## `asset-vision.py` — Claude Vision analysis (standalone)

Módulo dedicado que analisa 1 asset (ou todos) e devolve análise semântica via Claude Vision.

```bash
# 1 asset
.venv/bin/python growthOS/scripts/asset-vision.py growthOS/assets/logos/openclaw.png

# Todos os assets que não têm vision ainda
.venv/bin/python growthOS/scripts/asset-vision.py --all

# Re-analisa tudo mesmo cached
.venv/bin/python growthOS/scripts/asset-vision.py --all --force
```

**Requer:** `ANTHROPIC_API_KEY` via env OR `~/.growthos/claude.env` (formato `KEY=value`).
**Modelo:** `claude-sonnet-4-5` (configurável via env `GROWTHOS_VISION_MODEL`).
**SVGs:** renderizados pra PNG via `cairosvg` se instalado (`.venv/bin/pip install cairosvg`). Senão são puladas com warning.
**Custo:** ~$0.005-0.010 por asset. Negligível.

## `organize-approved.py` — Approved organizer

Move PNGs + gera metadata + atualiza APPROVED.md quando um carrossel é aprovado.

```bash
python growthOS/scripts/organize-approved.py --carousel c04 --source carousels-v3
```

## `update-profile.py` — Learning loop aggregator

Regenera `growthOS/voice/preferences/PROFILE.md` a partir de APPROVED.md + REJECTED.md.

```bash
python growthOS/scripts/update-profile.py
```

Auto-triggered pelo review-server após cada aprovação/rejeição.
