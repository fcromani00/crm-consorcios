import bcrypt
import streamlit as st
from core.supabase_client import get_client


def check_password() -> bool:
    if st.session_state.get("autenticado", False):
        return True
    _login_form()
    if st.session_state.get("login_erro"):
        st.error("Email ou senha incorretos.")
    return False


def logout():
    keys = ["autenticado", "login_erro", "usuario_id", "usuario_nome", "usuario_perfil"]
    for k in keys:
        st.session_state.pop(k, None)
    st.rerun()


def sidebar_usuario():
    with st.sidebar:
        nome = st.session_state.get("usuario_nome", "Usuário")
        perfil = st.session_state.get("usuario_perfil", "")
        st.markdown(f"**{nome}**  \n`{perfil}`")
        st.divider()
        if st.button("Sair", use_container_width=True):
            logout()


# ── privado ──────────────────────────────────────────────────

def _login_form():
    col = st.columns([1, 2, 1])[1]
    with col:
        st.title("CRM Consórcios")
        with st.form("login"):
            email = st.text_input("Email")
            senha = st.text_input("Senha", type="password")
            submitted = st.form_submit_button("Entrar", use_container_width=True)
        if submitted:
            _verificar_credenciais(email, senha)


def _verificar_credenciais(email: str, senha: str):
    if not email or not senha:
        st.session_state.login_erro = True
        st.rerun()
        return

    try:
        resp = get_client().table("usuarios").select("*").eq("email", email).eq("ativo", True).single().execute()
        usuario = resp.data
    except Exception:
        st.session_state.login_erro = True
        st.rerun()
        return

    senha_hash = usuario.get("senha_hash", "").encode()
    if bcrypt.checkpw(senha.encode(), senha_hash):
        st.session_state.autenticado = True
        st.session_state.login_erro = False
        st.session_state.usuario_id = usuario["id"]
        st.session_state.usuario_nome = usuario["nome"]
        st.session_state.usuario_perfil = usuario["perfil"]
        st.rerun()
    else:
        st.session_state.login_erro = True
        st.rerun()
