# CoffeeApplicationRuntime — Conceituação e Uso

**Status:** PROPOSAL (conceituação validada pelo DEV; implementação atual é parcial — ver §7)  
**Código-fonte:**
- `src/coffee/core/runtime/CoffeAplicationRuntime.py`
- `src/coffee/core/runtime/contener/CoffeeApplicationContainer.py`

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
src/coffee/core/
├── runtime/
│   ├── CoffeAplicationRuntime.py        # Ciclo de vida + decorator
│   └── contener/
│       └── CoffeeApplicationContainer.py # Contexto compartilhado
├── data/
│   ├── Config.py                        # Configurações (dado)
│   └── Host.py                          # Dados de host
├── Services/
│   └── module/
│       └── ModuleManager.py             # Serviço de módulos
├── cli/
│   └── CLI.py                           # Ponto de entrada CLI
└── domain/
    └── models/                          # Modelos de domínio
```

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

Depois do `init()`, o ponto de entrada recebe o contexto — sem conhecer os detalhes de construção:

```python
@CoffeeApplicationRuntime()
async def main(app):
    container = app.getContainer()
    config = container.getConfig()
```

```text
Runtime
   │
   │ injeta
   ▼
App / Entry Point
   │
   ▼
Container
   │
   ├── Config
   ├── módulos
   └── serviços
```

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

- `__init__` **só** cria o objeto runtime (container = `None`).
- A subida real da aplicação acontece em `init()` (futuramente talvez `start()`).
- O encerramento acontece em `stop()`.

Com decorator, o lifecycle é automático:

```python
# O que se escreve:
@CoffeeApplicationRuntime()
async def main(app):
    ...

# O que acontece conceitualmente:
runtime.init()
try:
    await main(runtime)
finally:
    runtime.stop()
```

O `try/finally` é parte do contrato: **`stop()` deve rodar mesmo se a aplicação lançar exceção**.

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
from core.runtime.CoffeAplicationRuntime import CoffeeApplicationRuntime

runtime = CoffeeApplicationRuntime()
runtime.init()          # Config().build() + cria container

try:
    container = runtime.getContener()
    config = container.getConfig()
    # ... lógica da aplicação ...
finally:
    runtime.stop()      # libera o container
```

### 8.2 Uso como decorator (CONCEITO — ainda não funcional)

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

### 8.3 Pontos de entrada previstos no código

O padrão já aparece em:

```text
src/coffee/main.py          → @CoffeeApplicationRuntime em main()
src/coffee/core/cli/CLI.py  → @CoffeeApplicationRuntime em RuntimeCLI
src/coffee/core/Services/module/ModuleManager.py → @CoffeeApplicationRuntime em ModuleManager
```

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

> **Resumo:** `CoffeeApplicationRuntime` é a fronteira de lifecycle do Coffee — inspirada no *around advice* do AOP, mas reduzida a um único papel: **inicializar, entregar contexto e encerrar**. `Config` define, `Container` disponibiliza, `Runtime` controla, `Service` executa.