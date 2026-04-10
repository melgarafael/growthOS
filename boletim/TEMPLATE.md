# Template Canônico — Boletim dos Magos

> Formato fixo de cada edição. Variar o formato quebra o ritual da comunidade — não mude sem Rafael aprovar.

---

## Padrão do título no Circle

`Boletim dos Magos #N l Edição da Semana` — separador é **`l` (L minúsculo)**, não `|`. Começa em **#12** (a iniciativa antiga parou na #11 do Apolo; a nova operação começou na #12 em 2026-04-09).

## Capa (obrigatória)

Toda edição leva capa **840×300 PNG** gerada por `scripts/generate-cover.mjs` a partir de `cover-template.html`. Upload no Circle via botão "Alterar capa" antes de clicar Publicar. Arquivo salvo em `growthOS/boletim/covers/cover-{N}.png`.

## Estrutura obrigatória do corpo

```
🔮 Boletim dos Magos #{NÚMERO} — {DATA por extenso}

{GANCHO DE 1 LINHA — conecta a edição com o arco narrativo atual}

━━━━━━━━━━━━━━━━━━━━━━━━━

📰 As 3 notícias que importam esta semana

1. {MANCHETE CURTA}
   {2–3 linhas: o que aconteceu + por que importa PRA VOCÊ que quer usar IA no trabalho}
   🔗 Fonte: {link primário}

2. {MANCHETE CURTA}
   {2–3 linhas}
   🔗 Fonte: {link}

3. {MANCHETE CURTA}
   {2–3 linhas}
   🔗 Fonte: {link}

━━━━━━━━━━━━━━━━━━━━━━━━━

★ Insight Prático ─────────────────────────────────────
{1–3 pontos acionáveis — coisa que o aluno pode testar HOJE}
{Se couber: um mini-exemplo de prompt, um comando, um workflow}
─────────────────────────────────────────────────────

━━━━━━━━━━━━━━━━━━━━━━━━━

📚 Referências completas
• {link 1 com descrição curta}
• {link 2}
• {link 3}

💬 Qual dessas você vai testar essa semana? Comenta aí 👇

— Rafa
```

---

## Regras de escrita

**Voz (ver `growthOS/voice/GOLDEN-DOC.md`):**
- Português brasileiro, direto, sem firula
- "Você" singular (nunca "vocês", nunca "pessoal")
- Proibido: "revolucionário", "game changer", "insano", "bombar", "quebra tudo", "absurdo"
- Proibido: emojis decorativos no meio do texto (só nos marcadores de seção)
- Proibido: hype vazio ("a IA vai mudar tudo")
- Permitido: números concretos, benchmarks, custos em dólar/real, nomes de modelos

**Tamanho:**
- Gancho: máx 1 linha
- Cada manchete: 2–3 linhas
- Insight prático: 4–8 linhas
- Total: **entre 180 e 320 palavras** (boletim lê em 60 segundos)

**Insight Prático — regras específicas:**
- Sempre no formato `★ Insight Prático ─────` (réplica do Claude Code)
- Deve ser **executável hoje** — não "no futuro você poderá..."
- Se incluir prompt, usar bloco de código
- Se incluir comando, explicar em 1 linha o que faz
- NUNCA vago ("experimente a nova ferramenta"). SEMPRE específico ("cole este prompt no Claude para gerar X em 30s").

**Referências:**
- Mínimo 3, máximo 6
- Todas com link primário (não agregador)
- Descrição de 5–10 palavras cada
