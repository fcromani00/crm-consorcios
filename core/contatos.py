from core.supabase_client import get_client

FUNIL_STATUS = [
    "novo_lead",
    "contactado",
    "em_negociacao",
    "proposta_enviada",
    "cliente_ativo",
    "contemplado",
    "encerrado",
]

STATUS_LABELS = {
    "novo_lead": "Novo Lead",
    "contactado": "Contactado",
    "em_negociacao": "Em Negociação",
    "proposta_enviada": "Proposta Enviada",
    "cliente_ativo": "Cliente Ativo",
    "contemplado": "Contemplado",
    "encerrado": "Encerrado",
}


def listar(status: str = None, busca: str = None) -> list:
    q = get_client().table("contatos").select(
        "id, nome, telefone, email, cpf, status, origem, observacoes, id_usuario_responsavel, criado_em"
    )
    if status:
        q = q.eq("status", status)
    dados = q.order("criado_em", desc=True).execute().data or []
    if busca:
        bl = busca.lower()
        dados = [
            c for c in dados
            if bl in (c.get("nome") or "").lower()
            or bl in (c.get("telefone") or "").lower()
        ]
    return dados


def buscar(id: str) -> dict:
    return get_client().table("contatos").select("*").eq("id", id).single().execute().data


def criar(dados: dict) -> dict:
    return get_client().table("contatos").insert(dados).execute().data[0]


def atualizar(id: str, dados: dict) -> dict:
    return get_client().table("contatos").update(dados).eq("id", id).execute().data[0]


def deletar(id: str):
    get_client().table("contatos").delete().eq("id", id).execute()


def proximo_status(status_atual: str) -> str | None:
    try:
        idx = FUNIL_STATUS.index(status_atual)
    except ValueError:
        return None
    if idx < len(FUNIL_STATUS) - 1:
        return FUNIL_STATUS[idx + 1]
    return None
