# Research: Python CLI Framework Comparison

**Status:** IN PROGRESS  
**Objetivo:** Decidir framework para Coffee CLI V1 (ADR 003)  
**Critérios:** Produtividade, ergonomia, performance, ecossistema, manutenibilidade

---

## Candidatos

### Click
- **Maturidade:** Muito alta (Pallets, Flask usa)
- **API:** Decorator-based, declarativo
- **Features:** Subcommands, groups, callbacks, types, validation, help auto
- **Rich integration:** Via `rich_click` ou manual
- **Performance:** Boa, startup ~50-100ms
- **Learning curve:** Baixa
- **Extensibilidade:** Boa (custom types, parameter sources)

### Typer
- **Base:** Built on Click + type hints
- **API:** Type hints + docstrings = CLI automático
- **Features:** Modern Python (3.7+), async support, shells completion
- **Rich integration:** Nativa (usa Rich para help/errors)
- **Performance:** Similar a Click
- **Learning curve:** Muito baixa se conhece type hints
- **Limitações:** Menos flexível que Click puro para casos complexos

### Rich (CLI + TUI)
- **Rich CLI:** `rich-cli` package para CLI simples
- **Rich TUI:** `Textual` para apps terminais interativas
- **Não é framework CLI completo** — foco em output/formatting
- **Pode combinar:** Click/Typer + Rich para output

### Custom (argparse + Rich)
- **Controle total**
- **Boilerplate alto**
- **Reinventar roda:** help, completion, validation, subcommands
- **Só justificável se necessidades muito específicas**

### Cliff / Cement / Cleo / Fire / Plac / Cyclopts
- **Menos adotados, comunidade menor**
- **Avaliar só se Click/Typer falharem em requisito crítico**

---

## Comparação Prática (TODO: testar)

| Critério | Click | Typer | Click+Rich | Custom |
|---|---|---|---|---|
| Type hints first | ❌ | ✅ | ❌ | Manual |
| Rich output nativo | Via `rich_click` | ✅ | ✅ | Manual |
| Async commands | Limitado | ✅ | Limitado | Manual |
| Shell completion | ✅ | ✅ | ✅ | Manual |
| Subcommands/groups | ✅ | ✅ | ✅ | Manual |
| Validation/coercion | ✅ | ✅ (pydantic-like) | ✅ | Manual |
| Plugin/extensibility | ✅ | Média | ✅ | Total |
| Startup time | ~60ms | ~70ms | ~80ms | ~40ms |
| Comunidade/docs | Excelente | Boa | Boa | N/A |
| Curva aprendizado | Baixa | Muito baixa | Baixa | Alta |

---

## Requisitos Coffee CLI

- [ ] Subcommands hierárquicos (`coffee task add`, `coffee git status`)
- [ ] Type hints para validação automática
- [ ] Rich output (tabelas, progress, trees, syntax highlight)
- [ ] Async command support
- [ ] Shell completion (bash, zsh, fish, powershell)
- [ ] Config file integration (TOML)
- [ ] Plugin command registration dinâmico
- [ ] Help customizado / branding
- [ ] Exit codes estruturados
- [ ] Testabilidade (invocar commands em testes)

---

## Experimentos Planejados

1. **Spike Click + Rich:** Implementar `coffee task add/list` com Rich tables
2. **Spike Typer:** Mesmo escopo, comparar boilerplate e ergonomia
3. **Benchmark startup:** `time coffee --help` frio/quente
4. **Teste plugin registration:** Como registrar commands dinamicamente
5. **Teste config integration:** Carregar TOML e passar para commands

---

## Decisão Pendente

**Próximo passo:** Rodar spikes (1-2h cada) e documentar findings aqui.