---
description: Spec do sistema de componentes AOP do Coffee — CoffeeComponent como abstração base de tudo que é gerenciável (Component, Service, Module, Repository, System Functions), CoffeeRegistry como registro/descoberta/resolução, CoffeeApplicationContainer como Dependency Injection e DIP como princípio. Definida pelo DEV em 2026-09-25. Carregar em qualquer trabalho sobre componentes, registry, DI ou AOP do Coffee.
---

# Coffee CLI — Components AOP

**Status:** DECISION (arquitetura definida pelo DEV em 2026-09-25) · implementação parcial

**Especifica:** infraestrutura de componentes, registro, AOP e Dependency Injection do Coffee

**Não especifica:** contrato formal de plugin, formato de configuração, modelo de Context Pack — UNDEFINED, decisão do DEV

**Fontes:** definição do DEV (2026-09-25) + ADR 006 + ADR 007 + `docs/architecture/runtime.md`

**Espelho em docs/:** `docs/architecture/components-aop.md`

---

## Arquitetura do Coffee

O Coffee possui uma infraestrutura baseada em **AOP (Aspect-Oriented Programming)** já integrada ao runtime. O AOP atua como uma camada transversal para interceptação, aplicação de comportamentos e extensão dos componentes sem acoplar essas responsabilidades diretamente à implementação das classes.

A arquitetura principal é dividida em dois conceitos:

### CoffeeComponents

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

### CoffeeRegistry

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

### Relação entre as camadas

A responsabilidade de cada parte pode ser resumida como:

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

## Estado no código (FACT)

| Item | Spec | Código hoje |
|---|---|---|
| `CoffeeComponent` | abstração base de todos os componentes | **existe** — `componets/base/CoffeeComponent.py` (ABC + `initialize()`) |
| `Component` / `Service` / `Module` / `Repository` / `System Functions` | tipos especializados | **parcial** — só existe o decorator `@Component` (`Componet.py`); os demais, não |
| `CoffeeRegistry` | registro / discovery / resolution | **em construção, com 2 definições homônimas**: `contener/CofeeRegistry.py` (funcional) e `componets/base/CoffeeRegistry.py` (`register()` é stub) |
| `CoffeeApplicationContainer` | resolve dependências e faz DI | **parcial** — guarda só `Config`; `_create()` lança `NotImplementedError` |
| AOP transversal | comportamentos sobre os componentes | **ainda não existe** — o único around implementado é o decorator de lifecycle (`CoffeeApplicationRuntime.__call__`) |
| `@Component` → registro | declaração → `CoffeeRegistry` | **quebra** — chama `packageRegister()`, que exige `.id`; classes sem `.id` falham com `AttributeError` (decisão pendente: `register()` × `packageRegister()`) |

> **DECISION (DEV, 2026-09-25):** a definição de AOP do Coffee **foi alargada** — cobre a infraestrutura declarativa de componentes (`CoffeeComponent` → `CoffeeRegistry` → `CoffeeApplicationContainer`) **e** o único around de execução (lifecycle). O alargamento **não** adota AOP de verdade: sem pointcuts, weaving, proxies ou interceptação arbitrária ("nada muito grande"). `docs/architecture/runtime.md` §3 foi reconciliado com esta definição.
