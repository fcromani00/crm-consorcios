# CRM Consórcios

## Contexto
CRM para gestão de consórcios de pequeno porte. Controla leads, clientes, cotas e parcelas.
Desenvolvido para uso interno por operadores da empresa (admin + vendedores).

## Stack
- Linguagem: Python 3.11+
- Frontend: Streamlit (multi-page app)
- Banco de dados: Supabase (PostgreSQL)
- Auth: Streamlit session_state + tabela `usuarios` no Supabase
- Futuro: Integração WhatsApp (a definir: Z-API ou Evolution API)

## Entidades principais
- **contatos**: leads e clientes (diferenciados por status)
- **cotas**: cotas de consórcio vinculadas a um contato (tipo: imovel | veiculo | outros)
- **parcelas**: prestações mensais vinculadas a uma cota

## Funil de status (contatos)
novo_lead → contactado → em_negociacao → proposta_enviada → cliente_ativo → contemplado → encerrado

## Arquitetura
```
/core/
  supabase_client.py   # cliente singleton do Supabase
  auth.py              # check_password, sidebar_usuario, logout (padrão NutriV3)
  contatos.py          # CRUD contatos
  cotas.py             # CRUD cotas
  parcelas.py          # CRUD parcelas
/pages/
  0_Dashboard.py
  1_Funil_de_Leads.py
  2_Clientes.py
  3_Parcelas.py
  4_Relatorios.py
app.py                 # ponto de entrada Streamlit
.env                   # SUPABASE_URL, SUPABASE_KEY
requirements.txt
```

## Convenções
- Naming: snake_case para variáveis e funções, PascalCase para classes
- Idioma do código: inglês
- Commits: inglês
- Respostas/comentários: português (pt-BR)
- Toda página protegida deve chamar `check_password()` e `st.stop()` se não autenticado

## Auth
Padrão herdado do NutriV3 (`core/auth.py`):
- `check_password()` → verifica `st.session_state.autenticado`
- `sidebar_usuario()` → exibe nome do usuário e botão de logout
- Tabela `usuarios` no Supabase com campos: id, nome, email, senha (hash bcrypt)

## Regras
- Sempre usar `supabase_client.py` para acessar o banco, nunca instanciar o cliente direto nas páginas
- Senhas devem usar hash (bcrypt) — não armazenar plain text
- Tipo de consórcio é enum: `imovel`, `veiculo`, `outros`
- Integração WhatsApp será via API externa (a definir: Z-API ou Evolution API)

## Comandos úteis
```bash
streamlit run app.py        # rodar local
pip install -r requirements.txt
```
