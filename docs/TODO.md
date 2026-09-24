# TODO — Coffee CLI

## Human

- [ ] [H][HIGH] Definir framework CLI (Click/Typer/Rich/Custom) → `docs/research/cli-framework-comparison.md`
- [ ] [H][HIGH] Definir contrato de Plugin (interface mínima, metadata, descoberta) → ADR 006
- [ ] [H][HIGH] Definir protocolo Python ↔ C++ (JSON/stdin-stdout? gRPC?) → ADR 004
- [ ] [H][HIGH] Definir formato de configuração (TOML/YAML/Python) → ADR 007
- [ ] [H][MEDIUM] Definir esquema completo Tasks/Projects
- [ ] [H][MEDIUM] Decidir nome definitivo da pasta/engine C++ (`engine/`, `native/`, `core/`)
- [ ] [H][MEDIUM] Validar arquitetura plugin-oriented
- [ ] [H][LOW] Decidir sobre offline mode/sync no V1
- [ ] [H][LOW] Definir formato de Context Pack

## Agent

- [x] [A][MECHANICAL] Criar estrutura de docs (ai/, specs/, decisions/, research/, diagrams/)
- [x] [A][MECHANICAL] Criar `docs/ai/STATE.md` atualizado
- [x] [A][MECHANICAL] Criar `docs/doc.md` — documentação técnica consolidada
- [x] [A][MECHANICAL] Mover `docs/coffee-application-runtime.md` para `docs/architecture/runtime.md`
- [x] [A][MECHANICAL] Criar ADRs em `docs/decisions/` para decisões chave
  - [x] ADR 001: Runtime lifecycle boundary
  - [x] ADR 002: Plugin-oriented architecture (PROPOSAL)
  - [x] ADR 003: Python as CLI V1 language
  - [x] ADR 004: C++ engine isolation + protocol (PROPOSAL)
  - [x] ADR 005: Coffee Server as central API
- [x] [A][MECHANICAL] Criar spec inicial `docs/specs/coffee-cli-v1.md`
- [x] [A][MECHANICAL] Criar diagramas em `docs/diagrams/architecture.mmd`
- [x] [A][MECHANICAL] Criar research placeholder `docs/research/cli-framework-comparison.md`
- [ ] [A][MECHANICAL] Documentar domain models (Task, Project, Repository, Machine, Context) — parcialmente em spec
- [ ] [A][MECHANICAL] Mapear código atual para doc (gaps conceito vs implementação) — em `docs/doc.md` §17

## Shared

- [ ] [S][REVIEW] Revisar CoffeeApplicationRuntime: decorator, typo getContener, try/finally
- [ ] [S][REVIEW] Validar separação Runtime/Container/Config/Services
- [ ] [S][REVIEW] Confirmar que ModuleManager NÃO deve ter @CoffeeApplicationRuntime
- [ ] [S][REVIEW] Definir estrutura de pastas do CLI (plugins, domain, core, engine)

## Blocked

- [ ] [H][BLOCKED] Implementação CLI V1 aguarda decisões de framework, plugins, config
- [ ] [H][BLOCKED] Engine C++ aguarda protocolo e responsabilidade concreta
- [ ] [H][BLOCKED] Coffee Server V2 aguarda especificação de API e Task Manager

## Completed

- [x] [A] Estrutura de docs criada (ai/, specs/, decisions/, research/, diagrams/)
- [x] [A] STATE.md atualizado
- [x] [A] Documentação técnica consolidada (doc.md)
- [x] [A] Runtime architecture documentada (architecture/runtime.md)
- [x] [A] ADRs criadas para 5 decisões chave
- [x] [A] Spec inicial Coffee CLI V1 (specs/coffee-cli-v1.md)
- [x] [A] Diagramas de arquitetura (diagrams/architecture.mmd)
- [x] [A] Research CLI framework iniciado
- [x] [H] CoffeeApplicationRuntime conceituado e documentado
- [x] [H] Decisões macro do ecossistema registradas
- [x] [H] Python como CLI V1, C++ como engine nativa isolada