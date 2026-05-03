import streamlit as st
from core.contatos import criar

TIPO_LABELS = {"imovel": "Imóvel", "veiculo": "Veículo", "outros": "Outros"}

# Tela de sucesso após envio
if st.session_state.get("_captacao_ok"):
    st.balloons()
    st.success("Recebemos seu cadastro! Nossa equipe entrará em contato em breve.")
    if st.button("Novo cadastro"):
        del st.session_state._captacao_ok
        st.rerun()
    st.stop()

# Layout centralizado
_, col, _ = st.columns([1, 2, 1])

with col:
    st.title("Tenho interesse em consórcio")
    st.write("Preencha o formulário e entraremos em contato.")
    st.divider()

    nome      = st.text_input("Nome completo *")
    c1, c2    = st.columns(2)
    telefone  = c1.text_input("Telefone / WhatsApp *")
    email     = c2.text_input("Email")
    tipo      = st.selectbox(
        "Tipo de consórcio de interesse",
        list(TIPO_LABELS.keys()),
        format_func=lambda x: TIPO_LABELS[x],
    )
    mensagem  = st.text_area(
        "Mensagem (opcional)",
        placeholder="Conte mais sobre o que você está buscando...",
    )

    if st.button("Quero ser contactado →", type="primary", use_container_width=True):
        erros = []
        if not nome.strip():
            erros.append("Nome é obrigatório.")
        if not telefone.strip():
            erros.append("Telefone é obrigatório.")

        if erros:
            for e in erros:
                st.error(e)
        else:
            criar({
                "nome": nome.strip(),
                "telefone": telefone.strip(),
                "email": email.strip() or None,
                "status": "novo_lead",
                "origem": f"formulario_web — {TIPO_LABELS[tipo]}",
                "observacoes": mensagem.strip() or None,
            })
            st.session_state._captacao_ok = True
            st.rerun()
