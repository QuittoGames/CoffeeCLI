# ADR 001: CoffeeApplicationRuntime como Fronteira de Lifecycle

**Status:** ACCEPTED  
**Data:** 2026-09-22  
**Contexto:** `docs/architecture/runtime.md`, `src/coffee/core/runtime/`

## Contexto

A aplicação precisa de um modelo de inicialização consistente para múltiplos pontos de entrada (CLI, workers, Hermes, API, processos auxiliares). Sem um runtime centralizado, cada entrypoint duplicaria bootstrap, acoplando-se a detalhes de construção de dependências.

## Opções Consideradas

1. **Runtime dedicado (escolhido)** — Componente único controla lifecycle, cria container, injeta contexto via decorator
2. **Factory functions por entrypoint** — Cada entrypoint chama `create_app()` — simples mas propenso a divergência
3. **Framework DI completo (ex.: python-dependency-injector)** — Poderoso mas overkill para necessidade atual
4. **Singleton global** — Anti-pattern; dificulta testes e lifecycle explícito

## Decisão

Adotar `CoffeeApplicationRuntime` como fronteira de lifecycle:
- `init()` = composition root (monta Config + Container)
- `stop()` = encerramento garantido via `try/finally` no decorator
- Decorator `@CoffeeApplicationRuntime()` envolve pontos de entrada
- Container expõe dependências (Config, serviços) sem criar lifecycle

## Consequências

**Positivas:**
- Bootstrap único e previsível
- Entry points não conhecem detalhes de construção
- `stop()` sempre executa (exceções não vazam recursos)
- Fronteira clara: Config define, Container disponibiliza, Runtime controla, Service executa

**Negativas/Riscos:**
- Decorator ainda não implementado (`__call__` ausente)
- Typo `getContener` precisa correção antes de virar API pública
- `ModuleManager` atualmente viola regra ao usar `@CoffeeApplicationRuntime`

## Próximos Passos

1. Implementar `__call__` no runtime com `try/finally`
2. Corrigir `getContener` → `getContainer`
3. Remover decorator de `ModuleManager`
4. Expandir container para incluir `ModuleManager` e futuros serviços