# ADR 002: Arquitetura Plugin-Oriented para Coffee CLI

**Status:** PROPOSAL  
**Data:** 2026-09-22  
**Contexto:** `.agents/context/coffee-ecosystem-conversation-documentation.md` §14-15

## Contexto

O Coffee CLI deve crescer por anos e não pode depender de uma enorme coleção de services globais acoplados. A arquitetura tradicional `models/services/controllers` cria dependências circulares e dificulta isolamento de features.

## Opções Consideradas

1. **Plugin-oriented architecture (escolhida)** — Features como módulos independentes com próprios models, services, adapters, ports, commands, config, metadata
2. **Layered architecture tradicional** — `models/`, `services/`, `controllers/` globais — simples mas não escala bem para CLI extenso
3. **Microservices internos** — Overkill, complexidade de comunicação desnecessária
4. **Monolito modular por pastas** — Melhor que layered, mas sem contratos formais de plugin

## Decisão (Proposta)

Estrutura alvo:

```
src/coffee/
├── core/                          # Núcleo estável
│   ├── runtime/                   # CoffeeApplicationRuntime + Container
│   ├── config/                    # Configuration system
│   ├── plugin/                    # Plugin system (discovery, loading, contract)
│   ├── domain/                    # Domain models (Task, Project, Repository, Machine, Context)
│   └── ports/                     # Contracts/ports para adapters
├── plugins/                       # Features como plugins independentes
│   ├── task/
│   │   ├── models/
│   │   ├── services/
│   │   ├── adapters/
│   │   ├── ports/
│   │   ├── commands/
│   │   └── plugin.py
│   ├── project/
│   ├── git/
│   ├── context/
│   ├── system/
│   ├── ai/
│   └── ...
├── engine/ (ou native/)           # C++ native capabilities (isolado)
├── cli/                           # CLI entry, command routing, output
└── main.py                        # Bootstrap
```

Cada plugin concentra:
- **models** — domain entities específicas do plugin
- **services/use cases** — lógica de negócio
- **adapters** — implementações concretas (HTTP, filesystem, C++, Git)
- **ports/contracts** — interfaces que o core conhece
- **commands** — comandos CLI expostos
- **plugin.py** — metadata, registro, configuração

## Consequências

**Positivas:**
- Isolamento: plugins não se acoplam diretamente
- Extensibilidade: novos features = novos plugins
- Testabilidade: cada plugin testável independentemente
- Substituibilidade: adapters trocáveis sem tocar domain
- Onboarding: novo dev entende um plugin por vez

**Negativas/Riscos:**
- Complexidade inicial: plugin system, discovery, loading, contracts
- Overhead: boilerplate por plugin
- Decisões abertas: discovery mechanism, config schema, versioning, inter-plugin communication

## Questões Abertas (devem virar ADRs separados)

- [ ] Framework CLI Python (Click/Typer/Rich/Custom) → ADR 003
- [ ] Protocolo Python ↔ C++ → ADR 004
- [ ] Modelo de descoberta/carregamento de plugins
- [ ] Contrato formal de Plugin (interface mínima, metadata)
- [ ] Sistema de configuração (TOML/YAML/Python)
- [ ] Inter-plugin communication (event bus? shared ports?)
- [ ] Plugin versioning e compatibilidade