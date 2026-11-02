"""Retriever lexical (TF simples) com security trimming ANTES do ranking.

Ponto-chave de design: o filtro de ACL roda ANTES de pontuar/ordenar, não depois.
Filtrar depois pode vazar por canal lateral (contagem, score, top-k preenchido
com itens proibidos). Em produção isso vira filtro de metadados no pgvector
(WHERE tenant_id = $1 AND acl_principals && $2) — aqui o contrato é o mesmo."""
from __future__ import annotations
import math
import re
import unicodedata
from collections import Counter

from .acl import can_read
from .models import Chunk, Principal


def _tok(s: str) -> list[str]:
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.findall(r"[a-z0-9]+", s)


class Retriever:
    def __init__(self, chunks: list[Chunk]):
        self.chunks = chunks
        self._tf = {c.chunk_id: Counter(_tok(c.text)) for c in chunks}
        df: Counter = Counter()
        for tf in self._tf.values():
            df.update(tf.keys())
        n = len(chunks) or 1
        self._idf = {t: math.log(1 + n / d) for t, d in df.items()}

    def _score(self, q: list[str], c: Chunk) -> float:
        tf = self._tf[c.chunk_id]
        return sum(tf[t] * self._idf.get(t, 0.0) for t in q)

    def search(self, query: str, who: Principal, k: int = 3) -> list[tuple[Chunk, float]]:
        visiveis = [c for c in self.chunks if can_read(c, who)]  # trimming PRIMEIRO
        q = _tok(query)
        ranked = sorted(((c, self._score(q, c)) for c in visiveis), key=lambda x: -x[1])
        return [(c, s) for c, s in ranked[:k] if s > 0]
