# ADR 007 — Injeção de dependência do ModuleManager via composition root

**Data:** 2026-09-22
**Status:** ✅ ACCEPTED — DEV decidiu proseguir com a proposta
**Relacionado:** `docs/architecture/runtime.md` (§6.1, §8.3)

---

## Context

O `ModuleManager` precisa de acesso aos dados do `Config` para funcionar.

Hoje o código tenta resolver isso aplicando o decorator de lifecycle nele:

```python
# src/coffee/core/Services/module/ModuleManager.py (atual)
@dataclass
@CoffeeApplicationRuntime
class ModuleManager:
    def loadModules(self) -> list[Module]: ...
```

Isso usa a **ferramenta errada** para o problema certo:

| Mecanismo | Serve para | Quem deve usar |
|---|---|---|
| Decorator `@CoffeeApplicationRuntime` | interceptar **lifecycle** (init/stop) | pontos de entrada |
| Constructor injection (`config: Config`) | entregar **dependência** | serviços |

O `ModuleManager` não precisa **criar nem controlar** o `Config` — ele precisa apenas **recebê-lo**. Além disso:

- O decorator no serviço contradiz a regra arquitetural §6.1: *serviços não controlam o lifecycle da aplicação*.
- O decorator, hoje, sequer funciona (falta `__call__` na classe) — ver `docs/architecture/runtime.md` §7.

**Pergunta:** como entregar o `Config` ao `ModuleManager` sem colocar interceptação de lifecycle onde não deve haver?

---

## Options

### Opção A — Manter o decorator no serviço (status quo)

```python
@CoffeeApplicationRuntime
class ModuleManager: ...
```

- ❌ Lifecycle e dependência ficam misturados.
- ❌ Viola a separação Config/Container/Runtime/Service.
- ❌ Duplo lifecycle se o decorator for implementado (entrypoint + serviço).

### Opção B — Singleton global de Config

```python
class ModuleManager:
    def loadModules(self):
        config = global_config  # acesso direto
```

- ❌ Estado global escondido; teste e reasoning ficam difíceis.
- ❌ Contradiz "1 Runtime → 1 Container → instâncias daquela aplicação".

### Opção C — Constructor injection pelo composition root ✅

O Runtime (único composition root) **cria** o `ModuleManager` e **injeta** o `Config`; o Container guarda a instância pronta.

- ✅ Dependência explícita e visível no construtor.
- ✅ Lifecycle continua só no entrypoint.
- ✅ Testável: `ModuleManager(config=fake_config)` sem app real.
- ✅ Alinhado com a regra: *serviço recebe contexto, não o cria*.

---

## Proposal (Opção C)

### Fluxo

```text
Runtime.init()                        ← composition root
    │
    ├── Config().build()
    ├── Container(config)
    ├── ModuleManager(config=...)     ← criado e injetado aqui
    └── container.moduleManager = mm
              │
              ▼
EntryPoint (@CoffeeApplicationRuntime ← ÚNICO interceptor)
    │
    └── app.getContener().getModuleManager()
              │
              ▼
        mm.loadModules()              ← usa self.config
```

### Forma conceitual

```python
# Serviço — recebe a dependência, sem decorator
@dataclass
class ModuleManager:
    config: Config

    def loadModules(self) -> list[Module]:
        ...  # usa self.config


# Composition root — único lugar que monta
def init(self) -> None:
    config = Config().build()
    self.container = CoffeeApplicationContainer(config=config)
    self.container.moduleManager = ModuleManager(config=config)


# Ponto de entrada — só consome
@CoffeeApplicationRuntime()
async def main(app):
    mm = app.getContener().getModuleManager()
    mm.loadModules()
```

### Regra resultante

```text
Serviço        NÃO intercepta contexto  →  RECEBE contexto (construtor)
Ponto de entrada NÃO monta nada        →  SÓ CONSUME contexto
Runtime        NÃO executa domínio      →  MONTA e CONTROLA lifecycle
```

---

## Decision

**O DEV decide proseguir com a Opção C** (constructor injection via composition root).

- Decorator de lifecycle: **somente** em pontos de entrada.
- `ModuleManager`: **sem** decorator; recebe `Config` no construtor.
- Criação/injeção do `ModuleManager`: **dentro** de `Runtime.init()` (composição interna, não nova classe AOP).

---

## Consequences

### Código que muda

| Arquivo | Mudança |
|---|---|
| `ModuleManager.py` | remover `@CoffeeApplicationRuntime`; adicionar campo `config: Config` |
| `CoffeAplicationRuntime.py` | `init()` passa a instanciar `ModuleManager(config=...)` |
| `CoffeeApplicationContainer.py` | ganhar campo/getter para `moduleManager` |
| `main.py` / `CLI.py` | consumir via container; decorator permanece só aqui |

### Ganhos

- Fronteira lifecycle × dependência explícita e verificável.
- Serviços continuam pequenos e testáveis isoladamente.
- Nenhum decorator empilhado; fluxo de execução legível.

### Custos / cuidados

- Ordem de construção no `init()` importa: `Config` → `Container` → serviços.
- Se surgir um 2º serviço com dependência, repetir o padrão **dentro do mesmo `init()`** — não criar uma nova classe interceptadora (ver `docs/architecture/runtime.md` §12: 1 interceptor na borda; composição em passos internos).

### Fora deste escopo (ainda aberto)

- Definir o destino do `setConfig` redundante (Runtime ↔ Container) — diagnóstico confirmado, escolha da política de escrita ainda pendente.
- Implementação do `__call__` do decorator.

---

## References

- `docs/architecture/runtime.md` — conceituação do Runtime
- `src/coffee/core/Services/module/ModuleManager.py`
- `src/coffee/core/runtime/CoffeAplicationRuntime.py`
- `src/coffee/core/runtime/contener/CoffeeApplicationContainer.py`
