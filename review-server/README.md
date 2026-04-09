# GrowthOS Review Server

Dashboard local para aprovar/reprovar carrosséis. Flask + vanilla JS, roda em `localhost:5050`.

## Uso

```bash
# Primeiro run — garantir dependência
python -m pip install flask

# Subir o servidor
python growthOS/review-server/server.py

# Abrir no browser
open http://localhost:5050
```

Ou via `/grow review` (subcomando do /grow).

## Atalhos de teclado

- **A** — aprovar carrossel atual
- **R** — reprovar carrossel atual
- **→** / **J** — próximo carrossel
- **←** / **K** — carrossel anterior

## Pipeline automático (on approve)

Quando você clica APPROVE, o servidor dispara em cascata:

1. `export-carousel.mjs` — gera PNGs 1080×1080 retina em `output/carousels/`
2. `organize-approved.py` — move pra `output/approved/{data}/{cid}/` + gera `metadata.json`
3. `caption-writer` agent — escreve `caption.md` com CTA e hashtags
4. `update-profile.py` — regenera `voice/preferences/PROFILE.md`
5. Entrada em `voice/preferences/APPROVED.md`

Quando você clica REJECT:

1. Entrada em `voice/preferences/REJECTED.md` com tag + razão
2. `update-profile.py` regenera PROFILE.md (próxima geração aprende a evitar o padrão)

## State

Tudo persiste em `growthOS/output/reviews/reviews.json`. Formato:

```json
{
  "carousels-v3.html": {
    "c01": {"status":"approved","tag":"","reason":"","timestamp":"2026-04-08T15:00:00"},
    "c02": {"status":"rejected","tag":"tom_guru","reason":"soou motivacional","timestamp":"..."}
  }
}
```

Arquivo é reversível, versionável, editável à mão se preciso.
