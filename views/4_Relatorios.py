import streamlit as st
from core.auth import check_password

if not check_password():
    st.stop()

st.title("Relatórios")
st.info("Em construção.")
