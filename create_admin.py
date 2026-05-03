"""
Rode uma vez para criar o primeiro usuário admin:
    python create_admin.py
"""
import bcrypt
from dotenv import load_dotenv
from core.supabase_client import get_client

load_dotenv()

print("=== Criar Usuário Admin ===")
nome = input("Nome: ")
email = input("Email: ")
senha = input("Senha: ")

senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

result = get_client().table("usuarios").insert({
    "nome": nome,
    "email": email,
    "senha_hash": senha_hash,
    "perfil": "admin",
}).execute()

print(f"\nUsuário criado: {result.data[0]['email']}")
