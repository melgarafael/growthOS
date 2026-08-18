# /grow free-content — Educational Team bridge

Subcommand that pulls raw material (videos, lessons, transcripts) from the Educational Team project (TIM) via Maestri, runs it through the `content-factory` skill to extract viral-worthy chunks, and pipes the result into the normal carousel pipeline.

## Usage

```
/grow free-content                              # interactive: asks which source
/grow free-content "última aula sobre 3 Camadas da Maestria"
/grow free-content --source ~/educational-team/lessons/aula-05-maestria.md
```

## Pipeline

1. **Maestri terminal check** — `maestri list` to confirm `Orquestrador - Educational team` is connected
2. **Source selection** — if not passed as arg, ask user:
   - "qual aula/vídeo você quer transformar em conteúdo?"
   - "quer escolher um específico OU pegar o mais recente no repo educational-team?"
3. **Dispatch Orquestrador** — `maestri ask "Orquestrador - Educational team"` with compact prompt:
   ```
   FREE CONTENT REQUEST from GrowthOS. Locate {source}, transcribe if video, extract:
   1) viral chunks (self-contained, 60-90s worth)
   2) key frameworks mentioned (3 Camadas, 3 Pilares, 7 Passos, etc.)
   3) suggested carousel topics
   Return path to a markdown file at growthOS/voice/free-content/from-educational-{timestamp}.md
   ```
4. **Wait for Orquestrador output** — monitor via `maestri check` every 3-5 min
5. **Process via content-factory skill** — the raw output is passed through `content-factory` which already knows how to turn educational material into AutomatikClub Free Content Hub posts
6. **Generate carousel briefs** — for each viral chunk, create a `BRIEF-free-content-{slug}.md` in `growthOS/design-system/`
7. **Hand off to carousel-designer** — each brief enters the normal pipeline (asset auto-pick → lime-geist render → review dashboard)
8. **Notify user** — list the briefs that were created and next steps

## Folder structure

```
growthOS/voice/free-content/
├── from-educational-{timestamp}.md     # raw output from Orquestrador
├── chunks/                              # extracted viral chunks
│   └── chunk-{slug}.md
└── INDEX.md                             # tracks all free-content runs
```

## Integration with learning loop

Every carousel generated from free-content is tagged in `metadata.json` with `source: "free-content"` so the review dashboard and PROFILE.md can track which topics came from educational material vs native ideation.

## Example autonomous run

```
User: /grow free-content

Claude:
  → Loading Maestri terminals...
  → Orquestrador - Educational team ✓ connected
  → Which lesson/source?
User: última aula sobre as 3 camadas
Claude:
  → Dispatching Orquestrador...
  → [waiting 3 min]
  → Received: growthOS/voice/free-content/from-educational-20260408-163200.md
  → Extracted 4 viral chunks:
      - "A maestria não é o fim" (filosófico)
      - "Técnica vs Lógica vs Maestria — quanto você cobra em cada camada" (paradox)
      - "O aluno que pulou direto pra Maestria sem técnica" (cautionary)
      - "Exercício: onde você está no cubo 3D?" (diagnostic)
  → Creating 4 briefs in growthOS/design-system/
  → Dispatching carousel-designer via Maestri for each
  → 4 carousel sections added to carousels-v4.html
  → Ready for review: /grow review
```

## Rules

- NEVER bypass the Orquestrador (it owns the educational-team repo context)
- ALWAYS cross-reference the output with GOLDEN-DOC voice
- If a chunk violates the vocabulary rules (bot/chatbot/etc), FILTER it out before handing to carousel-designer
- Free content is ALWAYS voice-tagged: every generated carousel includes `source: free-content, lesson: {id}` in metadata
