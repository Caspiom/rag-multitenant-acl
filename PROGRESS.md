# PROGRESSO — rag-multitenant-acl

Último ponto onde parei (atualize ao fim de cada sessão de 1h):

- **Data:** 2026-11-02 (bloco de DOMINGO 01/11 feito pelo Hermes a pedido do Lucas)
- **Onde parei:** núcleo de security trimming pronto — `Chunk`/`Principal`, regra única em `acl.py` (tenant duro + default-deny + trimming antes do ranking), retriever lexical, corpus sintético (2 tenants). 8 testes de vazamento passando; eval de isolamento com oráculo independente: 24 pares, 0 vazamentos, recall 1,0. Mutation testing: 2/2 mutações de comportamento detectadas (1 mutante equivalente documentado no README).
- **Próximo passo:** (1) trocar o retriever em memória por pgvector com filtro de metadados (`tenant_id = $1 AND acl_principals && $2`) e repetir o eval nele; (2) API FastAPI com auth JWT → `Principal`; (3) camada de geração + teste de que o LLM nunca recebe chunk proibido no prompt.
