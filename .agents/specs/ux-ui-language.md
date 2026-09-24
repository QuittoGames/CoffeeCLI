---
description: Linguagem visual oficial e aprovada das TUIs do Coffee CLI — black + blue + transparent, terminal-native (nunca substituir o background do terminal), radius 8px como linguagem de forma, densidade compacta, motion discreto. Aprovada pelo DEV em 2026-09-23. Carregar em qualquer trabalho de UI/TUI do Coffee. UX detalhada (telas, fluxos, componentes, copy) é UNDEFINED e pertence ao DEV.
---

# Coffee CLI — UX / UI Language

**Status:** DECISION (linguagem visual geral — definida pelo DEV) · DECISION (aplicação detalhada — aprovada pelo DEV em 2026-09-23) · UNDEFINED (decisões pendentes do DEV)

**Especifica:** linguagem visual das TUIs do Coffee CLI

**Não especifica:** telas, fluxos, layouts, componentes, copy — UNDEFINED, decisão do DEV

**Fontes:** definição do DEV (2026-09-22) + Quitto UI System (harness global) + harness (.agents/harness.md §13-19, §29)

---

## 1. Filosofia [DECISION]

O Coffee CLI é uma ferramenta de desenvolvimento — não uma aplicação decorativa.

A interface transmite:

```text
BLUE        → identidade / foco / ação
BLACK       → contraste / estrutura
TRANSPARENT → integração com o terminal
8px         → linguagem de forma
FAST        → baixa fricção
MODERN      → hierarquia limpa
TECHNICAL   → informação acima de decoração
```

---

## 2. Identidade [DECISION]

Direção definida pelo DEV:

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

Motif Coffee faz parte da identidade — somado ao preto, azul e transparência.

---

## 3. Cores — papéis semânticos [DECISION]

A linguagem visual usa três elementos principais:

```text
Black
Blue
Transparent / terminal-native background
```

Papéis definidos:

```text
BLUE
→ accent
→ focus
→ active state
→ important information
→ primary interaction

BLACK
→ contraste
→ estrutura
→ quando o ambiente permitir

TRANSPARENT
→ integração com o terminal
→ a UI trabalha sobre o terminal existente
```

Regras:

```text
azul contrastante, mas não forçado
a interface inteira nunca vira azul
cores sem significado são proibidas
```

---

## 4. Background do terminal [DECISION]

```text
O terminal NUNCA tem seu background substituído pela aplicação.
```

O modelo é:

```text
Terminal background
        +
Coffee foreground/UI
```

A interface deve parecer integrada ao terminal.

---

## 5. Radius [DECISION]

```text
radius = 8px
```

8px é a referência geral do design system Coffee — a linguagem de forma.

Em TUI, quando o framework não oferece radius real:

```text
usar a representação terminal mais próxima
```

Não criar efeitos artificiais apenas para simular 8px.

[FACT] Terminais não renderizam radius — o token é linguagem visual; a representação TUI mais próxima são as bordas/frames de painel do framework.

---

## 6. Densidade [DECISION]

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

O Coffee deve parecer uma ferramenta de desenvolvimento moderna.

---

## 7. Motion / Feedback [DECISION]

Prioridade:

```text
velocidade
feedback imediato
transições discretas
automação
```

Nunca adicionar animação apenas por ornamentação.

O comportamento transmite:

```text
fast
responsive
alive
```

sem atrasar operações.

---

## 8. Quitto UI System — gosto global [DECISION]

O gosto global do DEV (harness global) é parte desta linguagem:

```text
dark-first
blue identity
8px radius
desktop-app aesthetic
```

Inspirações (definidas no Quitto UI System global):

```text
Windows 11 Fluent UI
GNOME Adwaitaa
VS Code
JetBrains IDEs
terminal tools
```

Regras UX globais aplicáveis (adaptadas a TUI):

```text
keyboard-first — foco visível e atalhos
estados claros — default, hover, active, focus, disabled, loading
sem gradientes decorativos — cor sólida ou token semântico
empty state = convite à ação, não ilustração decorativa
```

---

## 9. Mapeamento para TUI [DECISION — aprovado pelo DEV em 2026-09-23]

Aplicação dos papéis em TUI — aprovada pelo DEV:

```text
BLUE
→ item selecionado / foco de teclado
→ borda do painel ativo
→ labels de ação primária
→ valores e status importantes
→ cursor/caret e indicadores ativos

BLACK / dark surface
→ superfícies internas de componentes (painéis, modais) quando necessário
→ separadores estruturais
→ contraste de texto secundário (quando o terminal permitir)
→ sem nunca substituir o fundo geral do terminal (§4)

TRANSPARENT
→ área principal de listagem/texto
→ qualquer região onde o terminal deve aparecer
```

Papéis semânticos complementares (o Quitto UI System global já os define para GUI):

```text
success → confirmação, tarefa concluída
warning → atenção, degradação
danger  → erro, operação destrutiva
muted   → texto secundário, hints, placeholders
```

Referência de paleta (do Quitto UI System global — para terminais truecolor):

```text
blue-primary   #1E40AF
blue-secondary #3B82F6   → ação primária, links
blue-accent    #60A5FA   → hover, detalhes
blue-electric  #38BDF8   → highlights, status ativo
success        #22C55E
warning        #EAB308
error          #EF4444
muted          #6B7280
```

---

## 10. Comportamento cross-terminal [DECISION — aprovado pelo DEV em 2026-09-23]

[FACT] Terminais variam: 16 cores ANSI, 256 cores, truecolor — e backgrounds variam (escuros e claros).

Regra:

```text
respeitar o tema do terminal do usuário
preferir cores do tema ANSI quando o terminal não suportar truecolor
nunca forçar background próprio (§4 é DECISION)
em terminais claros: confiar nos papéis semânticos do tema, não em hexcodes fixos
```

---

## 11. Feedback TUI [DECISION — aprovado pelo DEV em 2026-09-23]

Feedback (dentro do motion §7):

```text
spinners discretos para operações em andamento
progress bars para operações mensuráveis
transições curtas — 100-300ms (referência do Quitto UI System global)
estados de loading sempre definidos
reduced-motion respeitado quando o framework suportar
```

---

## 12. Tipografia terminal [DECISION — aprovado pelo DEV em 2026-09-23]

[FACT] TUI não escolhe fontes — o terminal define a fonte.

Ponderação via estrutura de texto:

```text
títulos → destaque, espaçamento, hierarquia
corpo   → texto direto, densidade compacta
labels  → curtos, consistentes
colunas → alinhamento monospace nativo como vantagem
```

---

## 13. Motif Coffee [DECISION — aprovado pelo DEV em 2026-09-23]

O tema Coffee é identidade, não decoração.

Manifestações conceituais aprovadas (nenhuma tela foi inventada; telas específicas permanecem UNDEFINED):

```text
nome e identidade verbal — o assistente é "Coffee"
indicador de carregamento com forma de xícara (se o framework suportar)
copy com vocabulário de café, usado com parcimônia
sem arte ASCII decorativa em telas de trabalho
```

---

## 14. UNDEFINED — aguardando decisão do DEV

```text
framework de TUI / CLI (Rich? Textual? Custom?) — questão aberta do projeto
telas, fluxos e layouts específicos
componentes e hierarquia de telas
copy final e tom de voz
comandos de UI
paleta final hexcode para TUI
política final de tema claro/escuro
```

Nenhum destes deve ser preenchido por inferência.

---

## 15. Fontes desta spec

```text
1. Definição do DEV (mensagem original, 2026-09-22)       → DECISION
2. Quitto UI System (skill/harness global)                 → DECISION (gosto global)
3. Harness do projeto (.agents/harness.md §13-19, §29)     → DECISION
4. Mapeamento TUI, cross-terminal, feedback, motif         → DECISION (aprovado pelo DEV em 2026-09-23)
5. Limitações de terminal                                  → FACT
```
