import streamlit as st
import requests

# Endereço da API
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Sistema de Doações",
    page_icon="🤝",
    layout="wide"
)

st.title("🤝 Sistema de Doações para Abrigos Afetados pelas Chuvas")

st.write("""
Este sistema ajuda a organizar doações para abrigos, conectando doadores,
voluntários e famílias afetadas pelas chuvas.
""")

menu = st.sidebar.selectbox(
    "Escolha uma opção",
    [
        "Início",
        "Cadastrar Abrigo",
        "Cadastrar Doador",
        "Cadastrar Voluntário",
        "Cadastrar Necessidade",
        "Registrar Doação",
        "Listar Abrigos",
        "Listar Doadores",
        "Listar Voluntários",
        "Listar Necessidades",
        "Listar Doações"
    ]
)


# -------------------------
# FUNÇÕES AUXILIARES
# -------------------------

def buscar_abrigos():
    resposta = requests.get(f"{API_URL}/abrigos")
    if resposta.status_code == 200:
        return resposta.json()
    return []


def buscar_doadores():
    resposta = requests.get(f"{API_URL}/doadores")
    if resposta.status_code == 200:
        return resposta.json()
    return []


# -------------------------
# PÁGINA INICIAL
# -------------------------

if menu == "Início":
    st.header("Bem-vindo ao sistema!")

    st.info("""
    Use o menu lateral para cadastrar abrigos, doadores, voluntários,
    necessidades e doações.
    """)

    st.subheader("Objetivo do projeto")

    st.write("""
    O objetivo deste sistema é facilitar a comunicação entre quem deseja doar
    e os abrigos que precisam de ajuda. Com isso, evitamos desperdício,
    organizamos melhor os itens recebidos e garantimos que as doações cheguem
    com mais rapidez para quem realmente precisa.
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Foco", "Organização")

    with col2:
        st.metric("Impacto", "Solidariedade")

    with col3:
        st.metric("Resultado", "Ajuda rápida")


# -------------------------
# CADASTRAR ABRIGO
# -------------------------

elif menu == "Cadastrar Abrigo":
    st.header("Cadastrar Abrigo")

    nome = st.text_input("Nome do abrigo")
    endereco = st.text_input("Endereço")
    telefone = st.text_input("Telefone")
    responsavel = st.text_input("Responsável")

    if st.button("Cadastrar Abrigo"):
        dados = {
            "nome": nome,
            "endereco": endereco,
            "telefone": telefone,
            "responsavel": responsavel
        }

        resposta = requests.post(f"{API_URL}/abrigos", json=dados)

        if resposta.status_code == 200:
            st.success("Abrigo cadastrado com sucesso!")
        else:
            st.error("Erro ao cadastrar abrigo.")


# -------------------------
# CADASTRAR DOADOR
# -------------------------

elif menu == "Cadastrar Doador":
    st.header("Cadastrar Doador")

    nome = st.text_input("Nome do doador")
    telefone = st.text_input("Telefone")
    email = st.text_input("E-mail")

    if st.button("Cadastrar Doador"):
        dados = {
            "nome": nome,
            "telefone": telefone,
            "email": email
        }

        resposta = requests.post(f"{API_URL}/doadores", json=dados)

        if resposta.status_code == 200:
            st.success("Doador cadastrado com sucesso!")
        else:
            st.error("Erro ao cadastrar doador.")


# -------------------------
# CADASTRAR VOLUNTÁRIO
# -------------------------

elif menu == "Cadastrar Voluntário":
    st.header("Cadastrar Voluntário")

    nome = st.text_input("Nome do voluntário")
    telefone = st.text_input("Telefone")
    disponibilidade = st.selectbox(
        "Disponibilidade",
        [
            "Manhã",
            "Tarde",
            "Noite",
            "Fim de semana",
            "Qualquer horário"
        ]
    )

    if st.button("Cadastrar Voluntário"):
        dados = {
            "nome": nome,
            "telefone": telefone,
            "disponibilidade": disponibilidade
        }

        resposta = requests.post(f"{API_URL}/voluntarios", json=dados)

        if resposta.status_code == 200:
            st.success("Voluntário cadastrado com sucesso!")
        else:
            st.error("Erro ao cadastrar voluntário.")


# -------------------------
# CADASTRAR NECESSIDADE
# -------------------------

elif menu == "Cadastrar Necessidade":
    st.header("Cadastrar Necessidade do Abrigo")

    abrigos = buscar_abrigos()

    if len(abrigos) == 0:
        st.warning("Cadastre um abrigo antes de cadastrar necessidades.")
    else:
        nomes_abrigos = {}

        for abrigo in abrigos:
            texto = f"{abrigo['id']} - {abrigo['nome']}"
            nomes_abrigos[texto] = abrigo["id"]

        abrigo_escolhido = st.selectbox("Escolha o abrigo", list(nomes_abrigos.keys()))

        item = st.text_input("Item necessário")
        categoria = st.selectbox(
            "Categoria",
            [
                "Alimentos e Água",
                "Produtos de Higiene",
                "Roupas e Cobertores",
                "Materiais de Limpeza",
                "Outros"
            ]
        )
        quantidade = st.number_input("Quantidade", min_value=1, step=1)
        urgencia = st.selectbox(
            "Urgência",
            [
                "Baixa",
                "Média",
                "Alta",
                "Urgente"
            ]
        )

        if st.button("Cadastrar Necessidade"):
            dados = {
                "abrigo_id": nomes_abrigos[abrigo_escolhido],
                "item": item,
                "categoria": categoria,
                "quantidade": quantidade,
                "urgencia": urgencia
            }

            resposta = requests.post(f"{API_URL}/necessidades", json=dados)

            if resposta.status_code == 200:
                st.success("Necessidade cadastrada com sucesso!")
            else:
                st.error("Erro ao cadastrar necessidade.")


# -------------------------
# REGISTRAR DOAÇÃO
# -------------------------

elif menu == "Registrar Doação":
    st.header("Registrar Doação")

    doadores = buscar_doadores()
    abrigos = buscar_abrigos()

    if len(doadores) == 0:
        st.warning("Cadastre um doador antes de registrar uma doação.")
    elif len(abrigos) == 0:
        st.warning("Cadastre um abrigo antes de registrar uma doação.")
    else:
        nomes_doadores = {}
        nomes_abrigos = {}

        for doador in doadores:
            texto = f"{doador['id']} - {doador['nome']}"
            nomes_doadores[texto] = doador["id"]

        for abrigo in abrigos:
            texto = f"{abrigo['id']} - {abrigo['nome']}"
            nomes_abrigos[texto] = abrigo["id"]

        doador_escolhido = st.selectbox("Escolha o doador", list(nomes_doadores.keys()))
        abrigo_escolhido = st.selectbox("Escolha o abrigo", list(nomes_abrigos.keys()))

        item = st.text_input("Item doado")
        categoria = st.selectbox(
            "Categoria",
            [
                "Alimentos e Água",
                "Produtos de Higiene",
                "Roupas e Cobertores",
                "Materiais de Limpeza",
                "Outros"
            ]
        )
        quantidade = st.number_input("Quantidade", min_value=1, step=1)
        status = st.selectbox(
            "Status da doação",
            [
                "Pendente",
                "Recebida",
                "Separada",
                "Entregue"
            ]
        )

        if st.button("Registrar Doação"):
            dados = {
                "doador_id": nomes_doadores[doador_escolhido],
                "abrigo_id": nomes_abrigos[abrigo_escolhido],
                "item": item,
                "categoria": categoria,
                "quantidade": quantidade,
                "status": status
            }

            resposta = requests.post(f"{API_URL}/doacoes", json=dados)

            if resposta.status_code == 200:
                st.success("Doação registrada com sucesso!")
            else:
                st.error("Erro ao registrar doação.")


# -------------------------
# LISTAR ABRIGOS
# -------------------------

elif menu == "Listar Abrigos":
    st.header("Abrigos Cadastrados")

    resposta = requests.get(f"{API_URL}/abrigos")

    if resposta.status_code == 200:
        dados = resposta.json()

        if len(dados) == 0:
            st.warning("Nenhum abrigo cadastrado.")
        else:
            st.dataframe(dados)
    else:
        st.error("Erro ao buscar abrigos.")


# -------------------------
# LISTAR DOADORES
# -------------------------

elif menu == "Listar Doadores":
    st.header("Doadores Cadastrados")

    resposta = requests.get(f"{API_URL}/doadores")

    if resposta.status_code == 200:
        dados = resposta.json()

        if len(dados) == 0:
            st.warning("Nenhum doador cadastrado.")
        else:
            st.dataframe(dados)
    else:
        st.error("Erro ao buscar doadores.")


# -------------------------
# LISTAR VOLUNTÁRIOS
# -------------------------

elif menu == "Listar Voluntários":
    st.header("Voluntários Cadastrados")

    resposta = requests.get(f"{API_URL}/voluntarios")

    if resposta.status_code == 200:
        dados = resposta.json()

        if len(dados) == 0:
            st.warning("Nenhum voluntário cadastrado.")
        else:
            st.dataframe(dados)
    else:
        st.error("Erro ao buscar voluntários.")


# -------------------------
# LISTAR NECESSIDADES
# -------------------------

elif menu == "Listar Necessidades":
    st.header("Necessidades dos Abrigos")

    resposta = requests.get(f"{API_URL}/necessidades")

    if resposta.status_code == 200:
        dados = resposta.json()

        if len(dados) == 0:
            st.warning("Nenhuma necessidade cadastrada.")
        else:
            st.dataframe(dados)
    else:
        st.error("Erro ao buscar necessidades.")


# -------------------------
# LISTAR DOAÇÕES
# -------------------------

elif menu == "Listar Doações":
    st.header("Doações Registradas")

    resposta = requests.get(f"{API_URL}/doacoes")

    if resposta.status_code == 200:
        dados = resposta.json()

        if len(dados) == 0:
            st.warning("Nenhuma doação registrada.")
        else:
            st.dataframe(dados)
    else:
        st.error("Erro ao buscar doações.")