---
description: Coffee CLI — contexto essencial do projeto. Governança completa do trabalho de IA vive em .agents/harness.md — carregar em toda tarefa de desenvolvimento, refatoração, revisão ou decisão técnica. UX, arquitetura e contratos pertencem ao DEV.
---

# Coffee CLI

CLI do Coffee Ecosystem — interface humana e orquestrador local. Python >= 3.11, código em `src/coffee/`. Não é um segundo servidor; o OS funciona sem Coffee.

## Pointers de contexto

- **`.agents/harness.md`** — harness de governança do projeto: ownership, escopo, decision gate, capabilities, boundaries do ecossistema, security model e não-fabricação. **Carregar antes de qualquer trabalho de desenvolvimento.**
- **`.agents/context/coffee-ecosystem-conversation-documentation.md`** — fonte arquitetural definida pelo DEV (Coffee Ecosystem). **Carregar para decisões arquiteturais, novas features ou dúvidas sobre fronteiras do ecossistema.**
- **`.agents/specs/ux-ui-language.md`** — linguagem visual das TUIs (black + blue + transparent, terminal-native, radius 8px). **Carregar em qualquer trabalho de UI/TUI.** UX detalhada (telas, fluxos, componentes, copy) é UNDEFINED e pertence ao DEV.
- **`docs/architecture/runtime.md` §13–§17** — Application Runtime + Application Context (ContextVar), token, concorrência, erros comuns e invariantes. **Carregar em qualquer trabalho de Runtime/Context/DI/Components.** Estado técnico canônico: `docs/doc.md` §4.3/§4.10; cache: `.agents/protocol/docs/codebase-explorer.json`.

## Invariantes de arquitetura — Runtime / Context / DI / Components

Registrados em 2026-10-03 (verificados no código — `628e772`; detalhes em `docs/architecture/runtime.md` §17):

1. `CoffeeApplicationRuntime` é **instância normal**, não singleton estático (ciclo é de classe → 1 container compartilhado).
2. `ContextVar` contém **referência contextual** para o App atual (não cópia, não variável global comum).
3. `CoffeeApplicationContext` **não** é singleton do Runtime — é o encapsulamento do ContextVar (`setApp`/`getApp`/`resetApp`; nunca mexer em `_current_app` diretamente).
4. Component acessa o App atual via `CoffeeApplicationContext.getApp()` — não recebe `app` obrigatoriamente por parâmetro.
5. Component depende preferencialmente de `ApplicationContainer` (abstração), não de `CoffeeApplicationContainer` (DIP).
6. Registry **registra classes**; Container **resolve instâncias** (`@Component` = registro, não instanciação).
7. `setApp()` precisa acontecer **antes** do acesso dos componentes (antes do entrypoint e do `init` consumir contexto).
8. `resetApp(token)` deve ocorrer **no final do lifecycle** — hoje confirmado **só na rota sync**; rota async e factory-form têm leak (GAP conhecido, `doc.md` §17.10).
9. `ContextVar` **não** substitui sincronização de estado compartilhado mutável (registry/container/`_container` — 0 travas no código).
10. `RuntimeError: CoffeeApplicationRuntime is not running` = acesso fora da janela do ciclo, **não** é automaticamente race condition.

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
