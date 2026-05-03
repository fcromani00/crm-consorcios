import streamlit as st
from datetime import date
from core.auth import check_password
from core.parcelas import listar, criar, marcar_pago, sincronizar_atrasados
from core.cotas import listar as listar_cotas, TIPO_LABELS

if not check_password():
    st.stop()

st.title("Parcelas")

sincronizar_atrasados()


@st.dialog("Nova Parcela")
def modal_parcela():
    cotas = listar_cotas(status="ativa")
    if not cotas:
        st.warning("Nenhuma cota ativa encontrada.")
        return

    opcoes = {
        c["id"]: f"{TIPO_LABELS.get(c['tipo'], c['tipo'])} — Cota {c.get('numero_cota') or 'S/N'} — Grupo {c.get('grupo') or '—'}"
        for c in cotas
    }
    id_cota = st.selectbox("Cota", options=list(opcoes.keys()), format_func=lambda x: opcoes[x])

    col1, col2 = st.columns(2)
    numero    = col1.number_input("Nº da parcela", min_value=1, step=1)
    valor     = col2.number_input("Valor (R$)", min_value=0.01, step=100.0)
    vencimento = st.date_input("Vencimento", value=date.today())

    if st.button("Salvar", type="primary", use_container_width=True):
        criar({
            "id_cota": id_cota,
            "numero": int(numero),
            "valor": float(valor),
            "vencimento": vencimento.isoformat(),
        })
        st.rerun()


def render_lista(parcelas: list, pode_pagar: bool = False):
    if not parcelas:
        st.info("Nenhuma parcela.")
        return

    h1, h2, h3, h4 = st.columns([3, 2, 2, 2])
    h1.caption("Cliente / Cota")
    h2.caption("Nº Parcela")
    h3.caption("Valor")
    h4.caption("Vencimento" if not pode_pagar else "Vencimento / Ação")

    for p in parcelas:
        cota_info    = p.get("cotas") or {}
        contato_info = cota_info.get("contatos") or {}

        r1, r2, r3, r4 = st.columns([3, 2, 2, 2])
        r1.write(
            f"{contato_info.get('nome', '—')}  \n"
            f"`{cota_info.get('numero_cota') or '—'}`"
        )
        r2.write(f"#{p['numero']}")
        r3.write(f"R$ {float(p['valor']):,.2f}")

        if pode_pagar:
            with r4:
                b1, b2 = st.columns(2)
                b1.write(str(p["vencimento"]))
                if b2.button("Pago", key=f"pg_{p['id']}", use_container_width=True):
                    marcar_pago(p["id"])
                    st.rerun()
        else:
            r4.write(f"{p['vencimento']}  \n`{p.get('pago_em') or ''}`")


# --- Tabs ---
tab_pend, tab_atras, tab_pago = st.tabs(["Pendentes", "Atrasadas", "Pagas"])

with tab_pend:
    t1, t2 = st.columns([4, 1])
    t1.subheader("Parcelas Pendentes")
    if t2.button("+ Parcela", type="primary", use_container_width=True):
        modal_parcela()
    render_lista(listar(status="pendente"), pode_pagar=True)

with tab_atras:
    st.subheader("Parcelas Atrasadas")
    render_lista(listar(status="atrasado"), pode_pagar=True)

with tab_pago:
    st.subheader("Parcelas Pagas")
    render_lista(listar(status="pago"), pode_pagar=False)
