"""Testes de segurança do retrieval. O foco é o que NÃO pode vazar."""
from src.acl import can_read
from src.corpus import (ANA_RH_ACME, BRUNO_DIR_ACME, CAIO_ACME, CHUNKS,
                        DORA_DIR_BETA)
from src.models import Chunk, Principal
from src.retriever import Retriever

R = Retriever(CHUNKS)


def ids(res):
    return {c.chunk_id for c, _ in res}


def test_funcionario_comum_nao_ve_salario_da_diretoria():
    assert "c02" not in ids(R.search("salario do diretor financeiro", CAIO_ACME, k=10))


def test_diretoria_ve_o_proprio_salario():
    assert "c02" in ids(R.search("salario do diretor financeiro", BRUNO_DIR_ACME))


def test_rh_ve_plano_de_rh_mas_nao_salario_da_diretoria():
    r = ids(R.search("salario reajuste bonus diretoria", ANA_RH_ACME, k=10))
    assert "c03" in r and "c02" not in r


def test_isolamento_entre_tenants_mesmo_com_cargo_igual():
    # Dora é diretoria da BETA: não pode ver NADA da ACME (nem o salario da diretoria ACME)
    r = R.search("salario do diretor financeiro", DORA_DIR_BETA, k=10)
    assert all(c.tenant_id == "tenant-beta" for c, _ in r)
    assert "c02" not in ids(r)


def test_acl_vazia_e_default_deny_para_todos():
    # A consulta casa de verdade com o texto do c05 (senão o teste passaria por acaso).
    from src.corpus import CHUNKS as ALL
    c05 = next(c for c in ALL if c.chunk_id == "c05")
    assert not c05.acl_principals  # premissa: ACL vazia
    for p in (ANA_RH_ACME, BRUNO_DIR_ACME, CAIO_ACME):
        assert can_read(c05, p) is False
        assert "c05" not in ids(R.search("demissao em massa planejada rascunho", p, k=10))


def test_publico_so_vale_dentro_do_proprio_tenant():
    c = next(c for c in CHUNKS if c.chunk_id == "c01")  # publico ACME
    assert can_read(c, CAIO_ACME) is True
    assert can_read(c, DORA_DIR_BETA) is False  # role:public NÃO cruza tenant


def test_principal_forjado_com_tenant_errado_nao_cruza():
    intruso = Principal.of("x", "tenant-beta", "group:diretoria", "group:acme-todos")
    assert all(c.tenant_id == "tenant-beta" for c, _ in R.search("ferias salario vpn", intruso, k=10))


def test_filtro_roda_antes_do_ranking_topk_nao_e_preenchido_com_proibidos():
    # k=1: se o filtro fosse depois, o top-1 seria o chunk proibido c02 e voltaria vazio.
    r = R.search("salario diretor financeiro", CAIO_ACME, k=1)
    assert "c02" not in ids(r)
