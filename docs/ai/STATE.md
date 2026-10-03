# Coffee CLI — Estado Operacional

**Última atualização:** 2026-10-03  
**Versão do projeto:** 0.1.0  
**Branch atual:** main

---

## Modo Atual

**BUILD** (documentação sincronizada com o código; imports saneados; consolidação da arquitetura Runtime/Context/DI)

---

## Objetivo Atual

Consolidação arquitetural concluída (2026-10-03): Application Runtime + Application Context (ContextVar) + DI + Components documentados — `runtime.md` §13–§17 (conceitos, token, concorrência, erros, invariantes), `doc.md` v0.3.3 (§4.3/§4.10/§6.2/§17/§18), `components-aop.md` §5.1–§5.5, invariantes em `AGENTS.md`. **Boot re-verificado: exit 1 desde `628e772`** (gap `resetApp` na rota async — exit 0 valia até `9ddf051`). Próximo foco: decisões abertas do DEV (entrypoint, drift `packageRegister`, gap `resetApp` async, formalização do ContextVar/U-002).

---

## Escopo

### Human Scope
- Definir entrypoint do pyproject (`coffee.cli.main` inexistente) — **TODO:14**
- Confirmar drift DECISION × código: `packageRegister` decidido × `register` em uso no `@Component` — **TODO:53 / doc.md §17.9**
- Definir framework CLI (Click/Typer/Rich/Custom) — **URGENTE**
- Definir contrato de Plugin — **URGENTE**
- Definir protocolo Python ↔ C++ — **URGENTE**
- Definir formato de configuração — **URGENTE**
- Validar decisões arquiteturais / aprovar especificações

### Agent Scope
- Manter documentação sincronizada com código (rotina)
- Executar spikes de pesquisa (framework CLI) quando solicitado
- Registrar OUT-OF-SCOPE FINDINGS em `docs/TODO.md` (não corrigir silenciosamente)

### Shared Scope
- Revisar arquitetura do runtime
- Confirmar separação Runtime/Container/Config/Services

---

## Decisões Atuais

| Decisão | Status | Arquivo |
|---------|--------|---------|
| CoffeeApplicationRuntime como fronteira de lifecycle | **DECIDED** | `docs/decisions/001-runtime-lifecycle-boundary.md` |
| Plugin-oriented architecture para CLI | **PROPOSAL** | `docs/decisions/002-cli-plugin-oriented-architecture.md` |
| Python como linguagem principal do CLI V1 | **DECIDED** | `docs/decisions/003-python-as-cli-v1-language.md` |
| C++ como engine nativa isolada | **PROPOSAL** | `docs/decisions/004-cpp-engine-isolation-protocol.md` |
| Coffee Server como API central | **DECIDED** | `docs/decisions/005-coffee-server-central-api.md` |
| Task Manager próprio no Server | **DECIDED** | `docs/decisions/005-coffee-server-central-api.md` |
| Componentes via @Component sem AOP (decorators + CoffeeRegistry + Container) | **DECIDED** | `docs/decisions/006-component-decorators-no-aop.md` |
| DI do ModuleManager via composition root | **DECIDED** | `docs/decisions/007-modulemanager-dependency-injection.md` |
| `@Component` deve usar `packageRegister` | **DRIFT** — código usa `register` desde `c60908d` (aguarda confirmação do DEV) | `doc.md` §17.9, `TODO:53` |

---

## Questões Abertas (Críticas para V1)

1. **Framework de CLI em Python** — Click? Typer? Rich? Custom? → `docs/research/cli-framework-comparison.md`
2. **Protocolo Python ↔ C++** — JSON sobre stdin/stdout? gRPC? Named pipes? → ADR 004
3. **Modelo definitivo de plugins** — Descoberta? Carregamento? Configuração? → ADR 008
4. **Contrato formal de Plugin** — Interface mínima? Metadata? → ADR 008
5. **Sistema de configuração do CLI** — TOML? YAML? Python? → ADR 009
6. **Offline mode / sync** — Necessário no V1?
7. **Formato de Context Pack** — Estrutura? Serialização?
8. **Modelo final do Coffee Server V2** — REST? GraphQL? MCP?
9. **Esquema completo de Tasks/Projects** — Campos? Relacionamentos?
10. **Nome definitivo da pasta/engine C++** — `engine/`? `native/`? `core/`?
11. **Entrypoint do pyproject** — `coffee.main:main` (coroutine decorada) como alvo? → `TODO:14`

---

## Blockers

- **CRÍTICO:** Framework CLI não decidido — bloqueia implementação V1
- **CRÍTICO:** Contrato de Plugin não definido — bloqueia arquitetura modular
- **CRÍTICO:** Protocolo Python ↔ C++ não definido — bloqueia engine nativa
- **ALTO:** Formato de configuração não decidido — afeta todo CLI
- **MÉDIO:** Drift DECISION × código (`packageRegister` × `register`) — `TODO:53`
- **MÉDIO:** Entrypoint quebrado — `TODO:14`

---

## Próximo Passo (Imediato)

1. **Decisão DEV:** confirmar `register()` no `@Component` (atualizar DECISION) ou reverter — `TODO:53`
2. **Decisão DEV:** entrypoint do pyproject — `TODO:14`
3. **Spike pesquisa:** Testar Click + Rich vs Typer para CLI (`docs/research/cli-framework-comparison.md`)
4. **Decisão humana:** Escolher framework CLI baseado nos spikes
5. **ADR 008:** Definir contrato de Plugin
6. **ADR 009:** Definir formato config (recomendação: TOML)

---

## Handoff

> **Estado (2026-10-03):** consolidação da arquitetura **Runtime + Application Context + DI + Components** — `doc.md` v0.3.3 (§4.1/§4.3/§4.10/§6.2/§17.10-12/§18.1), `runtime.md` (§5.3/§5.4 + novas §13–§17), `components-aop.md` (tabela + §5.1–§5.5), espelho `.agents/specs/coffee-components-aop.md`, invariantes em `AGENTS.md`. Base: relatório do `codebase-explorer` (`628e772`) + task context `runtime-context-di-components-task-context.json`. **Boot exit 1 confirmado por execução** (leak `resetApp` rota async).
>
> **Decisões/drifts abertos para o DEV:** `TODO:14` (entrypoint), `TODO:53` (drift `packageRegister` × `register`), `TODO:54` (placeholder `Start()`); **novos:** U-001 (resetApp ausente async/factory = bug ou intenção?), U-002 (ContextVar formalizado como mecanismo oficial? sem ADR), C-002 (ADR 007 constructor injection × service-locator contextual), modelo de instância do container (class-level).
>
> **Arquivos atualizados em 2026-10-03:**
> - `docs/doc.md` (v0.3.3), `docs/architecture/runtime.md`, `docs/architecture/components-aop.md`
> - `.agents/specs/coffee-components-aop.md`, `AGENTS.md` (invariantes)
> - `docs/ai/STATE.md` (este arquivo), `.agents/state.json`
> - cache: `.agents/protocol/docs/codebase-explorer.json` + task context (pelo `codebase-explorer`)

> **Estado (2026-10-01):** doc.md em **v0.3.2** sincronizada com o código (paths pós-restructure, status de imports, boot funcional após reescrita de `Config.build()` pelo DEV — exit 0 verificado por execução na época; **exit 0 válido apenas até `9ddf051`**). Task de saneamento de imports concluída (61/61 resolvem, 0 paths antigos, 0 ciclos, 0 core→modules, 1 fix `abstractmethod`). Relatório global do explorer em `.agents/protocol/docs/codebase-explorer.json` (HEAD `b9b15a8`).
>
> **Decisões/drifts abertos para o DEV:** `TODO:14` (entrypoint), `TODO:53` (drift `packageRegister` × `register`), `TODO:54` (placeholder `Start()`).
>
> **Arquivos atualizados nesta sessão:**
> - `docs/doc.md` (v0.3.2 — paths, boot flow, §4/§6/§16/§18)
> - `docs/architecture/runtime.md`, `docs/architecture/components-aop.md` (paths atuais)
> - `.agents/specs/coffee-components-aop.md` (estado no código)
> - `docs/TODO.md` (:14, :53, :54 + Completed)
> - `docs/ai/STATE.md` (este arquivo)
> - `src/coffee/core/components/CoffeeComponent.py` (1 fix de import)
> - `.agents/state.json`, `.agents/protocol/docs/codebase-explorer.json`
