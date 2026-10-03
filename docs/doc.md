# Coffee CLI — Documentação Técnica Principal

**Versão:** 0.3.3
**Status:** FACT (verificado por execução/análise de código) + INFERENCE (onde a evidência é indireta) + PROPOSAL (intenção documentada, não implementada) + UNKNOWN (contexto insuficiente)
**Última atualização:** 2026-10-03
**Base de evidência:** task context do `codebase-explorer` — `.agents/protocol/tasks/temp/docs-main-technical-context.md`, HEAD `cb2b812` — **atualizado por leitura direta em 2026-09-28** após (a) renomeação de typos no código e (b) evolução do Container/`Dependency` posteriores ao relatório do explorer; **atualizado em 2026-09-29** após refatoração de tipos `SystemModule` → `CoffeeComponent` no decorator `@Component` (§4.5, §16.11); **atualizado em 2026-10-01** após (c) geração do relatório global do explorer (`.agents/protocol/docs/codebase-explorer.json`, HEAD `b9b15a8`) e (d) task de saneamento de imports (5 instâncias `import-cleaner` + verificação final: 61/61 imports resolvem, 0 paths antigos, 0 ciclos, 0 violações core→modules, 1 fix — `abstractmethod` removido de `CoffeeComponent.py`) e (e) **sincronização com as edições de código do DEV em 2026-10-01** (`Config.build()` reescrito — cria `configPath` se faltante e retorna `self`; `main.py` sem `config_local`, lendo config via container; **boot verificado por execução: exit 0** — §4.1/§4.2/§6.2) e (f) **atualização 2026-10-03** — task de consolidação da arquitetura Application Runtime + Application Context + DI + Components: relatório do `codebase-explorer` em `.agents/protocol/docs/codebase-explorer.json` (HEAD `628e772`) + task context `.agents/protocol/tasks/temp/runtime-context-di-components-task-context.json`; nova §4.10 (`CoffeeApplicationContext`), lifecycle sync/async com `setApp`/`resetApp` documentado (§4.3), **boot re-verificado: exit 1 desde `628e772`** (leak do ContextVar na rota async — §4.1/§6.2/§17.10), invariantes em `docs/architecture/runtime.md` §13–§17 e `AGENTS.md`.
> **Resolvido (2026-10-01):** a linha "base de evidência" já citava o report global `.agents/protocol/docs/codebase-explorer.json` como **inexistente** (FACT em 2026-09-29) — o arquivo **foi criado** em 2026-10-01 (gerado pelo `codebase-explorer` em `b9b15a8`) e é agora a referência de frescor; o task context antigo permanece STALE e é mantido como histórico.

> **Legenda de classificação** (usada em todo o documento):
> `FACT` = suportado diretamente por código/execução · `INFERENCE` = inferência forte a partir de evidência · `PROPOSAL` = intenção documentada, não implementada · `UNKNOWN` = contexto insuficiente.
> Confiança: HIGH / MEDIUM / LOW.

> **DECISION (DEV · 2026-09-28):** **`docs/doc.md` é a fonte documental principal do projeto.** Quando outras docs (`runtime.md`, ADRs, specs) divergirem entre si ou deste documento, **doc.md prevalece**. Quando doc.md divergir do código, o conflito é registrado em §17 — código = estado atual, doc.md = referência documental canônica.

---

## 1. Overview

O Coffee CLI é a interface de linha de comando do ecossistema Coffee — uma camada pessoal de produtividade, desenvolvimento, automação, contexto e integração com IA. É a camada humana e o orquestrador local: **não é um segundo servidor** — o OS funciona sem Coffee.

**Estado real do código (FACT):** projeto em fase de skeleton. O núcleo de dados (`Config`), o contrato de domínio (`SystemModule`) e a fronteira de runtime (`CoffeeApplicationRuntime`) existem; o bootstrap **completa o entry** desde 2026-10-01 (execução direta entra no Runtime e executa o `main` async), porém **termina com exit 1 desde `628e772`** (`Start()` → `RuntimeError` pós-lifecycle — §4.1/§6.2), não há comandos CLI funcionais, não há testes e não há CI. **Imports (atualização 2026-10-01):** todos os módulos do projeto importam (14/14 verificados; `compileall` exit 0) — os2 defeitos históricos de import (`CLI`/`ModuleManager` via `@Component`) foram resolvidos pelo commit `c60908d` (ver §16.2/§16.9).

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
├── config/
│   └── Config.py                      # dataclass Config + build() que cria configPath e retorna self
├── data/
│   └── Host.py                        # dados de host (username, platform)
├── core/
│   ├── __main__.py                    # VAZIO (0 bytes)
│   ├── components/
│   │   ├── CoffeeComponent.py         # ABC base dos componentes
│   │   ├── decorators/
│   │   │   ├── Component.py           # decorator @Component → registry.register
│   │   │   └── Module.py              # decorator @Module → registry.packageRegister
│   │   └── metadata/                  # __init__ vazio
│   ├── container/
│   │   ├── CoffeeApplicationContainer.py  # composição + DI (dependencies/systemModules)
│   │   ├── CoffeeRegistry.py          # ABC do registry (dataclass sobre ABC)
│   │   ├── DefaultCoffeeRegistry.py   # registry funcional (herda CoffeeRegistry)
│   │   └── registry.py                # singleton: registry = DefaultCoffeeRegistry()
│   ├── domain/
│   │   ├── exceptions/
│   │   │   └── InvalidCoffeeApplicationException.py
│   │   ├── interface/SystemModule.py  # ABC de módulos (contrato de domínio)
│   │   └── models/
│   │       └── Dependency.py          # registro de dependência (classe intermediária de DI)
│   ├── runtime/
│   │   ├── CoffeeApplicationRuntime.py    # lifecycle + decorator de entrada
│   │   ├── CLI.py                     # RuntimeCLI (argparse) — importa OK (§16.2)
│   │   └── lifecycle/                 # __init__ vazio
│   └── services/
│       ├── tool.py                    # utilitários (clear, verify_modules, add_path_modules)
│       └── module/ModuleManager.py    # serviço de módulos — importa OK (§16.2)
└── modules/
    ├── ssh/package.py                 # SSHModule (@Module) — sem consumidores
    ├── system/ , update/              # __init__ vazios
```

> **Estrutura pós-`3d47da8` (2026-09-30, atualização 2026-10-01):** `Config`/`Host` saíram de `core/data/` para os pacotes de topo `config/` e `data/`; `components/` e `container/` saíram de `core/runtime/` para dentro direto de `core/`; `CLI.py` passou a viver em `core/runtime/`; os decorators estão em `components/decorators/`. Nota: `domain/models/` **não** tem `__init__.py` (resolve como namespace package — consistency-note da verificação de imports).

Diretórios vazios sem código (FACT): `egine/` (nome UNDEFINED), `modules/ssh/{Adpiter,models,Services}/`.

> **Nota sobre typos (atualização 2026-09-28):** os typos de pasta/arquivo (`contener`, `componets`, `CoffeAplication`, `exepiton`, `Services/`, `CofeeRegistry`, `Componet`, `Dependecy`) vêm do **skeleton original do DEV** (`1b938f2`) — **não** são criação da IA. Foram **corrigidos por instrução do DEV em 2026-09-28** (§16.10); o histórico de typos permanece documentado em §16. Os paths atuais desta doc foram **sincronizados com o código em 2026-10-01**; ainda citam caminhos antigos apenas os **registros históricos** (ADRs 006/007, tabelas de rename §16.10/§16.11, diagrama `CoffeeSDK.drawio`) — ver §17.

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

- **`config_local = Config()` foi removido pelo DEV em 2026-10-01** — a config agora vem do container (`contener = app.getContainer()` dentro de `main`); o import `Config` permanece em `main.py:1` (hoje **unused** — OUT-OF-SCOPE, não alterado).
- `@CoffeeApplicationRuntime` decora `async def main(app)` (13-14): após o decorator, `main` deixa de ser função e vira **instância** de `CoffeeApplicationRuntime` (verificado por execução).
- `Start()` (10-11) — **estado em 2026-10-01:** contém `print("coffe")` (placeholder que substituiu o `tool.menu()` inexistente — FACT histórico, `TODO:54`) e é **alcançável** — executa após `asyncio.run(main())`.
- `if __name__ == "__main__"` (29-31): `asyncio.run(main())` → `Start()`.

**Execução verificada (FACT — re-verificado em 2026-10-03, HEAD `628e772`):** `python -m coffee.main` → `asyncio.run(main())` executa o entry (init + corpo OK, imprime `coffe` via `Start()`), mas **termina com exit 1**: `Start()` (34) → `ModuleManager().loadModules()` (13) → property `container` → `getApp()` OK (**leak**: a rota async não chama `resetApp`) → `getContainer()` → `RuntimeError: CoffeeApplicationRuntime is not initialized` (Runtime:37) — causa: `stop()` já zerou `_container` no `finally` da rota async. Até `9ddf051` (sem `ModuleManager` em `Start()`) o boot era **exit 0** — registros anteriores de "exit 0" (§4.1 antiga, §6.2, `STATE.md`, `state.json`) refletem aquele estado. Defeitos que permanecem: `tool.verify_modules()` é `async` e é agendado com `asyncio.create_task(...)` (21) **sem aguardar o resultado** (só executa se `Debug=True`; `Debug` default é `False`); condição `if not (app or app.getContainer())` (23) nunca dispara.

### 4.2 `config` e `data` — Config e Host (FACT)

**Arquivo:** `src/coffee/config/Config.py` (movido de `core/data/Config.py` no restructure `3d47da8`; `Host.py` vive em `src/coffee/data/Host.py`)

```python
@dataclass
class Config:
    configPath: Path = Path(user_config_dir("Coffee"))
    hostData: Host = field(default_factory=Host)
    Debug: bool = False
    modules_local: list[str] | None = None

    def build(self) -> Config:
        if not (self.configPath.exists()):
            os.makedirs(self.configPath, exist_ok=True)
        if not os.path.isdir(self.configPath.absolute()):
            raise RuntimeError("The configuration path is not a directory.")
        if not self.hostData.platform == None:   # condição invertida (hoje inócua)
            self.getHost()                       # recria hostData = Host()
        return self
```

- `configPath` resolve via platformdirs — no Windows observado: `C:\Users\Quitto\AppData\Local\Coffee`; o harness §35 documenta `~/.config/Coffee/` (diferença Unix/platformdirs).
- **`build()` não lança mais incondicionalmente (FACT — DEV, 2026-10-01):** a versão anterior levantava `RuntimeError` sempre (`Host.platform = system()` nunca é `None` → branch disparava sempre; histórico em §16.6). O DEV reescreveu o método: cria `configPath` com `os.makedirs(..., exist_ok=True)` se faltante, só lança se o path existir **e não for diretório** (`RuntimeError` com mensagem `"The configuration path is not a directory."`), e o branch da condição invertida agora chama `self.getHost()` (reset de `hostData`) em vez de `raise`. **Verificado por execução 2026-10-01:** boot exit 0.
- **Resíduo (OUT-OF-SCOPE, não alterado):** a condição invertida `if not self.hostData.platform == None` continua no código; com `hostData` já instanciado no `__init__`, o branch **sempre recria** o `Host()` — `getHost()` não agrega nada além de resetar. `from time import sleep` (`Config.py:3`) está **unused**.

### 4.3 `CoffeeApplicationRuntime` — fronteira de lifecycle (FACT + INFERENCE sobre autoria)

**Arquivo:** `src/coffee/core/runtime/CoffeeApplicationRuntime.py` (renomeado de `CoffeAplicationRuntime.py` em 2026-09-28)

**O que é (FACT):** classe que combina duas coisas:

1. **Estado de ciclo de aplicação** — `_container`/`_registry` (atributos de **classe**, 16-17), `init()` (22-32) cria `Config().build()` + `CoffeeApplicationContainer`; `getContainer()` (34-39) retorna o container ou lança `RuntimeError`; `setConfig()` (41-43); `stop()` (45-48) zera `_container` e retorna `True`. Todos são `@classmethod` (contrato da ABC `ApplicationRuntime`).
2. **Decorator de lifecycle** — `__init__(func)` (19-20), `__call__` (50-83), `_invokeAsync` (85-93).

**Comportamento do decorator (FACT — verificado por execução):**

```python
@CoffeeApplicationRuntime        # e também @CoffeeApplicationRuntime()
async def main(app: CoffeeApplicationRuntime): ...
```

- Aceita as duas formas (factory em 63-68); args/kwargs na chamada → `TypeError` (70-73).
- **`token = CoffeeApplicationContext.setApp(self)` (61)** ocorre **antes** de `init()` nas duas rotas — o App fica registrado no ContextVar antes de qualquer componente acessar `getApp()`.
- Sync: `init()` (78) → `func(self)` (80) → `finally`: `resetApp(token)` (82) + `stop()` (83) — **ciclo fechado corretamente** (verificado: após reset, `getApp()` → `RuntimeError: not running`).
- Async: retorna coroutine → `_invokeAsync`: `init()` (86) → `await func(self)` (88-90) → `finally`: **apenas `stop()` (92-93) — SEM `resetApp(token)`** (GAP, ver §17.10).
- Injeta `self` (a instância runtime) como argumento do ponto de entrada.
- **Factory-form:** `@CoffeeApplicationRuntime()` sem alvo → `setApp` roda no decorate (61) e o token **nunca é resetado** (leak verificado).

**Limitações verificadas (FACT):**

- `init()` está **fora** do `try` nas duas rotas (78 e 86): se `init()` falhar, `stop()` **não roda** — a garantia de `try/finally` documentada em `runtime.md` não se sustenta. *(Desde 2026-10-01 `init()` não lança mais — `Config.build()` foi reescrito (§4.2); a assimetria estrutural permanece.)*
- **Rota async sem `resetApp`:** o token setado em `__call__` (61) nunca reseta na rota assíncrona → após `stop()`, o ContextVar ainda aponta para o app → `Start()` falha com `RuntimeError: CoffeeApplicationRuntime is not initialized` → **boot exit 1** (verificado 2026-10-03).
- **Atenção:** `main()` é coroutine mas `__call__` é síncrono e retorna a coroutine `_invokeAsync(...)` — o `await` real acontece dentro de `_invokeAsync`, que é agendado por `asyncio.run(main())` no `__main__`.

**Marcas de autoria (INFERENCE · confiança MEDIUM-HIGH — agente, commit `dad3b2d`, lote 2026-09-25 22:27):**

- Docstring cita **`runtime.md §12.3`** (linha 53-54) — `runtime.md` **não tem §12.3** → referência documental que não existe, usada para justificar código.
- Mistura de idiomas: docstring em PT, mensagens de `TypeError` em EN (68, 69-70).
- Comentário de fase em voz de agente: `# ... ainda estamos na fase de factory.` (62).

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

    def _create(self, dependency: type) -> None: ...  # 15-37 — reflete e descreve
    def get(self, component: type): ...               # 39-45 — resolve via registry
    def getConfig(self) -> Config: ...                # 47-48
    def setConfig(self, config: Config) -> None: ...  # 50-51
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

1. **Describe parcialmente implementado:** `_create` (15-37) reflete a assinatura, cria `Dependency` e deduplica por igualdade de dataclass (36-37); o `print` de debug só roda com `config.Debug = True` (25-30, gate adicionado em `eefb71a`). **Nunca é chamado por ninguém** (grep) — nenhum fluxo invoca `_create` hoje.
2. **Resolve ausente:** `get()` (39-45) resolve o `implementation` no registry e chama `implementation()` **sem injetar nada** — os `dependencies` declarados não são consumidos. Componentes com `__init__` exigindo argumentos (ex.: `RuntimeCLI(moduleManager, config)`) continuam falhando.
3. **Debug condicional:** o `print` dos parâmetros em `_create` (25-30) está atrás de `self.config.Debug` — em produção (`Debug=False`) não escreve em stdout, mas continua sendo print de biblioteca, não logging.
4. **Anomalia no `id` (FACT):** `id: UUID = uuid4()` é avaliado **uma única vez** na criação da classe — toda `Dependency` criada sem `id` explícito recebe o **mesmo UUID** (o default não é `default_factory`). Isso quebra a unicidade que o campo sugere e afeta o dedupe por igualdade.
5. **Edge case:** parâmetros sem anotação produzem `classImpl = inspect.Parameter.empty` (não `None`), divergindo do contrato `type | None`.
6. `get()`/`_create()` **não têm chamadores** fora da própria classe (FACT, grep).

> **Autoria (INFERENCE):** `_create`/`dependencie` não existiam no skeleton (`6cf711c` → `d326b2d`, agente); a versão atual com `Dependency`/`systemModules` é **posterior ao relatório do explorer** e de autoria DEV/agnóstica — UNKNOWN.

#### 4.4.4 `DefaultCoffeeRegistry` (`container/DefaultCoffeeRegistry.py`)

- **Estado atual (2026-10-01, pós-`c60908d`/`3d47da8`):** listas de classe — `dependencies: list[Dependency]` (registro de componentes como `Dependency(id=uuid4(), name, classImpl)`) e `systemModules: list[type[SystemModule]]` (módulos de `modules/`). Os dicts anteriores (`components`, `moduleRegistry`) **não existem mais**.
- API `@classmethod`: `register(component)` (append em `dependencies` — **não exige `.id`**), `packageRegister(module)` (append em `systemModules` — **não exige `.id`**; a antiga semântica `moduleRegistry[module.id]` foi removida), `contains`, `get`, `getModule`, `all`.

**Registry base × funcional (FACT):** a relação deixou de ser "duas classes homônimas": hoje existe a ABC `CoffeeRegistry` (em `container/CoffeeRegistry.py`, `@dataclass` sobre `ABC`) e `DefaultCoffeeRegistry(CoffeeRegistry)` (em `container/DefaultCoffeeRegistry.py`) — **herança, não duplicação**. O singleton `registry = DefaultCoffeeRegistry()` vive em `container/registry.py` (referência histórica do conflito em `components-aop.md:107,116`).

### 4.5 `components` — decorators de componentes e módulos (FACT)

**`decorators/Component.py`** (renomeado de `Componet.py`, depois movido para `decorators/`; classe `Component`):

```python
from coffee.core.container.registry import registry          # singleton de container/registry.py

def Component(component: type[T]) -> type[T]:                 # T bound=CoffeeComponent (§16.11)
    registry.register(component)                              # estado atual (desde c60908d)
    return component
```

- **Estado atual (2026-10-01):** `Component` chama **`register`** (desde o commit `c60908d`) → append de `Dependency` em `registry.dependencies` — **não exige `.id`**; classes decoradas importam sem `AttributeError` (CLI e ModuleManager importam OK — verificado 14/14).
- **`Module`** (`decorators/Module.py`) chama **`packageRegister(module=module)`** → append em `registry.systemModules` — também **não exige `.id`** (a exigência `moduleRegistry[module.id]` da versão antiga foi removida na reescrita do registry).
- Anomalias: o singleton `registry` é importado de `container/registry.py` apesar de todos os métodos serem `@classmethod`; assinatura `Component(component: type[T]) -> type[T]` usada como decorator de classe (recebe **classes**, não instâncias).
- **CONFLICT decisão × código (FACT, registrado em §17.9):** a **DECISION (DEV, 2026-09-29)** registrava **manter `packageRegister`** no decorator `@Component` (`packageRegister` = módulos de `modules/` no container; anotação `type` reservada para migração futura). Porém o commit **`c60908d` (2026-09-29)** trocou a chamada para **`register`** — o código atual **diverge** da decisão registrada. Aguarda confirmação do DEV (`TODO:53`).

**`decorators/Module.py`**: `Module(module)` → `registry.packageRegister(module=module)` → `systemModules` — caminho dos módulos de `modules/` (ex.: `SSHModule`).

**Regressão do `@Component` (FACT comportamento + INFERENCE HIGH autoria agente — HISTÓRICO):** `6cf711c` criou `Componet.py` já com `packageRegister`, substituindo o `register()` funcional do skeleton. Consequência verificada **em 2026-09-28:** importar `coffee.core.services.module.ModuleManager` ou `coffee.core.runtime.CLI` → `AttributeError: type object 'ModuleManager' has no attribute 'id'`. **Status 2026-10-01: RESOLVIDO** — `c60908d` trocou a chamada para `register` e a reescrita do registry eliminou a exigência de `.id`; ambos os módulos importam OK (ver §16.2).

### 4.6 `core.runtime.CLI` — parser argparse (FACT)

**Arquivo:** `src/coffee/core/runtime/CLI.py` (movido de `core/cli/CLI.py` no restructure `3d47da8`)

- `@Component class RuntimeCLI` com `__init__(moduleManager, config)` e `buildParser()` que cria `ArgumentParser(prog="coffee")`.
- `_addSubparsers()` = `for ...: pass` — vazio; `buildParser` **não tem chamador**.
- **Importa OK (2026-10-01)** — até 2026-09-30 falhava via `@Component`/`AttributeError` (§16.2).
- **CONFLICT:** `doc.md` (versão anterior):174 e `runtime.md:467` diziam que `CLI.py` usa `@CoffeeApplicationRuntime` → hoje usa `@Component`.
- Autoria (INFERENCE MEDIUM): `6cf711c` acrescentou `RuntimeCLI`/`__init__`/`_addSubparsers`; `b0c4c49` removeu uma herança inválida e arrumou imports. `@Component` é do skeleton.

### 4.7 `core.services` — ModuleManager e tool (FACT)

**`ModuleManager`** (`services/module/ModuleManager.py`): `@dataclass @Component class ModuleManager` com `_modulesRegistry` e `loadModules()`.

- `@Component` é do **skeleton**; a **quebra** foi do agente (mudança de semântica do registry em `6cf711c`) — **status 2026-10-01: importa OK** (`c60908d` resolveu; ver §4.5/§16.2).
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
- **`domain/models/`**: `Module.py` foi deletado em `6cf711c`; hoje contém apenas `Dependency.py` (sem `__init__.py` — namespace package). ~~O `SSHModule` **não** subclasseia `SystemModule`~~ — **corrigido:** desde o restructure `3d47da8` `SSHModule` **subclasseia `SystemModule`** (ver §4.9).

### 4.9 `modules` — features (FACT)

- `modules/ssh/package.py`: `@Module class SSHModule(SystemModule)` — **subclasseia o contrato `SystemModule`** com `id/name/version` (status 2026-10-01; até o restructure era um dataclass "fora do contrato") — registrado em `registry.systemModules` via `packageRegister`, **sem consumidor**.
- `modules/system/`, `modules/update/`: `__init__` vazios.

### 4.10 `CoffeeApplicationContext` — Application Context via ContextVar (FACT)

**Arquivo:** `src/coffee/core/runtime/CoffeeApplicationContext.py` (introduzido em `628e772`, 2026-10-03)

**O que é (FACT):** portal de acesso **contextual** à aplicação atual. Um `ContextVar` de módulo:

```python
_current_app: ContextVar["CoffeeApplicationRuntime | None"] = ContextVar(
    "coffee_current_app", default=None,
)
```

e uma classe sem estado (`staticmethods` apenas):

| Método | Comportamento |
|---|---|
| `setApp(app)` | `_current_app.set(app)` → **retorna token** de restauração |
| `getApp()` | retorna a referência; se `None` → `RuntimeError("CoffeeApplicationRuntime is not running")` (24-26) |
| `resetApp(token)` | `_current_app.reset(token)` — restaura o estado anterior |

**Invariantes (FACT):**

- O ContextVar guarda uma **referência** à instância de `CoffeeApplicationRuntime` (identidade verificada por execução) — **não uma cópia**.
- `_current_app` é acessado **apenas** neste arquivo (grep) — o resto do sistema usa `setApp`/`getApp`/`resetApp`.
- **Não** é singleton nem variável global comum: cada contexto de execução (task/thread) tem o seu valor; `default = None` fora do ciclo.
- Não substitui sincronização de estado compartilhado mutável (`_container` de classe, listas do registry/container — 0 travas no código).

**Fluxo de uso (FACT):**

```text
CoffeeComponent.container (property, CoffeeComponent.py:10-12)
  → CoffeeApplicationContext.getApp()
  → CoffeeApplicationRuntime.getContainer()
  → ApplicationContainer (abstração — DIP)
```

**Erros comuns (documentados em `runtime.md` §16):** `not running` = `getApp()` sem App no contexto (antes do `setApp`/depois do `resetApp`/fora do ciclo/outro contexto); `not initialized` = `getContainer()` com `_container = None` (pós-`stop()` com leak do token na rota async).

> **Status de decisão:** mecanismo **commitado e em uso** (`628e772`), porém **sem ADR/spec** que o formalize (U-002 do task context — PROPOSAL/UNKNOWN; ADR 007 prevê constructor injection para `ModuleManager`, hoje divergente — conflito §17.11).

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

**Status 2026-10-01:** o pacote está instalado em modo editable no `.venv` do projeto (`pip install -e .` → `coffee-cli 0.1.0`), então `import coffee` **resolve** a partir de qualquer diretório; porém o script gerado `coffee.exe` ainda falha com `ModuleNotFoundError: No module named 'coffee.cli.main'` — o entrypoint quebrado permanece decisão do DEV (`TODO:14`). Enquanto isso, `python -m coffee.main` executa o entry no Runtime — mas **termina com exit 1 desde `628e772`** (gap `resetApp` na rota async — §6.2; exit 0 apenas até `9ddf051`).

### 6.2 Fluxo de execução direta (FACT — re-verificado em 2026-10-03, HEAD `628e772`)

```
import coffee.main
  → @CoffeeApplicationRuntime vira instância      (main.py:16)
python -m coffee.main (__main__)
  → asyncio.run(main())                          (main.py:33)
  → CoffeeApplicationRuntime.__call__
     → token = CoffeeApplicationContext.setApp(self)   (Runtime:61)  ← ANTES de init
     → _invokeAsync (coroutine; asyncio.run copia o contexto do caller)
  → _invokeAsync → init() → Config().build() OK  (cria configPath se faltante)
     → registry → Container(config)               (Runtime:28-32)
  → corpo de main: contener.config.Debug = False  → create_task NÃO agendado
  → finally → APENAS stop() → _container = None   (Runtime:92-93)   ← SEM resetApp (leak)
  → Start() → print("coffe") → ModuleManager().loadModules()
     → getApp() OK (leak) → getContainer() → RuntimeError "not initialized"
exit 1
```

> **Nota (FACT):** o caminho de sucesso `exit 0` valia até `9ddf051` (sem `ModuleManager` em `Start()`). Desde `628e772` o boot sai com **exit 1** pela causa acima (gap `resetApp` na rota async — §4.3/§17.10). O caminho **síncrono** do decorator continua fechando o ciclo corretamente (`resetApp` + `stop`).

> Nota (FACT — verificado por execução em 2026-10-01): o fluxo acima é o caminho **de sucesso** após o DEV reescrever `Config.build()` (§4.2). Antes disso, o boot falhava em `init()` (`RuntimeError` sem mensagem) e `Start()` era inalcançável — registro histórico em §16.6. `main.py` e `CoffeeApplicationRuntime.py` estavam **ativos em edição pelo DEV** em 2026-10-01 — refs de linha aproximadas.

### 6.3 Fluxo de registro de componentes (verificado) — FACT

```
import decorado
  → @Component → register       → dependencies.append(Dependency)   (sem exigência de .id)
  → @Module    → packageRegister → systemModules.append(module)     (sem exigência de .id)
Runtime.init() → Container(config)
Container.get(T) → registry.get(T) → T()          (sem DI)
```

> **Alteração (2026-10-01):** os papéis `@Component`/`@Module` estavam **invertidos** na versão anterior desta doc (atribuía-se `packageRegister` a `@Component`); o texto acima reflete o código atual (`c60908d`/`3d47da8`). O **DECISION drift** (`packageRegister` decidido × `register` no código) está registrado em §4.5/§17.9.

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

**Exceções atuais (FACT):** `InvalidCoffeeApplicationException` (uso apenas em `main.py`); `RuntimeError` com mensagem em `Config.build()` (só se `configPath` existir e não for diretório); `RuntimeError` em `Runtime.getContainer()` e em `Container._create` (`"Dependency cannot be None"`); `LookupError` em `Container.get()`; `TypeError` no decorator.

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
- **Defeitos do trecho (FACT):** `init()` fora do `try` em ambas as rotas → `stop()` não roda se `init()` falhar; *(histórico — até 2026-10-01, o ponto de entrada **nunca executava** porque `Config.build()` lançava; desde a reescrita do DEV o boot completa e `stop()` roda no `finally` — §4.1/§4.2; a assimetria estrutural permanece.)*
- **Por que fugiu do escopo (INFERENCE):** a doc (`runtime.md:410`, `doc.md` anterior) dizia "decorator não implementado" e `STATE.md` lista "Implementar `__call__`" como tarefa de agente — o agente implementou sem o fluxo de decisão do DEV, gerando código conflitante com a própria doc.
- **Callers:** apenas `main.py:4,16,17`. Referências em docs: `runtime.md` §3/§5.4/§7/§8, ADR 001, `specs/coffee-cli-v1.md:214,541,551`, `diagrams/architecture.mmd:69-74`.

### 16.2 `Componet.py` — regressão do `@Component` (quebra 2 imports)

> Renomeado em 2026-09-28 para **`components/Component.py`** (registro agora em `container/DefaultCoffeeRegistry.py`); posteriormente movido para **`components/decorators/Component.py`** (restructure `3d47da8`).
>
> **STATUS 2026-10-01 — RESOLVIDO:** o commit `c60908d` trocou `packageRegister` → `register` no decorator e a reescrita do registry removeu a exigência de `.id`. Verificação: `compileall` exit 0; **14/14 módulos importam** (CLI e ModuleManager incluídos); 5 instâncias `import-cleaner` + verificação final = **PASS**. O conteúdo abaixo é **histórico** (estado até 2026-09-30). O **drift decisão × código** (`packageRegister` decidido × `register` em uso) permanece aberto — §17.9, `TODO:53`.

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
- **Anomalias que permanecem:** `print` de debug em `_create` (agora atrás de `config.Debug` — `eefb71a`); `_create` sem chamadores; `get()` sem resolution/injeção; `id: UUID = uuid4()` não-único (§4.4.3).
- **Imports junk removidos em 2026-09-28** (autorados por autocomplete, fora de escopo do rename mas claramente acidentais): `from ast import List`, `from pickletools import uint4`, `from tkinter import NO`, `from uuid import UUID` — todos unused; `tkinter` em core era risco de import.

### 16.4 `main.py` — estrutura DEV remendada por agente

- **Class:** estrutura DEV (`1b938f2`) + remendos do agente (`b0c4c49`: `data`→`Config`, re-root de imports) · INFERENCE MEDIUM-HIGH p/ remendos, FACT p/ estado atual.
- Defeitos: `verify_modules()` agendado sem aguardar; condição `if not (app or ...)` nunca dispara. *(Histórico: `Start()` era inalcançável e pedia `tool.menu()` inexistente — substituído por placeholder `print("coffe")` e alcançável desde a reescrita de `Config.build()` em 2026-10-01 — §4.1.)* (Typo `"StopAsycnInteration"` corrigido em 2026-09-28 — §16.10.) Registro: `TODO:14,54`.

### 16.5 `CLI.py` e `ModuleManager.py`

- `6cf711c` acrescentou `class RuntimeCLI(Component)` com herança inválida (removida em `b0c4c49`), `__init__`, `_addSubparsers` (loop `pass`). **Status 2026-10-01:** imports **OK** (resolvido em `c60908d`); `buildParser` segue sem chamador. CONFLICTs documentais listados em §4.6/§4.7.

### 16.6 `Config.build()` — bug corrigido pelo DEV

- **AUTHORIA: UNKNOWN (provável DEV)** — a condição invertida `if not self.hostData.platform == None` já está no skeleton `1b938f2`. O agente corrigiu `os.path.isdir()`, re-rootou imports e adicionou `return self`/`modules_local`, **mantendo** a condição (FACT). Efeito antigo: nenhum boot completava (`RuntimeError` sempre).
- **Status 2026-10-01 (FACT — DEV, worktree):** o DEV **reescreveu** `build()` — `os.makedirs(configPath, exist_ok=True)` se faltante, `RuntimeError` com mensagem só se o path não for diretório, e o branch da condição invertida agora chama `self.getHost()` em vez de `raise`. Boot verificado: exit 0 (§6.2). **Resíduo não corrigido (OUT-OF-SCOPE):** condição invertida permanece (sempre recria o `Host()`) e `from time import sleep` está unused.

### 16.7 `tool.py`

- Remendos do agente (`b366df4`, `6cf711c`) trocaram import inexistente por `Config`. Hoje: requirements.txt alvo inexistente; `sys.path.append`. Risco auto-registrado: harness:1493-1504.

### 16.8 `__init__.py` ×10 e `.agents/state.json`

- **FACT — agente** (TODO TASK-001). `__init__.py` criados também em pacotes sem código. `state.json` (untracked) teve **encoding quebrado (mojibake)** e afirmava `PASS - 33/33 módulos importam` → **CONFLICT** com o `AttributeError` verificado à época (§16.2) — **resolvido**: reescrito em 2026-10-01 com encoding correto, refletindo o estado pós-import-cleanup.

### 16.9 Verificação dos erros estruturais citados em `AGENTS.md`

| Afirmação em AGENTS.md | Estado hoje | Class · Confiança |
|---|---|---|
| Entrypoint quebrado | **AINDA EXISTE** — `pyproject.toml:20` → `coffee.cli.main:main` inexistente | FACT · HIGH |
| Imports quebrados | **RESOLVIDOS (2026-10-01)** — re-root `core.*`→`coffee.core.*` + fix do `@Component` (`c60908d`); verificação: 14/14 módulos importam, 0 paths antigos, 0 ciclos, 0 core→modules | FACT · HIGH (verificado) |
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

**Efeito colateral registrado:** Pylance sinalizava `packageRegister(component)` (bound `SystemModule` × argumento `CoffeeComponent`) — **DECISION (DEV, 2026-09-29): manter** (`packageRegister` = módulos de `modules/` no container); eliminá-lo exige decisão futura (migrar p/ `register()` com anotação `type`, ou declarar `id` em `CoffeeComponent`). **Status 2026-10-01:** a migração para `register()` **aconteceu no código** (`c60908d`) sem registro de decisão correspondente → drift em §17.9.

---

## 17. Conflitos documentação ↔ código

A fonte de verdade sobre **estado** é o **código**; a fonte documental **canônica** é **`docs/doc.md`** (DECISION do DEV, 2026-09-28, front matter). Conflitos ativos (todos FACT):

1. `runtime.md:410`, doc anterior `doc.md:143,371` → "decorator NÃO implementado" × `__call__` existente — **resolvido nesta versão** (§4.3).
2. `runtime.md:372,389`, ADR 001:36 → typo `getContener` × código `getContainer` — código já corrigido; docs desatualizadas.
3. `runtime.md:467-468`, `STATE.md:91`, doc anterior → `@CoffeeApplicationRuntime` em ModuleManager/CLI × `@Component` real — **§4.6/§4.7**.
4. Doc anterior `doc.md:90` → árvore com `core/domain/models/Module.py` (deletado) — árvore corrigida em §3.2.
5. `doc.md:151` anterior, `runtime.md:404` → "container guarda apenas Config" × estado atual (`get/_create/dependencies/systemModules`) — resolvido em **§4.4** (doc.md atualizada).
6. `.agents/state.json` → "33/33 módulos importam" × AttributeError verificado — **§16.8**.
7. `components-aop.md:101-118` → conteúdo consistente com o código **na época**, mas citava caminhos antigos pré-rename — **paths atualizados em 2026-10-01** (§16.10); as linhas de status do texto seguem refletindo o estado pós-`c60908d`/`3d47da8`.
8. **Pós-rename (2026-09-28):** `runtime.md`, `docs/decisions/006` e `007` e `components-aop.md` referenciavam `contener/`, `componets/`, `Componet.py`, `CoffeAplicationRuntime.py`, `Dependecy.py`, `Services/` — caminhos **obsoletos**. **Status 2026-10-01:** `runtime.md`, `components-aop.md` e `.agents/specs/coffee-components-aop.md` foram **sincronizados com os paths atuais**; permanecem com paths históricos apenas **ADRs 006/007** (registros de decisão — preservados por serem histórico) e o diagrama `CoffeeSDK.drawio`. Observação: a alegação de que `specs/coffee-cli-v1.md` citava paths antigos era **incorreta** (grep = 0 ocorrências).
9. **DECISION × código (novo, 2026-10-01):** a **DECISION (DEV, 2026-09-29)** de **manter `packageRegister`** no decorator `@Component` diverge do código atual, que chama **`register`** desde `c60908d` (`decorators/Component.py:10`). `@Module` continua em `packageRegister`. Documentação registrada; correção requer decisão do DEV (`TODO:53`).
10. **Boot exit 1 × docs "exit 0" (2026-10-03):** desde `628e772` o boot sai com **exit 1** (`Start()` → `RuntimeError: CoffeeApplicationRuntime is not initialized`) porque a rota assíncrona não chama `resetApp` (leak do ContextVar). `doc.md` §4.1/§6.2 **corrigidos nesta versão**; `docs/ai/STATE.md` e `.agents/state.json` sincronizados. Os registros de "exit 0" eram válidos para commits ≤ `9ddf051`.
11. **ADR 007 × código (C-002):** ADR 007 (ACCEPTED) prevê `ModuleManager` com config via **constructor injection** criado no `init()` do Runtime; o código atual (`628e772`) usa **service-locator contextual** (`property container` → `CoffeeApplicationContext`) e `init()` não cria `ModuleManager`. Conflito registrado; correção requer decisão do DEV.
12. **Spec/espelho "ABC + initialize()" (C-003) — RESOLVIDO 2026-10-03:** `docs/architecture/components-aop.md` §5 e `.agents/specs/coffee-components-aop.md` descreviam `CoffeeComponent` com `initialize()` — removido desde `628e772` (base hoje: `property container` + `get()`, sem `__init__`/`initialize`). Tabela corrigida.

**Resolução da questão anterior (DECISION · DEV · 2026-09-28):** *"qual doc prevalece?"* → **`doc.md` é mais relevante** — é a fonte documental principal; as demais docs ficam subordinadas a ela. Divergências doc × código continuam sendo registradas nesta seção (código = estado atual, doc.md = referência canônica).

---

## 18. Known Limitations (FACT — todos verificados)

1. **Boot termina com exit 1 (desde `628e772`, verificado 2026-10-03)** — a rota assíncrona do decorator **não chama `resetApp(token)`** no `finally` (Runtime:92-93) → ContextVar leak → `Start()` → `ModuleManager().loadModules()` → `getContainer()` lança `RuntimeError: CoffeeApplicationRuntime is not initialized`. A reescrita de `Config.build()` (§4.2) resolveu a falha anterior em `init()`; o gap atual é o `resetApp` ausente (§4.3/§17.10) + `init()` fora do `try` (assimetria estrutural).
2. **Entrypoint de instalação quebrado** — `pyproject.toml:20` (decisão do DEV, `TODO:14`); o script `coffee.exe` agora existe no `.venv` (editable install em 2026-10-01) mas falha com `ModuleNotFoundError: coffee.cli.main`.
3. ~~**2 módulos não importam**~~ — **RESOLVIDO (2026-10-01)**: `CLI` e `ModuleManager` importam OK (`c60908d`); 14/14 módulos verificados (`TODO:53` — o drift decisão × código permanece aberto).
4. **Container: DI incompleta** — `_create` descreve `dependencies` via `Dependency`, mas nunca é chamado e `get()` não injeta (§4.4.3); `systemModules` sem escritor/leitor.
5. ~~**Registry duplicado**~~ — **reclassificado (2026-10-01):** relação atual é **herança** — `container/CoffeeRegistry.py` (ABC `CoffeeRegistry`) × `container/DefaultCoffeeRegistry.py` (`DefaultCoffeeRegistry(CoffeeRegistry)`); os antigos dicts viraram listas `dependencies`/`systemModules` (§4.4.4).
6. ~~**Typos em nomes públicos/pacotes**~~ — **CORRIGIDO em 2026-09-28** por instrução do DEV (§16.10); resta atualizar docs históricas que citam caminhos antigos (§17.8).
7. **Sem plugin system** — `moduleRegistry`/`components` sem consumidores reais (ADR 002 = PROPOSAL).
8. **Sem framework CLI, sem comandos** — `buildParser` sem chamador, `_addSubparsers` vazio.
9. **Sem testes, sem CI, README vazio, LICENSE ausente** (referenciados por `pyproject.toml:16-17`).
10. **Superfícies de segurança conhecidas** — `tool.py` pip/`sys.path`, `Config`/`Host` fora de adapter (harness §37).
11. **Diretórios órfãos** — `egine/` (UNDEFINED), `modules/ssh/{Adpiter,models,Services}/` (`TODO:55`).
12. ~~**Trabalho não commitado**~~ — **RESOLVIDO (2026-10-01):** renomeações de 2026-09-28 commitadas (`ecc3603`, `3d47da8`); `state.json` reescrito sem mojibake; doc sincronizada (v0.3.2) — commit desta sessão.
13. ~~**Ambiente** — `.venv` observado sem `platformdirs`~~ — **RESOLVIDO (2026-10-01):** `pip install -e .` executado no `.venv` (Python 3.14.7, `platformdirs` 4.12.1 OK); `import coffee` resolve de qualquer diretório.
14. **`main.py` defects (atualizado 2026-10-01)** — `Start()` contém placeholder `print("coffe")` (substituiu o `tool.menu()` inexistente), `verify_modules()` agendado via `create_task` sem aguardar (só roda com `Debug=True`), condição `if not (app or ...)` morta, import `Config` unused desde a remoção de `config_local`. `Start()` é **alcançável** (executa após `asyncio.run(main())`) — desde `628e772` falha dentro dele (`ModuleManager().loadModules()` → `RuntimeError`, §4.1/§18.1).

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
| `docs/doc.md` | **ESTE ARQUIVO (0.3.3)** | doc principal, atualizada contra HEAD `628e772` (consolidação Runtime/Context/DI 2026-10-03: §4.1/§4.3/§4.10/§6.2/§17.10-12/§18.1) |
| `docs/TODO.md` | — | registra os findings; atualizado 2026-10-03 (U-001 gap resetApp, U-002 formalização ContextVar, review boot exit 1) |
| `docs/ai/STATE.md` | 2026-10-03 | sincronizado com consolidação + boot exit 1 |
| `docs/architecture/runtime.md` | PROPOSAL + FACT; §13–§17 desde 2026-10-03 | Application Context/ContextVar/token/concorrência/erros/invariantes; §7 = código anterior ao HEAD (banner); conflitos em doc.md §17 |
| `docs/architecture/components-aop.md` | DECISION 2026-09-25; §5.1–§5.5 desde 2026-10-03 | Registry×Container, @Component, DIP, dataclass; tabela sem `initialize()` |
| `docs/decisions/001-007` | 001/003/005/006/007 DECIDED | 006 (componentes) e 007 (DI) governam a área |
| `docs/specs/coffee-cli-v1.md` | spec V1 | comandos, domínio, config, lifecycle (PROPOSAL) |
| `docs/diagrams/architecture.mmd` | — | 4 diagramas |
| `docs/research/cli-framework-comparison.md` | placeholder | framework CLI UNDEFINED |
| `README.md` / `LICENSE` | vazio / ausente | referenciados pelo `pyproject.toml` |
| `.agents/harness.md`, `context/…`, `specs/…` | — | governança e contexto do ecossistema |

## Apêndice B — Como esta doc foi produzida

1. Exploração completa da codebase pelo `codebase-explorer` (task context histórico: `.agents/protocol/tasks/temp/docs-main-technical-context.md`; **relatório global agora existe**: `.agents/protocol/docs/codebase-explorer.json`, gerado em 2026-10-01 @ `b9b15a8`), com classificação FACT/INFERENCE/PROPOSAL/UNKNOWN e confidence por achado.
2. Verificação por execução de comportamento crítico (decorator, `Config.build()`, imports quebrados, `tool.menu()`).
3. Cruzamento doc ↔ código (§17) e com o relato do DEV sobre trechos fora de escopo (§16).
4. Escrita seguindo a estrutura de documentação técnica consolidada (AGENTS.md §18) e padrões de doc técnica profissional (escopo explícito, não documentar features que não existem, evidência antes de certeza).
