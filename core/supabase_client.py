import os
import streamlit as st
from supabase import create_client, Client

_client: Client | None = None


def get_client() -> Client:
    global _client
    if _client is None:
        # Streamlit Cloud (st.secrets) tem prioridade; .env serve como fallback local
        try:
            url = st.secrets["SUPABASE_URL"]
            key = st.secrets["SUPABASE_KEY"]
        except (KeyError, FileNotFoundError):
            from dotenv import load_dotenv
            load_dotenv()
            url = os.getenv("SUPABASE_URL")
            key = os.getenv("SUPABASE_KEY")

        if not url or not key:
            raise RuntimeError("SUPABASE_URL e SUPABASE_KEY não configurados.")
        _client = create_client(url, key)
    return _client
