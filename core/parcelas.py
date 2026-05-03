from datetime import date
from core.supabase_client import get_client

STATUS_LIST = ["pendente", "pago", "atrasado"]
STATUS_LABELS = {"pendente": "Pendente", "pago": "Pago", "atrasado": "Atrasado"}


def listar(id_cota: str = None, status: str = None) -> list:
    q = get_client().table("parcelas").select(
        "*, cotas(numero_cota, tipo, contatos(nome))"
    )
    if id_cota:
        q = q.eq("id_cota", id_cota)
    if status:
        q = q.eq("status", status)
    return q.order("vencimento").execute().data or []


def criar(dados: dict) -> dict:
    return get_client().table("parcelas").insert(dados).execute().data[0]


def criar_lote(lista: list) -> None:
    get_client().table("parcelas").insert(lista).execute()


def atualizar(id: str, dados: dict) -> dict:
    return get_client().table("parcelas").update(dados).eq("id", id).execute().data[0]


def marcar_pago(id: str) -> None:
    atualizar(id, {"status": "pago", "pago_em": date.today().isoformat()})


def sincronizar_atrasados() -> None:
    hoje = date.today().isoformat()
    (
        get_client()
        .table("parcelas")
        .update({"status": "atrasado"})
        .eq("status", "pendente")
        .lt("vencimento", hoje)
        .execute()
    )
