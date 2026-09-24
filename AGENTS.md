---
description: Coffee CLI — contexto essencial do projeto. Governança completa do trabalho de IA vive em .agents/harness.md — carregar em toda tarefa de desenvolvimento, refatoração, revisão ou decisão técnica. UX, arquitetura e contratos pertencem ao DEV.
---

# Coffee CLI

CLI do Coffee Ecosystem — interface humana e orquestrador local. Python >= 3.11, código em `src/coffee/`. Não é um segundo servidor; o OS funciona sem Coffee.

## Pointers de contexto

- **`.agents/harness.md`** — harness de governança do projeto: ownership, escopo, decision gate, capabilities, boundaries do ecossistema, security model e não-fabricação. **Carregar antes de qualquer trabalho de desenvolvimento.**
- **`.agents/context/coffee-ecosystem-conversation-documentation.md`** — fonte arquitetural definida pelo DEV (Coffee Ecosystem). **Carregar para decisões arquiteturais, novas features ou dúvidas sobre fronteiras do ecossistema.**
- **`.agents/specs/ux-ui-language.md`** — linguagem visual das TUIs (black + blue + transparent, terminal-native, radius 8px). **Carregar em qualquer trabalho de UI/TUI.** UX detalhada (telas, fluxos, componentes, copy) é UNDEFINED e pertence ao DEV.

## Regra base

```text
DEV define
    ↓
IA assiste dentro do escopo
    ↓
sistema valida
    ↓
DEV permanece dono
```

Ausência de definição = `UNDEFINED` — nunca preencher por inferência. `PROPOSAL ≠ DECISION`.

## Notas de organização

- `docs/` é gerido por fluxo separado — ver `docs/ai/STATE.md` para estado atual (documentação técnica, TODO, ADRs, specs V1).
- Código atual: skeleton inicial — problemas estruturais conhecidos (entrypoint, imports, arquivo de runtime sem extensão) são registrados via OUT-OF-SCOPE FINDING e TODO, não corrigidos silenciosamente.
