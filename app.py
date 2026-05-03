import streamlit as st

st.set_page_config(
    page_title="CRM Consórcios",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Páginas privadas (requerem login)
dashboard  = st.Page("views/0_Dashboard.py",        title="Dashboard",      icon="📊")
funil      = st.Page("views/1_Funil_de_Leads.py",   title="Funil de Leads", icon="🔄")
clientes   = st.Page("views/2_Clientes.py",         title="Clientes",       icon="👥")
parcelas   = st.Page("views/3_Parcelas.py",         title="Parcelas",       icon="💰")
relatorios = st.Page("views/4_Relatorios.py",       title="Relatórios",     icon="📈")

# Página pública — sem login
captacao = st.Page("views/Formulario_Lead.py", title="Captação de Lead", url_path="captacao")

pg = st.navigation(
    [dashboard, funil, clientes, parcelas, relatorios, captacao],
    position="hidden",
)

if pg == captacao:
    pg.run()
else:
    from core.auth import check_password, sidebar_usuario

    if not check_password():
        st.stop()

    with st.sidebar:
        st.page_link(dashboard,  label="📊 Dashboard")
        st.page_link(funil,      label="🔄 Funil de Leads")
        st.page_link(clientes,   label="👥 Clientes")
        st.page_link(parcelas,   label="💰 Parcelas")
        st.page_link(relatorios, label="📈 Relatórios")
        st.divider()
        sidebar_usuario()

    pg.run()
