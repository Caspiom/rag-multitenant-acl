"""Eval de isolamento com ORACULO INDEPENDENTE.

O gabarito NÃO usa `can_read`: é uma tabela escrita à mão de quem pode ver o quê.
Assim, se alguém quebrar a regra de ACL, o retriever e o gabarito discordam e o
eval reprova (um oráculo que reusa o código sob teste nunca discorda dele).

Métricas: vazamentos (gate: deve ser 0) e recall dos chunks permitidos.
Uso: python -m evals.isolamento"""
import json

from src.corpus import (ANA_RH_ACME, BRUNO_DIR_ACME, CAIO_ACME, CHUNKS,
                        DORA_DIR_BETA)
from src.retriever import Retriever

# Gabarito manual: usuário -> chunks que ele PODE ver (c05 = ACL vazia: ninguém).
PODE_VER = {
    "ana": {"c01", "c03", "c04"},
    "bruno": {"c01", "c02", "c03", "c04"},
    "caio": {"c01", "c04"},
    "dora": {"c06", "c07", "c08"},
}
USERS = {"ana": ANA_RH_ACME, "bruno": BRUNO_DIR_ACME, "caio": CAIO_ACME, "dora": DORA_DIR_BETA}
# Consultas que casam lexicalmente com TODOS os chunks, inclusive os proibidos.
QUERIES = ["salario diretor financeiro tabela diretoria", "dias de ferias por ano funcionarios",
           "senha da VPN redefinir", "plano de RH reajuste salarial bonus",
           "demissao em massa planejada rascunho", "salarios ferias VPN RH demissao"]

R = Retriever(CHUNKS)
todos = {c.chunk_id for c in CHUNKS}
vazamentos = pares = 0
detalhes = []
for uname, who in USERS.items():
    proibidos = todos - PODE_VER[uname]
    for q in QUERIES:
        pares += 1
        got = {c.chunk_id for c, _ in R.search(q, who, k=len(CHUNKS))}
        vaz = got & proibidos
        vazamentos += len(vaz)
        if vaz:
            detalhes.append({"user": uname, "query": q, "vazou": sorted(vaz)})

# recall: pra cada usuário, a união das consultas deve alcançar tudo que ele pode ver
rec_ok = rec_tot = 0
for uname, who in USERS.items():
    alcancados = set()
    for q in QUERIES:
        alcancados |= {c.chunk_id for c, _ in R.search(q, who, k=len(CHUNKS))}
    rec_tot += len(PODE_VER[uname])
    rec_ok += len(alcancados & PODE_VER[uname])

out = {"pares_usuario_consulta": pares, "vazamentos": vazamentos,
       "recall_permitidos": round(rec_ok / rec_tot, 3), "detalhes": detalhes}
print(json.dumps(out, indent=2, ensure_ascii=False))
raise SystemExit(1 if vazamentos else 0)  # gate: qualquer vazamento reprova
