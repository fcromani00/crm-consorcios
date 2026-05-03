from core.supabase_client import get_client

TIPOS = ["imovel", "veiculo", "outros"]
TIPO_LABELS = {"imovel": "Imóvel", "veiculo": "Veículo", "outros": "Outros"}

STATUS_LIST = ["ativa", "contemplada", "cancelada", "encerrada"]
STATUS_LABELS = {
    "ativa": "Ativa",
    "contemplada": "Contemplada",
    "cancelada": "Cancelada",
    "encerrada": "Encerrada",
}


def listar(id_contato: str = None, status: str = None) -> list:
    q = get_client().table("cotas").select("*")
    if id_contato:
        q = q.eq("id_contato", id_contato)
    if status:
        q = q.eq("status", status)
    return q.order("criado_em", desc=True).execute().data or []


def listar_com_contatos() -> list:
    return (
        get_client()
        .table("cotas")
        .select("*, contatos(nome, telefone)")
        .order("criado_em", desc=True)
        .execute()
        .data or []
    )


def buscar(id: str) -> dict:
    return get_client().table("cotas").select("*").eq("id", id).single().execute().data


def criar(dados: dict) -> dict:
    return get_client().table("cotas").insert(dados).execute().data[0]


def atualizar(id: str, dados: dict) -> dict:
    return get_client().table("cotas").update(dados).eq("id", id).execute().data[0]
