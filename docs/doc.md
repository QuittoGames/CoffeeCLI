# Coffee CLI — Documentação Técnica Principal

**Versão:** 0.3.1
**Status:** FACT (verificado por execução/análise de código) + INFERENCE (onde a evidência é indireta) + PROPOSAL (intenção documentada, não implementada) + UNKNOWN (contexto insuficiente)
**Última atualização:** 2026-09-29
**Base de evidência:** task context do `codebase-explorer` — `.agents/protocol/tasks/temp/docs-main-technical-context.md`, HEAD `cb2b812` — **atualizado por leitura direta em 2026-09-28** após (a) renomeação de typos no código e (b) evolução do Container/`Dependency` posteriores ao relatório do explorer; **atualizado em 2026-09-29** após refatoração de tipos `SystemModule` → `CoffeeComponent` no decorator `@Component` (§4.5, §16.11).
> **CONFLICT registrado (2026-09-29):** a linha "base de evidência" desta doc citava `.agents/protocol/docs/codebase-explorer.json` (report global) — **arquivo inexistente** (FACT; o diretório `protocol/docs/` nunca foi criado). A citação foi corrigida; o único artefato do explorer é o task context acima, que está **STALE** (gerado em `cb2b812`, pré-rename e pré-refatoração).

> **Legenda de classificação** (usada em todo o documento):
> `FACT` = suportado diretamente por código/execução · `INFERENCE` = inferência forte a partir de evidência · `PROPOSAL` = intenção documentada, não implementada · `UNKNOWN` = contexto insuficiente.
> Confiança: HIGH / MEDIUM / LOW.

> **DECISION (DEV · 2026-09-28):** **`docs/doc.md` é a fonte documental principal do projeto.** Quando outras docs (`runtime.md`, ADRs, specs) divergirem entre si ou deste documento, **doc.md prevalece**. Quando doc.md divergir do código, o conflito é registrado em §17 — código = estado atual, doc.md = referência documental canônica.

---

## 1. Overview

O Coffee CLI é a interface de linha de comando do ecossistema Coffee — uma camada pessoal de produtividade, desenvolvimento, automação, contexto e integração com IA. É a camada humana e o orquestrador local: **não é um segundo servidor** — o OS funciona sem Coffee.

**Estado real do código (FACT):** projeto em fase de skeleton. O núcleo de dados (`Config`), o contrato de domínio (`SystemModule`) e a fronteira de runtime (`CoffeeApplicationRuntime`) existem; o bootstrap **não completa** (ver §18), dois módulos **não importam** (ver §16.2), não há comandos CLI funcionais, não há testes e não há CI.

**Stack (FACT — `pyproject.toml`):** Python `>=3.11`, layout `src/`, setuptools, única dependência declarada `platformdirs`. Zero frameworks CLI (argparse puro).

---

## 2. Goals and Non-Goals

### 2.1 Goals (V1 — PROPOSAL)

- CLI unificada para: tasks, projects, Git, contexto, AI, system, machine, serviços, ferramentas de dev, automações.
- Operações locais independentes do Coffee Server.
- Arquitetura modular orientada a plugins/features.
- Python como linguagem principal; fronteira limpa para engine C++ futura.
- Clean Architecture: domain separado de implementações concretas.

### 2.2 Non-Goals (V1)

- Substituir o shell · ser um segundo servidor · tornar o sistema dependente do Coffee.
- Reproduzir ClickUp inteiro · usar Rust como linguagem principal · espalhar C++ pelo projeto.

---

## 3. Architecture

### 3.1 High-Level no ecossistema (PROPOSAL)

```
Coffee Interface
       │
       ├── Coffee CLI  ← este repositório
       └── outras UIs
              │
        Coffee Server  (tasks, projects, context, AI)
              │
     Local System Layer (Fedora / Windows)
```

### 3.2 Código atual (FACT — árvore verificada)

```
src/coffee/
├── main.py                            # bootstrap: decorator + asyncio.run + Start()
├── core/
│   ├── __main__.py                    # VAZIO (0 bytes)
│   ├── cli/
│   │   └── CLI.py                     # RuntimeCLI (argparse) — NÃO IMPORTA (§16.2)
│   ├── data/
│   │   ├── Config.py                  # dataclass Config + build() que sempre lança
│   │   └── Host.py                    # dados de host (username, platform)
│   ├── domain/
│   │   ├── exceptions/
│   │   │   └── InvalidCoffeeApplicationException.py
│   │   ├── interface/SystemModule.py  # ABC de módulos (contrato de domínio)
│   │   └── models/
│   │       └── Dependency.py          # registro de dependência (classe intermediária de DI)
│   ├── runtime/
│   │   ├── CoffeeApplicationRuntime.py    # lifecycle + decorator de entrada
│   │   ├── components/
│   │   │   ├── Component.py           # decorator @Component
│   │   │   ├── ModulePackage.py       # decorator @Module
│   │   │   └── base/                  # CoffeeComponent (ABC) + CoffeeRegistry (ABC stub)
│   │   └── container/
│   │       ├── CoffeeApplicationContainer.py   # composição + DI (systemModules/dependencies)
│   │       └── DefaultCoffeeRegistry.py        # catálogo de componentes
│   └── services/
│       ├── tool.py                    # utilitários (clear, verify_modules, add_path_modules)
│       └── module/ModuleManager.py    # serviço de módulos — NÃO IMPORTA (§16.2)
└── modules/
    ├── ssh/package.py                 # SSHModule (@Module) — sem consumidores
    ├── system/ , update/              # __init__ vazios
```

Diretórios vazios sem código (FACT): `egine/` (nome UNDEFINED), `modules/ssh/{Adpiter,models,Services}/`.

> **Nota sobre typos (atualização 2026-09-28):** os typos de pasta/arquivo (`contener`, `componets`, `CoffeAplication`, `exepiton`, `Services/`, `CofeeRegistry`, `Componet`, `Dependecy`) vêm do **skeleton original do DEV** (`1b938f2`) — **não** são criação da IA. Foram **corrigidos por instrução do DEV em 2026-09-28** (§16.10); o histórico de typos permanece documentado em §16. As docs históricas (`runtime.md`, ADRs, specs) ainda citam os caminhos antigos — ver §17.

### 3.3 Grafo de dependências internas (FACT)

```
main ──► {Config, tool, CoffeeApplicationRuntime, InvalidCoffeeApplicationException}
CoffeeApplicationRuntime ──► {Config, CoffeeApplicationContainer}
CoffeeApplicationContainer ──► {Config, SystemModule, DefaultCoffeeRegistry}
@Component / @Module ──► DefaultCoffeeRegistry
CLI ──► {Component, ModuleManager, Config}
ModuleManager ──► {Component, SystemModule}
tool ──► {Config, os/subprocess/sys}
Config ──► {Host, platformdirs}
```

Callers reais (grep): `Container.get()` e `Runtime.getContainer()` **não têm chamadores** fora do próprio runtime/main (FACT).

### 3.4 Arquitetura alvo (PROPOSAL — não implementada)

```
src/coffee/
├── core/            # núcleo estável: runtime/, config/, plugin/, domain/, ports/
├── plugins/         # features como plugins (task/, project/, git/, context/, ...)
├── engine/ (ou native/)  # C++ nativo, isolado
├── cli/             # entry, command routing, output
└── main.py          # bootstrap
```

---

## 4. Modules

### 4.1 `coffee.main` — bootstrap (FACT)

**Arquivo:** `src/coffee/main.py`

- `config_local = Config()` criado no **escopo de módulo** (linha 9) — um `Config` paralelo ao que o runtime cria internamente.
- `@CoffeeApplicationRuntime` decora `async def main(app)` (16-17): após o decorator, `main` deixa de ser função e vira **instância** de `CoffeeApplicationRuntime` (verificado por execução).
- `Start()` (12-13) chama `tool.menu()` — **não existe** (`hasattr(tool, 'menu') == False`, FACT).
- `if __name__ == "__main__"` (31-33): `asyncio.run(main())` → `Start()`.

**Falha observada (FACT — verificado):** `asyncio.run(main())` → `init()` → `Config().build()` → `RuntimeError` antes do corpo de `main`; `Start()` é inalcançável. Defeitos adicionais: `tool.verify_modules()` é `async` chamado sem `await` (20); condição `if not (app or app.getContainer())` (22) nunca dispara. (O typo da mensagem `"StopAsycnInteration"` foi corrigido em 2026-09-28 — §16.10.)

### 4.2 `core.data` — Config e Host (FACT)

**Arquivo:** `src/coffee/core/data/Config.py`

```python
@dataclass
class Config:
    configPath: Path = Path(user_config_dir("Coffee"))
    hostData: Host = field(default_factory=Host)
    Debug: bool = False
    modules_local: list[str] | None = None

    def build(self) -> Config:
        if not (self.configPath.exists() and os.path.isdir(...)): raise RuntimeError()
        if not self.hostData.platform == None:   # condição invertida
            raise RuntimeError()
        return self
```

- `configPath` resolve via platformdirs — no Windows observado: `C:\Users\Quitto\AppData\Local\Coffee`; o harness §35 documenta `~/.config/Coffee/` (diferença Unix/platformdirs).
- **`build()` sempre lança (FACT — verificado):** `Host.platform = system()` nunca é `None`, então a linha 21-22 dispara sempre e `return self` (24) é inalcançável. **A condição invertida já existe no skeleton do DEV** (`1b938f2`) — autoria do bug: UNKNOWN/provável DEV; o agente corrigiu outros pontos (`os.path.isdir`, `return self`, imports) e **manteve** a condição.
- `RuntimeError()` é lançado **sem mensagem**.

### 4.3 `CoffeeApplicationRuntime` — fronteira de lifecycle (FACT + INFERENCE sobre autoria)

**Arquivo:** `src/coffee/core/runtime/CoffeeApplicationRuntime.py` (renomeado de `CoffeAplicationRuntime.py` em 2026-09-28)

**O que é (FACT):** classe que combina duas coisas:

1. **Estado estático de aplicação** — `_container` (atributo de classe), `init()` (16-25) cria `Config().build()` + `CoffeeApplicationContainer`; `getContainer()` (27-32) retorna o container ou lança `RuntimeError`; `setConfig()` (34-36); `stop()` (38-41) zera `_container` e retorna `True`.
2. **Decorator de lifecycle** — `__init__(func)` (13-14), `__call__` (43-74), `_invokeAsync` (76-84).

**Comportamento do decorator (FACT — verificado por execução):**

```python
@CoffeeApplicationRuntime        # e também @CoffeeApplicationRuntime()
async def main(app: CoffeeApplicationRuntime): ...
```

- Aceita as duas formas (factory em 55-60); args/kwargs na chamada → `TypeError`.
- Sync: `init()` → `func(self)` → `finally stop()`.
- Async: retorna coroutine → `init()` → `await func(self)` → `finally stop()`.
- Injeta `self` (a instância runtime) como argumento do ponto de entrada.

**Limitações verificadas (FACT):**

- `init()` está **fora** do `try` nas duas rotas (70-74 e 77-84): se `init()` falhar (como falha hoje — §4.2), `stop()` **não roda** — a garantia de `try/finally` documentada em `runtime.md:307` não se sustenta.
- **Hoje o corpo do ponto de entrada nunca executa** porque `init()` lança.

**Marcas de autoria (INFERENCE · confiança MEDIUM-HIGH — agente, commit `dad3b2d`, lote 2026-09-25 22:27):**

- Docstring cita **`runtime.md §12.3`** (linha 46) — `runtime.md` **não tem §12.3** → referência documental que não existe, usada para justificar código.
- Mistura de idiomas: docstring em PT, mensagens de `TypeError` em EN (60, 63-65).
- Comentário de fase em voz de agente: `# ... ainda estamos na fase de factory.` (56).

**Conflitos registrados:**

- `runtime.md:410` e `doc.md` (versão anterior) diziam "**decorator NÃO implementado**" → hoje existe → CONFLICT (doc desatualizada, agora corrigida aqui).
- `runtime.md:526-531` prevê "1 Runtime → 1 Container"; `_container` é **singleton de classe** → divergência de modelo.
- `runtime.md:410` ainda usa o typo `getContener` × código `getContainer` (já corrigido no código).

### 4.4 `container` — Container: módulos externos, composição e DI via `Dependency` (FACT)

**`CoffeeApplicationContainer`** (`runtime/container/CoffeeApplicationContainer.py`)

O Container é a **composition root** do runtime: guarda o `Config`, mantém o catálogo vivo de **módulos externos** e controla a **inversão de dependência** por meio de uma classe intermediária `Dependency`.

#### 4.4.1 Estado (linhas atuais do arquivo)

```python
class CoffeeApplicationContainer:
    def __init__(self, config: Config):
        self.config = config
        self.dependencies: list[Dependency] = []      # registros de DI (12)
        self.systemModules: list[SystemModule] = []   # módulos externos (13)

    def _create(self, dependency: type) -> None: ...  # 15-36 — reflete e descreve
    def get(self, component: type): ...               # 38-44 — resolve via registry
    def getConfig(self) -> Config: ...                # 46-47
    def setConfig(self, config: Config) -> None: ...  # 49-50
```

#### 4.4.2 Controle dos módulos externos (`SystemModule`)

- `systemModules: list[SystemModule]` (13) é o ponto onde o Container deve **receber e controlar os módulos externos** — implementações do contrato `core.domain.interface.SystemModule` (ex.: `SSHModule` em `modules/ssh/package.py`), que é a ABC com `id/name/version` (§4.8).
- **Estado (FACT):** a lista existe, mas hoje **não tem escritor nem leitor** (grep: única ocorrência é a própria definição) — o registro real de módulos ainda acontece no `DefaultCoffeeRegistry` (§4.4.4), e o `ModuleManager` não a alimenta. A integração `systemModules` × registry × `ModuleManager` é o gap de ligação atual.

#### 4.4.3 Inversão de dependência via classe intermediária `Dependency`

**`Dependency`** (`core/domain/models/Dependency.py`, renomeado de `Dependecy.py`):

```python
@dataclass
class Dependency:
    id: UUID = uuid4()
    name: str = field(default_factory=str)
    classImpl: type | None = None
```

**Design (intenção — INFERENCE MEDIUM, sustentada pelo código):** em vez de instanciar direto, o Container primeiro **descreve** cada dependência de um componente como um registro `Dependency` (nome do parâmetro + tipo/concreção `classImpl` + identidade `id`). A classe intermediária serve como contrato comum entre:

```text
_create(cls)                       fase de DESCRIBE
    │  reflecte cls.__init__ (inspect.signature)
    │  para cada parâmetro (além de self):
    │      dep = Dependency(name=parameter.name,
    │                       classImpl=parameter.annotation)
    │      dedupe → self.dependencies.append(dep)
    ▼
self.dependencies: list[Dependency]   catálogo de dependências declaradas
    │
    │  (fase de RESOLVE — ainda NÃO implementada)
    ▼
get(component) → registry.get(cls) → cls()   hoje: instancia sem injetar
```

**Análise do estado atual (FACT):**

1. **Describe parcialmente implementado:** `_create` (15-36) reflete a assinatura, cria `Dependency` e deduplica por igualdade de dataclass (35-36). **Nunca é chamado por ninguém** (grep) — nenhum fluxo invoca `_create` hoje.
2. **Resolve ausente:** `get()` (38-44) resolve o `implementation` no registry e chama `implementation()` **sem injetar nada** — os `dependencies` declarados não são consumidos. Componentes com `__init__` exigindo argumentos (ex.: `RuntimeCLI(moduleManager, config)`) continuam falhando.
3. **Debug em produção:** `print` dos parâmetros em `_create` (25-29) — código de biblioteca não deveria escrever em stdout (devia ser logging ou sair antes da entrega).
4. **Anomalia no `id` (FACT):** `id: UUID = uuid4()` é avaliado **uma única vez** na criação da classe — toda `Dependency` criada sem `id` explícito recebe o **mesmo UUID** (o default não é `default_factory`). Isso quebra a unicidade que o campo sugere e afeta o dedupe por igualdade.
5. **Edge case:** parâmetros sem anotação produzem `classImpl = inspect.Parameter.empty` (não `None`), divergindo do contrato `type | None`.
6. `get()`/`_create()` **não têm chamadores** fora da própria classe (FACT, grep).

> **Autoria (INFERENCE):** `_create`/`dependencie` não existiam no skeleton (`6cf711c` → `d326b2d`, agente); a versão atual com `Dependency`/`systemModules` é **posterior ao relatório do explorer** e de autoria DEV/agnóstica — UNKNOWN.

#### 4.4.4 `DefaultCoffeeRegistry` (`container/DefaultCoffeeRegistry.py`)

- Dois dicts de classe: `components: dict[type, type]` (registro de classes) e `moduleRegistry: dict[str, SystemModule]` (renomeado de `moduleRegestry`; **sem nenhum leitor externo**).
- API `@classmethod`: `register`, `packageRegister` (acessa `module.id`), `contains`, `get`, `getModule`, `all`.

**Registry duplicado (FACT):** existem **duas classes homônimas `CoffeeRegistry`**: a funcional `DefaultCoffeeRegistry` (em `container/DefaultCoffeeRegistry.py`) e o stub ABC `CoffeeRegistry` (em `components/base/CoffeeRegistry.py`, com `@dataclass` sobre ABC, `TypeVar` como atributo, `abstractmethod` sem uso) — questão aberta em `components-aop.md:107,116`.

### 4.5 `components` — decorators de componentes e módulos (FACT)

**`Component.py`** (renomeado de `Componet.py`; classe `Component`):

```python
registry = DefaultCoffeeRegistry()

def Component(component: CoffeeComponent) -> CoffeeComponent:   # refatorado em 2026-09-29 (§16.11)
    registry.packageRegister(component)   # exige .id
    return component
```

- **`Component` chama `packageRegister`, que faz `moduleRegistry[module.id]`** — classes decoradas **sem atributo `id`** explícito lançam `AttributeError` no momento do import.
- Anomalias: `registry = DefaultCoffeeRegistry()` instanciado apesar de todos os métodos serem `@classmethod`; assinatura `Component(component: CoffeeComponent) -> CoffeeComponent` usada como decorator de classe (recebe **classes**, não instâncias).
- **MISMATCH estático intencional (FACT, 2026-09-29):** `packageRegister` continua com `bound=SystemModule` (registry é orientado a **módulos** — `moduleRegistry`/`.id` são conceito de `SystemModule`), então Pylance sinaliza a chamada `packageRegister(component)` em `Component.py`. **DECISION (DEV, 2026-09-29): manter `packageRegister` no decorator** — `packageRegister` representa os módulos de `modules/` carregados no container; a anotação `type` simples fica reservada para eventual migração do decorator. O mismatch é a manifestação estática do defeito de runtime (§16.2), que permanece aberto (`TODO:53`).

**`ModulePackage.py`**: `Module(module)` → `registry.register(module)` → `components[cls]` — este caminho não exige `.id` e funciona.

**Regressão do `@Component` (FACT comportamento + INFERENCE HIGH autoria agente):** `6cf711c` criou `Componet.py` já com `packageRegister`, substituindo o `register()` funcional do skeleton. Consequência verificada: importar `coffee.core.services.module.ModuleManager` ou `coffee.core.cli.CLI` → `AttributeError: type object 'ModuleManager' has no attribute 'id'`. (Arquivo renomeado para `Component.py` em 2026-09-28 — o defect é de **semântica**, não de nome.)

### 4.6 `core.cli.CLI` — parser argparse (FACT)

**Arquivo:** `src/coffee/core/cli/CLI.py`

- `@Component class RuntimeCLI` (7-8) com `__init__(moduleManager, config)` e `buildParser()` que cria `ArgumentParser(prog="coffee")`.
- `_addSubparsers()` (21-23) = `for ...: pass` — vazio; `buildParser` **não tem chamador**.
- **Não importa hoje** (herda a falha do `@Component` via `ModuleManager`).
- **CONFLICT:** `doc.md` (versão anterior):174 e `runtime.md:467` diziam que `CLI.py` usa `@CoffeeApplicationRuntime` → hoje usa `@Component`.
- Autoria (INFERENCE MEDIUM): `6cf711c` acrescentou `RuntimeCLI`/`__init__`/`_addSubparsers`; `b0c4c49` removeu uma herança inválida e arrumou imports. `@Component` é do skeleton.

### 4.7 `core.services` — ModuleManager e tool (FACT)

**`ModuleManager`** (`services/module/ModuleManager.py`): `@dataclass @Component class ModuleManager` com `_modulesRegistry` e `loadModules()`.

- `@Component` é do **skeleton**; a **quebra** é do agente (mudança de semântica do registry em `6cf711c`) → import falha (§4.5).
- **CONFLICT:** `doc.md`:86,166,373, `runtime.md:468`, `STATE.md:91` e ADR 001:37 dizem que tem `@CoffeeApplicationRuntime` (violação de lifecycle) → hoje tem `@Component`. ADR 007 (DECIDED) prevê constructor injection via composition root — não implementado.

**`tool`** (`services/tool.py`): dataclass com `@staticmethod`s:

- `clear_screen()` — `os.system("cls"/"clear")`.
- `verify_modules()` (async) — roda `pip install -r Services/requirements/requirements.txt`; **o arquivo não existe** (Test-Path = False) → exceção capturada + print.
- `add_path_modules(config)` (async) — `sys.path.append` dinâmico por `config.modules_local`; nunca chamado.

> **Autoria (INFERENCE MEDIUM-HIGH — agente):** `b366df4` trocou import de módulo inexistente por `Config` + `@staticmethod`; `6cf711c` moveu de `src/tool.py`.
> **Superfície de segurança conhecida** (harness §37): pip install no boot e `sys.path.append` — registrar, não corrigir silenciosamente.

### 4.8 `core.domain` — contratos (FACT)

- **`SystemModule`** (`domain/interface/SystemModule.py`): ABC com `id/name/version` (properties), herda `CoffeeComponent`. É o contrato dos módulos do sistema.
- **`InvalidCoffeeApplicationException`** (`domain/exceptions/`): usada em `main.py:23`.
- **`Dependency`** (`domain/models/Dependency.py`): classe intermediária de DI do Container (§4.4.3).
- **`domain/models/`**: `Module.py` foi deletado em `6cf711c`; hoje contém apenas `Dependency.py`. O `SSHModule` **não** subclasseia `SystemModule` (ver §4.9).

### 4.9 `modules` — features (FACT)

- `modules/ssh/package.py`: `@Module class SSHModule` (dataclass com atributos de classe) — registrado em `components`, **sem consumidor** e fora do contrato `SystemModule`.
- `modules/system/`, `modules/update/`: `__init__` vazios.

---

## 5. Domain Model

### 5.1 Entidades centrais (PROPOSAL — baseada em conversa/spec)

| Entidade | Descrição | Status |
|---|---|---|
| Task | Unidade executável | PROPOSAL |
| Project | Iniciativa/estrutura contínua | PROPOSAL |
| Repository | Git repository vinculado | PROPOSAL |
| Machine | Máquina gerenciada | PROPOSAL |
| Context | Contexto resolvido para IA | PROPOSAL |
| Module/Plugin | Feature extensível | FACT parcial (`SystemModule`, `@Module`) |
| Dependency | Registro de dependência — classe intermediária de DI do Container (§4.4.3) | FACT parcial (`domain/models/Dependency.py`) |

### 5.2 Regras de domínio

- Domain **não** conhece: ClickUp, PostgreSQL, HTTP, Rich/TUI, Fedora, C++.
- Dependências externas via **contracts/ports → adapters**.

---

## 6. Data Flow e Application Flow

### 6.1 Fluxo instalado (quebrado) — FACT

```
coffee (shell)
  → pyproject.toml:20 → coffee.cli.main:main → ModuleNotFoundError
    (não existe src/coffee/cli/)
```

### 6.2 Fluxo de execução direta (FACT — verificado)

```
import coffee.main
  → config_local = Config()                      (main.py:9)
  → @CoffeeApplicationRuntime vira instância      (main.py:16)
python main.py / __main__
  → asyncio.run(main())                          (main.py:32)
  → CoffeeApplicationRuntime.__call__ (43)
  → _invokeAsync (76)
  → init() (16) → Config().build() (21) → RuntimeError('')   ← FALHA AQUI
     (Container nunca criado; try/finally não alcançado;
      _invokeAsync: init() fora do try em 77 → stop() não roda)
  → Start() → tool.menu()                        ← inalcançável; menu não existe
```

### 6.3 Fluxo de registro de componentes (se os imports funcionassem) — FACT

```
import decorado
  → @Component → packageRegister → moduleRegistry[id]   (quebra p/ classes sem .id)
  → @Module    → register        → components[cls]
Runtime.init() → Container(config)
Container.get(T) → registry.get(T) → T()          (sem DI)
```

### 6.4 Lifecycle alvo documentado (PROPOSAL)

```
EntryPoint → Runtime → init() → Config.build() → Container → serviços → stop() em try/finally
```
(`runtime.md:227-243`; bootstrap com plugins em `specs/coffee-cli-v1.md` §11.1 — não implementado.)

---

## 7. Configuration and Persistence

- **Config real (FACT):** apenas o dataclass `Config` (§4.2). **Zero leituras/escritas de arquivo** em `src/coffee` (grep: sem `open(`, `json`, `toml`, `yaml`, `read_text/write_text`) — nenhum arquivo de config é lido ou escrito hoje.
- **Estado:** não existe camada de estado. `Debug`/`modules_local` são lidos só por `main.py:19` e `tool.add_path_modules` (nunca chamado).
- **Caminhos platformdirs (FACT):** config `user_config_dir("Coffee")`; data/cache previstos em `doc.md` §9 (não usados).
- **Formato (PROPOSAL/UNDEFINED):** harness §35 diz "formato: UNDEFINED DECISION"; a spec §8.1 propõe `coffee.toml` com precedência `args > ./coffee.toml > ~/.config/coffee/coffee.toml > /etc/coffee/ > defaults` (ADR pendente).

---

## 8. APIs

### 8.1 CLI commands (PLANNED)

```
coffee task add/list/inbox/today/next/done
coffee project create/list
coffee git status/log/diff
coffee context get/resolve
coffee system info/doctor
coffee machine export/doctor/bootstrap
coffee ai <subcommand>
```

Nenhum implementado (FACT): framework CLI é decisão aberta (`docs/research/cli-framework-comparison.md`), `_addSubparsers` vazio.

### 8.2 Coffee Server Interfaces (PLANNED)

REST (geral) · MCP (agentes IA) · WebSocket/events (realtime) · capability layer: `task.read`, `task.create`, `project.read`, `context.resolve`, `machine.inspect`, `event.publish`.

---

## 9. Error Handling

**Exceções atuais (FACT):** `InvalidCoffeeApplicationException` (uso apenas em `main.py`); `RuntimeError` sem mensagem em `Config.build()`; `RuntimeError` em `Runtime.getContainer()`; `LookupError` em `Container.get()`; `NotImplementedError` em `Container._create`; `TypeError` no decorator.

**Estratégia alvo (PROPOSAL):** domain exceptions para regras de negócio; infra exceptions isoladas em adapters; exit codes padronizados; structured logging.

---

## 10. Security

- **Superfícies conhecidas (FACT — harness §37, registrar, não corrigir aqui):** `tool.py` (pip install no boot, `sys.path.append`), `Config`/`Host` usando `os`/`platform` fora de adapter.
- **Visão alvo (PROPOSAL):** SELinux/firewalld/SSH hardening; secrets fora do código (config/environment); containers (Podman/Docker) para isolamento.

---

## 11. Concurrency

- `asyncio` para I/O bound (API, filesystem, subprocess) — já presente no design de `main`/`tool`.
- ThreadPoolExecutor para CPU bound se necessário.
- Engine C++ (PLANNED): processo separado + JSON/stdin-stdout (ADR 004, PROPOSAL).

---

## 12. External Integrations

| Integração | Tipo | Status |
|---|---|---|
| Coffee Server | REST/MCP/WS | PLANNED |
| Git | subprocess/local | FACT parcial |
| Filesystem | stdlib | FACT |
| System (Linux/Windows) | subprocess/psutil | PLANNED |
| AI (OpenCode etc.) | MCP/HTTP | PLANNED |
| VS Code / Obsidian / Quarto | MCP/extensão/parser/subprocess | PLANNED |

---

## 13. Testing Strategy

**Estado (FACT):** **zero testes** — sem `tests/`, sem `test*.py`, sem `[tool.pytest]`, sem CI. Validação real disponível: `compileall` (sintaxe) e import por módulo — este **falha** em 2 módulos (§16.2).

**Estratégia alvo (PROPOSAL):** unit (domain/services/adapters, pytest) → integration (CLI commands, comunicação Server) → contract (plugin interface, ports) → E2E (task CRUD, project, context) → property-based (config parsing, invariants). TODO TASK-005: check de `python -m compileall src` quando houver CI.

---

## 14. Deployment

- **CLI (PLANNED):** `pipx install coffee-cli` / `pip install coffee-cli`; entry point `coffee = coffee.cli.main:main` (**quebrado** — §16.9); futuro binary via PyInstaller/Nuitka.
- **Server (projeto separado, PLANNED):** container + systemd + health checks.

---

## 15. Operational Considerations

- **Offline-first:** operações locais funcionam sem Server.
- **Doctor/diagnostic, recovery, dual boot, backup:** previstos na spec (PROPOSAL).

---

## 16. Análise especial — trechos escritos fora do escopo (violação DEV + AGENT)

> **Contexto (relato do DEV):** o agente, em loop, escreveu/reescreveu trechos que **fugiram do escopo** porque havia erros no código do DEV. Esta seção registra cada trecho, o que ele faz hoje e as anomalias — sem corrigir nada de lógica (exceto a **correção de typos autorizada pelo DEV em 2026-09-28**, registrada em §16.10).
> **Linha de base de autoria:** skeleton DEV `1b938f2`; lote de commits de agente em 2026-09-25 22:27 (`b0c4c49`, `10fbefd`, `dad3b2d`, `d326b2d`, `d5092f2`, `b366df4`, `0d8fe94`) e `6cf711c`.

### 16.1 `CoffeAplicationRuntime.py` — decorator de lifecycle (o caso citado)

> Renomeado em 2026-09-28 para **`CoffeeApplicationRuntime.py`** (§16.10). Os trechos abaixo referem-se ao arquivo/conteúdo da época dos commits citados.

| Campo | Valor |
|---|---|
| Trecho | `__init__(func)` (13-15), `__call__` (43-74), `_invokeAsync` (76-84) |
| Class | INFERENCE (autoria) · **confiança MEDIUM-HIGH — agente** |
| Commit | `dad3b2d` |

- **Comportamento observável (FACT):** transforma a função decorada numa instância de `CoffeeApplicationRuntime`; aceita `@X` e `@X()`; executa `init → entry → stop (finally)`; injeta `self` no ponto de entrada; sync e async.
- **Marcas de geração por agente:** docstring cita `runtime.md §12.3` (46) — **seção inexistente**; PT na docstring × EN nos `TypeError`; comentário `# ... fase de factory` (56).
- **Defeitos do trecho (FACT):** `init()` fora do `try` em ambas as rotas → `stop()` não roda se `init()` falhar; na prática atual, o ponto de entrada **nunca executa** porque `Config.build()` lança (§4.2).
- **Por que fugiu do escopo (INFERENCE):** a doc (`runtime.md:410`, `doc.md` anterior) dizia "decorator não implementado" e `STATE.md` lista "Implementar `__call__`" como tarefa de agente — o agente implementou sem o fluxo de decisão do DEV, gerando código conflitante com a própria doc.
- **Callers:** apenas `main.py:4,16,17`. Referências em docs: `runtime.md` §3/§5.4/§7/§8, ADR 001, `specs/coffee-cli-v1.md:214,541,551`, `diagrams/architecture.mmd:69-74`.

### 16.2 `Componet.py` — regressão do `@Component` (quebra 2 imports)

> Renomeado em 2026-09-28 para **`components/Component.py`** (registro agora em `container/DefaultCoffeeRegistry.py`).

| Campo | Valor |
|---|---|
| Trecho | `Componet.py:10-12` + semântica de `CofeeRegistry.py:16-19` (nomes da época) |
| Class | FACT (comportamento) + INFERENCE HIGH (autoria agente) |
| Commit | `6cf711c` (criou `Componet.py` "new file" já com `packageRegister`) |

- **Comportamento (FACT — verificado em 2026-09-28, pós-rename):** `import coffee.core.services.module.ModuleManager` e `import coffee.core.cli.CLI` → `AttributeError: type object 'ModuleManager' has no attribute 'id'`. **2 módulos do projeto não importam.**
- **Mecanismo:** `Component()` → `packageRegister(cls)` → `moduleRegistry[cls.id]` — classes decoradas não têm `id` de classe (`SystemModule.id` é property de **instância**).
- **Anomalias:** arquivo `Componet.py` × classe `Component` (corrigido no rename); `TypeVar` sem uso (**corrigido em 2026-09-29** — §16.11); `registry` instanciado à toa; duas classes `CoffeeRegistry` homônimas (§4.4.4).
- **Registro:** `docs/TODO.md:53` (OUT-OF-SCOPE FINDING).

### 16.3 `CoffeeApplicationContainer.py` — de `dependencie` morto à DI via `Dependency`

| Campo | Valor |
|---|---|
| Trecho original | `dependencie: list[SystemModule]` + `_create` com `print` + `NotImplementedError` |
| Class | INFERENCE · MEDIUM-HIGH — agente (`6cf711c` → `d326b2d`); versão atual com `Dependency` = **UNKNOWN** (posterior ao relatório do explorer) |

- **Versão original (agente):** `dependencie` nunca lido; `_create` imprimia params e lançava `NotImplementedError`; typos `dependencie/dependecy`. Divergia de `runtime.md:404` ("container guarda apenas Config").
- **Versão atual (2026-09-28):** o DEV reescreveu o arquivo para `dependencies: list[Dependency]` + `systemModules: list[SystemModule]` + `_create` que reflete `__init__` e popula `dependencies` — **análise completa em §4.4** (design de DI via classe intermediária `Dependency`).
- **Anomalias que permanecem:** `print` de debug em `_create`; `_create` sem chamadores; `get()` sem resolution/injeção; `id: UUID = uuid4()` não-único (§4.4.3).
- **Imports junk removidos em 2026-09-28** (autorados por autocomplete, fora de escopo do rename mas claramente acidentais): `from ast import List`, `from pickletools import uint4`, `from tkinter import NO`, `from uuid import UUID` — todos unused; `tkinter` em core era risco de import.

### 16.4 `main.py` — estrutura DEV remendada por agente

- **Class:** estrutura DEV (`1b938f2`) + remendos do agente (`b0c4c49`: `data`→`Config`, re-root de imports) · INFERENCE MEDIUM-HIGH p/ remendos, FACT p/ estado atual.
- Defeitos verificados: `Start()` inalcançável → `tool.menu()` inexistente; `verify_modules()` sem `await`; condição `if not (app or ...)` nunca dispara. (Typo `"StopAsycnInteration"` corrigido em 2026-09-28 — §16.10.) Registro: `TODO:14,54`.

### 16.5 `CLI.py` e `ModuleManager.py`

- `6cf711c` acrescentou `class RuntimeCLI(Component)` com herança inválida (removida em `b0c4c49`), `__init__`, `_addSubparsers` (loop `pass`). Hoje: imports falham; `buildParser` sem chamador. CONFLICTs documentais listados em §4.6/§4.7.

### 16.6 `Config.build()` — bug preservado

- **AUTHORIA: UNKNOWN (provável DEV)** — a condição invertida `if not self.hostData.platform == None` já está no skeleton `1b938f2`. O agente corrigiu `os.path.isdir()`, re-rootou imports e adicionou `return self`/`modules_local`, **mantendo** a condição (FACT). Efeito: nenhum boot completa.

### 16.7 `tool.py`

- Remendos do agente (`b366df4`, `6cf711c`) trocaram import inexistente por `Config`. Hoje: requirements.txt alvo inexistente; `sys.path.append`. Risco auto-registrado: harness:1493-1504.

### 16.8 `__init__.py` ×10 e `.agents/state.json`

- **FACT — agente** (TODO TASK-001). `__init__.py` criados também em pacotes sem código. `state.json` (untracked) tem **encoding quebrado (mojibake)** e afirma `PASS - 33/33 módulos importam` → **CONFLICT** com o `AttributeError` verificado (§16.2).

### 16.9 Verificação dos erros estruturais citados em `AGENTS.md`

| Afirmação em AGENTS.md | Estado hoje | Class · Confiança |
|---|---|---|
| Entrypoint quebrado | **AINDA EXISTE** — `pyproject.toml:20` → `coffee.cli.main:main` inexistente | FACT · HIGH |
| Imports quebrados | **PARCIALMENTE CORRIGIDOS** — re-root `core.*`→`coffee.core.*` feito; hoje a falha é `AttributeError` em 2 módulos | FACT · HIGH (verificado) |
| "Arquivo de runtime sem extensão" | **NÃO ENCONTRADO** — nem em disco nem em todo o histórico git; `core/__main__.py` existe e está vazio (0 bytes) | UNKNOWN · questão ao DEV |
| — | `egine/` (pasta vazia, nome UNDEFINED) | FACT |

### 16.10 Correção de typos no código (2026-09-28, DECISION do DEV)

Instrução do DEV: *"ajuste os typos do code interno"*. Renomeação em cascata executada e validada:

| Antes (skeleton/agentes) | Depois | Escopo |
|---|---|---|
| `core/runtime/CoffeAplicationRuntime.py` | `core/runtime/CoffeeApplicationRuntime.py` | arquivo |
| `core/runtime/contener/` | `core/runtime/container/` | pasta |
| `contener/CofeeRegistry.py` | `container/DefaultCoffeeRegistry.py` | arquivo (igual à classe) |
| `core/runtime/componets/` | `core/runtime/components/` | pasta |
| `componets/Componet.py` | `components/Component.py` | arquivo |
| `core/domain/exepiton/` | `core/domain/exceptions/` | pasta |
| `exepiton/InvalidCoffeeAplicationException.py` | `exceptions/InvalidCoffeeApplicationException.py` | arquivo |
| `core/Services/` | `core/services/` | pasta (case-only; `git mv` em 2 passos por `core.ignorecase=true`) |
| `models/Dependecy.py` + classe `Dependecy` | `models/Dependency.py` + classe `Dependency` | arquivo + classe |
| `moduleRegestry` | `moduleRegistry` | identificador |
| `dependencie` | `dependencies` | identificador |
| `regitry` (`CoffeeComponent`) | `registry` | identificador |
| `"StopAsycnInteration"` (`main.py:28`) | `"StopAsyncIteration"` | string |

**Validação pós-rename (FACT):** `python -m compileall -q src` → exit 0 · import por módulo → **13/15 OK**, falhando apenas `CLI` e `ModuleManager` (bug `@Component` pré-existente, §16.2 — nenhuma regressão) · grep de todos os typos em `src/` → **zero ocorrências**.

**Fora do escopo deste rename (pendências separadas):** diretórios vazios `egine/` (nome UNDEFINED) e `modules/ssh/Adpiter/` — decisão em `TODO:55`; docs históricas (`runtime.md`, ADRs, specs, `components-aop.md`) ainda citam caminhos antigos (§17).

### 16.11 Refatoração de tipos `SystemModule` → `CoffeeComponent` no decorator `@Component` (2026-09-29)

| Campo | Valor |
|---|---|
| Instrução | DEV: `Component.py` aceitava `SystemModule` (contrato dos módulos externos de `modules/`); o tipo correto de componentes é `CoffeeComponent` |
| Escopo | tipagem + caches + docs — **sem mudança de comportamento** |
| Class | FACT (verificado por execução) |

**Mudanças:**

| Arquivo | Antes | Depois |
|---|---|---|
| `components/Component.py` | import `SystemModule`, `TypeVar("component", bound=SystemModule)`, `def Component(component: SystemModule) -> SystemModule` | import `CoffeeComponent`, **`TypeVar` morto removido** (+ import `typing`), `def Component(component: CoffeeComponent) -> CoffeeComponent` |
| `components/base/CoffeeRegistry.py` | import `SystemModule` + `T = TypeVar("T", bound=SystemModule)` (**nunca usado**) + `abstractmethod` unused | todos removidos (dead code) |

**Não mudou (usos legítimos de módulos externos):** `SystemModule.py` (contrato permanece), `ModuleManager` (`list[SystemModule]`), `CoffeeApplicationContainer.systemModules`, `DefaultCoffeeRegistry` (`bound=SystemModule` + `moduleRegistry: dict[str, SystemModule]` — registry orientado a módulos).

**Validação (FACT):** `compileall -f` → exit 0 · import por módulo → **33/35 OK**, falhando apenas `CLI` e `ModuleManager` (bug `@Component` pré-existente, §16.2 — **sem regressão**) · grep residual: nenhuma referência a `SystemModule` fora dos usos legítimos.

**Efeito colateral registrado:** Pylance sinaliza `packageRegister(component)` (bound `SystemModule` × argumento `CoffeeComponent`) — **DECISION (DEV, 2026-09-29): manter** (`packageRegister` = módulos de `modules/` no container); eliminá-lo exige decisão futura (migrar p/ `register()` com anotação `type`, ou declarar `id` em `CoffeeComponent`).

---

## 17. Conflitos documentação ↔ código

A fonte de verdade sobre **estado** é o **código**; a fonte documental **canônica** é **`docs/doc.md`** (DECISION do DEV, 2026-09-28, front matter). Conflitos ativos (todos FACT):

1. `runtime.md:410`, doc anterior `doc.md:143,371` → "decorator NÃO implementado" × `__call__` existente — **resolvido nesta versão** (§4.3).
2. `runtime.md:372,389`, ADR 001:36 → typo `getContener` × código `getContainer` — código já corrigido; docs desatualizadas.
3. `runtime.md:467-468`, `STATE.md:91`, doc anterior → `@CoffeeApplicationRuntime` em ModuleManager/CLI × `@Component` real — **§4.6/§4.7**.
4. Doc anterior `doc.md:90` → árvore com `core/domain/models/Module.py` (deletado) — árvore corrigida em §3.2.
5. `doc.md:151` anterior, `runtime.md:404` → "container guarda apenas Config" × estado atual (`get/_create/dependencies/systemModules`) — resolvido em **§4.4** (doc.md atualizada).
6. `.agents/state.json` → "33/33 módulos importam" × AttributeError verificado — **§16.8**.
7. `components-aop.md:101-118` → conteúdo consistente com o código **na época**, mas cita caminhos antigos pré-rename (§16.10).
8. **Pós-rename (2026-09-28):** `runtime.md`, `docs/decisions/006` e `007`, `specs/coffee-cli-v1.md` e `components-aop.md` ainda referenciam `contener/`, `componets/`, `Componet.py`, `CoffeAplicationRuntime.py`, `Dependecy.py`, `Services/` — caminhos **obsoletos**; doc.md (§3.2/§16.10) prevalece sobre eles.

**Resolução da questão anterior (DECISION · DEV · 2026-09-28):** *"qual doc prevalece?"* → **`doc.md` é mais relevante** — é a fonte documental principal; as demais docs ficam subordinadas a ela. Divergências doc × código continuam sendo registradas nesta seção (código = estado atual, doc.md = referência canônica).

---

## 18. Known Limitations (FACT — todos verificados)

1. **Boot nunca completa** — `Config.build()` sempre lança (`Config.py:21-22`) → `Runtime.init()` falha → `stop()` não roda (`init()` fora do `try`).
2. **Entrypoint de instalação quebrado** — `pyproject.toml:20` (decisão do DEV, `TODO:14`).
3. **2 módulos não importam** — `CLI` e `ModuleManager` via `@Component`/`AttributeError` (`TODO:53`).
4. **Container: DI incompleta** — `_create` descreve `dependencies` via `Dependency`, mas nunca é chamado e `get()` não injeta (§4.4.3); `systemModules` sem escritor/leitor.
5. **Registry duplicado** — `container/DefaultCoffeeRegistry.py` × `components/base/CoffeeRegistry.py`.
6. ~~**Typos em nomes públicos/pacotes**~~ — **CORRIGIDO em 2026-09-28** por instrução do DEV (§16.10); resta atualizar docs históricas que citam caminhos antigos (§17.8).
7. **Sem plugin system** — `moduleRegistry`/`components` sem consumidores reais (ADR 002 = PROPOSAL).
8. **Sem framework CLI, sem comandos** — `buildParser` sem chamador, `_addSubparsers` vazio.
9. **Sem testes, sem CI, README vazio, LICENSE ausente** (referenciados por `pyproject.toml:16-17`).
10. **Superfícies de segurança conhecidas** — `tool.py` pip/`sys.path`, `Config`/`Host` fora de adapter (harness §37).
11. **Diretórios órfãos** — `egine/` (UNDEFINED), `modules/ssh/{Adpiter,models,Services}/` (`TODO:55`).
12. **Trabalho não commitado** — renomeações/edits de 2026-09-28 (case-rename `services` staged via `git mv`; demais mudanças no working tree) + `state.json` com mojibake.
13. **Ambiente** — `.venv` observado sem `platformdirs` apesar de `TODO:38` registrar `pip install -e .` OK.
14. **`main.py` defects** — `tool.menu()` inexistente, `verify_modules()` sem `await`, `Start()` inalcançável.

---

## 19. Future Evolution

### Próximos passos (sequência discutida)

1. Definir contratos do ecossistema → 2. contrato do Coffee CLI → 3. domínio de Tasks → 4. implementar CLI V1 → 5. integrar Task Service do Server → 6. baseline/doctor Linux → 7. máquina/dual boot/recovery → 8. refatorar Server → 9. Context Engine → 10. reconstruir AI Harness.

### Decisões abertas (`docs/decisions/` + `STATE.md`)

Framework CLI · protocolo Python ↔ C++ · modelo de plugins/contrato de plugin · formato de configuração · offline mode/sync · Context Pack · API do Server V2 · schema Tasks/Projects · nome da pasta da engine C++ · **(novo)** prevalecência doc × código (§17) · **(novo)** ordem da renomeação de typos (antes ou depois desta doc).

### Endereçar limitações de §18

Cada item de §18 corresponde a entrada em `docs/TODO.md` ([H] decisão do DEV, [S] revisão compartilhada, [A] agente).

---

## Apêndice A — Inventário de docs

| Arquivo | Status | Observação |
|---|---|---|
| `docs/doc.md` | **ESTE ARQUIVO (0.3.1)** | doc principal, atualizada contra HEAD `cb2b812` + rename 2026-09-28 + refatoração de tipos 2026-09-29 (§16.11) |
| `docs/TODO.md` | não commitado | registra os findings (14-15, 47-49) |
| `docs/ai/STATE.md` | 2026-09-23 | itens 5-6 do próximo passo já feitos; item 7 mudou de objeto |
| `docs/architecture/runtime.md` | PROPOSAL, stale | §7 = código anterior ao HEAD; conflitos em §17 |
| `docs/architecture/components-aop.md` | DECISION 2026-09-25 | **mais atualizado**, consistente com o código |
| `docs/decisions/001-007` | 001/003/005/006/007 DECIDED | 006 (componentes) e 007 (DI) governam a área |
| `docs/specs/coffee-cli-v1.md` | spec V1 | comandos, domínio, config, lifecycle (PROPOSAL) |
| `docs/diagrams/architecture.mmd` | — | 4 diagramas |
| `docs/research/cli-framework-comparison.md` | placeholder | framework CLI UNDEFINED |
| `README.md` / `LICENSE` | vazio / ausente | referenciados pelo `pyproject.toml` |
| `.agents/harness.md`, `context/…`, `specs/…` | — | governança e contexto do ecossistema |

## Apêndice B — Como esta doc foi produzida

1. Exploração completa da codebase pelo `codebase-explorer` (task context: `.agents/protocol/tasks/temp/docs-main-technical-context.md`), com classificação FACT/INFERENCE/PROPOSAL/UNKNOWN e confidence por achado.
2. Verificação por execução de comportamento crítico (decorator, `Config.build()`, imports quebrados, `tool.menu()`).
3. Cruzamento doc ↔ código (§17) e com o relato do DEV sobre trechos fora de escopo (§16).
4. Escrita seguindo a estrutura de documentação técnica consolidada (AGENTS.md §18) e padrões de doc técnica profissional (escopo explícito, não documentar features que não existem, evidência antes de certeza).
