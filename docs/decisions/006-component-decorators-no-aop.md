# ADR 006: Componentes via Decorators Declarativos (@Component) sem AOP

**Status:** ACCEPTED  
**Data:** 2026-09-23  
**Contexto:** `.agents/harness.md` §45, `docs/architecture/runtime.md`, `src/coffee/core/runtime/contener/`, `src/coffee/core/runtime/componets/`

## Contexto

O Coffee precisa declarar, registrar e resolver componentes (ex.: `ModuleManager`, `CLI`) sem adotar AOP tradicional. Python não possui suporte nativo a AOP no mesmo modelo de frameworks como Spring; weaving, interceptação global de métodos ou alteração dinâmica de comportamento adicionariam complexidade sem necessidade atual.

Pergunta: qual mecanismo liga declaração (`@Component`), registro (`CoffeeRegistry`), resolução (Container) e lifecycle (Runtime) sem misturar responsabilidades?

## Opções Consideradas

1. **AOP tradicional (weaving / interceptação global)** — cross-cutting potente, mas complexo, opaco e sem suporte nativo em Python
2. **Framework DI completo (ex.: python-dependency-injector)** — rejeitado em ADR 001 (`001-runtime-lifecycle-boundary.md`) (overkill para a necessidade atual)
3. **Decorators declarativos + Registry + Container (escolhido)** — simples, explícito, sem alteração dinâmica de comportamento

## Decisão

O Coffee **não** adota AOP tradicional para gerenciamento de componentes e injeção de dependências. A arquitetura utiliza **decorators como mecanismo declarativo** — sem weaving, sem interceptação global de métodos e sem alteração dinâmica do comportamento das classes.

### `@Component`

O decorator `@Component` é a API pública do SDK para declarar uma classe como componente gerenciado pelo Coffee:

```python
@Component
class ModuleManager:
    ...
```

Ao ser aplicado, registra a classe no `CoffeeRegistry` — catálogo global dos componentes declarados:

```text
@Component
    ↓
CoffeeRegistry
    ↓
componente registrado
```

### Runtime → Container → Registry

O `CoffeeApplicationRuntime` é responsável pelo bootstrap e pelo ciclo de vida da aplicação. Ele inicializa a configuração e cria o `CoffeeApplicationContainer`.

O `CoffeeApplicationContainer` é responsável pela composição da aplicação e pela resolução dos componentes registrados:

```text
CoffeeApplicationRuntime
        ↓
CoffeeApplicationContainer
        ↓
CoffeeRegistry
        ↓
Componentes registrados
```

### Responsabilidades

```text
@Component                  → declaração de componentes no SDK
CoffeeRegistry              → registro e descoberta dos componentes
CoffeeApplicationContainer  → resolução e instanciação das dependências
CoffeeApplicationRuntime    → inicialização e encerramento do runtime
```

### Regras

- Decorators **não** são AOP por si só: no Coffee funcionam como **metadado e ponto de registro**.
- A resolução de dependências permanece sob responsabilidade do **Container**.
- O mecanismo permanece simples, explícito e compatível com a filosofia do Coffee.

### Evolução futura

Interceptores ou aspectos específicos (logging, métricas, tracing, controle de execução) poderão ser adicionados somente caso exista necessidade real — de forma explícita e sem alterar o papel fundamental do `@Component`.

## Consequências

**Positivas:**
- Mecanismo simples e explícito; sem infraestrutura de weaving
- Separação clara: declaração ≠ registro ≠ resolução ≠ lifecycle
- Compatível com a decisão de DI do ADR 007 (constructor injection via composition root)
- Testável: registry e container podem ser inspecionados/limpos por teste

**Negativas/Riscos:**
- Registro via decorator depende da importação da classe (descoberta de módulos precisa acontecer antes da resolução)
- Sem interceptação automática — cross-cutting deverá ser explícito no futuro
- `CoffeeRegistry` global exige disciplina (estado por processo; testes precisam resetá-lo)

## Relacionado

- ADR 001 (`001-runtime-lifecycle-boundary.md`) — Runtime como fronteira de lifecycle
- ADR 007 (`007-modulemanager-dependency-injection.md`) — DI via composition root; "não criar nova classe AOP"
- `.agents/harness.md` §45 — registro da decisão no harness de governança
