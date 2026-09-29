# Codebase Explorer — Task Context: Documentação Técnica Principal (CoffeeCLI)

> **⚠️ STALE (2026-09-29) — não usar como fonte de estado atual.** Artefato histórico gerado em `cb2b812`; o código mudou desde então:
> 1. **Renomeação de typos (2026-09-28, DECISION do DEV):** todos os paths `contener/`, `componets/`, `Componet.py`, `CofeeRegistry.py`, `moduleRegestry`, `Services/`, `exepiton/` citados aqui estão **obsoletos** — ver `docs/doc.md` §16.10.
> 2. **Refatoração de tipos (2026-09-29):** o decorator `Component` agora usa `CoffeeComponent` (não `SystemModule`) e os `TypeVar` mortos de `Component.py`/`base/CoffeeRegistry.py` foram removidos — as linhas **156, 158, 207-208, 211** que descrevem a assinatura antiga estão **obsoletas** — ver `docs/doc.md` §4.5/§16.11.
> 3. Fonte atual: `docs/doc.md` (0.3.1). Regenerar este contexto antes de reutilizá-lo.

- **Modo:** TASK CONTEXT EXPLORATION
- **Gerado em:** 2026-09-28
- **Base report global:** `.agents/protocol/docs/codebase-explorer.json` — **NÃO EXISTE** (FACT: primeira exploração; nenhum relatório global prévio no projeto)
- **Git:** branch `main`, HEAD `cb2b812`, working tree SUJO (ver §0)
- **Escopo:** `src/coffee/`, `docs/`, `.agents/`, `AGENTS.md`, `pyproject.toml`

---

## 0. Estado Git (FACT)

```
branch: main · HEAD: cb2b812 "refactor: replace CoffeeRegistry with DefaultCoffeeRegistry across components"
M docs/TODO.md · M pyproject.toml · M src/coffee/core/data/Config.py
M src/coffee/core/runtime/componets/base/CoffeeRegistry.py
M src/coffee/core/runtime/contener/CofeeRegistry.py
?? .agents/state.json + 10 __init__.py (untracked)
```

Commits recentes (mesmo autor, lotes no mesmo minuto — ver §3):

```
cb2b812 refactor: replace CoffeeRegistry with DefaultCoffeeRegistry across components   2026-09-27
10fbefd docs: add components AOP spec and reconcile runtime.md section 3                2026-09-25
b0c4c49 fix(cli): root CLI/main imports and drop invalid Component inheritance          2026-09-25
dad3b2d feat(runtime): implement decorator __call__ with lifecycle entry point          2026-09-25
d326b2d refactor(core): rename ModuleRegistry to SystemModule                          2026-09-25
d5092f2 feat(componets): add CoffeeComponent/CoffeeRegistry base abstractions           2026-09-25
b366df4 fix(services): root tool imports to Config and mark helpers static             2026-09-25
0d8fe94 fix(data): correct Host/Config imports and add modules_local                   2026-09-25
6cf711c feat(core): refactor module management and introduce SSH module                (anterior)
1b938f2 feat(core): add Coffee CLI runtime skeleton                                    (skeleton DEV)
198c6c6 chore(repo): add project scaffolding
```

---

## 1. Visão geral do projeto

- **Propósito (FACT — AGENTS.md, .agents/harness.md §2):** CLI do Coffee Ecosystem — interface humana e orquestrador local. Não é um segundo servidor; o OS funciona sem Coffee.
- **Stack (FACT — pyproject.toml:1-28):** Python `>=3.11`, setuptools (`setuptools.build_meta`), layout `src/`, única dependência `platformdirs` (pyproject.toml:10, alteração não commitada). Runtime observado no `.venv`: Python 3.14.7 com **apenas pip** instalado (FACT — `pip list`: platformdirs ausente no venv).
- **Entry points:**
  1. `pyproject.toml:20` → `coffee = "coffee.cli.main:main"` — **módulo inexistente** (não há `src/coffee/cli/`) → FACT: entrypoint de instalação quebrado.
  2. `src/coffee/main.py:31-33` → `if __name__ == "__main__": asyncio.run(main()); Start()`.
  3. `src/coffee/core/__main__.py` — arquivo **vazio (0 bytes)**; não há `src/coffee/__main__.py` → `python -m coffee` não existe (FACT).
- **Zero framework CLI** (argparse puro), **zero testes**, **zero CI** (FACT).

### Árvore de `src/coffee/` (papel de cada diretório)

```
src/coffee/
├── __init__.py                      (vazio)
├── main.py                          ponto de entrada atual: decorator + Start()
├── core/
│   ├── __init__.py                  (vazio)
│   ├── __main__.py                  VAZIO (0 bytes)
│   ├── cli/
│   │   └── CLI.py                   RuntimeCLI — parser argparse (incompleto, import quebra)
│   ├── data/
│   │   ├── Config.py                Config dataclass + build() de validação
│   │   └── Host.py                  Host (username, platform)
│   ├── domain/
│   │   ├── exepiton/                (typo) InvalidCoffeeAplicationException
│   │   ├── interface/               SystemModule (ABC de módulos)
│   │   └── models/                  VAZIO (Module.py deletado em 6cf711c)
│   ├── runtime/
│   │   ├── CoffeAplicationRuntime.py (typo no nome) — lifecycle + decorator
│   │   ├── componets/               (typo)
│   │   │   ├── Componet.py          (typo) decorator @Component
│   │   │   ├── ModulePackage.py     decorator @Module
│   │   │   └── base/                CoffeeComponent (ABC) e CoffeeRegistry (ABC stub)
│   │   └── contener/                (typo)
│   │       ├── CoffeeApplicationContainer.py  composição/DI (parcial)
│   │       └── CofeeRegistry.py     (typo) DefaultCoffeeRegistry (registro)
│   └── Services/                    (maiúsculo)
│       ├── tool.py                  utilitários de terminal/paths (static methods)
│       └── module/ModuleManager.py  serviço de módulos (import quebra)
└── modules/
    ├── ssh/package.py               SSHModule (@Module) — sem consumidores
    ├── system/                      __init__ vazio
    └── update/                      __init__ vazio
```

Diretórios vazios (FACT): `egine/`, `src/coffee/core/domain/models/`, `src/coffee/modules/ssh/{Adpiter,models,Services}/`.

---

## 2. Módulos (um por um)

### 2.1 `coffee.main` — ponto de entrada
- **Responsabilidade:** bootstrap + disparo do ciclo.
- **Público:** `config_local: Config` (módulo-level, main.py:9), `Start()` (main.py:12), `main` decorado (main.py:16).
- **Deps internas:** `core.data.Config`, `core.Services.tool`, `core.runtime.CoffeAplicationRuntime`, `core.domain.exepiton.*`.
- **Fluxo típico (FACT):** import → `Config()` instanciado no escopo de módulo → `asyncio.run(main())` → `CoffeeApplicationRuntime.__call__` → `init()` → `Config().build()` **lança RuntimeError** → coroutine falha antes do corpo de `main` → `Start()` (linha 33) nunca alcança `tool.menu()` (inexistente).

### 2.2 `core.data.Config` / `core.data.Host`
- **Responsabilidade:** dados de configuração + validação de ambiente.
- **Público:** `Config` (dataclass: `configPath`, `hostData`, `Debug`, `modules_local`, `build()`), `Host` (`username`, `platform`).
- **Deps:** `platformdirs.user_config_dir`, `os`, `platform.system`.
- **Fluxo:** `Config().build()` valida path e host → usado por `Runtime.init()` (CoffeAplicationRuntime.py:21). Detalhes em §5.

### 2.3 `core.runtime.CoffeAplicationRuntime`
- **Responsabilidade:** fronteira de lifecycle (DECIDED — ADR 001, harness §42).
- **Público:** classe `CoffeeApplicationRuntime` com estado de **classe** `_container` (linha 11) e métodos de classe: `init()` (16), `getContainer()` (27), `setConfig()` (34), `stop()` (38); mais `__init__(func)` (13), `__call__` (43) e `_invokeAsync` (76).
- **Deps:** `Config`, `CoffeeApplicationContainer`.
- **Fluxo:** `init()` → `Config().build()` → `CoffeeApplicationContainer(config=...)` → guarda em `cls._container`; `getContainer()` lança `RuntimeError` se não inicializado; `stop()` zera `_container`.

### 2.4 `core.runtime.contener.CoffeeApplicationContainer`
- **Responsabilidade:** contexto/composição (segurar config e resolver componentes).
- **Público:** `__init__(config)`, `_create(dependency)` (14), `get(component)` (31), `getConfig()` (39), `setConfig()` (42); atributo de classe `dependencie: list[SystemModule] = []` (9, **nunca usado**).
- **Deps:** `Config`, `SystemModule`, `DefaultCoffeeRegistry`.
- **Fluxo:** `get(T)` → `DefaultCoffeeRegistry.get(T)` → se `None` lança `LookupError` → senão `implementation()` (nova instância a cada chamada, sem cache). `_create()` imprime parâmetros do `__init__` e **sempre lança `NotImplementedError`** (linha 29) — nunca é chamado por ninguém.

### 2.5 `core.runtime.contener.CofeeRegistry` — `DefaultCoffeeRegistry`
- **Responsabilidade:** catálogo de componentes (`components`) e de módulos (`moduleRegestry`).
- **Público (classmethods):** `register` (12), `packageRegister` (17), `contains` (22), `get` (26), `getModule` (30), `all` (34).
- **Estado:** dicionários de **classe** (compartilhados globalmente).
- **Deps:** `SystemModule`, `CoffeeRegistry` (base em `componets/base/`).
- **Leitores (FACT, grep):** `moduleRegestry` só é escrito/lido dentro do próprio arquivo — **nenhum consumidor**. `components` é lido por `Container.get()`.

### 2.6 `core.runtime.componets` (decorators)
- `Componet.Component(component)` (linha 10) → `registry.packageRegister(component)` → exige `component.id` **na classe** → `AttributeError` para classes sem `.id`. Retorna a classe.
- `ModulePackage.Module(module)` → `registry.register(module)` → `components[module] = module`. Retorna a classe.
- `base.CoffeeComponent`: ABC com `regitry = None` (typo, linha 4) e `initialize()` no-op.
- `base.CoffeeRegistry`: `@dataclass` + ABC com stubs `register`/`contains` (classmethods `...`), atributo `domain = TypeVar(...)` (13); alteração **não commitada** adiciona `T = TypeVar` (sem uso) e `contains`.

### 2.7 `core.cli.CLI`
- **Público:** `RuntimeCLI` com `@Component`, `__init__(moduleManager, config)`, `buildParser()` (retorna `ArgumentParser`), `_addSubparsers()` (loop com `pass`).
- **Deps:** `Component`, `ModuleManager`, `Config`.
- **Fluxo típico:** **não existe hoje** — o import falha (ver §3.3) e `buildParser` não tem chamador.

### 2.8 `core.Services.module.ModuleManager`
- **Público:** `ModuleManager` (`@dataclass` + `@Component`), `_modulesRegistry: list[SystemModule]`, `loadModules()` (retorna a lista vazia).
- **Fluxo típico:** `RuntimeCLI._addSubparsers` itera `loadModules()` — mas o import do módulo falha antes.

### 2.9 `core.Services.tool`
- **Público (staticmethods):** `clear_screen()` (os.system cls/clear), `verify_modules()` (async; `pip install -r <Services/requirements/requirements.txt>`), `add_path_modules(config)` (async; `sys.path.append` para cada `modules_local`).
- **Deps:** `Config`, `os`, `platform`, `subprocess`, `sys`.
- **FACT:** `src/coffee/core/Services/requirements/requirements.txt` **não existe** (Test-Path = False) → `verify_modules` falharia e cairia no `except` com print.

### 2.10 `core.domain.interface.SystemModule` / `core.domain.exepiton.*`
- `SystemModule(CoffeeComponent, ABC)`: `__slots__`, `id/name/version` (properties). `CoffeeComponent` base não declara `__slots__` → base ganha `__dict__`.
- `InvalidCoffeeApplicationException(Exception)` — usada só em `main.py:23`.

### 2.11 `modules.ssh.package`
- `SSHModule` (`@dataclass` + `@Module`) com atributos **de classe** `id/name/version`. Registrado em `components`; **nenhum consumidor** (grep: nada importa `coffee.modules.ssh`).

### Grafo de dependências internas (FACT)

```
main → Config, tool, CoffeeApplicationRuntime, InvalidCoffeeApplicationException
CoffeeApplicationRuntime → Config, CoffeeApplicationContainer
CoffeeApplicationContainer → Config, SystemModule, DefaultCoffeeRegistry
DefaultCoffeeRegistry → SystemModule, CoffeeRegistry(base)
Componet.Component → DefaultCoffeeRegistry, SystemModule
ModulePackage.Module → DefaultCoffeeRegistry
CoffeeRegistry(base) → CoffeeComponent, SystemModule
SystemModule → CoffeeComponent
CLI → Component, ModuleManager, Config
ModuleManager → Component, SystemModule
tool → Config
Config → Host, platformdirs
ssh/package → Module
```

---

## 3. INVESTIGAÇÃO ESPECIAL — trechos fora de escopo (violação DEV+AGENT)

Critério: código escrito/alterado por agente em loop, identificável por (a) diffs de commits de "fix/feat" em lote, (b) citações a docs no próprio código, (c) estilo inconsistente, (d) typos novos, (e) imports órfãos/decorators quebrados. O skeleton `1b938f2` é atribuído ao DEV e usado como linha de base.

### 3.1 `src/coffee/core/runtime/CoffeAplicationRuntime.py` — `__call__` + `_invokeAsync` + `__init__(func)`
- **Trecho:** linhas 13-15 e 43-84 (commit `dad3b2d`, 2026-09-25).
- **Classificação:** INFERENCE · **confidence MEDIUM-HIGH** (agente).
- **Evidências de autoria:**
  - Docstring cita `runtime.md §12.3` (CoffeAplicationRuntime.py:46) — `docs/architecture/runtime.md` **não possui §12.3** (§12 "Manutenção e evolução" não tem subseções numeradas) → referência documental como justificativa de código, padrão de geração por agente.
  - Docstring em português + mensagens de `TypeError` em inglês (linhas 60, 63-65) — mistura de idiomas inexistente no skeleton.
  - Commit do mesmo lote/meio-minuto de `b0c4c49`, `10fbefd`, `d326b2d` (2026-09-25 22:27).
  - Comentário de fase `# @CoffeeApplicationRuntime() — ainda estamos na fase de factory.` (linha 56) — voz de explicação de agente.
- **Comportamento observável (FACT — verificado por execução):**
  - `@CoffeeApplicationRuntime` sobre função → a função **vira uma instância** de `CoffeeApplicationRuntime` (verificado: `type(mm.main).__name__ == 'CoffeeApplicationRuntime'`).
  - Suporta `@X` e `@X()` (factory branch, linhas 55-60); qualquer outra chamada com args/kwargs lança `TypeError`.
  - Sync: `init()` → `func(self)` → `finally: stop()` (70-74). Async: retorna coroutine `_invokeAsync` → `init()` → `await func(self)` → `finally: stop()` (76-84).
  - **Com o código atual o corpo do ponto de entrada nunca executa:** `init()` → `Config().build()` lança `RuntimeError('')` (verificado) antes do `try` (linha 77 — `init()` fora do `try`, logo `stop()` nem é alcançado).
  - `func(self)` injeta a **instância runtime** (não o container) — coerente com `app: CoffeeApplicationRuntime` em main.py:17.
- **Anomalias vs. resto do projeto:**
  - `docs/architecture/runtime.md:410` e `docs/doc.md:143,371` declaram "**Não implementado** — a classe não possui `__call__`" → **CONFLICT com o código**.
  - Container é atributo de **classe** (`_container`, singleton por processo) enquanto `runtime.md:526-531` descreve "1 Application Runtime → 1 Application Container".
  - `init()` fora do `try` em `_invokeAsync` (77) quebra a garantia de `stop()` descrita em `runtime.md:307`.
  - Nomenclatura/mensagens de erro em inglês num projeto com mensagens em português (`tool.py`, `main.py:28`).
- **Callers/referências:** `src/coffee/main.py:4,16,17` (único uso real em código). Referências documentais: `runtime.md` (§3, §5.4, §7, §8), `doc.md` §4.1, ADR 001, `docs/specs/coffee-cli-v1.md:214,541,551`, `docs/diagrams/architecture.mmd:69-74`.

### 3.2 `src/coffee/core/runtime/componets/Componet.py` + `contener/CofeeRegistry.py` — regressão do `@Component`
- **Trecho:** `Componet.py:10-12` (`registry.packageRegister(component)`) e `CofeeRegistry.py:16-19` (`moduleRegestry[module.id] = module`).
- **Classificação:** FACT (comportamento) · INFERENCE (autoria agente) · **confidence HIGH** para comportamento, **HIGH** para autoria do trecho (diff de `6cf711c` mostra `Componet.py` como "new file" com `packageRegister`, substituindo o `Componet.py`→`register` do skeleton `1b938f2`).
- **Comportamento observável (FACT — verificado):**
  ```
  import coffee.core.Services.module.ModuleManager
  → AttributeError: type object 'ModuleManager' has no attribute 'id'
  import coffee.core.cli.CLI
  → AttributeError (por importar ModuleManager)
  ```
  Ou seja: **dois módulos do projeto não importam hoje.**
- **Anomalias:**
  - Skeleton usava `registry.register(component)` (funciona com classes); agente trocou para `packageRegister` que exige instância com `.id` → **regressão**.
  - Nome de arquivo `Componet.py` vs classe `Component`; assinatura `Component(component: SystemModule) -> SystemModule` usada como decorator de **classe** (tipagem incorreta).
  - `TypeVar component` declarado e nunca usado (`Componet.py:7`).
  - `registry = DefaultCoffeeRegistry()` instanciado (Componet.py:5, ModulePackage.py:3) apesar de todos os métodos serem `@classmethod`.
  - Duas classes **homônimas** `CoffeeRegistry`: `contener/CofeeRegistry.py` (funcional, classe `DefaultCoffeeRegistry`) e `componets/base/CoffeeRegistry.py` (ABC stub) — reconhecido como questão aberta em `docs/architecture/components-aop.md:107,116`.
  - `base/CoffeeRegistry.py`: `@dataclass` sobre ABC, `domain = TypeVar(...)` como atributo de classe (13), `abstractmethod` importado sem uso, `T` adicionado sem uso (diff não commitado).
  - Typo `moduleRegestry` (CofeeRegistry.py:9).
- **Registro já existente:** `docs/TODO.md:47` (OUT-OF-SCOPE FINDING) e `components-aop.md:110`.

### 3.3 `src/coffee/core/runtime/contener/CoffeeApplicationContainer.py` — `_create`/`dependencie`
- **Trecho:** linhas 9 (`dependencie: list[SystemModule] = []`), 14-29 (`_create` com `print` de debug e `NotImplementedError`), imports `inspect`/`SystemModule` (1, 4).
- **Classificação:** INFERENCE (agente) · **confidence MEDIUM-HIGH** — skeleton `1b938f2` não tinha `_create`, `dependencie` nem `inspect`; foram introduzidos em `6cf711c` (`depencies: dict[inspect.Signature, type]` + `_create` sem `self`) e reescritos em `d326b2d` (vira `_create(self, dependency)`, `dependencie`, `print`, `NotImplementedError`).
- **Comportamento observável:** `_create` **nunca é chamado** por nenhum código; se fosse, imprimiria os parâmetros e lançaria `NotImplementedError`. `dependencie` nunca é lido (grep). `get()` instancia do zero a cada chamada.
- **Anomalias:** `dependencie`/`dependecy` (typos, herdados do rascunho), `print` de debug deixado em código de biblioteca, divergência com `runtime.md:404` ("container guarda apenas Config") e com `components-aop.md:108` (registra `_create()` → `NotImplementedError`).

### 3.4 `src/coffee/main.py` — estrutura de entrada remendada
- **Trecho:** linhas 9, 12-14, 16-29, 31-33.
- **Classificação:** estrutura original do DEV (`1b938f2` tinha `from ..data.data import data`, `data_local = data()`, `from tool import tool`) + remendos do agente (`b0c4c49` trocou `data`→`Config` e re-rootou imports) · **INFERENCE MEDIUM-HIGH** para os remendos, **FACT** para o estado atual.
- **Comportamento observável (FACT — verificado):**
  - `config_local = Config()` no import (linha 9).
  - `main` vira instância do runtime; `asyncio.run(main())` → `RuntimeError` (de `Config.build()`) e o corpo de `main` não executa; `Start()` (linha 33) não é alcançado.
  - Mesmo sem o erro: `tool.menu()` **não existe** (verificado: `hasattr(tool,'menu') == False`), `tool.verify_modules()` é `async` chamado sem `await` (linha 20), `if not (app or app.getContainer())` (linha 22) é sempre `False` quando `app` é truthy → exceção nunca disparada.
  - Mensagem com typo: `"Erro StopAsycnInteration"` (linha 28); `except` captura `StopAsyncIteration`, que nunca ocorre no corpo.
- **Registro já existente:** `docs/TODO.md:14,48`.

### 3.5 `src/coffee/core/cli/CLI.py`
- **Trecho:** `@Component` (linha 7), `_addSubparsers` com `for ... : pass` (21-23).
- **Classificação:** INFERENCE (agente) · **confidence MEDIUM**. `6cf711c` acrescentou `class RuntimeCLI(Component)` (herança de função — inválida), `__init__` e `_addSubparsers`; `b0c4c49` **removeu** a herança e arrumou imports. `@Component` veio do skeleton.
- **Comportamento:** import falha (AttributeError via ModuleManager/Component); `buildParser()` não tem chamador; `_addSubparsers` não faz nada.
- **Anomalias vs. docs:** `doc.md:174` e `runtime.md:467` dizem que `CLI.py` tem `@CoffeeApplicationRuntime` → **CONFLICT** (hoje tem `@Component`, removido do runtime em `b0c4c49`).

### 3.6 `src/coffee/core/Services/module/ModuleManager.py`
- **Trecho:** `@dataclass` + `@Component` (6-7), `loadModules` (11-12).
- **Classificação:** `@Component` é do **skeleton DEV**; a **quebra** é do agente (mudança de semântica do registry em `6cf711c`) · **FACT** (comportamento) / **INFERENCE MEDIUM** (atribuição).
- **Comportamento:** import falha com `AttributeError` (verificado).
- **Anomalias vs. docs:** `doc.md:86,166,373`, `runtime.md:468`, `STATE.md:91`, ADR 001:37 dizem que `ModuleManager` tem **`@CoffeeApplicationRuntime`** (violação de lifecycle) → **CONFLICT**: hoje tem `@Component`; o runtime foi removido em algum momento anterior ao HEAD. ADR 007 (DECIDED) prevê constructor injection — ainda não implementado.

### 3.7 `src/coffee/core/data/Config.py` — `build()` sempre lança
- **Trecho:** linhas 18-22.
- **Classificação:** FACT comportamental · **AUTHORIA: UNKNOWN (provável DEV)** — a condição invertida `if not self.hostData.platform == None: raise RuntimeError()` **já existe no skeleton `1b938f2`**. O agente (`0d8fe94`) corrigiu `os.path.isdir()` sem argumento → `os.path.isdir(self.configPath.absolute())`, re-rootou imports, adicionou `return self` e `modules_local` — e **manteve** a condição invertida.
- **Comportamento observável (FACT — verificado):** `Config(configPath=Path('.')).build()` → `RuntimeError ''` mesmo com o path existindo, porque `Host.platform = system()` nunca é `None` → `not (platform == None)` é sempre `True` → sempre lança. **Consequência: `Runtime.init()` nunca completa.**
- **Anomalias:** `RuntimeError()` sem mensagem; validação não cria o diretório de config; `main.py` instancia `Config()` sem `build()` em paralelo ao runtime que chama outro `Config()`.

### 3.8 `src/coffee/core/Services/tool.py`
- **Trecho:** `verify_modules` (19-31), `add_path_modules` (34-47), `@staticmethod` em tudo.
- **Classificação:** INFERENCE (agente) · **confidence MEDIUM-HIGH** — `b366df4` trocou `from coffee.core.data.data import data` (módulo inexistente) por `Config` e marcou métodos `@staticmethod`; `6cf711c` moveu `src/tool.py` → `core/Services/tool.py`.
- **Comportamento:** `verify_modules` aponta para `Services/requirements/requirements.txt` **inexistente** → `FileNotFoundError` capturado → print; `add_path_modules` faz `sys.path.append` dinâmico.
- **Risco registrado pelo próprio projeto:** `harness.md:1496-1501` (pip install no boot + sys.path.append = superfícies de supply chain/import; `Config.py`/`Host.py` com `os`/`platform` fora de adapter).

### 3.9 `__init__.py` vazios ×10 (untracked) e `.agents/state.json`
- **Classificação:** FACT — gerados pelo agente (TODO TASK-001, `docs/TODO.md:35`; `state.json` registra TASK-001..004 concluídos).
- **Anomalias:** criados também em pacotes sem código (`modules/system`, `modules/update`); `state.json` está com **encoding quebrado** (mojibake: "conclu?dos") e afirma `validationStatus: PASS - 33/33 módulos importam` → **CONFLICT** com o AttributeError verificado hoje em 2 módulos.

### 3.10 `modules/ssh/package.py`
- **Classificação:** FACT (criado em `6cf711c`, lote de agente) · INFERENCE MEDIUM.
- **Comportamento:** `@Module` registra `SSHModule` (dataclass com atributos de classe, **não** subclasse de `SystemModule`) em `components`; nenhum leitor/consumidor existe.

### 3.11 Erros estruturais conhecidos (AGENTS.md) — verificação
| Afirmação em AGENTS.md | Estado hoje | Confidence |
|---|---|---|
| entrypoint quebrado | **AINDA EXISTE** — `pyproject.toml:20` → `coffee.cli.main:main` inexistente | FACT · HIGH |
| imports quebrados | **PARCIALMENTE CORRIGIDOS** — re-rooting `core.*` → `coffee.core.*` feito; hoje a falha é `AttributeError` no import de `CLI` e `ModuleManager` | FACT · HIGH (verificado por execução) |
| "arquivo de runtime sem extensão" | **NÃO ENCONTRADO** — scan de disco e de todo o histórico git não achou nenhum arquivo sem extensão; `core/__main__.py` existe e está vazio (0 bytes) | UNKNOWN · o que AGENTS.md quer dizer com isso |
| — | `egine/` (pasta vazia, nome sem decisão — harness §42 "UNDEFINED") | FACT |

---

## 4. Fluxos de execução

### 4.1 Fluxo instalado (quebrado)
```
`coffee` (entry point pyproject) → coffee.cli.main:main → ModuleNotFoundError (módulo não existe)
FACT · pyproject.toml:20 · confidence HIGH
```

### 4.2 Fluxo atual por execução direta (`python src/coffee/main.py` / `python -m coffee.main`)
```
import coffee.main
  ├─ Config()            (main.py:9)   → dataclass default, sem build()
  ├─ @CoffeeApplicationRuntime (16)    → main vira instância do runtime
  └─ __main__ (31)
       ├─ asyncio.run(main())
       │    └─ __call__ (CoffeAplicationRuntime.py:43)
       │         └─ _invokeAsync (76)
       │              ├─ init() (16)
       │              │    ├─ Config().build() (21) → RuntimeError('')  ← FALHA AQUI (verificado)
       │              │    └─ (não alcança) CoffeeApplicationContainer(config=...)
       │              └─ (try/finally não alcançado → stop() não roda)
       └─ Start() (33) → tool.menu()  ← inalcançável; mesmo alcançando: AttributeError (menu não existe)
```

### 4.3 Fluxo de registro de componentes (quando os imports funcionassem)
```
import do módulo decorado
  → @Component → DefaultCoffeeRegistry.packageRegister → moduleRegestry[id]   (quebra p/ classes sem .id)
  → @Module    → DefaultCoffeeRegistry.register → components[cls]
Runtime.init() → Container(config)
Container.get(T) → DefaultCoffeeRegistry.get(T) → T()   (instância nova por chamada)
```
**FACT:** nenhum código chama `Container.get()` nem `Runtime.getContainer()` fora do próprio runtime/main (grep).

### 4.4 Fluxo documentado (intenção)
```
EntryPoint → CoffeeApplicationRuntime → init() → Config.build() → Container → serviços
           → execução → stop() em try/finally
```
`docs/architecture/runtime.md:227-243`, `docs/specs/coffee-cli-v1.md` §11.1 (bootstrap com plugins — PROPOSAL, não implementado).

---

## 5. Configuração e persistência

- **`Config` (FACT — `core/data/Config.py:7-24`):** dataclass com `configPath = Path(user_config_dir("Coffee"))`, `hostData: Host`, `Debug: bool = False`, `modules_local: list[str] | None = None`.
- **Caminho observado (FACT):** `C:\Users\Quitto\AppData\Local\Coffee` (Windows, platformdirs). Harness §35 documenta `~/.config/Coffee/` como destino — **diferença de convenção Unix vs platformdirs**.
- **`build()` (FACT — verificado):** valida `configPath.exists() and isdir` (lança `RuntimeError()` vazio se falhar) e depois **sempre** lança por causa da condição invertida em `Config.py:21-22` → nunca retorna `self`.
- **Persistência real (FACT — grep em `src/coffee/**.`):** **zero** ocorrências de `open(`, `json.`, `toml`, `yaml`, `read_text`, `write_text`, `user_data_dir`, `user_cache_dir`. **Nenhum arquivo de config é lido ou escrito hoje.**
- **`Host` (FACT):** `username = os.getlogin()`, `platform = system()` — defaults avaliados na instanciação; `os.getlogin()` pode falhar em ambientes sem sessão interativa.
- **Estado:** não existe camada de estado; `Debug`/`modules_local` só são lidos por `main.py:19` e `tool.add_path_modules` (que nunca é chamado).
- **Formato/plano (PROPOSAL/UNDEFINED):** `harness.md:1408-1412` → "Formato do sistema de configuração: UNDEFINED DECISION"; `docs/specs/coffee-cli-v1.md` §8.1 propõe `coffee.toml` com precedência args > `./coffee.toml` > `~/.config/coffee/coffee.toml` > `/etc/coffee/` > defaults (ADR pendente).
- **Segurança registrada (FACT — harness.md:1493-1504):** `tool.py` (pip install no boot, `sys.path.append`) e `Config.py`/`Host.py` (acesso direto a `os`/`platform` fora de adapter) são riscos conhecidos — registrar, não corrigir.

---

## 6. Testes e docs existentes

### Testes
- **Nenhum** (FACT): não há `tests/`, nenhum `test*.py`/`*_test.py`, nenhuma seção `[tool.pytest]` no `pyproject.toml`, nenhum CI (TODO TASK-005 pendente). `.gitignore` só prepara caches de pytest/coverage.
- **Validação real disponível hoje (FACT):** `python -m compileall src` (sintaxe) e import por módulo — esta última **falha** para `coffee.core.cli.CLI` e `coffee.core.Services.module.ModuleManager`.

### Docs — inventário (FACT)
| Arquivo | Linhas | Data/Status | Observação para a doc principal |
|---|---|---|---|
| `docs/doc.md` | 405 | 2026-09-22 | **Documentação técnica consolidada existente — STALE** (ver §6.1) |
| `docs/TODO.md` | 72 | **sujo (não commitado)** | traz findings OUT-OF-SCOPE já registrados (linhas 14-15, 47-49) |
| `docs/ai/STATE.md` | 107 | 2026-09-23 | estado operacional; próximo passo 5-7 parcialmente cumprido/stale |
| `docs/architecture/runtime.md` | 636 | PROPOSAL | §7 "Implementação atual (FACT)" descreve código **anterior** ao HEAD |
| `docs/architecture/components-aop.md` | 139 | DECISION 2026-09-25 | **mais atualizado** — §5 "Estado no código" bate com o código |
| `docs/decisions/001..007` | — | 001/003/005/006/007 DECIDED, 002/004 PROPOSAL | ADRs 006 e 007 governam componentes/DI |
| `docs/specs/coffee-cli-v1.md` | 537 | spec V1 | comandos MVP, domínio, config, lifecycle (PROPOSAL) |
| `docs/diagrams/architecture.mmd` | 190 | — | 4 diagramas Mermaid |
| `docs/research/cli-framework-comparison.md` | 71 | placeholder | framework CLI ainda UNDEFINED |
| `README.md` | **0** | vazio | referenciado por `pyproject.toml:17` |
| `LICENSE` | **ausente** | — | referenciado por `pyproject.toml:16` |
| `.agents/harness.md` | 1838 | governança | §41 mapa de docs, §42 decisões |
| `.agents/context/coffee-ecosystem-conversation-documentation.md` | 973 | fonte arquitetural DEV | contexto de produto |
| `.agents/specs/ux-ui-language.md` | 247 | DECISION | linguagem visual TUI |
| `.agents/specs/coffee-components-aop.md` | 78 | espelho de `docs/architecture/components-aop.md` | |
| `.agents/state.json` | — | untracked, mojibake | afirma "33/33 módulos importam" (CONFLICT) |

### 6.1 CONFLITOS doc ↔ código (obrigatório sinalizar na doc principal)
1. `runtime.md:410` + `doc.md:143,371` → "decorator NÃO implementado" vs `__call__` existente (`CoffeAplicationRuntime.py:43`) — **CONFLICT** (código mais novo que a doc).
2. `runtime.md:372,389` + `doc.md:140,372` + ADR 001:36 → typo `getContener` vs código `getContainer` (`CoffeAplicationRuntime.py:28`) — **CONFLICT** (já corrigido).
3. `doc.md:86,166,174,247`, `runtime.md:467-468`, `STATE.md:91` → `ModuleManager`/`CLI` com `@CoffeeApplicationRuntime` vs `@Component` — **CONFLICT**.
4. `doc.md:90` → árvore com `core/domain/models/Module.py` (deletado em `6cf711c`, dir vazio) — **CONFLICT**.
5. `doc.md:151` / `runtime.md:404` → "container guarda apenas Config" vs `get/_create/dependencie` — **parcialmente stale**.
6. `.agents/state.json` → "33/33 módulos importam" vs AttributeError verificado — **CONFLICT**.
7. `components-aop.md:101-118` → **consistente** com o código (usar como referência de estado atual).
8. `STATE.md:89-91` → próximos passos 5 (implementar `__call__`) e 6 (`getContener`→`getContainer`) **já feitos**; 7 (remover decorator do ModuleManager) **mudou de objeto** (hoje é `@Component`).

---

## 7. Known limitations / dívidas técnicas evidenciadas pelo código

Todos FACT, com evidência:

1. **Entrypoint de instalação quebrado** — `pyproject.toml:20` aponta para módulo inexistente; decisão é do DEV (TODO:14).
2. **`Config.build()` sempre lança** — `Config.py:21-22` (verificado) → nenhum boot completa.
3. **Dois módulos não importam** — `CLI` e `ModuleManager` → `AttributeError` via `@Component`/`packageRegister` (verificado; TODO:47).
4. **Decorator de lifecycle vs. realidade** — `stop()` não roda se `init()` falhar (`CoffeAplicationRuntime.py:77`); `_container` é singleton de classe.
5. **Container sem DI real** — `_create` sempre `NotImplementedError` (linha 29); `get()` não injeta dependências (só `T()` sem argumentos — falharia para `RuntimeCLI`, que exige 2 args).
6. **Registry duplicado** — `contener/CofeeRegistry.py` vs `componets/base/CoffeeRegistry.py` (components-aop.md:107,116).
7. **Nomenclatura com typos em nomes públicos/pacotes** — `CoffeAplicationRuntime.py`, `contener/`, `componets/`, `Componet.py`, `CofeeRegistry.py`, `exepiton/`, `InvalidCoffeeAplicationException.py`, `Services/` (maiúsculo), `moduleRegestry`, `dependencie`, `regitry`, `StopAsycnInteration` (main.py:28) — renomear exige cascata de imports (TODO:15, decisão do DEV).
8. **Sem sistema de plugins** — `modules/` não tem discovery/loading; `moduleRegestry` e `components` sem consumidores (ADR 002 = PROPOSAL).
9. **Sem framework CLI, sem comandos** — só `buildParser()` não chamado; `_addSubparsers` vazio (CLI.py:21-23).
10. **Sem testes, sem CI, sem README/LICENSE** (§6).
11. **Superfícies de segurança conhecidas** — `tool.py` pip install + `sys.path.append`; `Config`/`Host` com `os`/`platform` fora de adapter (harness §37).
12. **Diretórios órfãos** — `egine/` (nome UNDEFINED, harness §42), `core/domain/models/`, `modules/ssh/{Adpiter,models,Services}/` (TODO:49).
13. **Estado de trabalho não commitado** — 5 arquivos modificados + 11 untracked; doc/estado podem divergir do HEAD.
14. **Ambiente** — `.venv` sem `platformdirs` instalado (só pip), apesar de TODO:38 registrar `pip install -e .` OK (UNKNOWN em qual ambiente).

---

## Incertezas / QUESTIONS TO DEV

- **UNKNOWN:** o que AGENTS.md quer dizer com "arquivo de runtime sem extensão" — nenhum arquivo sem extensão existe em disco nem no histórico git.
- **UNKNOWN (autoria):** condição invertida do `Config.build()` é do skeleton do DEV; agente a preservou em `0d8fe94`.
- **UNKNOWN:** em qual ambiente a validação "33/33 módulos importam" de `state.json` foi executada (hoje falha em 2).
- **QUESTION:** qual fonte a doc principal deve seguir quando `runtime.md`/`doc.md` divergirem do código — código = estado atual (regra do harness §3), mas a intenção de lifecycle continua documentada.
- **QUESTION:** decisão de renomear a estrutura com typos antes ou depois de escrever a doc principal (afeta todos os caminhos citados).

## Recomendação de especialização (fora do escopo do Explorer)
- Análise de segurança de `tool.py`/`sys.path` → `security-lead`.
- Estrutura de testes e CI → `test-engineer`.
- Decisões de entrada/renomeação → DEV (já em `docs/TODO.md`).
