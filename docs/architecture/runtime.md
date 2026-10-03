# CoffeeApplicationRuntime — Conceituação e Uso

**Status:** PROPOSAL (conceituação validada pelo DEV) + FACT onde verificado por execução — **atualizado em 2026-10-03** (Application Context/ContextVar documentado nas §13–§17; comportamento real do lifecycle nas §5.3/§5.4; ver também `docs/doc.md` §4.3/§4.10 — doc.md prevalece)  
**Código-fonte:**
- `src/coffee/core/runtime/CoffeeApplicationRuntime.py`
- `src/coffee/core/runtime/CoffeeApplicationContext.py`
- `src/coffee/core/container/CoffeeApplicationContainer.py`
- `src/coffee/core/components/CoffeeComponent.py`

> **Paths atualizados em 2026-10-01** (antes: `CoffeAplicationRuntime.py`, `runtime/contener/` — typos corrigidos no rename de 2026-09-28 e estrutura movida no restructure `3d47da8`; ver `docs/doc.md` §3.2/§16.10).

---

## Sumário

1. [Problema](#1-problema)
2. [Conceito central](#2-conceito-central)
3. [Relação com AOP](#3-relação-com-aop)
4. [CoffeeApplicationContainer](#4-coffeeapplicationcontainer)
5. [Arquitetura e fluxo](#5-arquitetura-e-fluxo)
6. [Responsabilidades e regra arquitetural](#6-responsabilidades-e-regra-arquitetural)
7. [Implementação atual (FACT)](#7-implementação-atual-fact)
8. [Uso](#8-uso)
9. [Dependência e inversão de controle](#9-dependência-e-inversão-de-controle)
10. [Instâncias compartilhadas](#10-instâncias-compartilhadas)
11. [Escopo e limites](#11-escopo-e-limites)
12. [Manutenção e evolução](#12-manutenção-e-evolução)
13. [Application Context (ContextVar)](#13-application-context-contextvar)
14. [Token do ContextVar](#14-token-do-contextvar)
15. [ContextVar e concorrência](#15-contextvar-e-concorrência)
16. [Erros comuns](#16-erros-comuns)
17. [Invariantes arquiteturais](#17-invariantes-arquiteturais)

---

## 1. Problema

Sem um runtime, cada ponto de entrada da aplicação (CLI, workers, processos auxiliares) precisaria repetir o mesmo bootstrap:

```text
main
 ├── cria Config
 ├── cria Container
 ├── cria serviços
 └── inicia aplicação
```

Isso gera:

- **Duplicação** — toda entrada reimplementa a inicialização.
- **Acoplamento** — o ponto de entrada conhece detalhes de construção das dependências.
- **Imprevisibilidade** — cada entrada sobe e desce a aplicação de um jeito.

O `CoffeeApplicationRuntime` resolve isso encapsulando o ciclo de vida em um único lugar.

---

## 2. Conceito central

O `CoffeeApplicationRuntime` é a **fronteira entre a criação da aplicação e a execução da lógica da aplicação**.

> **Princípio:** o Runtime **não é o cérebro da aplicação**. Ele é a fronteira que cria o contexto necessário para que a aplicação possa funcionar.

Ele representa **a vida da aplicação**, não o domínio:

```text
                  CoffeeApplicationRuntime
                        │
                   intercepta execução
                        │
              ┌─────────┴─────────┐
              │                   │
            antes               depois
              │                   │
            init()              stop()
              │
              ▼
     CoffeeApplicationContainer
              │
              ├── Config
              ├── instâncias compartilhadas
              └── contexto da aplicação
              │
              ▼
         execução do componente
```

Fluxo resumido:

```text
interceptar a execução
        ↓
inicializar a aplicação
        ↓
disponibilizar o contexto
        ↓
executar o código
        ↓
encerrar a aplicação
```

### Por que "Runtime"?

Porque o componente não guarda dados de negócio nem implementa regras — ele controla **quando a aplicação começa e quando ela termina**. É análogo ao ciclo de vida de um servlet container ou de um `Application` web framework, mas deliberadamente menor.

---

## 3. Relação com AOP

A comparação com **AOP** (Aspect-Oriented Programming) é **conceitual**, e foi
alargada pela spec de componentes (`.agents/specs/coffee-components-aop.md`,
DECISION 2026-09-25): o AOP do Coffee cobre a **infraestrutura declarativa de
componentes** (`CoffeeComponent` → `CoffeeRegistry` → `CoffeeApplicationContainer`,
com registro, resolução e DI) **e** o **único around de execução**, que continua
sendo o lifecycle da aplicação.

Alargada, porém **nada muito grande**: continua sendo uma infraestrutura leve,
não um framework AOP — ver a tabela "O que o Coffee NÃO pretende ser" abaixo.

No AOP clássico (ex.: Spring), um *around advice* envolve a execução de um ponto de entrada:

```text
antes da execução
        ↓
execução
        ↓
depois da execução
```

No Coffee, o runtime é usado como **decorator** para envolver uma função:

```python
@CoffeeApplicationRuntime()
async def main(app):
    ...
```

Ou seja, conceitualmente:

```text
@CoffeeApplicationRuntime()
        ↓
runtime.init()
        ↓
main(app)
        ↓
runtime.stop()
```

### O que o Coffee NÃO pretende ser

| AOP completo (Spring) | Coffee Runtime |
|---|---|
| pointcuts genéricos | — |
| weaving em tempo de compilação/load | — |
| interceptação arbitrária de métodos | — |
| proxies complexos | — |
| infraestrutura de aspectos | — |
| — | **1 único around: lifecycle da aplicação** |

O objetivo continua sendo uma **abstração leve**: não há pointcuts, weaving,
proxies nem interceptação arbitrária de métodos. O "AOP" do Coffee é a
infraestrutura declarativa de componentes descrita em
`docs/architecture/components-aop.md`, e não aspectos em tempo de execução.

---

## 4. CoffeeApplicationContainer

O `CoffeeApplicationContainer` é o **contexto de execução criado pelo runtime**. Ele guarda as referências das instâncias que pertencem à aplicação e precisam ser compartilhadas durante aquele ciclo de vida.

```text
CoffeeApplicationRuntime
            │
            ▼
CoffeeApplicationContainer
            │
            ├── Config
            ├── ModuleManager   (futuro)
            ├── outros serviços (futuro)
            └── instâncias compartilhadas
```

### Separação de papéis (essencial)

```text
Config     = dados e configurações da aplicação
Container  = contexto e referências das instâncias da aplicação
Runtime    = ciclo de vida da aplicação
```

A `Config` **não** deve conhecer os serviços do Coffee nem ser responsável por construí-los. Se essa fronteira cair, a `Config` vira uma *God Class*.

---

## 5. Arquitetura e fluxo

### 5.1 Estrutura do código

```text
src/coffee/
├── config/
│   └── Config.py                        # Configurações (dado)
├── data/
│   └── Host.py                          # Dados de host
└── core/
    ├── runtime/
    │   ├── CoffeeApplicationRuntime.py  # Ciclo de vida + decorator
    │   ├── CLI.py                       # Ponto de entrada CLI
    │   └── lifecycle/
    ├── container/
    │   ├── CoffeeApplicationContainer.py # Contexto compartilhado
    │   ├── CoffeeRegistry.py             # ABC do registry
    │   ├── DefaultCoffeeRegistry.py      # Registry funcional
    │   └── registry.py                   # Singleton registry
    ├── components/
    │   ├── CoffeeComponent.py            # ABC base
    │   └── decorators/                   # @Component, @Module
    ├── services/
    │   └── module/ModuleManager.py       # Serviço de módulos
    └── domain/
        └── models/                       # Modelos de domínio
```

> **Estrutura atualizada em 2026-10-01** (o quadro anterior refletia a árvore pré-rename: `contener/`, `Services/`, `cli/`, `data/` dentro de `core/` — ver `docs/doc.md` §3.2).

### 5.2 Fluxo de inicialização

```mermaid
graph TD
    A[EntryPoint: main / CLI / worker] --> B[CoffeeApplicationRuntime]
    B --> C{init()}
    C --> D[Config.build]
    D --> E[CoffeeApplicationContainer]
    E --> F[Config]
    E --> G[Serviços / instâncias]
    B -- injeta contexto --> A
    A --> H[Execução da aplicação]
    H --> I{stop()}
    I --> J[container = None]
```

Versão em ASCII:

```text
main / entrypoint
        ↓
CoffeeApplicationRuntime
        ↓
init()
        ↓
Config.build()
        ↓
CoffeeApplicationContainer
        ↓
instâncias necessárias
        ↓
execução da aplicação
        ↓
stop()
```

### 5.3 Disponibilização do contexto

Existem **dois caminhos** de acesso ao contexto — ambos resolvem para a mesma instância de `CoffeeApplicationRuntime`:

**Caminho 1 — parâmetro do ponto de entrada** (o entrypoint recebe `app` explicitamente):

```python
@CoffeeApplicationRuntime
async def main(app):
    container = app.getContainer()
    config = container.getConfig()
```

**Caminho 2 — Application Context** (componentes acessam sem receber `app`):

```python
@Component
class ModuleManager(CoffeeComponent):
    def loadModules(self):
        config = self.container.getConfig()   # via CoffeeApplicationContext
```

```text
CoffeeComponent.container (property)
        ↓
CoffeeApplicationContext.getApp()      ← ContextVar
        ↓
CoffeeApplicationRuntime
        ↓
getContainer()
        ↓
ApplicationContainer
```

Documentação detalhada do caminho 2 em [§13](#13-application-context-contextvar).

### 5.4 Lifecycle

Quatro momentos:

```text
construction      → __init__    (cria o objeto runtime)
      ↓
initialization    → init()      (sobe a aplicação)
      ↓
execution         → código do ponto de entrada
      ↓
shutdown          → stop()      (encerra recursos)
```

Regras:

- `__init__` **só** cria o objeto runtime (guarda o `func` do decorator).
- A subida real da aplicação acontece em `init()` (composition root: `Config` → `registry` → `Container`).
- O encerramento acontece em `stop()`.

Com o decorator, o lifecycle real (**FACT — código atual, verificado por execução**) é:

```python
# Caminho síncrono (CoffeeApplicationRuntime.__call__):
token = CoffeeApplicationContext.setApp(self)   # ANTES de init
self.init()
try:
    return func(self)
finally:
    CoffeeApplicationContext.resetApp(token)    # restaura estado anterior
    self.stop()                                 # libera o container

# Caminho assíncrono (_invokeAsync):
token = CoffeeApplicationContext.setApp(self)   # setApp ocorre em __call__
self.init()
try:
    return await func(self)
finally:
    self.stop()                                 # ⚠ GAP: sem resetApp(token)
```

Ordem crítica: **`setApp()` precisa acontecer antes de qualquer componente acessar `CoffeeApplicationContext.getApp()`** — e de fato acontece antes de `init()` e antes do entrypoint nas duas rotas (Runtime:61 × 78/86).

> **GAPS CONHECIDOS (FACT, 2026-10-03 — registrados, não corrigidos):**
> 1. A rota **assíncrona não chama `resetApp(token)`** no `finally` (Runtime:92-93) — o token vaza; verificado por execução: o boot atual (`python -m coffee.main`) termina com **exit 1** (`Start()` → `RuntimeError: CoffeeApplicationRuntime is not initialized`), porque o ContextVar ainda aponta para o app (leak) após `stop()` ter liberado o container.
> 2. A forma **factory** `@CoffeeApplicationRuntime()` chama `setApp` na decoração (Runtime:61) e **nunca reseta** aquele token.
> 3. `init()` está **fora** do `try` nas duas rotas — se `init()` falhar, `stop()` não roda.
>
> O modelo conceitual correto permanece: `init → setApp → entrypoint → resetApp → stop`. Correção dos gaps requer decisão do DEV (U-001 do task context do explorer).

---

## 6. Responsabilidades e regra arquitetural

### 6.1 Quem faz o quê

| Componente | Responsabilidade | NÃO é responsável por |
|---|---|---|
| **Runtime** | controlar lifecycle; criar o container; disponibilizar contexto; finalizar recursos; interceptar via decorator | lógica de negócio, configuração, persistência |
| **Container** | manter referências das instâncias; servir como contexto compartilhado; expor dependências | criar serviços, controlar lifecycle |
| **Config** | representar/validar/construir configurações e ambiente | gerenciar serviços da aplicação |
| **Serviços** | executar o próprio domínio (ModuleManager → módulos; Storage → persistência; etc.) | lifecycle completo da aplicação |

### 6.2 Regra principal

```text
Config       define
Container    disponibiliza
Runtime      controla
Service      executa
```

Ou em camadas:

```text
CONFIGURATION
      ↓
COMPOSITION
      ↓
LIFECYCLE
      ↓
EXECUTION
```

### 6.3 Composition Root

O `init()` do runtime é o **composition root** da aplicação — o lugar onde as dependências principais são montadas:

```python
def init(self) -> None:
    config = Config().build()
    self.container = CoffeeApplicationContainer(config=config)
```

Isso concentra a montagem em um ponto único e previsível.

---

## 7. Implementação atual (FACT)

> **STATUS 2026-10-01 — snapshot DESATUALIZADO:** o quadro abaixo anterior ao rework de `2026-09-28/29` (classmethods + `_container` de classe + decorator `__call__`/`_invokeAsync` funcionais + registry `DefaultCoffeeRegistry`). Ele ainda mostra `getContener` (typo corrigido no código), um container "só `Config`" e métodos de instância — **não é o código atual**. A implementação real está em `src/coffee/core/runtime/CoffeeApplicationRuntime.py` e é documentada em `docs/doc.md` §4.3/§4.4 (**doc.md prevalece** — DECISION 2026-09-28). Mantido abaixo como referência histórica do formato pretendido (§2–§5).

O código real em `CoffeAplicationRuntime.py`:

```python
@dataclass
class CoffeeApplicationRuntime:

    def __init__(self):
        self.container: CoffeeApplicationContainer | None = None

    def init(self) -> None:
        config = Config().build()
        self.container = CoffeeApplicationContainer(config=config)

    def getContener(self) -> CoffeeApplicationContainer:
        return self.container

    def setConfig(self, config: Config) -> None:
        self.container.setConfig(config=config)

    def stop(self) -> bool:
        self.container = None
        return True
```

### API pública atual

| Método | Assinatura | O que faz |
|---|---|---|
| `__init__` | `() -> None` | Cria o runtime com `container = None` |
| `init` | `() -> None` | Constrói `Config` e cria o `CoffeeApplicationContainer` |
| `getContener` | `() -> CoffeeApplicationContainer` | Devolve o container *(nome com typo: "Contener")* |
| `setConfig` | `(config: Config) -> None` | Repassa a config ao container |
| `stop` | `() -> bool` | Zera o container; retorna `True` |

### Container atual

```python
@dataclass
class CoffeeApplicationContainer:
    config: Config

    def getConfig(self) -> Config: ...
    def setConfig(self, config: Config) -> None: ...
```

Hoje o container guarda **apenas** `Config`. `ModuleManager` e demais serviços ainda **não** estão no container.

### Lacunas entre conceito e código (FACT)

| Item | Conceito (§2–§5) | Código atual |
|---|---|---|
| Decorator com `init`/`stop` automático | `@CoffeeApplicationRuntime()` envolve a função | **Não implementado** — a classe não possui `__call__`; usar `@CoffeeApplicationRuntime` em `main.py`, `CLI.py` e `ModuleManager.py` hoje não injeta contexto nem controla lifecycle |
| Injeção do contexto no ponto de entrada | `main(app)` recebe o runtime/container | Depende do decorator, que ainda não existe |
| `try/finally` no `stop()` | garantido pelo decorator | Não existe |
| Serviços no container | ModuleManager, etc. | Apenas `Config` |

> **INFERENCE:** o uso atual de `@CoffeeApplicationRuntime` (sem parênteses, sem `__call__`) provavelmente falha ou não produz o efeito desejado — a classe está sendo usada como decorator antes de implementá-lo. É o próximo passo natural de implementação.

---

## 8. Uso

### 8.1 Uso manual (disponível hoje)

```python
from coffee.core.runtime.CoffeeApplicationRuntime import CoffeeApplicationRuntime

runtime = CoffeeApplicationRuntime()
runtime.init()          # Config().build() + cria container

try:
    container = runtime.getContainer()   # nome atual (typo getContener corrigido)
    config = container.getConfig()
    # ... lógica da aplicação ...
finally:
    runtime.stop()      # libera o container
```

> **Nota (2026-10-01):** o caminho de import acima é o atual (`coffee.` root, pós-restructure); o exemplo anterior usava `core.runtime.CoffeAplicationRuntime` (path e typo obsoletos). `init()` fora do `try` continua sendo a assimetria conhecida (doc.md §4.3).

### 8.2 Uso como decorator (FUNCIONAL — verificado 2026-10-01)

O alvo de uso é o decorator:

```python
@CoffeeApplicationRuntime()
async def main(app: CoffeeApplicationRuntime):
    container = app.getContainer()
    config = container.getConfig()
    # ... lógica da aplicação ...

asyncio.run(main())
```

Comportamento esperado (PROPOSAL):

```python
runtime.init()
try:
    await main(runtime)
finally:
    runtime.stop()
```

> **STATUS 2026-10-03 (FACT — por execução):** o decorator **funciona** — `@CoffeeApplicationRuntime` (sem parênteses também é aceito) chama `_invokeAsync` → `init()` → `await func(self)` → `finally stop()`; **porém, desde `628e772`, o boot termina com exit 1** (`Start()` → `RuntimeError: CoffeeApplicationRuntime is not initialized`) porque a rota assíncrona **não chama `resetApp(token)`** (leak do ContextVar — ver §5.4/§16.2). Até `9ddf051` o boot era exit 0 (afirmação das docs anteriores).

### 8.3 Pontos de entrada previstos no código

O padrão já aparece em:

```text
src/coffee/main.py                          → @CoffeeApplicationRuntime em main()
src/coffee/core/runtime/CLI.py              → @Component em RuntimeCLI   (hoje; antes @CoffeeApplicationRuntime)
src/coffee/core/services/module/ModuleManager.py → @Component em ModuleManager (hoje; antes @CoffeeApplicationRuntime)
```

> **Atualizado em 2026-10-01 (FACT):** os paths mudaram (`core/cli/` → `core/runtime/`, `core/Services/` → `core/services/`) e os decoradores de `CLI`/`ModuleManager` hoje são **`@Component`**, não `@CoffeeApplicationRuntime` (ver `docs/doc.md` §4.6/§4.7 — doc.md prevalece).

> **Observação (FACT):** aplicar o runtime diretamente em `ModuleManager` contradiz §6.1 — serviços **não** devem controlar o lifecycle da aplicação. O decorator deve envolver **pontos de entrada**, não serviços. Isso pode ser um resquício exploratório e vale revisar.
>
> **Resolvido em [ADR 007](../decisions/007-modulemanager-dependency-injection.md)** (ACCEPTED): o ModuleManager receberá `Config` por **constructor injection**, criado no `init()` do Runtime (composition root). O decorator sai do serviço.

### 8.4 Quem deve usar o Runtime

```text
CLI            → sim (ponto de entrada)
Hermes         → sim (ponto de entrada)
Coffee API     → sim (ponto de entrada)
workers        → sim (ponto de entrada)
processos aux. → sim (ponto de entrada)

ModuleManager  → NÃO (é serviço; recebe o contexto, não o cria)
Storage        → NÃO
Config         → NÃO
```

---

## 9. Dependência e inversão de controle

O runtime é uma forma simples de **Inversion of Control (IoC)**.

**Sem runtime** — o ponto de entrada constrói a infraestrutura:

```text
main
 ├── cria Config
 ├── cria Container
 ├── cria serviços
 └── inicia aplicação
```

**Com runtime** — a infraestrutura entrega o contexto ao ponto de entrada:

```text
main
    ↑
recebe contexto
    ↑
Runtime
    ↑
Container
```

Benefício: CLI, Hermes, Coffee API, workers e processos auxiliares **compartilham o mesmo modelo de inicialização** sem reproduzir o bootstrap.

---

## 10. Instâncias compartilhadas

O container mantém instâncias que existem **dentro daquele ciclo de vida**. A regra não é transformar tudo em singleton global:

```text
1 Application Runtime
        ↓
1 Application Container
        ↓
instâncias compartilhadas pertencentes àquela aplicação
```

Ao encerrar:

```python
def stop(self) -> bool:
    self.container = None
    return True
```

O runtime **libera sua referência**. A coleta de memória fica a cargo do coletor do Python, desde que não haja outras referências.

O que se controla, portanto, não é "evitar toda alocação", mas:

```text
lifecycle
+
ownership
+
references
+
resources
```

---

## 11. Escopo e limites

O `CoffeeApplicationRuntime` deve permanecer **propositalmente pequeno**. Ele **não** deve se transformar em:

```text
Runtime
 ├── business logic
 ├── module implementation
 ├── configuration management
 ├── persistence
 ├── network layer
 ├── AI orchestration
 └── ...
```

Se crescer nessa direção, sinal de que a responsabilidade errada está no lugar errado — a complexidade deve ficar nos componentes que a possuem (Serviços, Config, etc.).

### Visão geral da arquitetura

```text
                         APPLICATION ENTRYPOINT
                                  │
                                  ▼
                      CoffeeApplicationRuntime
                                  │
                      ┌───────────┴───────────┐
                      │                       │
                   init()                   stop()
                      │                       │
                      ▼                       │
               Config().build()               │
                      │                       │
                      ▼                       │
            CoffeeApplicationContainer         │
                      │                       │
            ┌─────────┼─────────┐             │
            │         │         │             │
            ▼         ▼         ▼             │
         Config    Modules    Services        │
            │         │         │             │
            └─────────┴─────────┘             │
                      │                       │
                      ▼                       │
               Application running            │
                      │                       │
                      └───────────────────────┘
```

---

## 12. Manutenção e evolução

### Ao evoluir, observar

1. **Manter o runtime pequeno** — nova responsabilidade concreta = novo componente, não novo método no runtime.
2. **Implementar o decorator com `try/finally`** — `stop()` nunca pode ser pulado em caso de exceção.
3. **Corrigir o typo `getContener`** → `getContainer` antes que o nome vire contrato público.
4. **Não aplicar o decorator em serviços** (ver §8.3) — apenas em pontos de entrada.
5. **Adicionar serviços ao container** conforme o `init()` amadurecer (ModuleManager, etc.).
6. **`setConfig` em runtime** carrega risco (próprio aviso no código do container): substituir a config depois de iniciado pode causar inconsistência — tratar com cuidado.

### Próximos passos prováveis (PROPOSAL)

> **STATUS 2026-10-03:** itens 2 (`__call__`), 3 (com/sem parênteses) e 7 (`getContainer`) **já implementados** no código; item 1 (ADR 007) segue divergente do código (service-locator contextual — `doc.md` §17.11). **Novo item prioritário:** corrigir/decidir o gap `resetApp` da rota async/factory (§5.4, U-001).

```text
1. [ACEITO · ADR 007] Remover decorator do ModuleManager; injetar Config
   no construtor; criar instância dentro de Runtime.init();
   container ganha getter do moduleManager
2. Implementar __call__ no runtime (decorator com init/try/finally/stop)
3. Definir se o decorator é usável com e sem parênteses (@X e @X())
4. Mover pontos de entrada para o decorator (main/CLI); removê-lo de serviços
5. Expandir o container para carregar serviços
6. Definir política única de escrita do Config
   (diagnóstico do setConfig pass-through já confirmado; opção em aberto:
    config imutável pós-init × fachada única no Runtime)
7. Renomear getContener → getContainer
```

---

## 13. Application Context (ContextVar)

> **Status:** FACT (código verificado em `628e772`, 2026-10-03) · sem ADR específico (U-002 — formalização como mecanismo oficial é decisão aberta do DEV).

### 13.1 Problema

Sem contexto, todo componente precisaria receber `app`/`container` explicitamente:

```python
ModuleManager(container).loadModules()   # propagação manual de dependência
```

O `CoffeeApplicationContext` permite que componentes acessem **a aplicação atual do contexto de execução** sem recebê-la por parâmetro.

### 13.2 Conceito central

```python
_current_app: ContextVar["CoffeeApplicationRuntime | None"] = ContextVar(
    "coffee_current_app", default=None,
)
```

```text
ContextVar
    │
    └──────────────→ CoffeeApplicationRuntime   (referência, NÃO cópia)
```

Pontos que a documentação deve preservar:

- `ContextVar` **não** é uma variável global comum e **não** é o próprio Application.
- É um mecanismo **contextual**: mantém um valor associado ao contexto de execução atual.
- O valor armazenado é uma **referência para uma instância de `CoffeeApplicationRuntime`** — o Runtime continua sendo uma instância normal; não existe cópia dentro do ContextVar.
- **Não** significa "alocar o App na heap": o objeto Runtime é gerenciado pela memória do Python como qualquer objeto; o ContextVar só mantém a referência contextual.

```text
Heap / objetos Python
        │
        └── CoffeeApplicationRuntime
                ▲
                │ referência
                │
           ContextVar
```

### 13.3 Responsabilidade do CoffeeApplicationContext

A classe (`core/runtime/CoffeeApplicationContext.py`) existe **principalmente para encapsular o acesso ao ContextVar** — sem estado próprio, só `staticmethods`:

```python
class CoffeeApplicationContext:
    @staticmethod
    def setApp(app):   return _current_app.set(app)      # retorna token

    @staticmethod
    def getApp():
        app = _current_app.get()
        if app is None:
            raise RuntimeError("CoffeeApplicationRuntime is not running")
        return app

    @staticmethod
    def resetApp(token): _current_app.reset(token)
```

**Regra:** o restante do sistema **não** manipula `_current_app` diretamente — sempre via `setApp`/`getApp`/`resetApp` (verificado: `_current_app` só é acessado neste arquivo).

### 13.4 Singleton vs instância normal

O `CoffeeApplicationRuntime` **não** é um singleton clássico:

```text
app = CoffeeApplicationRuntime(...)     ← instância comum
Context
  ↓
current App                              ← qual instância está ativa NESTE contexto
  ↓
CoffeeApplicationRuntime instance
```

"Application globalmente acessível" **não** significa "Application implementada como singleton estático" — o mecanismo contextual define apenas **qual** instância está ativa no contexto atual.

> **Qualificação (FACT):** o ciclo (`_container`/`_registry` e `init`/`getContainer`/`stop`) é implementado em **atributos/métodos de classe** (contrato ABC `ApplicationRuntime`) → todas as instâncias compartilham o mesmo container. Isso é singleton-*like* no estado do ciclo, mas **não** é um singleton estático de acesso global direto (detalhe em `docs/doc.md` §4.3).

### 13.5 Relação com Registry/Container

```text
CoffeeComponent
      ↓
CoffeeApplicationContext.getApp()
      ↓
CoffeeApplicationRuntime
      ↓
getContainer()
      ↓
ApplicationContainer          ← abstração (Dependency Inversion)
      ↑
CoffeeApplicationContainer    ← implementação concreta
```

---

## 14. Token do ContextVar

`token = CoffeeApplicationContext.setApp(app)` retorna um **token de restauração contextual**.

O token **NÃO** é:

- token de autenticação;
- token de usuário;
- ID do Runtime;
- identificador persistente;
- referência global para a aplicação.

O token representa **a alteração feita no ContextVar** e permite restaurar o estado anterior:

```text
estado anterior
      ↓
setApp(App A)
      ↓
token
      ↓
App A está ativo
      ↓
resetApp(token)
      ↓
estado anterior restaurado
```

### Contexto aninhado

```text
estado original
      ↓
App A        (token_A)
      ↓
App B        (token_B)
      ↓
resetApp(token_B)
      ↓
App A
      ↓
resetApp(token_A)
      ↓
estado original
```

Funciona como um mecanismo de restauração contextual — conceitualmente análogo a uma **pilha de estados**, gerenciada pelo próprio `contextvars`.

---

## 15. ContextVar e concorrência

A diferença central:

```python
_current_app = app        # atributo comum: um valor global compartilhado
ContextVar                # contextual: cada contexto de execução tem o seu
```

```text
Contexto A                      Contexto B
    current_app → App A             current_app → App B
```

Relevante para `asyncio`, tasks, execução concorrente, workers e contextos temporários.

**Afirmação precisa (não exagerar):**

> `ContextVar` fornece **isolamento contextual do valor**, mas **não substitui** mecanismos de sincronização quando existe **estado compartilhado mutável**.

No Coffee, existe estado mutável compartilhado **fora** do ContextVar: `_container`/`_registry` (atributos de classe do Runtime), listas do `DefaultCoffeeRegistry` e do Container, `sys.path`. **0 travas de sincronização** no código (FACT) — o ContextVar isola só a referência do app.

---

## 16. Erros comuns

### 16.1 `RuntimeError: CoffeeApplicationRuntime is not running`

Lançado por `CoffeeApplicationContext.getApp()` quando **não há App registrado no contexto atual**.

**Não é, por si só, uma race condition.** Causas típicas:

```text
1. Componente executado antes do setApp()
2. Componente executado depois do resetApp()
3. Componente executado fora do lifecycle (ContextVar default = None)
4. Execução em outro contexto/task/thread (contextvars não são
   herdados por novas threads; Task criada antes do setApp copia
   contexto sem o app)
5. Lifecycle assíncrono configurado incorretamente
```

É **comportamento esperado do sistema** — sinaliza acesso fora da janela do ciclo de vida.

### 16.2 `RuntimeError: CoffeeApplicationRuntime is not initialized`

Lançado por `getContainer()` (Runtime:37) quando `_container is None`:

```text
1. init() nunca rodou
2. stop() já rodou (container liberado) mas o ContextVar ainda aponta
   para o app — caso assíncrono com leak do token (verificado no boot:
   Start() cai aqui → exit 1)
3. chamada pós-lifecycle no mesmo contexto
```

### 16.3 `LookupError: Component not registered: <Nome>`

Lançado por `CoffeeApplicationContainer.get()` — classe nunca decorada com `@Component` (registro ocorre **apenas em import time**).

### 16.4 Instanciação manual × resolução pelo Container

```python
ModuleManager()               # criação manual — NÃO passa pelo lifecycle do DI
container.get(ModuleManager)  # resolução — criação dentro do DI (nova instância a cada get, sem cache)
```

**Decisão explícita registrada:** um componente criado **manualmente** ainda pode acessar a infraestrutura (via `CoffeeComponent.container` → `CoffeeApplicationContext`) desde que exista um **Runtime ativo no contexto atual** — porque o acesso é contextual, não depende de injeção no construtor. Isso é intencional no modelo atual (service-locator contextual), porém difere do ADR 007 (constructor injection) — conflito C-002, aguardando decisão do DEV.

### 16.5 Dataclass + herança de `CoffeeComponent`

```python
@dataclass
class ModuleManager(CoffeeComponent):
    ...
```

O `@dataclass` gera seu **próprio `__init__`** — `CoffeeComponent.__init__()` **não** é executado automaticamente. Se o estado da base depender do `__init__`, pode ser necessário:

```python
def __post_init__(self):
    super().__init__()
```

É uma questão do mecanismo do `dataclass`, **não** do sistema de herança em si. Hoje `CoffeeComponent` **não tem `__init__`** e `ModuleManager` chama `super().__init__()` em `__post_init__` (funciona — FACT, verificado); a pegadinha fica **latente** se a base ganhar `__init__` (invariant 7b do explorer).

---

## 17. Invariantes arquiteturais

Invariantes confirmados pelo código (FACT/HIGH — task context do `codebase-explorer`, `628e772`; ver `.agents/protocol/tasks/temp/runtime-context-di-components-task-context.json`):

```text
 1. Runtime é instância normal, não singleton estático
    (qualificação: estado do ciclo é de classe → 1 container compartilhado)
 2. ContextVar contém referência contextual para o App atual (não cópia)
 3. Context não é singleton do Runtime
 4. Component acessa o App atual via CoffeeApplicationContext
 5. Component prefere ApplicationContainer (abstração) como tipo
 6. Registry registra CLASSES; Container resolve INSTÂNCIAS
 7. setApp() acontece antes do acesso dos componentes   (CONFIRMADO)
 8. resetApp(token) no final do lifecycle               (só rota sync;
                                                         async/factory = GAP — §5.4)
 9. ContextVar não substitui sincronização de estado compartilhado
10. @Component apenas registra e devolve a classe (não instancia)
```

Estes invariantes também estão registrados em `AGENTS.md` (para agentes) e no cache `.agents/protocol/docs/codebase-explorer.json`.

---

> **Resumo:** `CoffeeApplicationRuntime` é a fronteira de lifecycle do Coffee — inspirada no *around advice* do AOP, mas reduzida a um único papel: **inicializar, entregar contexto e encerrar**. O contexto é entregue via `CoffeeApplicationContext` (ContextVar → referência ao App atual); componentes acessam `ApplicationContainer` por Dependency Inversion; `Config` define, `Container` disponibiliza, `Runtime` controla, `Service` executa.