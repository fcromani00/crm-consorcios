import streamlit as st
from core.auth import check_password
from core.contatos import listar as listar_contatos
from core.cotas import (
    listar as listar_cotas,
    criar as criar_cota,
    atualizar as atualizar_cota,
    TIPOS, TIPO_LABELS,
    STATUS_LIST as STATUS_COTA,
    STATUS_LABELS as COTA_STATUS_LABELS,
)

if not check_password():
    st.stop()

st.title("Clientes")

STATUSES_CLIENTE = ["cliente_ativo", "contemplado", "encerrado"]
todos = []
for s in STATUSES_CLIENTE:
    todos.extend(listar_contatos(status=s))

if not todos:
    st.info("Nenhum cliente ainda. Avance um lead para 'Cliente Ativo' no Funil de Leads.")
    st.stop()

nomes = {c["id"]: c["nome"] for c in todos}
cliente_id = st.selectbox("Selecionar cliente", options=list(nomes.keys()), format_func=lambda x: nomes[x])
cliente = next(c for c in todos if c["id"] == cliente_id)


@st.dialog("Cota")
def modal_cota():
    c = st.session_state.get("_cota_form") or {}
    is_edit = bool(c.get("id"))

    tipo_idx = TIPOS.index(c["tipo"]) if c.get("tipo") in TIPOS else 0
    tipo = st.selectbox("Tipo *", TIPOS, format_func=lambda x: TIPO_LABELS[x], index=tipo_idx)

    col1, col2 = st.columns(2)
    numero_cota = col1.text_input("Número da Cota", value=c.get("numero_cota", "") or "")
    grupo       = col2.text_input("Grupo", value=c.get("grupo", "") or "")

    col3, col4 = st.columns(2)
    valor_credito = col3.number_input("Crédito (R$)", min_value=0.0, step=1000.0,
                                      value=float(c.get("valor_credito") or 0))
    valor_parcela = col4.number_input("Parcela (R$)", min_value=0.0, step=100.0,
                                      value=float(c.get("valor_parcela") or 0))

    col5, col6 = st.columns(2)
    total_parcelas = col5.number_input("Total de parcelas", min_value=1, max_value=300,
                                       value=int(c.get("total_parcelas") or 60))
    data_adesao = col6.date_input("Data de adesão", value=None)

    status_idx = STATUS_COTA.index(c["status"]) if c.get("status") in STATUS_COTA else 0
    status = st.selectbox("Status", STATUS_COTA, format_func=lambda x: COTA_STATUS_LABELS[x], index=status_idx)
    observacoes = st.text_area("Observações", value=c.get("observacoes", "") or "")

    b1, b2 = st.columns(2)
    if b1.button("Salvar", type="primary", use_container_width=True):
        dados = {
            "id_contato": cliente_id,
            "tipo": tipo,
            "numero_cota": numero_cota.strip() or None,
            "grupo": grupo.strip() or None,
            "valor_credito": valor_credito or None,
            "valor_parcela": valor_parcela or None,
            "total_parcelas": total_parcelas,
            "data_adesao": data_adesao.isoformat() if data_adesao else None,
            "status": status,
            "observacoes": observacoes.strip() or None,
        }
        if is_edit:
            atualizar_cota(c["id"], dados)
        else:
            criar_cota(dados)
        st.session_state.pop("_cota_form", None)
        st.rerun()

    if b2.button("Cancelar", use_container_width=True):
        st.session_state.pop("_cota_form", None)
        st.rerun()


# --- Info do cliente ---
with st.expander("Dados do cliente"):
    i1, i2 = st.columns(2)
    i1.write(f"**Telefone:** {cliente.get('telefone') or '—'}")
    i1.write(f"**Email:** {cliente.get('email') or '—'}")
    i2.write(f"**CPF:** {cliente.get('cpf') or '—'}")
    i2.write(f"**Origem:** {cliente.get('origem') or '—'}")

st.divider()

# --- Cotas ---
c_title, c_btn = st.columns([4, 1])
c_title.subheader("Cotas")
if c_btn.button("+ Nova Cota", type="primary", use_container_width=True):
    st.session_state._cota_form = {}
    modal_cota()

cotas = listar_cotas(id_contato=cliente_id)

if not cotas:
    st.info("Este cliente ainda não tem cotas.")
else:
    for cota in cotas:
        with st.container(border=True):
            c1, c2, c3, c4, c5 = st.columns([2, 2, 2, 2, 1])

            tipo_label = TIPO_LABELS.get(cota["tipo"], cota["tipo"])
            c1.write(f"**{tipo_label}**  \nCota: `{cota.get('numero_cota') or '—'}`")
            c2.write(f"Grupo: {cota.get('grupo') or '—'}")

            credito  = f"R$ {cota['valor_credito']:,.2f}" if cota.get("valor_credito") else "—"
            parcela  = f"R$ {cota['valor_parcela']:,.2f}" if cota.get("valor_parcela") else "—"
            c3.write(f"Crédito: {credito}  \nParcela: {parcela}")

            status_label = COTA_STATUS_LABELS.get(cota["status"], cota["status"])
            c4.write(f"Status: **{status_label}**  \nParcelas: {cota.get('total_parcelas') or '—'}")

            if c5.button("Editar", key=f"ec_{cota['id']}", use_container_width=True):
                st.session_state._cota_form = cota
                modal_cota()
