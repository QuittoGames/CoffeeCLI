# ADR 005: Coffee Server como API Central do Ecossistema

**Status:** ACCEPTED  
**Data:** 2026-09-22  
**Contexto:** `.agents/context/coffee-ecosystem-conversation-documentation.md` §5-8

## Contexto

O ecossistema precisa de estado central persistente compartilhado entre clientes (CLI, VS Code, AI Harness, futuros UIs). O `coffe_server` atual deve ser refatorado para esse papel.

## Decisão

O **Coffee Server** será a API central do ecossistema, concentrando:

- Estado central
- Dados do ecossistema
- Contexto persistente
- Projetos
- Tarefas
- Máquinas
- Integrações
- Dados pessoais selecionados
- Capabilities expostas a diferentes clientes

### Divisão de Responsabilidades

```
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

**Regra:** O Server **não** executa diretamente operações na máquina local. Conhece o ecossistema; clientes locais executam operações que dependem da máquina.

### Interfaces do Server

```
                    Coffee Domain
                         |
              +----------+----------+
              |          |          |
            REST       MCP      WebSocket/events
              |          |          |
            Apps         AI       realtime
```

- **REST:** Interface geral para clientes (CLI, dashboards, etc.)
- **MCP:** Adaptador para agentes IA (não arquitetura central)
- **WebSocket/Events:** Tempo real quando necessário
- **Capability Layer:** `task.read`, `task.create`, `project.read`, `context.resolve`, `machine.inspect`, `event.publish` — mesma capability, múltiplas interfaces

### Task Manager Próprio

- Serviço **do Coffee Server** (não aplicação separada)
- Evita duplicação: `Coffee CLI Task Model` = `Coffee Server Task Model` (domain compartilhado)
- CLI é apenas uma das interfaces
- Substitui ClickUp gradualmente (export → validação → uso diário → descontinuar ClickUp)

## Consequências

**Positivas:**
- Estado único fonte de verdade
- Múltiplos clientes, mesma API
- Capability layer desacopla interface de implementação
- Task/Project domain compartilhado entre CLI e Server
- Clean Architecture preservada no Server

**Negativas/Riscos:**
- Server se torna ponto único de falha para dados centralizados
- Offline mode: CLI deve funcionar sem Server para operações locais
- Sync/conflict resolution para offline (aberto)
- Server V2: refatoração significativa do `coffe_server` atual

## Questões Abertas

- [ ] Modelo final Server V2: REST? GraphQL? MCP-first?
- [ ] Esquema completo Tasks/Projects (campos, relacionamentos)
- [ ] Offline mode / sync strategy
- [ ] Formato Context Pack (estrutura, serialização)
- [ ] Auth/Authorization model
- [ ] Deployment: container, systemd, health checks
- [ ] Database: PostgreSQL? SQLite? Outro?