# ADR 004: C++ Engine Isolada + Protocolo Python ↔ C++

**Status:** PROPOSAL  
**Data:** 2026-09-22  
**Contexto:** `.agents/context/coffee-ecosystem-conversation-documentation.md` §12-13, ADR 003

## Contexto

C++ entra no ecossistema apenas quando houver responsabilidade concreta que justifique camada nativa (performance, integração sistema, hardware, low-level). Não deve ser espalhado pelo projeto Python.

## Decisão (Proposta)

### Isolamento Arquitetural

```
Coffee CLI (Python)
     │
     ▼
Native capability / Engine (processo separado)
     │
     ▼
C++
```

- C++ como **processo/helper separado**, comunicação via protocolo simples
- Python não conhece detalhes internos do C++ — apenas contrato de protocolo
- Permite substituir/ampliar implementação C++ sem espalhar dependências

### Protocolo (ABERTO — precisa decisão)

Opções:
1. **JSON sobre stdin/stdout** — Simples, debuggable, language-agnostic, overhead serialização
2. **gRPC/Protobuf** — Contrato forte, performance, codegen, mais complexo
3. **Named pipes / Unix domain sockets** — Baixa latência, Windows/Linux diferenças
4. **MessagePack/CBOR sobre stdin/stdout** — Binário, mais eficiente que JSON
5. **Cap'n Proto / FlatBuffers** — Zero-copy, schema evolution, mais complexo

### Responsabilidades Candidatas para C++ Engine

- [ ] System diagnostics/inspection (CPU, GPU, memory, kernel params)
- [ ] Process management avançado
- [ ] Filesystem operations de alta performance
- [ ] Network packet capture/analysis
- [ ] Hardware enumeration (PCI, USB, sensors)
- [ ] Secure Boot / UEFI / TPM operations
- [ ] SELinux policy compilation/load
- [ ] Container runtime operations (Podman/Docker low-level)
- [ ] Crypto operations (HSM, TPM, key derivation)

**Regra:** C++ só entra quando **necessidade concreta** demonstrada. Não antecipar.

## Consequências

**Positivas:**
- Python permanece simples e produtivo
- C++ isolado: mudanças não quebram Python
- Protocolo versionável independentemente
- Engine C++ reutilizável por outros clientes (Server, outros CLIs)
- Debugging: processos independentes, logs separados

**Negativas/Riscos:**
- Latência IPC (mitigado: batch operations, async)
- Complexidade: dois processos, deployment, health checks
- Serialização: definir schema, versioning, compatibilidade
- Distribuição: dois binários (ou Python + C++ bundled)

## Questões Abertas

- [ ] Protocolo definitivo (JSON/stdin-stdout? gRPC? MessagePack?)
- [ ] Nome da pasta: `engine/`, `native/`, `core/`? → ADR separado
- [ ] Build system C++ (CMake? Meson? Bazel?)
- [ ] Como distribuir: bundled no wheel Python? Separado?
- [ ] Health check / lifecycle do processo C++
- [ ] Error handling cross-boundary