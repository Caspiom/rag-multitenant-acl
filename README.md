# rag-multitenant-acl

> **Pilar do portfólio — Domingo** · parte de uma série de 7 projetos de Engenharia de Software de IA (1h/dia).

## O problema
Chatbot RAG com isolamento por identidade/ACL: retrieval respeita acl_principals/tenant_id por chunk. Raro em portfólios.

## Por que está no portfólio
RAG multi-tenant com security trimming por ACL. Recrutadores de IA em 2026 valorizam este pilar — e o diferencial é a **execução com avaliação medida**, não só a demo.

## Stack
Python · pgvector (filtro de metadados) · auth hexagonal · FastAPI

## Estrutura
- `src/` — código principal
- `tests/` — testes
- demais pastas conforme o pilar

## Status
- [ ] Esqueleto / setup roda em < 15 min
- [ ] Núcleo funcional (happy path)
- [ ] Avaliação / métricas medidas
- [ ] README com números (eval, latência, custo)
- [ ] Deploy / demo reproduzível

## Como rodar
_(a preencher — manter setup em < 15 min é regra de ouro)_

---
Autor: Gappy · Série montada com apoio do Hermes
