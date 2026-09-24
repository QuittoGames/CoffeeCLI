# ADR 003: Python como Linguagem Principal do Coffee CLI V1

**Status:** ACCEPTED  
**Data:** 2026-09-22  
**Contexto:** `.agents/context/coffee-ecosystem-conversation-documentation.md` §12

## Contexto

Escolha da linguagem para implementação do Coffee CLI V1. Consideradas: Python, C++, Rust, Java, Go.

## Opções Consideradas

| Linguagem | Prós | Contras | Veredito |
|---|---|---|---|
| **Python** (escolhido) | Produtividade imediata, repertório forte, ecossistema rico (CLI, HTTP, JSON, filesystem, subprocess, asyncio), adequado para orchestration/API client/context/automation | Distribuição como ferramenta nativa, futuras necessidades low-level | **V1 principal** |
| **C++** | Performance, integração nativa, processos, sistema, hardware, low-level | Falta de fluência para CLI grande e manutenível rapidamente | **Engine nativa isolada** quando houver necessidade concreta |
| **Rust** | Tecnicamente adequado, segurança memória, performance | Curva de aprendizado consumiu muitas horas (sintaxe, conceitos) | **Futuro** — quando houver maior fluência |
| **Java** | Enterprise, Spring Boot, APIs REST | Verbosidade, startup lento para CLI, não é direção atual | Plausível mas não atual |
| **Go** | CLI nativo, concorrência, single binary | Não está no repertório atual | Não considerado profundamente |

## Decisão

```text
Python → implementação principal do CLI V1
C++    → engine/native capabilities quando existir necessidade concreta
Rust   → possível evolução futura
Java   → permanece plausível, mas não é a direção atual
```

## Consequências

**Positivas:**
- Velocidade de desenvolvimento V1
- Aproveita conhecimento atual (Python avançado: POO, async, automação, CLI, bibliotecas, estruturação)
- Ecossistema maduro para: Click/Typer/Rich, HTTP clients, asyncio, subprocess, platformdirs, etc.
- Fronteira limpa para C++ engine via processo separado + protocolo simples

**Negativas/Riscos:**
- Distribuição: `pipx`/`pip` vs binary standalone
- Performance: não é C++/Rust/Go para CPU-intensive
- GIL: limita concorrência CPU-bound (mitigado com subprocess/threadpool/C++ engine)
- Tipo: tipagem gradual vs estática (mitigado com mypy/pyright)

## Próximos Passos

1. Definir framework CLI (Click/Typer/Rich/Custom) → ADR separado
2. Definir protocolo Python ↔ C++ → ADR 004
3. Estruturar projeto para isolar engine C++ futura