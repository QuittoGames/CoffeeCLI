# Coffee Components AOP — Componentes, Registro e Dependency Injection

**Status:** DECISION (definida pelo DEV em 2026-09-25) — implementação parcial

**Relacionado:**
- `docs/decisions/006-component-decorators-no-aop.md` — `@Component` como decorator declarativo, sem weaving
- `docs/decisions/007-modulemanager-dependency-injection.md` — DI via composition root
- `docs/architecture/runtime.md` — fronteira de lifecycle do `CoffeeApplicationRuntime`

**Espelho em .agents/:** `.agents/specs/coffee-components-aop.md`

---

## 1. Visão geral

O Coffee possui uma infraestrutura baseada em **AOP (Aspect-Oriented Programming)** já integrada ao runtime. O AOP atua como uma camada transversal para interceptação, aplicação de comportamentos e extensão dos componentes sem acoplar essas responsabilidades diretamente à implementação das classes.

A arquitetura principal é dividida em dois conceitos.

---

## 2. CoffeeComponents

`CoffeeComponent` representa a abstração base de todos os elementos gerenciáveis pelo Coffee.

A partir dela existem diferentes tipos especializados de componentes, como:

```text
CoffeeComponent
├── Component
├── Service
├── Module
├── Repository
└── System Functions
```

Esses componentes representam as **unidades funcionais do sistema**. Eles possuem suas próprias responsabilidades e podem ser registrados, interceptados e gerenciados pelo runtime.

O objetivo de `CoffeeComponent` é fornecer uma abstração comum para que o Coffee consiga tratar diferentes tipos de objetos de maneira uniforme, sem que o runtime precise conhecer suas implementações concretas.

---

## 3. CoffeeRegistry

`CoffeeRegistry` é responsável pelo **registro, descoberta e resolução dos componentes**.

Ele funciona em conjunto com o `CoffeeApplicationContainer`, implementando a infraestrutura de **Dependency Injection (DI)** e aplicando os princípios de **Dependency Inversion (DIP)**.

A separação é:

```text
CoffeeComponent
        │
        ├── Components
        ├── Services
        ├── Modules
        └── System Functions
        │
        ▼
CoffeeRegistry
        │
        ├── Registration
        ├── Discovery
        └── Resolution
        │
        ▼
CoffeeApplicationContainer
        │
        └── Dependency Injection
```

Dessa forma, os componentes não precisam conhecer diretamente suas implementações concretas ou controlar manualmente a criação de suas dependências.

O Container recebe a abstração necessária, consulta o `CoffeeRegistry`, resolve as dependências e cria a implementação apropriada.

---

## 4. Relação entre as camadas

```text
CoffeeComponent
→ define o que pode ser gerenciado pelo Coffee.

AOP
→ adiciona comportamentos transversais ao runtime.

CoffeeRegistry
→ registra e localiza componentes e implementações.

CoffeeApplicationContainer
→ resolve dependências e realiza Dependency Injection.

DIP
→ mantém o código dependente de abstrações em vez de implementações concretas.
```

Assim, o Coffee deixa de ser apenas uma coleção de módulos e passa a possuir uma **infraestrutura própria de componentes, registro, AOP e Dependency Injection**, formando a base do runtime e do SDK do sistema.

---

## 5. Estado no código (FACT)

| Item | Conceito | Código hoje |
|---|---|---|
| `CoffeeComponent` | abstração base | **existe** — `src/coffee/core/components/CoffeeComponent.py` (ABC **sem** `__init__`/`initialize()`; `property container` = `CoffeeApplicationContext.getApp().getContainer()` + `get(component)`) |
| Tipos especializados (`Component`, `Service`, `Module`, `Repository`, `System Functions`) | unidades funcionais | **parcial** — apenas os decorators `@Component` (`components/decorators/Component.py`) e `@Module` (`components/decorators/Module.py`) existem; os demais, não |
| `CoffeeRegistry` | registro / discovery / resolution | **herança (não duplicação)** — ABC `CoffeeRegistry` (`container/CoffeeRegistry.py`) + `DefaultCoffeeRegistry(CoffeeRegistry)` (`container/DefaultCoffeeRegistry.py`, funcional: listas `dependencies`/`systemModules`); singleton em `container/registry.py` |
| `CoffeeApplicationContainer` | DI | **parcial** — guarda `Config` + `dependencies: list[Dependency]` + `systemModules`; `_create()` reflete assinaturas mas **nunca é chamado** e `get()` não injeta (ver `docs/doc.md` §4.4) |
| AOP transversal | comportamentos sobre componentes | **não implementado** — único around existente é o decorator de lifecycle (`CoffeeApplicationRuntime.__call__`) |
| `@Component` → registro | declaração → registry | **funciona (2026-10-01)** — chama `register()` (desde `c60908d`), sem exigência de `.id`; até 2026-09-30 chamava `packageRegister()` e quebrava com `AttributeError` |

> **Atualizado em 2026-10-01** contra o código pós-`c60908d`/`3d47da8` (paths e status); até 2026-09-30 esta tabela citava `componets/`, `contener/` e o defeito de `.id`. **Atualizado em 2026-10-03:** `CoffeeComponent` sem `initialize()` (removido em `628e772`).

### 5.1 Registry × Container (separação essencial)

```text
Registry
    ↓
sabe QUAIS componentes foram registrados (CLASSES, em import time)

Container
    ↓
sabe COMO obter/criar/resolver as INSTÂNCIAS
```

- `CoffeeRegistry`/`DefaultCoffeeRegistry` mantém **classes** registradas (via `register`/`packageRegister`).
- `CoffeeApplicationContainer` realiza a **resolução**: `container.get(T)` → `registry.get(T)` → `T()` — **nova instância sem args a cada chamada** (sem cache) — verificado por execução.
- Eles **não são a mesma coisa**.

### 5.2 Decorator `@Component` = registro, não instanciação

```python
class ComponentDecorator:
    def __call__(self, component):
        registry.register(component)
        return component

Component = ComponentDecorator()
```

1. recebe a classe;
2. registra-a no Registry;
3. devolve **a própria classe**.

```python
@Component
class ModuleManager(...): ...
```

**não** transforma `ModuleManager` em instância nem substitui a classe pelo decorator — é apenas mecanismo de registro (FACT, `decorators/Component.py:10-12`).

### 5.3 Acesso de componente ao contexto (Dependency Inversion)

`CoffeeComponent` **não** recebe o `CoffeeApplicationRuntime` por parâmetro:

```python
@property
def container(self) -> ApplicationContainer:
    return CoffeeApplicationContext.getApp().getContainer()
```

```text
CoffeeComponent
       ↓
ApplicationContainer        ← contrato/abstração (dependência do componente)
       ↑
CoffeeApplicationContainer  ← implementação concreta
```

Isso é **Dependency Inversion**: o componente depende do contrato `ApplicationContainer`, não da implementação. Detalhes do ContextVar em `runtime.md` §13.

### 5.4 Instanciação manual × resolução pelo Container

```python
ModuleManager()               # criação manual — fora do lifecycle do DI
container.get(ModuleManager)  # resolução — dentro do DI (nova instância por chamada)
```

**Decisão explícita:** mesmo criado manualmente, um `CoffeeComponent` acessa a infraestrutura via `CoffeeApplicationContext` **desde que exista um Runtime ativo no contexto atual** (service-locator contextual). Diverge do ADR 007 (constructor injection) — conflito registrado em `doc.md` §17.11.

### 5.5 Pegadinha: `@dataclass` + herança de `CoffeeComponent`

O `@dataclass` gera seu **próprio `__init__`** — o `__init__` da base **não** roda automaticamente. Se o estado da base depender dele:

```python
def __post_init__(self):
    super().__init__()
```

Questão do mecanismo do `dataclass`, não da herança. Hoje `CoffeeComponent` não tem `__init__` (funciona — FACT); latente se a base ganhar um.

### Decisões abertas relacionadas

```text
DECISION (2026-09-29) manter packageRegister × código usa register  → CONFLICT aguardando DEV (doc.md §17.9, TODO:53)
formato do contrato de plugin                                       → UNDEFINED
```

---

## 6. Resolução da tensão com `runtime.md` (DECISION)

**DECISION (DEV, 2026-09-25):** a definição de AOP do Coffee **foi alargada** e
deve ser lida como está nesta documentação.

O alargamento cobre:

1. **Infraestrutura declarativa de componentes** — `CoffeeComponent` →
   `CoffeeRegistry` → `CoffeeApplicationContainer` (registro, resolução, DI);
2. **O único around de execução** — lifecycle da aplicação
   (`CoffeeApplicationRuntime.__call__`).

O alargamento **não** significa adotar AOP de verdade (nada muito grande):
permanecem ausentes pointcuts, weaving, proxies e interceptação arbitrária de
métodos.

**Ação concluída:** `docs/architecture/runtime.md` §3 foi reconciliado com esta
definição (INFERENCE resolvida).
