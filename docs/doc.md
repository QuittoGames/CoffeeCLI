# Coffee CLI — Documentação Técnica Consolidada

**Versão:** 0.1.0  
**Status:** FACT (baseado em código atual) + INFERENCE (onde código não confirma)  
**Última atualização:** 2026-09-22

---

## 1. Overview

O Coffee CLI é a interface de linha de comando principal do ecossistema Coffee — uma camada pessoal de produtividade, desenvolvimento, automação, contexto e integração com IA.

**Objetivo:** Ser o principal cliente de uso diário, combinando operações locais (filesystem, Git, processos, sistema) com operações via Coffee Server (tasks, projects, context, AI).

**Não-objetivos:** Substituir o shell, ser um segundo servidor, tornar o sistema dependente do Coffee.

---

## 2. Goals and Non-Goals

### Goals (V1)
- CLI unificada para: tasks, projects, Git, contexto, AI, system, machine, serviços, ferramentas de dev, automações
- Operações locais independentes do Server
- Arquitetura modular orientada a plugins/features
- Python como linguagem principal; fronteira limpa para engine C++ futura
- Clean Architecture: domain separado de implementações concretas

### Non-Goals (V1)
- Reproduzir ClickUp inteiro
- Transformar CLI em servidor
- Rust como linguagem principal
- C++ espalhado pelo projeto
- OpenCode rebuild sem especificação

---

## 3. Architecture

### 3.1 High-Level

```
                         Coffee Interface
                              |
              +---------------+---------------+
              |                               |
          Coffee CLI                      outras UIs
              |                               |
              +---------------+---------------+
                              |
                        Coffee Server
                              |
         +-------------------+-------------------+
         |                   |                   |
      Tasks               Projects            Context
         |                   |                   |
         +-------------------+-------------------+
         |                   |                   |
        AI              Integrations          Personal
         |
         +-------------------------------+
                                       |
                                Local System Layer
                                       |
                           +-----------+-----------+
                           |                       |
                        Fedora                  Windows
```

### 3.2 Código Atual (FACT)

```
src/coffee/
├── __init__.py
├── main.py                          # Entry point com @CoffeeApplicationRuntime
├── core/
│   ├── __init__.py
│   ├── runtime/
│   │   ├── CoffeAplicationRuntime.py    # Lifecycle + decorator (parcial)
│   │   └── contener/
│   │       └── CoffeeApplicationContainer.py  # Contexto compartilhado
│   ├── data/
│   │   ├── Config.py                    # Configurações (dado)
│   │   └── Host.py                      # Dados de host
│   ├── Services/
│   │   └── module/
│   │       └── ModuleManager.py         # Serviço de módulos (tem @CoffeeApplicationRuntime — incorreto)
│   ├── cli/
│   │   └── CLI.py                       # argparse parser (tem @CoffeeApplicationRuntime)
│   └── domain/
│       └── models/
│           └── Module.py                # Modelo de domínio
└── modules/
    ├── update/
    │   └── __init__.py
    └── ssh/
        └── __init__.py
```

### 3.3 Arquitetura Alvo (PROPOSAL)

```
src/coffee/
├── core/                          # Núcleo estável
│   ├── runtime/                   # CoffeeApplicationRuntime + Container
│   ├── config/                    # Configuration system
│   ├── plugin/                    # Plugin system (discovery, loading, contract)
│   ├── domain/                    # Domain models (Task, Project, Repository, Machine, Context)
│   └── ports/                     # Contracts/ports para adapters
├── plugins/                       # Features como plugins independentes
│   ├── task/
│   │   ├── models/
│   │   ├── services/
│   │   ├── adapters/
│   │   ├── ports/
│   │   ├── commands/
│   │   └── plugin.py
│   ├── project/
│   ├── git/
│   ├── context/
│   ├── system/
│   ├── ai/
│   └── ...
├── engine/ (ou native/)           # C++ native capabilities (isolado)
├── cli/                           # CLI entry, command routing, output
└── main.py                        # Bootstrap
```

---

## 4. Modules

### 4.1 CoffeeApplicationRuntime (FACT + PROPOSAL)

**Arquivo:** `src/coffee/core/runtime/CoffeAplicationRuntime.py`

**Responsabilidade:** Fronteira de lifecycle da aplicação — inicializar, entregar contexto, encerrar.

**Estado atual:**
- `init()`: cria `Config().build()` + `CoffeeApplicationContainer`
- `getContener()`: retorna container (typo: "Contener")
- `setConfig()`: repassa config ao container
- `stop()`: zera container, retorna `True`
- **Decorator NÃO implementado** — classe não tem `__call__`

**Gaps conhecidos:** Ver `docs/architecture/runtime.md` §7

### 4.2 CoffeeApplicationContainer (FACT)

**Arquivo:** `src/coffee/core/runtime/contener/CoffeeApplicationContainer.py`

**Estado atual:** Guarda apenas `Config`. `ModuleManager` e outros serviços **não** estão no container.

### 4.3 Config (FACT)

**Arquivo:** `src/coffee/core/data/Config.py`

- `configPath`: `platformdirs.user_config_dir("Coffee")`
- `hostData`: `Host`
- `Debug`: `bool`
- `build()`: valida existência de path e hostData.platform

### 4.4 ModuleManager (FACT — com problema)

**Arquivo:** `src/coffee/core/Services/module/ModuleManager.py`

- Tem `@CoffeeApplicationRuntime` — **VIOLAÇÃO** da regra: serviços não devem controlar lifecycle
- Deve receber contexto, não criá-lo

### 4.5 CLI Parser (FACT)

**Arquivo:** `src/coffee/core/cli/CLI.py`

- `argparse.ArgumentParser` wrapper
- Tem `@CoffeeApplicationRuntime` — aceitável como ponto de entrada

### 4.6 Domain Models (FACT)

**Arquivo:** `src/coffee/core/domain/models/Module.py`

- Modelo base para módulos/plugins

---

## 5. Domain Model

### 5.1 Entidades Centrais (PROPOSAL — baseada em conversa)

| Entidade | Descrição | Status |
|---|---|---|
| **Task** | Unidade executável | PROPOSAL |
| **Project** | Iniciativa/estrutura contínua | PROPOSAL |
| **Repository** | Git repository vinculado | PROPOSAL |
| **Machine** | Máquina gerenciada | PROPOSAL |
| **Context** | Contexto resolvido para IA | PROPOSAL |
| **Module/Plugin** | Feature extensível | FACT (parcial) |

### 5.2 Regras de Domínio

- Domain **não** conhece: ClickUp, PostgreSQL, HTTP, Rich/TUI, Fedora, C++
- Dependências externas via **contracts/ports** → **adapters**

---

## 6. Data Flow

### 6.1 Lifecycle Atual (FACT)

```
main / entrypoint
        ↓
CoffeeApplicationRuntime (decorator NÃO funcional)
        ↓
init() → Config().build() → CoffeeApplicationContainer(config)
        ↓
execução manual (sem injeção automática)
        ↓
stop() → container = None
```

### 6.2 Lifecycle Alvo (PROPOSAL)

```
@CoffeeApplicationRuntime()
async def main(app):
    container = app.getContainer()
    config = container.getConfig()
    # ... lógica ...

# Conceitualmente:
runtime.init()
try:
    await main(runtime)
finally:
    runtime.stop()  # try/finally garantido
```

---

## 7. Application Flow

### 7.1 Pontos de Entrada Previstos

| Ponto de Entrada | Usa Runtime? | Status |
|---|---|---|
| `src/coffee/main.py` → `main()` | Sim (decorator) | Parcial |
| `src/coffee/core/cli/CLI.py` → `RuntimeCLI` | Sim (decorator) | Parcial |
| `src/coffee/core/Services/module/ModuleManager.py` | **Não** (é serviço) | VIOLAÇÃO |
| Workers futuros | Sim | Planejado |
| Hermes (futuro) | Sim | Planejado |

---

## 8. APIs

### 8.1 CLI Commands (PLANNED)

```
coffee task add/list/inbox/today/next/done
coffee project create/list
coffee git status/log/diff
coffee context get/resolve
coffee system info/doctor
coffee machine export/doctor/bootstrap
coffee ai <subcommand>
```

### 8.2 Coffee Server Interfaces (PLANNED)

- REST: interface geral
- MCP: adaptador para agentes IA
- WebSocket/events: realtime
- Capability layer: `task.read`, `task.create`, `project.read`, `context.resolve`, `machine.inspect`, `event.publish`

---

## 9. Persistence

### 9.1 Local
- Config: `platformdirs.user_config_dir("Coffee")`
- Data: `platformdirs.user_data_dir("Coffee")`
- Cache: `platformdirs.user_cache_dir("Coffee")`

### 9.2 Server (PLANNED)
- PostgreSQL (provavelmente)
- Tasks, Projects, Context, Machines, Integrations, Personal data

---

## 10. Error Handling

### 10.1 Exceções Atuais (FACT)
- `InvalidCoffeeApplicationException` — runtime/container indisponível

### 10.2 Estratégia Alvo (PROPOSAL)
- Domain exceptions para regras de negócio
- Infrastructure exceptions isoladas em adapters
- Exit codes padronizados para CLI
- Structured logging

---

## 11. Security

- SELinux: conter processos comprometidos, não bloquear workflow
- Firewall: `firewalld` gerenciado
- SSH: hardening
- Secrets: não no código, gerenciados via config/environment
- Containers: Podman/Docker para isolamento

---

## 12. Concurrency

- Python `asyncio` para I/O bound (API calls, filesystem, subprocess)
- ThreadPoolExecutor para CPU bound se necessário
- C++ engine: comunicação via processo separado + JSON/stdin-stdout (PLANNED)

---

## 13. External Integrations

| Integração | Tipo | Status |
|---|---|---|
| Coffee Server | REST/MCP/WS | PLANNED |
| Git | subprocess/local | FACT (parcial) |
| Filesystem | stdlib | FACT |
| System (Linux/Windows) | subprocess/psutil | PLANNED |
| AI (OpenCode, etc.) | MCP/HTTP | PLANNED |
| VS Code | MCP/extensão | PLANNED |
| Obsidian | filesystem/parser | PLANNED |
| Quarto/LaTeX | subprocess | PLANNED |

---

## 14. Testing Strategy

- Unit: domain, services, adapters (pytest)
- Integration: CLI commands, Server communication
- Contract: plugin interface, ports
- E2E: fluxos principais (task CRUD, project, context)
- Property-based: config parsing, domain invariants

---

## 15. Deployment

### 15.1 CLI Distribution (PLANNED)
- `pipx install coffee-cli` ou `pip install coffee-cli`
- Entry point: `coffee = coffee.cli.main:main` (pyproject.toml)
- Future: standalone binary via PyInstaller/Nuitka ou C++ engine

### 15.2 Server (SEPARATE PROJECT)
- Docker/Podman container
- Systemd service
- Health checks

---

## 16. Operational Considerations

- **Offline-first:** CLI funciona sem Server para operações locais
- **Doctor/Diagnostic:** `coffee system doctor` verifica OS, kernel, GPU, ferramentas
- **Recovery:** `coffee machine export/bootstrap/restore`
- **Dual boot:** rEFInd, Secure Boot, ESP backup
- **Backup:** configs, toolchain, repositories, dados

---

## 17. Known Limitations (FACT)

1. **Decorator não funcional** — `CoffeeApplicationRuntime` não implementa `__call__`
2. **Typo público** — `getContener()` deve ser `getContainer()`
3. **ModuleManager viola arquitetura** — tem `@CoffeeApplicationRuntime`
4. **Container vazio** — só tem `Config`, sem `ModuleManager` e outros serviços
5. **Sem plugin system** — arquitetura modular não implementada
6. **Sem config system robusto** — apenas `Config` básico
7. **Sem domain models completos** — Task, Project, etc. não existem
8. **Sem CLI framework** — apenas `argparse` básico

---

## 18. Future Evolution

### Próximos Passos (sequência discutida)
1. Definir contratos do ecossistema
2. Definir contrato do Coffee CLI
3. Definir Task Manager / domínio de Tasks
4. Implementar Coffee CLI V1
5. Integrar CLI + Task Service do Server
6. Criar baseline/doctor do Linux
7. Estruturar máquina / dual boot / recovery
8. Refatorar Coffee Server
9. Criar Context Engine
10. Reconstruir AI Harness

### Decisões Abertas (ver `docs/decisions/`)
- Framework CLI Python
- Protocolo Python ↔ C++
- Modelo de plugins
- Formato de configuração
- Offline mode/sync
- Context Pack format
- Coffee Server V2 API
- Tasks/Projects schema
- C++ engine folder name