# Spec: Coffee CLI V1

**Status:** DRAFT — aguarda decisões abertas (ver `docs/decisions/`)
**Versão:** 0.1.0-spec
**Base:** `docs/doc.md`, `docs/decisions/`, `.agents/context/coffee-ecosystem-conversation-documentation.md`

---

## 1. Objetivos

- CLI unificada para uso diário: tasks, projects, Git, contexto, AI, system, machine, serviços, ferramentas de dev, automações
- Operações locais independentes do Coffee Server
- Arquitetura modular orientada a plugins/features
- Python como linguagem principal; fronteira limpa para engine C++ futura
- Clean Architecture: domain separado de implementações concretas
- Offline-first: funciona sem Server para operações locais

## 1.1 Regras de Formatação

É preferível utilizar um estilo de escrita inspirado em **Java**, principalmente na declaração de funções, métodos e tipos.

O objetivo é manter as interfaces explícitas, facilitar a leitura por agentes e desenvolvedores e deixar claro quais tipos entram e saem de cada componente.

### Declaração de funções

As funções devem preferencialmente:

* declarar explicitamente os tipos dos parâmetros;
* declarar explicitamente o tipo de retorno;
* manter a assinatura legível em uma única linha quando seu tamanho permitir;
* utilizar nomes descritivos para parâmetros e funções.

Preferível:

```python
def nameFunction(parameter: type) -> ReturnValue:
    ...
```

Exemplo:

```python
def loadModule(moduleName: str) -> Module:
    ...
```

Em funções com múltiplos parâmetros:

```python
def createModule(
    moduleName: str,
    modulePath: Path,
    enabled: bool
) -> Module:
    ...
```

### Retorno explícito

Sempre que possível, o tipo de retorno deve ser declarado, inclusive em métodos que não retornam valor:

```python
def initialize() -> None:
    ...
```

Evitar:

```python
def initialize():
    ...
```

Quando uma função puder retornar mais de um tipo, a união deve ser explícita:

```python
def getContainer() -> CoffeeApplicationContainer | None:
    ...
```

Quando a ausência de valor representar uma condição inválida do fluxo, deve-se considerar validar essa condição antes do retorno:

```python
def getContainer() -> CoffeeApplicationContainer:
    if self.container is None:
        raise RuntimeError("Application container is not initialized")

    return self.container
```

### Métodos de classe

Métodos que utilizam `self` devem manter a assinatura explicitamente tipada:

```python
def build(self) -> Config:
    ...
```

Métodos estáticos devem ser utilizados somente quando não houver dependência do estado da instância:

```python
@staticmethod
def parseModule(path: Path) -> Module:
    ...
```

Métodos de classe devem utilizar `@classmethod` quando a operação depender da própria classe:

```python
@classmethod
def createDefault(cls) -> Config:
    ...
```

### Parâmetros opcionais

Parâmetros que podem receber `None` devem representar isso explicitamente no tipo:

```python
def setConfig(config: Config | None) -> None:
    ...
```

Evitar esconder opcionalidade através de tipos genéricos ou ausência de anotação.

### Generics e coleções

Coleções devem declarar o tipo dos elementos quando conhecido:

Preferível:

```python
def loadModules() -> list[Module]:
    ...
```

Em vez de:

```python
def loadModules() -> list:
    ...
```

Da mesma forma:

```python
modules: list[Module]
modulesByName: dict[str, Module]
moduleNames: set[str]
```

### Nomenclatura

Apesar da preferência por assinaturas inspiradas em Java, a implementação deve respeitar as convenções da linguagem Python sempre que isso melhorar consistência com o ecossistema.

Exemplo:

```python
def load_module(module_name: str) -> Module:
    ...
```

é preferível a:

```python
def loadModule(moduleName: str) -> Module:
    ...
```

quando a convenção Python estiver sendo aplicada ao projeto.

A preferência por estilo Java se refere principalmente à **clareza estrutural e explicitude de tipos**, e não à obrigação de converter todas as convenções de nomenclatura Python para camelCase.

### Formatação de classes

Classes devem apresentar uma estrutura previsível:

```python
@dataclass
class ExampleService:

    dependency: Dependency

    def execute(self, value: str) -> Result:
        ...
```

A ordem preferencial é:

```text
imports
↓
class declaration
↓
fields / attributes
↓
constructor ou dataclass fields
↓
public methods
↓
protected/private methods
```

### Assinaturas longas

Quando uma assinatura exceder o limite visual razoável, deve ser quebrada de maneira estruturada:

```python
def createApplication(
    config: Config,
    container: CoffeeApplicationContainer,
    debug: bool
) -> CoffeeApplicationRuntime:
    ...
```

Evitar quebras arbitrárias que dificultem identificar rapidamente:

```text
nome da função
→ parâmetros
→ retorno
```

### Objetivo da regra

A formatação deve priorizar:

```text
clareza
+
tipagem explícita
+
interfaces previsíveis
+
leitura fácil
```

O estilo semelhante ao Java deve ser utilizado como referência para **explicitude e organização da interface**, sem eliminar as características idiomáticas do Python.

**Skill de estilo de code java ja e presetne no harndness globlal e pode ser chamada pelo agente**

## 2. Não-Objetivos (V1)

- Substituir shell completo
- Ser um segundo servidor
- Reproduzir ClickUp inteiro
- Rust/C++ como linguagem principal
- OpenCode rebuild sem especificação
- Todas as features do ecossistema final



## 3. Comandos (MVP)

### 3.1 Task Manager

```
coffee task add "descrição" [--project <id>] [--priority <high|med|low>] [--due <date>] [--tags <tag,...>]
coffee task list [--project <id>] [--status <todo|doing|done>] [--tag <tag>] [--today|--next|--inbox]
coffee task show <id>
coffee task update <id> [--desc] [--priority] [--due] [--tags] [--project]
coffee task done <id>
coffee task undo <id>
coffee task delete <id>
coffee task inbox
coffee task today
coffee task next
coffee task project <id> [--list]
```

### 3.2 Project Manager

```
coffee project create <name> [--description] [--repo <path>]
coffee project list
coffee project show <id>
coffee project update <id> [--name] [--description] [--repo]
coffee project delete <id>
```

### 3.3 Git Integration

```
coffee git status [--repo <path>]
coffee git log [--repo <path>] [--oneline] [-n <count>]
coffee git diff [--repo <path>] [--staged]
coffee git branch [--repo <path>] [-a]
coffee git checkout <branch> [--repo <path>]
coffee git pull [--repo <path>]
coffee git push [--repo <path>]
```

### 3.4 Context

```
coffee context get [--task <id>] [--project <id>] [--format <json|markdown|text>]
coffee context resolve [--query <text>] [--max-tokens <n>]
coffee context pack create [--task <id>] [--project <id>] --output <file>
```

### 3.5 System / Machine

```
coffee system info
coffee system doctor
coffee machine export [--output <file>]
coffee machine doctor
coffee machine bootstrap [--config <file>]
coffee machine diff [--config <file>]
```

### 3.6 AI Integration

```
coffee ai chat [--model <name>] [--context <task|project|file>]
coffee ai complete <prompt> [--context <...>]
coffee ai embed <text> [--store]
```

### 3.7 Global

```
coffee --version
coffee --help
coffee <command> --help
coffee config get <key>
coffee config set <key> <value>
coffee config list
coffee plugin list
coffee plugin install <source>
coffee plugin remove <name>
```

---

## 4. Módulos/Plugins (MVP)

| Plugin | Responsabilidade | Depende do Server? |
|---|---|---|
| **task** | CRUD tasks, views (inbox/today/next), priorização | Sim (sync) |
| **project** | CRUD projects, vinculação repo | Sim |
| **git** | Status, log, diff, branch ops locais | Não |
| **context** | Resolução, packing, delivery para IA | Sim (fontes) |
| **system** | Info, doctor, diagnostics | Não |
| **machine** | Export, bootstrap, diff, recovery | Não |
| **ai** | Chat, completion, embedding | Sim (Server/IA) |
| **config** | Configuração global CLI | Não |

---

## 5. Domínio

### 5.1 Entidades

```python
# Task
Task:
    id: UUID
    title: str
    description: str | None
    status: TaskStatus (TODO | DOING | DONE | WAITING)
    priority: Priority (HIGH | MEDIUM | LOW)
    project_id: UUID | None
    tags: list[str]
    due_date: datetime | None
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None
    source: TaskSource (LOCAL | SERVER | CLICKUP_IMPORT)

# Project
Project:
    id: UUID
    name: str
    description: str | None
    repository_path: Path | None
    created_at: datetime
    updated_at: datetime
    archived: bool

# Repository
Repository:
    id: UUID
    path: Path
    remote_url: str | None
    default_branch: str
    project_id: UUID | None

# Machine
Machine:
    id: UUID
    name: str
    platform: Platform (LINUX | WINDOWS | MACOS)
    hostname: str
    specs: Host
    last_seen: datetime
    config_hash: str | None

# Context
ContextPack:
    id: UUID
    task_id: UUID | None
    project_id: UUID | None
    sections: list[ContextSection]
    token_estimate: int
    created_at: datetime

ContextSection:
    source: str
    content: str
    priority: int
    token_count: int
```

### 5.2 Regras de Domínio

- Task ≠ Project: Project = iniciativa contínua; Task = unidade executável
- Task não vira árvore complexa; views simples: Inbox, Today, Next, Projects, Waiting, Done
- Domain **não** conhece: ClickUp, PostgreSQL, HTTP, Rich/TUI, Fedora, C++
- Dependências externas via **ports** → **adapters**

---

## 6. Comunicação com Server

### 6.1 Capability Layer

| Capability | REST Endpoint | MCP Tool | Descrição |
|---|---|---|---|
| `task.read` | `GET /tasks/{id}` | `task_read` | Ler task |
| `task.create` | `POST /tasks` | `task_create` | Criar task |
| `task.update` | `PATCH /tasks/{id}` | `task_update` | Atualizar task |
| `task.delete` | `DELETE /tasks/{id}` | `task_delete` | Deletar task |
| `task.list` | `GET /tasks` | `task_list` | Listar com filtros |
| `project.read` | `GET /projects/{id}` | `project_read` | Ler project |
| `project.create` | `POST /projects` | `project_create` | Criar project |
| `context.resolve` | `POST /context/resolve` | `context_resolve` | Resolver contexto |
| `machine.inspect` | `GET /machines/{id}` | `machine_inspect` | Inspecionar máquina |
| `event.publish` | `POST /events` | `event_publish` | Publicar evento |

### 6.2 Offline Behavior

- Operações `git`, `system`, `machine`, `config` → **sempre locais**
- Operações `task`, `project`, `context`, `ai` → **tentam Server, fallback local se configurado**
- Queue local para writes offline → sync quando Server disponível (V1: opcional)
- `coffee sync` comando explícito para forçar sincronização

---

## 7. Operações Locais

- Filesystem: `pathlib`, `platformdirs` para config/data/cache
- Git: `subprocess` + `git` CLI (ou `pygit2` se performance)
- Processos: `subprocess`, `asyncio.subprocess`
- Sistema: `psutil`, `platform`, `distro` (Linux)
- Hardware: `psutil`, `GPUtil` (opcional), C++ engine (futuro)

---

## 8. Configuração

### 8.1 Formato (DECISÃO ABERTA — ADR pendente)

Opções: **TOML** (recomendado), YAML, Python

```toml
# coffee.toml (exemplo TOML)
[cli]
theme = "dark"
output_format = "rich"  # rich | json | plain
editor = "code --wait"

[server]
url = "http://localhost:8080"
timeout = 30
offline_mode = false

[plugins]
enabled = ["task", "project", "git", "context", "system", "machine", "ai"]
auto_discover = true

[task]
default_priority = "medium"
default_view = "today"
sync_on_start = true

[context]
max_tokens = 8000
include_git_diff = true
include_recent_files = 5

[ai]
default_model = "gpt-4o-mini"
temperature = 0.3
```

### 8.2 Locais (precedência)

1. CLI args / env vars
2. `./coffee.toml` (project-local)
3. `~/.config/coffee/coffee.toml` (user)
4. `/etc/coffee/coffee.toml` (system)
5. Defaults em código

---

## 9. Output

- **Default:** Rich (tabelas, progress, syntax highlight, trees)
- **Flags:** `--json`, `--plain`, `--no-color`
- **Exit codes:** 0=sucesso, 1=erro geral, 2=uso inválido, 3=Server indisponível, 4=config erro, 5=plugin erro

---

## 10. Erros / Exit Codes

| Code | Significado |
|---|---|
| 0 | Sucesso |
| 1 | Erro genérico não categorizado |
| 2 | Uso inválido (args, flags) |
| 3 | Server indisponível / timeout |
| 4 | Configuração inválida / ausente |
| 5 | Plugin não encontrado / erro de carregamento |
| 6 | Domínio: entidade não encontrada |
| 7 | Domínio: regra de negócio violada |
| 8 | IO: filesystem / permissão |
| 9 | C++ engine: comunicação falhou |

---

## 11. Lifecycle

### 11.1 Bootstrap

```
coffee (entry point)
    ↓
CoffeeApplicationRuntime.init()
    ↓
Config.load() → validação
    ↓
PluginSystem.discover() → carrega plugins habilitados
    ↓
PluginSystem.register_commands() → CLI router
    ↓
Command execution
    ↓
CoffeeApplicationRuntime.stop() [try/finally]
```

### 11.2 Plugin Lifecycle

```
discover (entry points / plugin dirs)
    ↓
load (import plugin.py)
    ↓
validate (contract compliance)
    ↓
register (commands, ports, config schema)
    ↓
initialize (opcional: setup connections, cache)
    ↓
ready
    ↓
shutdown (opcional: cleanup) — no Runtime.stop()
```

---

## 12. Extensibilidade

### 12.1 Plugin Contract (MÍNIMO)

```python
# plugin.py
from coffee.core.plugin import Plugin, PluginMetadata

class MyPlugin(Plugin):
    metadata = PluginMetadata(
        name="my-plugin",
        version="1.0.0",
        description="...",
        author="...",
        dependencies=[],  # outros plugins requeridos
        provides=["command:my-cmd", "port:MyPort"],  # capabilities
    )

    def register(self, registry: PluginRegistry) -> None:
        registry.add_command(MyCommand())
        registry.add_port(MyPort, MyAdapter())
        registry.add_config_schema(MyConfigSchema)
```

### 12.2 Discovery

- Entry points: `coffee.plugins` em `pyproject.toml`
- Diretório local: `~/.config/coffee/plugins/`
- Project-local: `./.coffee/plugins/`

---

## 13. Integração Futura com C++

### 13.1 Fronteira

```
Python (CLI Core)
    │
    ├── Plugin System
    ├── Domain
    ├── Ports
    └── Adapters (Server, Local FS, Git, etc.)
            │
            ▼
    ┌─────────────────────┐
    │  NativeCapability   │  ← Port abstrato
    └─────────────────────┘
            │
            ▼
    ┌─────────────────────┐
    │  CppEngineAdapter   │  ← Adapter concreto
    └─────────────────────┘
            │
            ▼ IPC (JSON/stdin-stdout? gRPC?)
    ┌─────────────────────┐
    │  C++ Engine Process │
    └─────────────────────┘
```

### 13.2 Responsabilidades Iniciais (quando necessárias)

- System diagnostics avançado
- Hardware enumeration
- Secure Boot / UEFI / TPM
- Container runtime ops
- Filesystem ops alta performance

---

## 14. Critérios de Qualidade (Definition of Done)

### 14.1 Código

- [ ] `mypy --strict` passa (ou config explícita)
- [ ] `ruff` / `black` formatado
- [ ] Testes unitários: domain, services, adapters ≥ 80% coverage
- [ ] Testes de integração: CLI commands principais
- [ ] Testes de contrato: plugin interface, ports

### 14.2 Arquitetura

- [ ] Domain não importa infraestrutura (HTTP, Rich, C++, etc.)
- [ ] Plugins carregam independentemente
- [ ] Runtime decorator funcional com `try/finally`
- [ ] `getContainer` (corrigido) expõe dependências
- [ ] ModuleManager **não** tem `@CoffeeApplicationRuntime`

### 14.3 UX

- [ ] `coffee --help` claro e organizado
- [ ] Output Rich por default, `--json` para automação
- [ ] Mensagens de erro acionáveis (sugestões, docs links)
- [ ] `coffee system doctor` executa checks relevantes
- [ ] Startup time < 200ms (sem Server), < 500ms (com Server)

### 14.4 Documentação

- [ ] `docs/doc.md` atualizado
- [ ] ADRs para decisões tomadas
- [ ] README com instalação, uso rápido, arquitetura
- [ ] Plugin development guide

---

## 15. Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| Framework CLI não decidido | Alta | Bloqueia implementação | Decidir ADR 003 esta semana |
| Plugin system complexo | Média | Atraso V1 | Começar simples: registry + entry points; evoluir |
| Server indisponível quebra CLI | Média | UX ruim | Offline-first design; local fallback |
| C++ engine protocol indefinido | Média | Bloqueia engine | Definir ADR 004 antes de precisar |
| Config format muda | Baixa | Migração chata | TOML + schema validation; version config |
| ClickUp migration complexa | Média | Dados perdidos | Export script + validação + rollback plan |

---

## 16. Próximos Passos Imediatos

1. [ ] **ADR 003:** Definir framework CLI (Click vs Typer vs Rich vs Custom)
2. [ ] **ADR 004:** Definir protocolo Python ↔ C++
3. [ ] **ADR 006:** Definir contrato de Plugin (interface, metadata, discovery)
4. [ ] **ADR 007:** Definir formato de configuração (TOML/YAML/Python)
5. [ ] Implementar `CoffeeApplicationRuntime.__call__` (decorator funcional)
6. [ ] Corrigir `getContener` → `getContainer`
7. [ ] Remover `@CoffeeApplicationRuntime` de `ModuleManager`
8. [ ] Estruturar `src/coffee/core/plugin/` + `src/coffee/plugins/`
9. [ ] Implementar plugin `task` com domain + port + adapter (local JSON file first)
10. [ ] Implementar CLI router com framework escolhido
