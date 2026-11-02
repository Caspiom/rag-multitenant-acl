"""Corpus SINTÉTICO (fictício) com 2 tenants e ACLs variadas.
Nenhum dado real da GaspariTec ou de cliente — só para demonstrar o isolamento."""
from __future__ import annotations
from .models import Chunk, Principal

A, B = "tenant-acme", "tenant-beta"


def _c(i, tenant, doc, text, acl, sens="interno"):
    return Chunk(f"c{i:02d}", tenant, doc, text, frozenset(acl), sens)


CHUNKS = [
    # --- tenant ACME ---
    _c(1, A, "politica-ferias.pdf", "Funcionarios da Acme tem 30 dias de ferias por ano, parcelaveis em ate tres periodos.", ["role:public"], "publico"),
    _c(2, A, "salarios-diretoria.xlsx", "Tabela de salarios da diretoria da Acme: salario do diretor financeiro e 45 mil reais.", ["group:diretoria"], "confidencial"),
    _c(3, A, "plano-rh-2026.docx", "Plano de RH da Acme para 2026: reajuste salarial de 6 por cento e programa de bonus.", ["group:rh", "group:diretoria"], "confidencial"),
    _c(4, A, "manual-ti.pdf", "Para redefinir a senha da VPN da Acme abra um chamado no portal de TI.", ["group:acme-todos"], "interno"),
    _c(5, A, "rascunho-sem-acl.txt", "Rascunho: demissao em massa planejada na Acme para o proximo trimestre.", [], "confidencial"),  # ACL vazia => ninguem
    # --- tenant BETA ---
    _c(6, B, "politica-ferias.pdf", "Funcionarios da Beta tem 20 dias de ferias por ano, sem parcelamento.", ["role:public"], "publico"),
    _c(7, B, "salarios-diretoria.xlsx", "Tabela de salarios da diretoria da Beta: salario do diretor financeiro e 80 mil reais.", ["group:diretoria"], "confidencial"),
    _c(8, B, "manual-ti.pdf", "Para redefinir a senha da VPN da Beta use o autoatendimento em beta.example/vpn.", ["group:beta-todos"], "interno"),
]

# Usuários de teste
ANA_RH_ACME = Principal.of("ana", A, "group:rh", "group:acme-todos")
BRUNO_DIR_ACME = Principal.of("bruno", A, "group:diretoria", "group:acme-todos")
CAIO_ACME = Principal.of("caio", A, "group:acme-todos")          # funcionário comum
DORA_DIR_BETA = Principal.of("dora", B, "group:diretoria", "group:beta-todos")
