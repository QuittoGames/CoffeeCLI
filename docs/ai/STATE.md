# Coffee CLI — Estado Operacional

**Última atualização:** 2026-09-23  
**Versão do projeto:** 0.1.0  
**Branch atual:** main

---

## Modo Atual

**LEARN** → **BUILD** (transição: documentação consolidada, pronto para implementação)

---

## Objetivo Atual

Documentação estruturada criada. Próximo foco: fechar decisões abertas (ADRs) e iniciar implementação V1.

---

## Escopo

### Human Scope
- Definir framework CLI (Click/Typer/Rich/Custom) — **URGENTE**
- Definir contrato de Plugin — **URGENTE**
- Definir protocolo Python ↔ C++ — **URGENTE**
- Definir formato de configuração — **URGENTE**
- Validar decisões arquiteturais
- Aprovar especificações

### Agent Scope
- Manter documentação sincronizada com código
- Implementar spikes de pesquisa (framework CLI)
- Criar ADRs para decisões pendentes
- Implementar CoffeeApplicationRuntime.__call__ (decorator funcional)

### Shared Scope
- Revisar arquitetura do runtime
- Confirmar separação Runtime/Container/Config/Services
- Definir estrutura de pastas do CLI

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

---

## Blockers

- **CRÍTICO:** Framework CLI não decidido — bloqueia implementação V1
- **CRÍTICO:** Contrato de Plugin não definido — bloqueia arquitetura modular
- **CRÍTICO:** Protocolo Python ↔ C++ não definido — bloqueia engine nativa
- **ALTO:** Formato de configuração não decidido — afeta todo CLI

---

## Próximo Passo (Imediato)

1. **Spike pesquisa:** Testar Click + Rich vs Typer para CLI (`docs/research/cli-framework-comparison.md`)
2. **Decisão humana:** Escolher framework CLI baseado em spikes
3. **ADR 008:** Definir contrato de Plugin
4. **ADR 009:** Definir formato config (recomendação: TOML)
5. **Implementar:** `CoffeeApplicationRuntime.__call__` com `try/finally`
6. **Corrigir:** `getContener` → `getContainer`
7. **Remover:** `@CoffeeApplicationRuntime` de `ModuleManager`

---

## Handoff

> **Estado:** Documentação consolidada completa. Pronto para fase de decisões técnicas (framework CLI, plugin contract, config format) e implementação do runtime decorator.
> 
> **Arquivos criados/atualizados:**
> - `docs/ai/STATE.md` (este arquivo)
> - `docs/TODO.md` (atualizado)
> - `docs/doc.md` (documentação técnica consolidada)
> - `docs/architecture/runtime.md` (movido de docs/coffee-application-runtime.md)
> - `docs/decisions/001-007-*.md` (ADRs 001–007)
> - `docs/specs/coffee-cli-v1.md` (spec inicial)
> - `docs/diagrams/architecture.mmd` (4 diagramas Mermaid)
> - `docs/research/cli-framework-comparison.md` (pesquisa em andamento)