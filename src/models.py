"""Modelo de dados do RAG multi-tenant: chunk com tenant_id + acl_principals,
e a identidade (Principal) de quem consulta. Esses dois campos são first-class:
toda a segurança do retrieval depende deles."""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Principal:
    """Quem está consultando. `principals` = usuário + grupos/papéis dele."""
    user_id: str
    tenant_id: str
    principals: frozenset[str] = field(default_factory=frozenset)

    @staticmethod
    def of(user_id: str, tenant_id: str, *groups: str) -> "Principal":
        return Principal(user_id, tenant_id, frozenset({f"user:{user_id}", *groups}))


@dataclass(frozen=True)
class Chunk:
    """Trecho indexado. `acl_principals` vazio => NEGA (default seguro)."""
    chunk_id: str
    tenant_id: str
    doc: str
    text: str
    acl_principals: frozenset[str] = field(default_factory=frozenset)
    sensitivity: str = "interno"  # publico | interno | confidencial
