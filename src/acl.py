"""Security trimming. Regra central, em UM lugar só (fácil de auditar):

    um chunk é visível  <=>  mesmo tenant  E  (acl ∩ principals do usuário) ≠ ∅

Default-deny: ACL vazia não é "público", é "ninguém". Isso evita o erro clássico
de esquecer de marcar um documento e ele vazar para todos."""
from __future__ import annotations
from .models import Chunk, Principal

PUBLIC = "role:public"  # principal curinga explícito (opt-in, nunca implícito)


def can_read(chunk: Chunk, who: Principal) -> bool:
    if chunk.tenant_id != who.tenant_id:
        return False  # isolamento duro entre tenants, antes de olhar ACL
    if not chunk.acl_principals:
        return False  # default-deny
    if PUBLIC in chunk.acl_principals:
        return True
    return bool(chunk.acl_principals & who.principals)
