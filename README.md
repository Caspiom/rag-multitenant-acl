# rag-multitenant-acl

> **Pilar do portfólio — Domingo** · parte de uma série de 7 projetos de Engenharia de Software de IA (1h/dia).

## O problema
Chatbot RAG com **isolamento por identidade/ACL**: o retrieval só devolve chunks que o usuário pode ver. Cada chunk carrega `tenant_id` + `acl_principals` + `sensitivity` como campos de primeira classe. É raro em portfólios e é o que separa um RAG de demo de um RAG que uma empresa pode usar.

## Regra central (uma só, num único arquivo — `src/acl.py`)
```
chunk visível  <=>  mesmo tenant  E  (acl_principals ∩ principals do usuário) ≠ ∅
```
- **Isolamento duro de tenant** antes de olhar a ACL (`role:public` não cruza tenant).
- **Default-deny:** ACL vazia = ninguém (não "público"). Esquecer de marcar um documento não o vaza.
- **Trimming ANTES do ranking** (`src/retriever.py`): filtrar depois vaza por canal lateral (score, contagem, top-k preenchido com itens proibidos). Em produção vira filtro de metadados no pgvector (`WHERE tenant_id = $1 AND acl_principals && $2`).

## Resultados medidos
| Verificação | Resultado |
|---|---|
| Testes de segurança | **8 passando** |
| Eval de isolamento (4 usuários × 6 consultas = 24 pares) | **0 vazamentos**, recall dos permitidos **1,0** |
| Mutation testing (quebrei a regra de propósito) | **2 de 2** mutações de comportamento detectadas (31 e 14 vazamentos no eval; 3 testes falham em cada) |

**Sobre o eval:** o gabarito é uma **tabela escrita à mão** (quem pode ver o quê), *não* chama `can_read`. Na primeira versão o oráculo reusava o código sob teste e **passava mesmo com o check de tenant removido** (0 vazamentos) — um oráculo que usa o código que testa nunca discorda dele. Foi corrigido e validado com mutação.

**Mutante equivalente (registrado por honestidade):** remover o `if not acl: return False` não muda o comportamento em nenhuma das 24 combinações (conjunto vazio ∩ qualquer coisa = vazio). Fica como defesa em profundidade/documentação da intenção; nenhum teste consegue distingui-lo.

## Stack
Python (stdlib) · retriever lexical TF-IDF simples · pytest. **Sem dependência de modelo/chave/rede** (corpus 100% sintético e fictício, 2 tenants). Alvo de produção: pgvector com filtro de metadados + auth hexagonal + FastAPI.

## Como rodar (< 5 min)
```bash
make setup     # cria .venv e instala pytest
make all       # testes + eval de isolamento (exit 1 se houver vazamento)
```

## Estrutura
- `src/models.py` — `Chunk` (tenant_id/acl_principals/sensitivity) e `Principal`
- `src/acl.py` — a regra de visibilidade
- `src/retriever.py` — retrieval com trimming antes do ranking
- `src/corpus.py` — corpus sintético (2 tenants) e usuários de teste
- `tests/test_acl.py` — testes de vazamento · `evals/isolamento.py` — eval com oráculo independente

## Status
- [x] Esqueleto / setup roda em < 15 min
- [x] Núcleo funcional (happy path)
- [x] Avaliação / métricas medidas (vazamentos, recall, mutation testing)
- [x] README com números
- [ ] pgvector com filtro de metadados (hoje retriever em memória)
- [ ] API FastAPI + auth (JWT → Principal) + camada de geração
- [ ] Deploy / demo reproduzível

---
Autor: Gappy · Série montada com apoio do Hermes
