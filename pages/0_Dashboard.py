import streamlit as st
import pandas as pd
import plotly.express as px
from core.auth import check_password
from core.supabase_client import get_client
from core.contatos import STATUS_LABELS

if not check_password():
    st.stop()

st.title("Dashboard")

client = get_client()

contatos  = client.table("contatos").select("status, criado_em").execute().data or []
cotas     = client.table("cotas").select("tipo, status").execute().data or []
parcelas  = client.table("parcelas").select("status, vencimento").execute().data or []

# --- Métricas ---
leads_ativos   = sum(1 for c in contatos if c["status"] not in ("cliente_ativo", "contemplado", "encerrado"))
clientes       = sum(1 for c in contatos if c["status"] in ("cliente_ativo", "contemplado"))
cotas_ativas   = sum(1 for c in cotas if c["status"] == "ativa")
atrasadas      = sum(1 for p in parcelas if p["status"] == "atrasado")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Leads Ativos", leads_ativos)
m2.metric("Clientes", clientes)
m3.metric("Cotas Ativas", cotas_ativas)
m4.metric("Parcelas Atrasadas", atrasadas, delta=f"+{atrasadas}" if atrasadas else None, delta_color="inverse")

st.divider()

# --- Gráficos ---
g1, g2 = st.columns(2)

with g1:
    st.subheader("Contatos por status")
    if contatos:
        df = pd.DataFrame(contatos)
        cnt = df["status"].value_counts().reset_index()
        cnt.columns = ["status", "total"]
        cnt["label"] = cnt["status"].map(STATUS_LABELS)
        fig = px.bar(cnt, x="label", y="total", color="label",
                     labels={"label": "", "total": "Qtd"})
        fig.update_layout(showlegend=False, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Sem dados.")

with g2:
    st.subheader("Cotas por tipo")
    if cotas:
        tipo_labels = {"imovel": "Imóvel", "veiculo": "Veículo", "outros": "Outros"}
        df_c = pd.DataFrame(cotas)
        df_c["tipo_label"] = df_c["tipo"].map(tipo_labels)
        cnt_tipo = df_c["tipo_label"].value_counts().reset_index()
        cnt_tipo.columns = ["tipo", "total"]
        fig2 = px.pie(cnt_tipo, names="tipo", values="total", hole=0.45)
        fig2.update_layout(margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Sem dados.")

# --- Últimos contatos ---
st.divider()
st.subheader("Últimos contatos adicionados")

ultimos = (
    client.table("contatos")
    .select("nome, telefone, status, criado_em")
    .order("criado_em", desc=True)
    .limit(8)
    .execute()
    .data or []
)

if ultimos:
    df_ult = pd.DataFrame(ultimos)
    df_ult["status"] = df_ult["status"].map(STATUS_LABELS)
    df_ult["criado_em"] = pd.to_datetime(df_ult["criado_em"]).dt.strftime("%d/%m/%Y")
    df_ult.columns = ["Nome", "Telefone", "Status", "Adicionado em"]
    st.dataframe(df_ult, use_container_width=True, hide_index=True)
else:
    st.info("Nenhum contato ainda.")
