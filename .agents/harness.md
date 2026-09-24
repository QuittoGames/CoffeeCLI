---
description: Harness de governança do Coffee CLI — regras de toda tarefa de desenvolvimento, refatoração, revisão ou decisão técnica neste projeto. Define ownership (DEV define, IA assiste), escopo, decision gate, capabilities, boundaries do ecossistema e não-fabricação. Fonte arquitetural em .agents/context/coffee-ecosystem-conversation-documentation.md. UX e arquitetura são DEV-owned; ausência de definição é UNDEFINED, nunca inferência.
---

# Coffee CLI Harness

## 1. Purpose

Este harness existe para controlar o trabalho de desenvolvimento dentro do projeto Coffee CLI.

Seu objetivo é:

```text
entender o projeto
      ↓
preservar suas decisões
      ↓
selecionar a menor capability necessária
      ↓
executar dentro do escopo
      ↓
validar
      ↓
reportar
```

O harness não é responsável por inventar o produto.

O harness serve para **trabalhar dentro do produto que o desenvolvedor definiu**.

---

# 2. Project Identity

O Coffee CLI pertence ao **Coffee Ecosystem**.

A referência principal do ecossistema está em:

```text
.agents/context/coffee-ecosystem-conversation-documentation.md
```

Esse documento deve ser tratado como contexto arquitetural do projeto.

O Coffee CLI deve seguir a conceituação geral do Coffee:

```text
Coffee Ecosystem
        │
        ├── Coffee Server
        ├── Coffee CLI
        ├── Context
        ├── Capabilities
        ├── Modules / Plugins
        ├── Integrations
        └── AI Runtime
```

O CLI é uma interface e um orquestrador local.

Ele não deve se tornar:

```text
um segundo servidor
um sistema operacional
um clone do ClickUp
um clone do OpenCode
um framework genérico
```

---

# 3. Source of Truth

Quando houver conflito entre informações, aplicar esta ordem:

```text
1. Instrução explícita do DEV
2. Especificação atual do projeto
3. Documentação arquitetural existente
4. Contratos/interfaces existentes
5. Implementação existente
6. Inferência
```

Inferência nunca deve ser apresentada como decisão já tomada.

Quando algo não estiver definido:

```text
UNDEFINED DECISION
```

A IA deve registrar a lacuna ou perguntar ao DEV, conforme o contexto.

Ela não deve preencher uma decisão de produto ou UX simplesmente porque "parece fazer sentido".

---

# 4. Architecture Ownership

O desenvolvedor possui:

```text
produto
arquitetura
contratos
UX
comportamento
prioridades
decisões técnicas
```

A IA pode:

```text
analisar
explicar
pesquisar
comparar
propor
testar
implementar dentro do escopo autorizado
```

A IA não deve:

```text
inventar requisitos
inventar UX
alterar arquitetura silenciosamente
expandir escopo
substituir uma decisão do DEV por uma preferência própria
```

---

# 5. Architectural Decision Gate

Mudanças que afetem:

```text
arquitetura
interfaces
contratos
persistência
plugins
capabilities
APIs
eventos
segurança
permissões
infraestrutura
concorrência
distribuição
organização de módulos
responsabilidade de componentes
```

devem ser tratadas como decisão arquitetural.

Formato:

```text
ARCHITECTURAL CHANGE DETECTED

Current:
<estado atual>

Proposed:
<mudança>

Benefits:
<benefícios>

Trade-offs:
<trade-offs>

Risks:
<riscos>

User decision required.
```

A implementação só segue automaticamente quando a decisão já estiver delegada.

---

# 6. Least Capability

O harness deve utilizar:

> **the least expensive capability that can reliably complete the work**

Preferir:

```text
capability atual
    ↓
comando simples
    ↓
agente especializado
    ↓
workflow complexo
```

Escalar somente quando necessário.

Evitar:

```text
agent explosion
premium-by-default
multi-agent sem necessidade
processo excessivo
delegação automática de trabalho simples
```

A política geral existente do ecossistema segue essa mesma lógica de delegação sob demanda e escalada somente quando necessária.

---

# 7. Scope

Toda tarefa executável deve possuir:

```text
Objective
Scope
Allowed Files
Forbidden Files
Dependencies
Expected Output
Validation
```

A IA não deve expandir o escopo automaticamente.

Quando encontrar um problema fora dele:

```text
OUT-OF-SCOPE FINDING

Location:
<arquivo>

Problem:
<problema>

Why it matters:
<impacto>

Suggested follow-up:
<proposta>
```

---

# 8. Conflict Detection

Antes de modificar arquivos, verificar:

```text
mudanças recentes
arquivos alterados
escopo humano ativo
dependências
possíveis conflitos semânticos
```

Conflito real:

```text
TASK CONFLICT DETECTED

Human scope:
<escopo>

Agent scope:
<escopo>

Conflict:
<conflito>

Recommended resolution:
<resolução>
```

Não resolver o conflito silenciosamente.

As regras existentes de conflito e atomicidade devem continuar sendo respeitadas.

---

# 9. Project Context

Antes de trabalho relevante, o harness deve entender:

```text
estrutura
linguagem
build system
entrypoints
dependências
testes
documentação
arquitetura
estado atual
```

No Coffee CLI, atenção especial para:

```text
pyproject.toml
src/coffee/
.agents/
README.md
interfaces
models
modules
runtime
cli
```

O harness não deve reconstruir a arquitetura somente observando uma pasta isolada.

---

# 10. Coffee CLI Architecture

A arquitetura atual segue uma organização modular.

Conceitualmente:

```text
coffee/
│
├── core/
│   ├── cli/
│   ├── runtime/
│   ├── data/
│   ├── domain/
│   └── module/
│
└── modules/
```

A tendência é manter features relativamente independentes.

O harness deve evitar criar:

```text
GlobalService
GlobalManager
God Object
```

quando uma capability ou módulo localizado for suficiente.

---

# 11. Runtime

O Runtime representa o ciclo de vida da aplicação.

Separação conceitual:

```text
CLI
→ entrada

Runtime
→ ciclo de execução

Context
→ recursos/contexto disponíveis

Container
→ composição das dependências
```

Não misturar esses conceitos simplesmente para reduzir arquivos.

---

# 12. Plugins / Modules

O Coffee utiliza uma direção orientada a plugins/features.

Um módulo pode possuir:

```text
models
services
adapters
interfaces
commands
configuration
metadata
```

O harness deve preservar a independência do módulo.

Discovery, registry e loading devem ser tratados separadamente quando necessário:

```text
Interpreter
→ descobre

Registry
→ registra

Loader
→ carrega

Runtime
→ inicia
```

O modelo final de plugins continua sendo uma decisão do projeto e não deve ser inventado pelo harness.

---

# 13. UX Authority

### Regra principal

A UX pertence ao DEV.

O harness **não pode criar telas, fluxos, componentes ou comportamentos de UX apenas por inferência estética**.

Quando a UX estiver definida pelo DEV, ela deve ser preservada.

Quando não estiver definida:

```text
não inventar
não cristalizar
não transformar preferência em requisito
```

Linguagem visual consolidada do projeto:

```text
.agents/specs/ux-ui-language.md
```

UX detalhada (telas, fluxos, componentes, copy) permanece UNDEFINED e é especificada somente pelo DEV.

---

# 14. Coffee UI Language

A identidade visual definida para o Coffee segue uma direção:

```text
modern
technical
dark-first
blue identity
transparent
fast
clean
controlled
```

### Cores

A linguagem visual utiliza principalmente:

```text
Black
Blue
Transparent / terminal-native background
```

O terminal **não deve ter seu background substituído** pela aplicação.

A interface deve trabalhar sobre o terminal existente.

Azul funciona como:

```text
accent
focus
active state
important information
primary interaction
```

Preto funciona como elemento de contraste/semântica quando o ambiente permitir.

A cor não deve ser utilizada para transformar toda a interface em azul.

---

# 15. Visual Density

A UI deve ser:

```text
compacta
legível
hierárquica
rápida de escanear
```

Evitar:

```text
elementos gigantes
espaçamento excessivo
ornamentação
gradientes excessivos
cores sem significado
informação duplicada
```

O Coffee deve parecer uma ferramenta de desenvolvimento moderna, não uma aplicação decorativa.

---

# 16. Transparency

Transparência é um princípio visual.

No contexto de terminal:

```text
Terminal background
        +
Coffee foreground/UI
```

Em vez de substituir o ambiente inteiro.

A interface deve parecer integrada ao terminal.

---

# 17. Radius

O token visual conceitual principal é:

```text
radius = 8px
```

Esse valor é a referência geral do design system do Coffee.

Em TUI, quando o framework não oferece radius real:

```text
usar a representação terminal mais próxima
```

Não criar efeitos artificiais apenas para simular 8px.

O token representa a linguagem visual, não uma obrigação técnica impossível do terminal.

---

# 18. Motion / Speed

A interface prioriza:

```text
velocidade
feedback imediato
transições discretas
automação
```

Nunca adicionar animação apenas para ornamentação.

O comportamento deve transmitir:

```text
fast
responsive
alive
```

sem atrasar operações.

---

# 19. TUI Principles

Como o Coffee CLI utiliza TUIs:

```text
terminal-native first
```

A UI deve respeitar:

```text
terminal background
terminal dimensions
keyboard interaction
readability
low visual noise
```

O design não deve depender de recursos que destruam a legibilidade em diferentes terminais.

---

# 20. Command Registry

O harness possui comandos especializados.

## `/agents`

Executa uma única tarefa de desenvolvimento de forma atômica e controlada.

```text
scope absoluto
alteração mínima
sem refatoração não solicitada
controle do DEV
```

---

## `/atomic_task`

Executa trabalho de engenharia controlado e atômico.

Uso adequado para:

```text
feature pequena
correção localizada
alteração isolada
mudança com escopo claro
```

---

## `/audit`

Audita:

```text
tests
quality
CI/CD
security
coverage
```

Deve detectar automaticamente o stack relevante quando possível.

Se existir:

```text
unit_tests.md
```

na raiz, suas convenções devem ser respeitadas.

---

## `/benchmark`

Investiga performance em:

```text
algoritmos
memória
alocações
I/O
rede
banco
concorrência
renderização
```

O resultado deve ser baseado em medições ou evidências, não em otimizações especulativas.

---

## `/bootstrap`

Descobre, formaliza e inicializa projetos.

Fluxo:

```text
Context
 ↓
Requirements
 ↓
Architecture
 ↓
SPEC.md
 ↓
Bootstrap
```

Quanto mais contexto existir, menos perguntas básicas devem ser repetidas.

A especificação deve preceder a geração estrutural.

---

## `/commit`

Analisa o estado atual do Git e produz:

```text
Conventional Commit
title
body
breaking changes
```

Caso o diff contenha mudanças não relacionadas, pode sugerir split.

Não deve alterar o histórico sem autorização.

---

## `/debug`

Investiga causa raiz antes da correção.

Prioridade:

```text
logs
stack traces
dependencies
environment
code flow
state
race conditions
reproduction
```

Não deve pular diretamente para um patch.

---

## `/dependencies`

Analisa dependências:

```text
version
vulnerability
maintenance
compatibility
alternatives
licenses
```

Resultado priorizado.

---

## `/devcontainer`

Gerencia o contexto de desenvolvimento em containers quando isso fizer parte do projeto.

Não deve tornar containerização obrigatória sem requisito.

---

## `/diff`

Abre/analisa a visão de diff.

O objetivo é facilitar revisão de alterações, não interpretar o diff como autorização para refatorar.

---

## `/docs`

Cria ou melhora:

```text
README
architecture
API
modules
classes
functions
examples
```

Documentação deve refletir o sistema real.

Não inventar APIs ou comportamentos que não existem.

---

## `/editor`

Abre o editor definido pelo ambiente/projeto.

Não deve modificar arquivos automaticamente apenas por abrir o editor.

---

## `/exit`

Encerra o harness.

Sem efeitos adicionais.

---

## `/help`

Exibe ajuda do harness e seus comandos.

A ajuda deve ser:

```text
rápida
escaneável
hierárquica
```

---

## `/init`

Configura inicialmente o contexto de agentes do projeto.

Deve respeitar:

```text
projeto existente
arquitetura existente
AGENTS.md existente
decisões do DEV
```

Não substituir contexto sem motivo.

---

# 21. Command Design

Todos os comandos devem seguir uma linguagem consistente.

Formato conceitual:

```text
/command
descrição curta
```

A descrição deve responder:

```text
o que faz
quando usar
limite principal
```

Evitar descrições vagas como:

```text
"faz análise"
"ajuda com código"
"gerencia projeto"
```

Preferir:

```text
"Investiga a causa raiz de um bug antes de propor correção."
```

O estilo atual dos comandos segue essa direção e deve ser preservado.

---

# 22. Agent Routing

O harness deve encaminhar uma tarefa para uma capability somente quando houver ganho real.

Ordem preferencial:

```text
current context
↓
current model capability
↓
specialized agent
↓
multi-agent workflow
```

Especialista antes de generalista quando a especialização realmente reduzir erro ou esforço.

Não criar um agente novo para cada pequena diferença de tarefa.

---

# 23. Workflow

Workflow descreve:

```text
HOW TO WORK
```

Mode descreve:

```text
HOW AI ACTS
```

Autonomy descreve:

```text
HOW FAR AI MAY ACT
```

Ownership descreve:

```text
WHO OWNS THE WORK
```

Esses conceitos não devem ser misturados.

---

# 24. Default Modes

### LEARN

```text
learning > speed
```

### BUILD

Implementação autorizada dentro do escopo.

### REVIEW

Análise sem modificação automática.

### WORKER

Execução mecânica e isolada.

### PAIR

Colaboração entre DEV e IA.

PAIR não concede autorização global.

---

# 25. Validation

Nenhuma tarefa relevante termina apenas porque o código foi escrito.

Sempre que aplicável:

```text
implement
 ↓
run
 ↓
test
 ↓
inspect
 ↓
validate
 ↓
report
```

A IA deve informar:

```text
what changed
what was tested
what passed
what failed
what remains
```

---

# 26. No Fabrication

É proibido fabricar:

```text
requirements
UX
API
commands
architecture
plugins
data model
user preferences
```

A ausência de informação deve permanecer uma ausência de informação.

O harness deve preferir:

```text
UNDEFINED
```

a inventar uma especificação.

---

# 27. Coffee Ecosystem Boundary

O Coffee deve permanecer:

```text
personal
modular
integrated
optional
extensible
```

Mas:

```text
Coffee ≠ Operating System
Coffee ≠ all-in-one replacement
Coffee ≠ OpenCode clone
Coffee ≠ ClickUp clone
Coffee ≠ unrestricted AI shell
```

A especificação do ecossistema define esses limites explicitamente.

---

# 28. Core Design Principle

O harness deve seguir:

```text
DEV defines
     ↓
Harness understands
     ↓
AI assists
     ↓
System validates
     ↓
DEV remains owner
```

E não:

```text
AI decides
     ↓
AI invents
     ↓
AI restructures
     ↓
DEV discovers afterward
```

---

# 29. UI Identity Summary

A interface do Coffee deve transmitir:

```text
BLUE
→ identidade / foco / ação

BLACK
→ contraste / estrutura

TRANSPARENT
→ integração com o terminal

8px
→ linguagem de forma

FAST
→ baixa fricção

MODERN
→ hierarquia limpa

TECHNICAL
→ informação acima de decoração
```

A aplicação não deve alterar o background do terminal.

---

# 30. Capabilities

Capabilities são a fronteira semântica do Coffee.

Uma capability representa:

```text
o que o Coffee consegue fazer
```

E não:

```text
qual biblioteca faz isso
```

Exemplos definidos pelo ecossistema:

```text
task.read
task.create
task.complete
project.read
project.create
context.resolve
machine.inspect
event.publish
```

A mesma capability pode ser consumida por:

```text
CLI
REST
MCP
WebSocket
AI
```

MCP é um adaptador — não é a arquitetura central.

O contrato formal de capability ainda é:

```text
UNDEFINED DECISION
```

---

# 31. Server Boundary

O CLI pode operar:

```text
LOCAL
SERVER
LOCAL + SERVER
AI
```

A fronteira não é local versus remoto.

A fronteira é:

```text
Onde aquela responsabilidade realmente pertence?
```

Exemplos definidos pelo ecossistema:

```text
coffee task add        → Server → Task Service
coffee git status      → CLI → Git local
coffee system inspect  → CLI / Local Agent → OS
```

O CLI é cliente do Server.

O CLI não é um segundo servidor.

Estado compartilhado pertence ao Server:

```text
Tasks
Projects
Context
Events
Persistência
```

---

# 32. Context Engine

Contexto é uma capability do ecossistema — não um truque do prompt.

Separação obrigatória:

```text
Knowledge  → documentos, Obsidian, arquivos, referências
State      → Coffee Server
Context    → seleção do que é relevante para uma operação
AI memory  → nunca fonte oficial de verdade
```

Fluxo definido:

```text
Request
   ↓
Context Resolver
   ↓
Relevant Sources
   ↓
Context Pack
   ↓
AI / CLI / Client
```

O objetivo é responder:

```text
Qual é o mínimo de contexto necessário
para esta operação ser corretamente entendida?
```

O formato do Context Pack é:

```text
UNDEFINED DECISION
```

---

# 33. AI / Hermes Boundary

Hermes é o AI runtime do ecossistema — a camada que raciocina sobre o Coffee.

O CLI expõe capabilities de IA como interface para essa camada.

Fronteiras:

```text
Coffee  → ferramentas / ecossistema
Hermes  → inteligência / orquestração cognitiva
```

A IA interpreta o estado.

A IA não é o armazenamento primário:

```text
Server     → possui e persiste os dados
Context    → seleciona o relevante
Hermes     → raciocina sobre eles
CLI / UI   → apresenta e interage
```

A IA é poderosa por encontrar **interfaces semânticas e controladas** — não por executar shell arbitrário.

Modelo mental de uma tarefa de IA:

```text
Pedido
 ↓
Entender
 ↓
Resolver contexto
 ↓
Descobrir capabilities
 ↓
Planejar
 ↓
Executar
 ↓
Observar resultado
 ↓
Validar
 ↓
Responder
```

Estratégia de memória do Hermes e provider routing:

```text
UNDEFINED DECISION
```

---

# 34. Events / Realtime

O ecossistema deve poder reagir a eventos.

Exemplos definidos:

```text
task.created
task.completed
project.changed
machine.connected
plugin.loaded
plugin.failed
context.updated
agent.started
agent.finished
```

Eventos podem alimentar:

```text
CLI
UI
MCP
AI
Automations
Logs
```

Regra central:

```text
evento não significa autonomia irrestrita
```

O mesmo sistema de permissões, ownership e autonomia continua valendo.

Event bus e o modelo final de realtime:

```text
UNDEFINED DECISION
```

---

# 35. Config / Container / Boot

Configuração não é Singleton global.

Fluxo definido:

```text
Config file / env / CLI
        ↓
    ConfigLoader
        ↓
       Config
        ↓
  CoffeeContainer
        ↓
  CoffeeRuntime
```

Existe uma instância de Config por processo — sem `Config.instance()` espalhado.

Papéis:

```text
Config     → define
Container  → disponibiliza
Runtime    → controla
Service    → executa
```

Boot conceitual:

```text
Bootstrap
  ↓
Load environment
  ↓
Load configuration
  ↓
Create Container
  ↓
Create Context
  ↓
Register core services
  ↓
Discover plugins
  ↓
Build Registry
  ↓
Load active plugins
  ↓
Initialize capabilities
  ↓
Initialize Server connections
  ↓
READY
```

Config persistente no host:

```text
~/.config/Coffee/
```

O formato do sistema de configuração:

```text
UNDEFINED DECISION
```

A fronteira de lifecycle consolidada está em:

```text
docs/architecture/runtime.md
```

---

# 36. Privileged Operations

O Coffee trabalha em níveis de privilégio:

```text
L0 — User
    Tasks / Projects / Git / AI / Context

L1 — System
    Services / Networking / Diagnostics / Packages

L2 — Privileged
    Boot / Mounts / Firewall / sensitive system operations
```

Regras:

```text
operações privilegiadas são separadas e controladas
o processo principal não vira "sudo tudo"
```

O modelo completo de permissões:

```text
UNDEFINED DECISION
```

---

# 37. Security Model

O caminho definido para operações de IA:

```text
AI
 ↓
Capability
 ↓
Permission
 ↓
Adapter
 ↓
Operation
```

E não:

```text
AI → shell
```

Exemplo:

```text
machine.inspect → diagnóstico permitido
system.mount    → exige nível diferente de autorização
```

Adapters são a fronteira:

```text
subprocess
powershell
bash
systemctl
sysfs
```

só existem dentro de adapters bem definidos — nunca espalhados pelo código.

Riscos conhecidos no código atual (FACT — registrar, não corrigir silenciosamente):

```text
tool.py
→ pip install automático no boot (superfície de supply chain)
→ sys.path.append dinâmico (superfície de import)

data/Config.py + data/Host.py
→ acesso direto a os / platform fora de adapter
```

Correções pertencem a tasks no TODO — não a decisões tomadas durante outra tarefa.

---

# 38. Portability

O Coffee roda em mais de um sistema.

```text
        Coffee Domain
              │
   ┌──────────┴──────────┐
   ▼                     ▼
Linux Adapter       Windows Adapter
   │                     │
 Fedora               Windows
```

Vale para:

```text
filesystem
shell
processes
network
packages
services
```

Regra:

```text
a plataforma fica nos adapters
o domínio permanece independente
```

---

# 39. Tasks / Projects

O Coffee possui um Task Manager próprio.

Decisões já tomadas:

```text
Task Manager fica centralizado no Server
CLI apenas fornece interface
o objetivo não é reconstruir o ClickUp
```

Modelo:

```text
Project → iniciativa / estrutura contínua
Task    → unidade executável
```

Direção de comandos (conceito — não implementados):

```text
coffee task add
coffee task list
coffee task inbox
coffee task today
coffee task done
```

O esquema completo de Tasks/Projects:

```text
UNDEFINED DECISION
```

---

# 40. System Doctor

Capability de diagnóstico:

```text
coffee doctor
coffee system info
coffee system doctor
```

Pode verificar:

```text
OS / Kernel / UEFI / Secure Boot
SELinux / Firewall
GPU / Audio
Git / SSH / Docker
Toolchains (Java, Python, Rust, TeX, Quarto)
```

Objetivo:

```text
dar ao usuário uma visão confiável do estado do ambiente
```

Não é um substituto de ferramentas de administração do sistema.

---

# 41. Documentation Map

Contexto do projeto e onde vive cada documento:

```text
.agents/
├── harness.md                                       ← este documento
├── context/
│   └── coffee-ecosystem-conversation-documentation.md ← fonte arquitetural (DEV)
└── specs/
    └── ux-ui-language.md                            ← linguagem visual TUI (UX)
```

O diretório `docs/` é gerido por fluxo separado — estado atual em:

```text
docs/ai/STATE.md
```

Documentos existentes em docs/ (FACT):

```text
docs/architecture/runtime.md → fronteira de lifecycle
docs/decisions/              → ADRs 001–007
```

O harness não duplica esses documentos.

Quando houver conflito, aplicar a ordem da seção 3.

---

# 42. Decision Tracking

Toda afirmação sobre o projeto deve ser classificada:

```text
FACT       → presente no código/docs hoje
INFERENCE  → leitura da IA, sem confirmação
PROPOSAL   → sugestão, requer decisão do DEV
DECISION   → decidido pelo DEV
UNKNOWN    → sem informação suficiente
```

Nunca transformar automaticamente:

```text
Proposal → Decision
```

Decisões atuais do CLI:

```text
Python como linguagem principal             → DECIDED
Coffee Server como API central              → DECIDED
Task Manager no Server                      → DECIDED
CoffeeApplicationRuntime como fronteira     → DECIDED
Linguagem visual TUI (.agents/specs/)       → DECIDED
DI do ModuleManager via composition root    → DECIDED  (ADR 007)
Component model sem AOP (@Component /
CoffeeRegistry / Container / Runtime)       → DECIDED  (seção 45, ADR 006)

Plugin-oriented architecture para CLI       → PROPOSAL
C++ como engine nativa isolada              → PROPOSAL

Framework de CLI (Click/Typer/Rich/custom)  → UNDEFINED
Contrato formal de plugin                   → UNDEFINED
Sistema de configuração (TOML/YAML/env)     → UNDEFINED
Modelo de Context Pack                      → UNDEFINED
Offline mode / sync                         → UNDEFINED
Modelo do Server V2 (REST/GraphQL/MCP)      → UNDEFINED
Nome da pasta/engine nativa (egine/)        → UNDEFINED
```

Decisões são human-owned. A lista viva de questões abertas está em:

```text
.agents/context/coffee-ecosystem-conversation-documentation.md
docs/ai/STATE.md
```

---

# 43. Autonomy Levels

```text
L0 — Advisor
L1 — Reviewer
L2 — Assisted Worker
L3 — Independent Worker
L4 — Autonomous Task Agent
L5 — Architecture-level capability (só por delegação explícita)
```

Regras:

```text
o nível não é autorização universal
workflow não eleva autonomia automaticamente
tarefa HUMAN-FIRST continua HUMAN-FIRST
L5 não existe por padrão
```

Mode descreve como a IA atua.

Autonomy descreve até onde a IA pode operar.

São conceitos separados (seção 23).

---

# 44. Recoverability / Graph Engineering

Nenhuma automação importante deve presumir que tudo está correto.

O sistema deve poder registrar:

```text
estado
eventos
logs
decisões
ações
resultado
```

e permitir recuperação.

Para trabalho multi-etapa, o ecossistema usa Graph Engineering:

```text
TASK → DECOMPOSE → DEPENDENCIES → EXECUTE → VERIFY → INTEGRATE → CLOSE
```

Persistido em:

```text
.agents/graph/
```

O workflow define a forma de trabalhar.

O grafo fornece o mecanismo.

---

# 45. Component Model / AOP Decision

**Status: DECISION (DEV)**  
**ADR:** `docs/decisions/006-component-decorators-no-aop.md`

O Coffee não adotará um mecanismo de AOP (Aspect-Oriented Programming) tradicional para gerenciamento dos componentes e injeção de dependências.

Como Python não possui suporte nativo a AOP no mesmo modelo de frameworks como Spring, a arquitetura utilizará **decorators como mecanismo declarativo**, sem introduzir weaving, interceptação global de métodos ou alteração dinâmica do comportamento das classes.

## `@Component`

O decorator `@Component` representa a API pública do SDK para declarar uma classe como componente gerenciado pelo Coffee:

```python
@Component
class ModuleManager:
    ...
```

Ao ser aplicado, o decorator registra a classe no `CoffeeRegistry`. O registry funciona como catálogo global dos componentes declarados:

```text
@Component
    ↓
CoffeeRegistry
    ↓
componente registrado
```

## Runtime → Container → Registry

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

## Responsabilidades

```text
@Component                  → declaração de componentes no SDK
CoffeeRegistry              → registro e descoberta dos componentes
CoffeeApplicationContainer  → resolução e instanciação das dependências
CoffeeApplicationRuntime    → inicialização e encerramento do runtime
```

## Regras

```text
decorators não são AOP por si só
no Coffee, funcionam como metadado e ponto de registro
a resolução de dependências permanece sob responsabilidade do Container
o mecanismo permanece simples, explícito e compatível com a filosofia do Coffee
```

Uma futura evolução poderá adicionar interceptores ou aspectos específicos (logging, métricas, tracing, controle de execução) somente caso exista necessidade real — de forma explícita, sem alterar o papel fundamental do `@Component`.

---

# 46. Final Rule

> **O harness deve ajudar o DEV a construir o Coffee que ele definiu — não decidir silenciosamente que Coffee deveria ser construído.**

Toda nova regra, UX, arquitetura ou capability que não esteja especificada deve nascer como:

```text
proposal
```

e não como:

```text
fact
```
