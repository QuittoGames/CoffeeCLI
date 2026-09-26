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
| `CoffeeComponent` | abstração base | **existe** — `src/coffee/core/runtime/componets/base/CoffeeComponent.py` (ABC + `initialize()`) |
| Tipos especializados (`Component`, `Service`, `Module`, `Repository`, `System Functions`) | unidades funcionais | **parcial** — apenas o decorator `@Component` (`componets/Componet.py`) existe |
| `CoffeeRegistry` | registro / discovery / resolution | **em construção, duas definições homônimas**: `contener/CofeeRegistry.py` (funcional) e `componets/base/CoffeeRegistry.py` (`register()` é stub) |
| `CoffeeApplicationContainer` | DI | **parcial** — guarda apenas `Config`; `_create()` lança `NotImplementedError` |
| AOP transversal | comportamentos sobre componentes | **não implementado** — único around existente é o decorator de lifecycle (`CoffeeApplicationRuntime.__call__`) |
| `@Component` → registro | declaração → registry | **quebra** — chama `packageRegister()`, que exige `.id`; classes sem `.id` falham (`AttributeError`) |

### Decisões abertas relacionadas

```text
register() × packageRegister() no decorator @Component  → aguardando DEV
CoffeeRegistry duplicado (base/ × contener/)             → aguardando DEV
formato do contrato de plugin                            → UNDEFINED
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
