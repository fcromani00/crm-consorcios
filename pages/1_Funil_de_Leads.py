import streamlit as st
from core.auth import check_password
from core.contatos import (
    listar, criar, atualizar,
    FUNIL_STATUS, STATUS_LABELS, proximo_status,
)

if not check_password():
    st.stop()

st.title("Funil de Leads")


@st.dialog("Contato")
def modal_contato():
    c = st.session_state.get("_contato_form") or {}
    is_edit = bool(c.get("id"))

    nome        = st.text_input("Nome *", value=c.get("nome", ""))
    col1, col2  = st.columns(2)
    telefone    = col1.text_input("Telefone", value=c.get("telefone", "") or "")
    email_val   = col2.text_input("Email", value=c.get("email", "") or "")
    cpf         = col1.text_input("CPF", value=c.get("cpf", "") or "")
    origem      = col2.text_input("Origem (ex: Instagram, Indicação)", value=c.get("origem", "") or "")

    status_idx = FUNIL_STATUS.index(c["status"]) if c.get("status") in FUNIL_STATUS else 0
    status = st.selectbox("Status", FUNIL_STATUS, format_func=lambda x: STATUS_LABELS[x], index=status_idx)

    observacoes = st.text_area("Observações", value=c.get("observacoes", "") or "")

    b1, b2 = st.columns(2)
    salvar    = b1.button("Salvar", type="primary", use_container_width=True)
    cancelar  = b2.button("Cancelar", use_container_width=True)

    if salvar:
        if not nome.strip():
            st.error("Nome é obrigatório.")
        else:
            dados = {
                "nome": nome.strip(),
                "telefone": telefone.strip() or None,
                "email": email_val.strip() or None,
                "cpf": cpf.strip() or None,
                "status": status,
                "origem": origem.strip() or None,
                "observacoes": observacoes.strip() or None,
                "id_usuario_responsavel": st.session_state.get("usuario_id"),
            }
            if is_edit:
                atualizar(c["id"], dados)
            else:
                criar(dados)
            st.session_state.pop("_contato_form", None)
            st.rerun()

    if cancelar:
        st.session_state.pop("_contato_form", None)
        st.rerun()


# --- Contadores por status ---
contatos = listar()

cols = st.columns(len(FUNIL_STATUS))
for i, s in enumerate(FUNIL_STATUS):
    count = sum(1 for c in contatos if c["status"] == s)
    cols[i].metric(STATUS_LABELS[s], count)

st.divider()

# --- Filtros e botão novo ---
f1, f2, f3 = st.columns([2, 3, 2])

filtro_status = f1.selectbox(
    "Filtrar por status",
    ["Todos"] + FUNIL_STATUS,
    format_func=lambda x: "Todos" if x == "Todos" else STATUS_LABELS[x],
)
busca = f2.text_input("Buscar por nome ou telefone", placeholder="Digite para filtrar...")

if f3.button("+ Novo Lead", type="primary", use_container_width=True):
    st.session_state._contato_form = {}
    modal_contato()

# --- Aplicar filtros ---
exibir = contatos
if filtro_status != "Todos":
    exibir = [c for c in exibir if c["status"] == filtro_status]
if busca:
    bl = busca.lower()
    exibir = [
        c for c in exibir
        if bl in (c.get("nome") or "").lower()
        or bl in (c.get("telefone") or "").lower()
    ]

# --- Lista ---
if not exibir:
    st.info("Nenhum contato encontrado.")
else:
    h1, h2, h3, h4, h5 = st.columns([3, 2, 2, 2, 2])
    h1.caption("Nome")
    h2.caption("Telefone")
    h3.caption("Email")
    h4.caption("Status")
    h5.caption("Ações")

    for c in exibir:
        r1, r2, r3, r4, r5 = st.columns([3, 2, 2, 2, 2])
        r1.write(c["nome"])
        r2.write(c.get("telefone") or "—")
        r3.write(c.get("email") or "—")
        r4.write(STATUS_LABELS.get(c["status"], c["status"]))

        with r5:
            a1, a2 = st.columns(2)
            if a1.button("Editar", key=f"ed_{c['id']}", use_container_width=True):
                st.session_state._contato_form = c
                modal_contato()

            proximo = proximo_status(c["status"])
            if proximo:
                if a2.button(
                    "→",
                    key=f"av_{c['id']}",
                    help=f"Avançar para {STATUS_LABELS[proximo]}",
                    use_container_width=True,
                ):
                    atualizar(c["id"], {"status": proximo})
                    st.rerun()
