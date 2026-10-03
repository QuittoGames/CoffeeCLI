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
- [ ] [H][HIGH] Decidir entrypoint do pyproject: `coffee = "coffee.cli.main:main"` aponta para módulo inexistente (`src/coffee/cli/` não existe). Alvo provável `coffee.main:main`, mas `main` é coroutine decorada por `@CoffeeApplicationRuntime` e `Start()` hoje contém placeholder `print("coffe")` — comportamento do entrypoint é decisão do DEV. **Status 2026-10-01:** pacote instalado via `pip install -e .` no `.venv` (`import coffee` resolve); o script `coffee.exe` existe mas falha com `ModuleNotFoundError: coffee.cli.main`
- [x] [H][MEDIUM] ~~Decidir renomeação de estrutura inconsistente: `CoffeAplicationRuntime.py`, `contener/`, `componets/`, `exepiton/`, `Services/` (maiúsculo)~~ — **EXECUTADO em 2026-09-28 por instrução explícita do DEV** (rename completo + identificadores, validado: compileall OK, 13/15 imports, zero typos em `src/`); tabela completa em `docs/doc.md` §16.10
- [x] [H][HIGH] TASK-031: Decidir escopo das interfaces DIP — quais classes além de `CoffeeApplicationRuntime` ganham interface; estilo (ABC vs Protocol — hoje só ABC existe); localização (`core/domain/interface/` vs colocalizado junto da impl, padrão `CoffeeRegistry`/`DefaultCoffeeRegistry`). DoD: DEV confirma lista + estilo + local — **CUMPRIDO** (DEV: 1ª leva = Runtime + Container + Registry completo; estilo ABC; novas em `core/domain/interface/`; Registry completado in-place, colocalizado)
- [x] [H][HIGH] TASK-032: Validar coerência das interfaces propostas com as implementações concretas (membros derivados do código real, nada inventado) antes da aplicação em massa — o DEV pediu explicitamente para ser consultado. DoD: DEV aprova membros de cada interface — **CUMPRIDO** (DEV aprovou tabela completa de membros; anotações com tipos de interface somente nas ABCs, concretas mantêm tipos concretos)

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
- [x] [A][MECHANICAL] Saneamento de imports/IntelliSense (TASK-001..004)
  - [x] TASK-001: Criar `__init__.py` em 10 pacotes sem eles (`modules/`, `core/data/`, `core/runtime/`, `core/runtime/componets/`, `componets/base/`, `contener/`, `core/Services/`, `Services/module/`, `domain/exepiton/`, `domain/interface/`) — setuptools `packages.find` não os empacotava e o Pylance perdia a resolução de classe (`Expected class but received "SystemModule"`)
  - [x] TASK-002: Corrigir `IndentationError` + `TypeVar T` não definido em `core/runtime/componets/base/CoffeeRegistry.py`
  - [x] TASK-003: Declarar `dependencies = ["platformdirs"]` no `pyproject.toml` (usado em `core/data/Config.py`)
  - [x] TASK-004: Validação — `compileall -f` OK, 33/33 módulos importam, `pip install -e .` OK
  - [ ] TASK-005: CI/validação contínua — adicionar check de `python -m compileall src` ao workflow (quando houver CI)

- [x] [A][HIGH] TASK-100: Trocar tipos `SystemModule` → `CoffeeComponent` em `core/runtime/components/Component.py` (import, `TypeVar bound=`, assinatura; remover `TypeVar` morto + import `typing`) — `SystemModule` é contrato de módulos externos (`modules/`), não de componentes. DoD: grep `SystemModule` em `Component.py` = 0; `compileall` OK — **CUMPRIDO** (ver `doc.md` §16.11)
- [x] [A][HIGH] TASK-101: Remover dead code `T = TypeVar("T", bound=SystemModule)` + import `SystemModule` + `abstractmethod` unused em `components/base/CoffeeRegistry.py`. DoD: arquivo sem `SystemModule`; `compileall` OK — **CUMPRIDO**
- [x] [A][MEDIUM] TASK-102: Validar código pós-TASK-100/101 — `python -m compileall -f src` + import por módulo. DoD: exit 0; falhas apenas `CLI`/`ModuleManager` (bug `@Component` pré-existente, sem regressão) — **CUMPRIDO** (33/35 OK)
- [x] [A][MEDIUM] TASK-103: Ajustar documentação — `docs/doc.md` (front matter 0.3.1, §4.5 snippet/anomalias, §16.2, novo §16.11, Apêndice A, CONFLICT do report global inexistente) + finding L53. DoD: grep `Component(component: SystemModule)` = 0 fora de contexto histórico — **CUMPRIDO**
- [x] [A][MEDIUM] TASK-104: Ajustar caches — `.agents/state.json` (transição operacional) + `.agents/protocol/tasks/temp/docs-main-technical-context.md` (banner STALE apontando §16.10/§16.11). DoD: caches não contradizem o código novo — **CUMPRIDO**

- [x] [A][MED] TASK-026: Validar estado WIP vs HEAD para definição da versão de referência (import-check: HEAD `206f180` = 10/10 OK vs WIP = 13/18 FAIL por `CoffeeComponent.py:8` — `container = None | None`). DoD: versão de referência decidida + justificativa registrada — **CUMPRIDO** (DEV escolheu corrigir WIP; fix mínimo `Any | None = None` em `CoffeeComponent.py:8`; pós-fix 38/38 → 40/40 imports OK)
- [x] [A][MED] TASK-027: Criar interface `ApplicationRuntime` (ABC, padrão do projeto) seguindo padrão `SystemModule.py` e fazer `CoffeeApplicationRuntime` implementá-la — **somente interface + herança, zero mudança de lógica**. DoD: classe declara herança; diff contém só interface/herança; imports OK — **CUMPRIDO** (`core/domain/interface/ApplicationRuntime.py`; 6 membros: `__init__/init/getContainer/setConfig/stop/__call__`)
- [x] [A][MED] TASK-028: Avaliar demais candidatas a interface (`CoffeeApplicationContainer`, `RuntimeCLI`, `Config`, `ModuleManager`, `Host`, `tool`, completar `CoffeeRegistry` com `@abstractmethod`) — documentar membros derivados do código real e classificar: agora / futuro (ADR 007) / desnecessária. DoD: tabela decidida por candidata, sem membros inventados — **CUMPRIDO** (DEV definiu 1ª leva = ApplicationRuntime + ApplicationContainer + CoffeeRegistry completo; `Config`/`ModuleManager`/`Host`/`tool`/`RuntimeCLI` postergadas)
- [x] [A][MED] TASK-029: Após aprovação do DEV (TASK-031/032), criar interfaces restantes aprovadas + declaração de implementação nas classes concretas, sem alterar lógica/wiring/container. DoD: imports OK; zero mudança de comportamento — **CUMPRIDO** (`ApplicationContainer` + `CoffeeApplicationContainer` herda; `CoffeeRegistry` completado com 6 `@abstractmethod` + `DefaultCoffeeRegistry` já herdava; smoke test: `issubclass` OK, todas as classes instanciáveis, `__abstractmethods__` vazio)
- [x] [A][MED] TASK-030: Registrar alinhamento com ADR 007 (composition root injection) — criação de interfaces é extensão natural ou divergência. DoD: nota no TODO.md — **CUMPRIDO**: criação de interfaces **alinha-se** à direção DIP da ADR 007 (Opção C ACCEPTED) — a ADR decide *onde* a injeção acontece (composition root), as interfaces habilitam *substituições* futuras; nenhuma mudança de wiring foi feita. **PROPOSAL futuro (não decidido):** usar as interfaces nas anotações do Runtime (`_container: ApplicationContainer`) e ligar o ctor injection do ModuleManager da ADR 007

## Shared

- [ ] [S][REVIEW] Revisar CoffeeApplicationRuntime: decorator, typo getContener, try/finally
- [ ] [S][REVIEW] Validar separação Runtime/Container/Config/Services
- [ ] [S][REVIEW] Confirmar que ModuleManager NÃO deve ter @CoffeeApplicationRuntime
- [ ] [S][REVIEW] Definir estrutura de pastas do CLI (plugins, domain, core, engine)
- [ ] [S][REVIEW] OUT-OF-SCOPE FINDING: `@Component` em `ModuleManager` (e `RuntimeCLI`) — defeito histórico de `packageRegister`/`.id`. **Status 2026-10-01:** o código passou a importar OK — `c60908d` trocou `Component.py` para `registry.register(component)` e o registry (reescrito) não exige mais `.id`; `@Module` continua em `packageRegister` (sem `.id` também). ⚠️ **DRIFT:** a DECISION registrada (DEV, 2026-09-29) dizia **MANTER `packageRegister`** no decorator — o código diverge da decisão (`doc.md` §17.9). **Ação DEV:** confirmar se `register()` em `@Component` é o comportamento oficial (e atualizar a DECISION) ou reverter. Enquanto isso, defeito segue registrado
- [ ] [S][REVIEW] OUT-OF-SCOPE FINDING: `main.py` — `Start()` tinha `tool.menu()` inexistente (**DEV substituiu por placeholder `print("coffe")` em 2026-10-01**); `tool.verify_modules()` é `async` e agora roda via `asyncio.create_task(...)` **sem aguardar o resultado** (substituiu a chamada direta sem `await`); arquivo em edição ativa pelo DEV
- [ ] [S][REVIEW] OUT-OF-SCOPE FINDING: diretórios vazios sem código (`core/domain/models/`, `modules/ssh/Adpiter/`, `modules/ssh/models/`, `modules/ssh/Services/`) — decidir se viram pacotes ou são removidos

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
- [x] [A] `__init__.py` criados em todos os pacotes com código (10 pacotes)
- [x] [A] `CoffeeRegistry.py` indentação/TypeVar corrigidos
- [x] [A] `platformdirs` declarado no pyproject; pacote instalado via `pip install -e .`
- [x] [A] Saneamento de imports (2026-10-01) — 5 instâncias `import-cleaner` (core-kernel, runtime/container, modules, shared/entry, grafo global) + verificação final: 61/61 imports resolvem, 0 paths históricos em `src/`, 0 imports relativos, 0 ciclos (DAG), 0 violações core→modules, `compileall` exit 0, 14/14 módulos importam; 1 fix (`abstractmethod` removido de `core/components/CoffeeComponent.py`); relatório global do explorer gerado (`.agents/protocol/docs/codebase-explorer.json`, `b9b15a8`); docs sincronizadas (doc.md 0.3.2, runtime.md, components-aop.md, `.agents/specs/coffee-components-aop.md`)
- [x] [A] `pip install -e .` no `.venv` (2026-10-01) — `coffee-cli 0.1.0` instalado; `import coffee` resolve de qualquer diretório; `platformdirs` 4.12.1 OK; script `coffee.exe` criado (entrypoint quebrado permanece — item [H]:14)
