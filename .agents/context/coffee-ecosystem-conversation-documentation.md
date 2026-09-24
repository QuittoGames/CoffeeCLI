# Coffee Ecosystem — Registro de decisões, ideias e direções

**Documento:** Conversa de arquitetura e reorganização do Coffee Ecosystem  
**Data:** 21/09/2026  
**Status:** Documento-base / especificação viva  
**Objetivo:** preservar as decisões, ideias, problemas identificados e pontos ainda abertos discutidos durante a conversa.

---

## 1. Contexto e motivação

O ecossistema atual foi crescendo principalmente por necessidade imediata. Como consequência, algumas decisões foram tomadas antes que existisse uma especificação global clara.

Isso gerou divergências entre componentes, especialmente no harness de IA/OpenCode, com regras, agentes, workflows e formatos que nem sempre nasceram de uma arquitetura previamente definida.

A intenção agora é fazer uma **refatoração arquitetural consciente**, reduzindo complexidade acidental e criando uma base mais previsível.

O objetivo não é transformar o Coffee em uma dependência fundamental do computador. O Coffee deve ser uma camada adicional, útil e poderosa, sobre o sistema operacional e sobre as demais ferramentas.

---

# 2. Visão geral do Coffee

## 2.1 Definição atual

O Coffee é um **ecossistema pessoal de ferramentas** para centralizar e acelerar atividades do dia a dia, principalmente:

- desenvolvimento;
- gerenciamento de tarefas e projetos;
- integração com IA;
- contexto;
- automação;
- integração entre ferramentas;
- controle e diagnóstico opcional do sistema;
- funcionalidades pessoais além de desenvolvimento.

Uma formulação consolidada:

> **Coffee é uma camada pessoal de produtividade, desenvolvimento, automação, contexto e integração com IA que pode controlar partes do sistema, mas não é a base de existência do sistema operacional e não deve ser uma dependência obrigatória da máquina.**

---

# 3. Princípio fundamental: Coffee não é o sistema operacional

Esta foi uma das decisões conceituais mais importantes.

O Coffee pode controlar o sistema operacional, mas o sistema operacional deve continuar funcional sem o Coffee.

### Modelo desejado

```text
PC / Fedora / Windows
        |
        +-- Git
        +-- VS Code
        +-- Docker
        +-- Quarto
        +-- Terminal
        +-- outras ferramentas
        |
        +-- Coffee Ecosystem
              +-- Tasks
              +-- Projects
              +-- AI
              +-- Context
              +-- Automation
              +-- Developer Tools
              +-- System Control
              +-- Diagnostics
```

### Consequência arquitetural

Se o Coffee for removido:

- Fedora continua funcionando;
- Windows continua funcionando;
- VS Code continua funcionando;
- Git continua funcionando;
- Docker continua funcionando;
- Java/Python/Rust/etc. continuam funcionando.

O que é perdido é a **integração, conveniência, automação e centralização** proporcionadas pelo Coffee.

---

# 4. Coffee pode controlar o sistema

O Coffee não deve ser limitado a um aplicativo puramente de user layer.

Ele poderá operar em diferentes níveis:

```text
L0 — User
    Tasks
    Projects
    Context
    Git
    AI

L1 — System
    Services
    Networking
    Diagnostics
    Packages
    Machine inspection

L2 — Privileged
    Boot
    Mounts
    Firewall
    operações sensíveis do sistema
```

Direção atual:

- L0 é normal;
- L1 é controlado;
- L2 exige mecanismos explícitos e protegidos.

O controle privilegiado deve preferencialmente ser separado do processo principal do Coffee, utilizando mecanismos apropriados do sistema em vez de simplesmente executar comandos arbitrários com `sudo`/privilégio elevado.

---

# 5. Coffee Server

## 5.1 Papel futuro

O `coffe_server` deve ser refatorado e passar a ser a **API central do ecossistema**.

Não é desejado simplesmente apagar a arquitetura atual. A direção é manter a base de Clean Architecture, pois ela trouxe resiliência e isolamento, mas rever decisões de domínio, responsabilidades e fronteiras que surgiram de forma incremental.

O servidor deverá concentrar principalmente:

- estado central;
- dados do ecossistema;
- contexto persistente;
- projetos;
- tarefas;
- máquinas;
- integrações;
- dados pessoais selecionados;
- capabilities que precisam ser expostas a diferentes clientes.

## 5.2 O servidor não deve virar um monólito operacional

O Server não deve ser responsável por executar diretamente tudo no computador local.

A divisão desejada é aproximadamente:

```text
Coffee Server
    |
    +-- estado
    +-- dados
    +-- contexto
    +-- capabilities
    +-- eventos
    |
    v
Coffee CLI / clientes locais
    |
    +-- filesystem
    +-- Git
    +-- processos
    +-- sistema operacional
    +-- recursos locais
```

O servidor conhece o ecossistema; os componentes locais executam operações que dependem da máquina.

---

# 6. Interfaces do Coffee Server

A arquitetura discutida prevê diferentes interfaces para o mesmo domínio:

```text
                    Coffee Domain
                         |
              +----------+----------+
              |          |          |
            REST       MCP      WebSocket/events
              |          |          |
            Apps         AI       realtime
```

O MCP não deve ser a arquitetura central. Ele é uma interface/adaptador para agentes.

REST pode funcionar como interface geral.

WebSocket/eventos podem suportar comunicação em tempo real quando necessário.

Clientes locais, como o Coffee CLI, também devem poder consumir o Server.

---

# 7. Capability Layer

Foi identificada a ideia de uma camada de capabilities para evitar que cada cliente precise conhecer dezenas de detalhes internos.

Exemplos:

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

As mesmas capabilities podem ser utilizadas por:

- REST;
- MCP;
- CLI;
- futuros clientes.

Isso permite separar:

```text
capability
    !=
implementação concreta
```

---

# 8. Contexto como parte central do Coffee

Uma ideia forte da conversa foi tirar a responsabilidade de contexto exclusivamente do harness de IA.

O Coffee deve futuramente possuir uma camada de contexto capaz de combinar informações de diferentes fontes:

```text
User profile
Project
Repository
Git state
Task
Documentation
Decisions
Machine
Runtime state
External data
```

Fluxo desejado:

```text
Request
   |
Context Resolver
   |
Relevant Information
   |
Context Pack
   |
AI Harness / Client
```

A intenção é fornecer apenas o contexto relevante ao modelo, em vez de carregar arbitrariamente grandes quantidades de informação.

---

# 9. AI Harness / OpenCode

## 9.1 Problema atual

O harness atual cresceu por necessidade e possui muitas peças, incluindo agentes, skills, commands, policies, workflows, schemas e routers.

Na inspeção do repositório atual, foram identificados muitos módulos, incluindo numerosos agents, skills e commands. A existência dessa quantidade de componentes reforça o diagnóstico de que uma reconstrução planejada pode ser mais limpa que tentar corrigir toda a estrutura incrementalmente. [`.opencode` no GitHub](https://github.com/QuittoGames/.opencode)

O repositório atual possui, entre outros componentes, `RULES.md`, `AGENTS.md`, Context Router, Workflow Router, policies e um registry de workflows.

## 9.2 Direção

A direção escolhida é tratar o harness atual como referência histórica e, em algum momento, reconstruir uma versão nova a partir de uma especificação definida pelo usuário.

Antes de criar agentes, definir:

```text
workflow
context
capabilities
ownership
routing
model selection
permissions
validation
escalation
```

Somente depois decidir:

```text
quais agentes existem
quais skills existem
quais commands existem
quais modelos usar
```

## 9.3 Context Router

O Context Router atual representa uma tentativa válida de resolver contexto, mas sua forma foi definida parcialmente pelo agente. Foi apontado especificamente que o formato YAML não era uma decisão originalmente especificada pelo usuário.

Direção para uma futura reconstrução:

> o formato, contrato e comportamento do Context Router devem ser definidos primeiro pelo desenvolvedor; o agente não deve escolher silenciosamente a arquitetura.

---

# 10. Coffee CLI

## 10.1 Papel

O Coffee CLI será o **principal cliente/interface de uso do Coffee** no dia a dia.

Ele deve atuar como uma entrada unificada para:

- tasks;
- projects;
- Git;
- contexto;
- AI;
- system;
- machine;
- serviços;
- ferramentas de desenvolvimento;
- automações.

O CLI não deve ser apenas uma substituição do shell atual.

Ele será um cliente local que combina operações locais com operações no Coffee Server.

---

# 11. Coffee CLI: local vs server

O CLI não deve depender do Server para tudo.

Exemplos:

```text
coffee system info
    -> local

coffee git status
    -> local

coffee task add "..."
    -> Server

coffee context get
    -> Server + fontes locais
```

A arquitetura deve continuar funcional quando o Server estiver indisponível para operações que não dependem dele.

No futuro pode existir uma fila/offline sync para algumas operações, mas isso ainda não foi decidido como requisito obrigatório.

---

# 12. Linguagem do Coffee CLI

Foram consideradas:

- Python;
- C++;
- Rust;
- Java;
- Go.

## 12.1 Rust

Rust é tecnicamente muito adequado para uma ferramenta de sistema/CLI, porém houve experiência prática de tentativa de implementação em que o aprendizado da linguagem consumiu muitas horas principalmente com sintaxe e conceitos, apesar de já haver conhecimento de strings, borrowing e ownership.

Conclusão da conversa:

> Rust é melhor tratado como possibilidade futura, quando houver maior fluência, e não como linguagem principal de um primeiro CLI que precisa ser produtivo e confiável imediatamente.

## 12.2 C++

C++ é forte para:

- performance;
- integração nativa;
- processos;
- sistema;
- hardware;
- low-level.

Porém há uma preocupação: ainda não existe fluência suficiente para produzir rapidamente um CLI grande e de manutenção confortável em C++.

## 12.3 Python

Python oferece o maior ganho imediato de produtividade e já é uma linguagem forte no repertório atual.

É adequado para:

- CLI;
- API client;
- JSON;
- HTTP;
- filesystem;
- subprocessos;
- contexto;
- automação;
- orquestração.

A principal limitação discutida não é robustez do código Python, mas a experiência de distribuição como ferramenta nativa e possíveis necessidades futuras de integração de baixo nível.

## 12.4 Direção atual

A direção de trabalho mais forte estabelecida na conversa é:

```text
Python → implementação principal do CLI V1
C++    → engine/native capabilities quando existir necessidade concreta
Rust   → possível evolução futura
Java   → permanece plausível, mas não é a direção atual
```

Importante: a decisão detalhada sobre exatamente quais partes usarão C++ ainda está aberta.

---

# 13. Python + C++

A ideia é usar os dois, mas não dividir artificialmente o sistema.

Direção proposta:

```text
Coffee CLI
    |
    v
Python
    |
    +-- CLI UX
    +-- orchestration
    +-- API client
    +-- task/project
    +-- context
    +-- configuration
    |
    v
Native capability / Engine
    |
    v
C++
```

O C++ deverá entrar apenas quando houver responsabilidade concreta que realmente justifique uma camada nativa.

Uma possibilidade inicial discutida foi utilizar o C++ como processo/helper separado, com comunicação via protocolo simples, potencialmente JSON.

Exemplo conceitual:

```text
Python
   |
spawn
   v
C++ helper
   |
JSON
   v
Python
```

Essa fronteira permitiria substituir ou ampliar a implementação sem espalhar dependências de C++ por todo o projeto.

---

# 14. Arquitetura interna do Coffee CLI

A direção arquitetural proposta não é a típica:

```text
models/
services/
controllers/
```

A razão é que o Coffee CLI deve continuar crescendo durante anos e não pode depender de uma enorme coleção de services globais.

A ideia escolhida para investigação é uma **arquitetura modular orientada a plugins/features**.

---

# 15. Plugin-oriented architecture

O Coffee CLI deverá permitir que features sejam módulos relativamente independentes.

Exemplo:

```text
Coffee Core
    |
    +-- Task Plugin
    +-- Project Plugin
    +-- Git Plugin
    +-- Context Plugin
    +-- System Plugin
    +-- AI Plugin
```

Cada feature poderá concentrar seus próprios:

- models;
- services/use cases;
- adapters;
- ports/contracts;
- commands;
- configuração;
- metadata de plugin.

Exemplo conceitual:

```text
services/task/
    models/
    services/
    adapters/
    ports/
    commands/
    plugin.py
```

A estrutura exata ainda não foi implementada e continua sendo uma decisão de arquitetura em aberto.

---

# 16. Domain

Foi discutida a ideia de manter uma camada `domain` com classes de domínio.

Exemplos:

```text
Task
Project
Repository
Machine
Context
```

O domínio deve representar conceitos da aplicação e evitar conhecimento concreto de:

- ClickUp;
- PostgreSQL;
- HTTP;
- Rich/TUI;
- Fedora;
- C++; etc.

A decisão arquitetural importante é que dependências externas sejam representadas por contratos/ports quando necessário, deixando implementações concretas nos adapters.

Assim:

```text
Domain
   |
Contract / Port
   |
Adapter
   |
HTTP / filesystem / C++ / Git / etc.
```

---

# 17. Core vs Engine

Ainda não foi decidido o nome definitivo para a camada C++.

Foi considerada a ideia de `core`, porém existe preocupação em usar `core` como nome genérico e acabar colocando metade do Coffee nessa pasta.

A direção atual é utilizar provisoriamente algo como:

```text
engine/
```

para representar componentes nativos/low-level, deixando `core` reservado para conceitos realmente centrais da aplicação, caso seja necessário.

---

# 18. Localização do projeto do CLI

Foi analisada a organização atual do workspace no Windows.

A decisão foi colocar o novo projeto dentro da pasta raiz do ecossistema.

A pasta raiz proposta é:

```text
Coffee/
```

E o primeiro projeto:

```text
Coffee/
└── coffee-cli/
```

Estruturas futuras possíveis:

```text
Coffee/
├── coffee-cli/
├── coffee-server/
├── coffee-engine/
├── project-setup/
└── docs/
```

No entanto, não há necessidade de criar toda essa árvore imediatamente.

---

# 19. ProjectSetup

O `ProjectSetup-3.0` continuará sendo uma peça importante.

O projeto já tem suporte declarado a Windows e Linux/macOS e possui launchers separados, além de lógica explícita de plataforma. [ProjectSetup-3.0 no GitHub](https://github.com/QuittoGames/ProjectSetup-3.0)

A direção futura é tornar o componente mais realmente cross-platform e reduzir código específico de plataforma espalhado.

Foi discutida uma evolução conceitual de:

```text
project generator
```

para algo mais próximo de:

```text
project bootstrap / environment bootstrapper
```

Possíveis operações futuras:

```text
project create
project detect
project configure
project setup
project doctor
project validate
```

---

# 20. Quarto / LaTeX / CABNT

Existe um template próprio baseado em ABNT que já é utilizado e considerado suficientemente funcional para o uso escolar atual.

A intenção é reaproveitá-lo em vez de trocar tudo.

O problema observado no Linux não é necessariamente o template, mas a integração do projeto com Quarto/LaTeX e diferenças entre ambientes.

Direção:

```text
Coffee/ProjectSetup
       |
Quarto
       |
Pandoc
       |
TeX Live / XeLaTeX
       |
CABNT
```

No futuro o Coffee poderá verificar o ambiente documental:

```text
quarto
pandoc
xelatex
latexmk
bibliografia
fonts
CABNT
```

A intenção é tornar o processo previsível e reproduzível no Fedora.

---

# 21. Fedora / Linux

O objetivo não é apenas instalar Fedora.

A meta é possuir um **Fedora previsível, estável, seguro e reproduzível**, sem transformar Flatpak na única forma de distribuição de aplicativos.

A preferência atual é:

```text
RPM/native
    -> sistema, toolchain e componentes necessários

Flatpak
    -> GUI quando fizer sentido

Container
    -> serviços isolados/agentes/infraestrutura

Source
    -> somente quando necessário
```

Não existe intenção de tornar tudo Flatpak.

---

# 22. Linux baseline

Áreas que precisam de baseline/configuração:

```text
UEFI
Secure Boot
SELinux
firewalld
systemd
GNOME
Wayland
PipeWire
NetworkManager
GPU/Mesa/Vulkan
Git
SSH
Python
Java
Rust
C/C++
Docker/Podman
Tailscale
Quarto
TeX Live
VS Code
```

A configuração deve ser automatizável, mas não precisa ser feita toda de uma vez.

---

# 23. SELinux

A conversa chegou à conclusão de que SELinux não precisa ser usado para restringir indiscriminadamente o acesso de processos a todas as pastas do usuário.

O valor mais relevante para o caso é a **contenção de processos/serviços comprometidos**.

Direção:

- manter o mecanismo da distribuição;
- evitar começar com políticas customizadas desnecessárias;
- usar confinamento principalmente para componentes em que o isolamento realmente traz benefício;
- evitar transformar permissões em um obstáculo para o workflow diário.

---

# 24. Segurança do Linux

O objetivo é melhorar a segurança sem transformar o sistema em um ambiente impraticável para desenvolvimento.

Áreas prioritárias:

```text
SELinux
firewalld
SSH
serviços
exposição de portas
containers
secrets
logs
backups
```

A filosofia é segurança pragmática:

```text
segurança
+
produtividade
+
diagnóstico
```

---

# 25. System Doctor / Observability

Uma das ideias mais importantes para o Coffee é possuir uma camada de diagnóstico.

Exemplo:

```bash
coffee doctor
coffee system doctor
coffee system info
```

O sistema poderia verificar:

```text
OS
Kernel
UEFI
Secure Boot
SELinux
Firewall
Wayland
GPU
Mesa
Vulkan
Audio
Git
SSH
Docker
Quarto
TeX Live
Java
Python
Rust
Tailscale
```

A intenção não é fazer do Coffee uma ferramenta de administração de sistemas. É oferecer uma **capability secundária de observabilidade e diagnóstico**.

---

# 26. Dual boot

O dual boot é tratado como infraestrutura separada.

A configuração desejada inclui:

```text
UEFI only
CSM/Legacy off
Secure Boot
rEFInd / cadeia de boot compatível
backup da ESP
backup de configuração
caminho de recuperação
```

O repositório `dualboot_rEFIind` atualmente contém instruções orientadas ao Windows e `bcdedit`; a intenção futura é torná-lo uma infraestrutura de boot mais claramente documentada para o ambiente híbrido. [dualboot_rEFIind no GitHub](https://github.com/QuittoGames/dualboot_rEFIind)

Também devem ser definidos procedimentos de recovery antes de alterações de boot.

---

# 27. Backup e Recovery

Foi identificada a necessidade de uma camada explícita de recuperação.

Objetivo:

```text
máquina perdida
    |
Fresh OS
    |
bootstrap
    |
configs
    |
toolchain
    |
Coffee
    |
repositories
    |
dados
```

Possíveis comandos futuros:

```text
coffee machine export
coffee machine doctor
coffee machine bootstrap
coffee machine diff
coffee machine restore
```

---

# 28. ClickUp / Task Manager

O ClickUp atualmente gera mais custo operacional do que benefício em determinados fluxos, principalmente por:

- peso da interface/browser;
- excesso de estrutura;
- pouca correspondência com o modelo desejado de organização;
- dificuldade de controlar exatamente como as tasks devem ser criadas e apresentadas.

A direção é criar um **Task Manager próprio integrado ao Coffee**.

Importante: não se deseja copiar o ClickUp inteiro.

---

# 29. Coffee Task Manager

O Task Manager será um **serviço do Coffee Server**, não uma aplicação totalmente separada.

Isso evita duplicação entre:

```text
Coffee CLI Task Model
Coffee Server Task Model
```

A base deve ser compartilhada pelo domínio/backend.

O CLI será apenas uma das interfaces.

Exemplos conceituais:

```bash
coffee task add "..."
coffee task list
coffee task inbox
coffee task today
coffee task next
coffee task done
```

Visões desejadas podem incluir:

```text
Inbox
Today
Next
Projects
Waiting
Done
```

A UI deve esconder complexidade desnecessária.

---

# 30. Task vs Project

Foi reforçada a separação entre:

```text
Project
→ iniciativa/estrutura contínua

Task
→ unidade executável
```

Um projeto pode possuir diversas tasks, e as tasks não devem se transformar em uma árvore de gestão exageradamente complexa.

---

# 31. Migração do ClickUp

A direção provável é migrar o gerenciamento de tarefas para o Coffee.

A migração deve extrair somente o modelo necessário:

```text
tasks
projects
relationships
tatus
priority
context
```

Não existe necessidade de reproduzir todos os recursos corporativos do ClickUp.

O processo ideal seria gradual:

```text
ClickUp
   |
export
   |
Coffee Tasks
   |
validação
   |
uso diário
   |
ClickUp deixa de ser necessário
```

A ferramenta substituta foi conceitualmente definida como Coffee Task Manager; detalhes de implementação e UX ainda precisam ser fechados.

---

# 32. Personal data / Finance

O Coffee não deve ser restrito a desenvolvimento.

Foi dada como possibilidade uma camada pessoal capaz de trabalhar com informações como dados financeiros atuais, desde que o domínio e as integrações sejam bem definidos.

A distinção desejada é:

```text
Coffee Server
→ possui/organiza os dados

AI
→ interpreta/análise

CLI/UI
→ apresenta
```

Assim o raciocínio da IA não precisa ser o dono do dado.

---

# 33. Developer Environment

O ecossistema precisa ser tratado como um ambiente integrado de desenvolvimento.

Componentes atuais relevantes incluem:

```text
VS Code
ProjectSetup
Git
Shell
AI Harness
Coffee CLI
Quarto
LaTeX
Docker
Java
Python
C/C++
Rust
```

O objetivo é que essas ferramentas permaneçam individuais, mas possam integrar-se ao Coffee.

---

# 34. VS Code

O repositório de VS Code atual já contém componentes de configuração, incluindo:

- settings;
- keybindings;
- MCP;
- prompts;
- snippets;
- formatter;
- workspace/sync.

[`.vscode` no GitHub](https://github.com/QuittoGames/.vscode)

Direção:

```text
VS Code = IDE
Coffee = camada de ambiente/integração
AI Harness = raciocínio
Coffee Server = estado central
```

A ideia é poder aprimorar o VS Code com ferramentas de aceleração e eventualmente integrar recursos de vibe coding, sem fazer o editor depender rigidamente do Coffee.

---

# 35. Shell

O `.coffe-sdk-shell` atual é considerado legado para o futuro do projeto.

A visão futura é substituir progressivamente a lógica de shell por um **Coffee CLI próprio**, em outra linguagem/estrutura.

O Zsh atual é tratado como fonte de funcionalidades a migrar, não necessariamente como arquitetura definitiva.

---

# 36. Obsidian / conhecimento

O Obsidian continua sendo a camada principal de conhecimento/documentação pessoal.

Ele não deve ser substituído pelo Coffee.

O Coffee deve futuramente conseguir consumir contexto/referências do conhecimento quando necessário.

O objetivo é separar:

```text
Knowledge
→ Obsidian / documentos

State
→ Coffee Server

Context delivery
→ Coffee Context System
```

---

# 37. GNOME / UX

O Fedora será personalizado para aproximar a experiência do workflow desejado.

Isso inclui:

- tema;
- extensões GNOME;
- Alt-Tab;
- ícones;
- terminal;
- atalhos;
- aparência.

Os projetos de tema Fluent e Alt-Tab são considerados camada de experiência/UX, não dependências fundamentais da infraestrutura. [Fluent GTK theme](https://github.com/QuittoGames/Fluent-gtk-theme-modified) · [Advanced Alt-Tab](https://github.com/QuittoGames/advanced-alt-tab-with-up-title)

---

# 38. Repositórios relacionados

Os principais projetos/repositórios discutidos foram:

```text
QuittoGames/coffe_server
QuittoGames/.opencode
QuittoGames/.vscode
QuittoGames/ProjectSetup-3.0
QuittoGames/.wintrasferlinux
QuittoGames/.coffe-sdk-shell
QuittoGames/.zsh
QuittoGames/dualboot_rEFIind
QuittoGames/Fluent-gtk-theme-modified
QuittoGames/Obisidian
QuittoGames/advanced-alt-tab-with-up-title
```

Eles representam componentes diferentes do mesmo ambiente de desenvolvimento/personalização, mas nem todos precisam virar dependências do Coffee.

---

# 39. Organização conceitual futura

Uma visão consolidada do ecossistema:

```text
                        QUITTO
                          |
                    Coffee Interface
                          |
             +------------+------------+
             |                         |
        Coffee CLI                 outras UIs
             |                         |
             +------------+------------+
                          |
                    Coffee Server
                          |
       +------------------+------------------+
       |                  |                  |
     Tasks              Projects           Context
       |                  |                  |
       +------------------+------------------+
       |                  |                  |
      AI            Integrations         Personal
       |
       +-------------------------------+
                                       |
                                Local System Layer
                                       |
                          +------------+-------------+
                          |                          |
                        Fedora                   Windows
```

---

# 40. O que NÃO fazer

## 40.1 Não transformar Coffee em OS

Não fazer o sistema depender do Coffee para boot, funcionamento básico ou existência.

## 40.2 Não tornar tudo server-side

Operações que precisam da máquina devem poder continuar locais.

## 40.3 Não transformar o CLI em um segundo servidor

O CLI é cliente/orquestrador local.

## 40.4 Não reproduzir o ClickUp inteiro

Criar somente o modelo de task/project necessário.

## 40.5 Não transformar cada serviço em um Service global gigante

Preferir módulos/features relativamente independentes.

## 40.6 Não espalhar C++ pelo projeto

Usar abstrações e adapters para que o restante do Python não conheça detalhes nativos.

## 40.7 Não refazer OpenCode sem especificação

Primeiro definir contrato e comportamento; depois implementar.

## 40.8 Não automatizar decisões arquiteturais silenciosamente

Agentes devem implementar dentro do escopo definido, não criar a arquitetura inteira por conta própria.

---

# 41. Sequência de desenvolvimento discutida

Uma sequência plausível, ainda sujeita a refinamento:

```text
1. Definir contratos do ecossistema
2. Definir contrato do Coffee CLI
3. Definir Task Manager / domínio de Tasks
4. Implementar Coffee CLI V1
5. Integrar CLI + Task Service do Server
6. Criar baseline/doctor do Linux
7. Estruturar máquina / dual boot / recovery
8. Refatorar Coffee Server
9. Criar Context Engine
10. Reconstruir AI Harness
```

Não é necessário executar tudo de uma vez.

---

# 42. O que já está decidido vs. o que ainda está aberto

## Decisões / direções fortes

- Coffee será uma camada sobre o sistema, não o sistema.
- Coffee pode controlar o sistema, inclusive com componentes privilegiados separados.
- Coffee Server será a API central do ecossistema.
- Clean Architecture será preservada no Server, com refatoração das decisões problemáticas.
- Task Manager próprio será um serviço do Coffee Server.
- ClickUp deverá ser gradualmente substituído por uma solução própria.
- Coffee CLI será o principal cliente de uso diário.
- CLI terá operações locais e operações via Server.
- Arquitetura do CLI será modular e orientada a plugins/features.
- Domain será separado de implementações concretas.
- C++ será mantido isolado como camada nativa/engine quando necessário.
- Rust será considerado para o futuro, não como requisito inicial.
- Fedora será configurado para estabilidade, segurança e reprodutibilidade.
- SELinux deve existir sem virar obstáculo ao workflow.
- System Doctor/diagnóstico será capability secundária.
- Dual boot será tratado como infraestrutura/recovery.
- Coffee não deve ser requisito para o funcionamento básico do PC.

## Decisões ainda abertas

- nome definitivo da pasta/engine C++;
- framework de CLI em Python;
- protocolo Python ↔ C++;
- modelo definitivo de plugins;
- contrato formal de Plugin;
- modelo de configuração do CLI;
- sistema de discovery/load de plugins;
- offline mode/sync;
- formato de Context Pack;
- modelo final do Coffee Server V2;
- esquema completo de Tasks/Projects;
- nova UX do Task Manager;
- forma final de integração VS Code ↔ Coffee;
- baseline final de pacotes do Fedora;
- detalhes da cadeia Secure Boot/rEFInd/MOK;
- política completa de privilégios do Coffee;
- estratégia de backup/recovery.

---

# 43. Próximo grande passo

O próximo trabalho lógico não é implementar o Coffee inteiro.

É escrever a **especificação inicial do Coffee CLI**, definindo:

```text
1. objetivos
2. não-objetivos
3. comandos
4. módulos/plugins
5. domínio
6. comunicação com Server
7. operações locais
8. configuração
9. output
10. erros/exit codes
11. lifecycle
12. extensibilidade
13. integração futura com C++
14. critérios de qualidade
```

Depois disso, a primeira implementação pode começar em Python, deixando uma fronteira limpa para uma camada C++ quando houver necessidade real.

---

# 44. Resumo executivo

O Coffee está sendo redefinido de uma coleção de projetos independentes para um **ecossistema pessoal integrado**, porém não obrigatório.

A estrutura conceitual é:

```text
                 COFFEE
                    |
        +-----------+-----------+
        |                       |
      SERVER                  CLI
        |                       |
  state / context         local tooling
  tasks / projects        system control
  integrations            AI interface
  capabilities            Git / automation
        |
        +-----------+-----------+
                    |
             AI / Context
                    |
       +------------+------------+
       |                         |
 Developer Tools            Personal Tools
```

O Coffee deve **reduzir atrito**, não criar outro sistema para administrar.

A prioridade é uma arquitetura simples o suficiente para ser mantida, modular o suficiente para crescer e desacoplada o suficiente para que nenhuma ferramenta individual se torne o ponto único de falha do computador.
