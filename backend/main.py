from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Nome do banco de dados
BANCO = "database.db"


# Função para conectar ao banco
def conectar_banco():
    conexao = sqlite3.connect(BANCO)
    conexao.row_factory = sqlite3.Row
    return conexao


# Função para criar as tabelas
def criar_tabelas():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS abrigos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            endereco TEXT NOT NULL,
            telefone TEXT NOT NULL,
            responsavel TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS voluntarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            disponibilidade TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS necessidades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            abrigo_id INTEGER NOT NULL,
            item TEXT NOT NULL,
            categoria TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            urgencia TEXT NOT NULL,
            FOREIGN KEY (abrigo_id) REFERENCES abrigos(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doador_id INTEGER NOT NULL,
            abrigo_id INTEGER NOT NULL,
            item TEXT NOT NULL,
            categoria TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (doador_id) REFERENCES doadores(id),
            FOREIGN KEY (abrigo_id) REFERENCES abrigos(id)
        )
    """)

    conexao.commit()
    conexao.close()


# Criar tabelas ao iniciar
criar_tabelas()


# Modelos de dados
class Abrigo(BaseModel):
    nome: str
    endereco: str
    telefone: str
    responsavel: str


class Doador(BaseModel):
    nome: str
    telefone: str
    email: str


class Voluntario(BaseModel):
    nome: str
    telefone: str
    disponibilidade: str


class Necessidade(BaseModel):
    abrigo_id: int
    item: str
    categoria: str
    quantidade: int
    urgencia: str


class Doacao(BaseModel):
    doador_id: int
    abrigo_id: int
    item: str
    categoria: str
    quantidade: int
    status: str


# Página inicial da API
@app.get("/")
def inicio():
    return {
        "mensagem": "API do Sistema de Doações funcionando!"
    }


# -------------------------
# ROTAS DE ABRIGOS
# -------------------------

@app.post("/abrigos")
def cadastrar_abrigo(abrigo: Abrigo):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO abrigos (nome, endereco, telefone, responsavel)
        VALUES (?, ?, ?, ?)
    """, (abrigo.nome, abrigo.endereco, abrigo.telefone, abrigo.responsavel))

    conexao.commit()
    conexao.close()

    return {
        "mensagem": "Abrigo cadastrado com sucesso!"
    }


@app.get("/abrigos")
def listar_abrigos():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM abrigos")
    dados = cursor.fetchall()

    conexao.close()

    lista = []

    for item in dados:
        lista.append(dict(item))

    return lista


# -------------------------
# ROTAS DE DOADORES
# -------------------------

@app.post("/doadores")
def cadastrar_doador(doador: Doador):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO doadores (nome, telefone, email)
        VALUES (?, ?, ?)
    """, (doador.nome, doador.telefone, doador.email))

    conexao.commit()
    conexao.close()

    return {
        "mensagem": "Doador cadastrado com sucesso!"
    }


@app.get("/doadores")
def listar_doadores():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM doadores")
    dados = cursor.fetchall()

    conexao.close()

    lista = []

    for item in dados:
        lista.append(dict(item))

    return lista


# -------------------------
# ROTAS DE VOLUNTÁRIOS
# -------------------------

@app.post("/voluntarios")
def cadastrar_voluntario(voluntario: Voluntario):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO voluntarios (nome, telefone, disponibilidade)
        VALUES (?, ?, ?)
    """, (voluntario.nome, voluntario.telefone, voluntario.disponibilidade))

    conexao.commit()
    conexao.close()

    return {
        "mensagem": "Voluntário cadastrado com sucesso!"
    }


@app.get("/voluntarios")
def listar_voluntarios():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM voluntarios")
    dados = cursor.fetchall()

    conexao.close()

    lista = []

    for item in dados:
        lista.append(dict(item))

    return lista


# -------------------------
# ROTAS DE NECESSIDADES
# -------------------------

@app.post("/necessidades")
def cadastrar_necessidade(necessidade: Necessidade):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO necessidades 
        (abrigo_id, item, categoria, quantidade, urgencia)
        VALUES (?, ?, ?, ?, ?)
    """, (
        necessidade.abrigo_id,
        necessidade.item,
        necessidade.categoria,
        necessidade.quantidade,
        necessidade.urgencia
    ))

    conexao.commit()
    conexao.close()

    return {
        "mensagem": "Necessidade cadastrada com sucesso!"
    }


@app.get("/necessidades")
def listar_necessidades():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT 
            necessidades.id,
            abrigos.nome AS abrigo,
            necessidades.item,
            necessidades.categoria,
            necessidades.quantidade,
            necessidades.urgencia
        FROM necessidades
        INNER JOIN abrigos
        ON necessidades.abrigo_id = abrigos.id
    """)

    dados = cursor.fetchall()
    conexao.close()

    lista = []

    for item in dados:
        lista.append(dict(item))

    return lista


# -------------------------
# ROTAS DE DOAÇÕES
# -------------------------

@app.post("/doacoes")
def cadastrar_doacao(doacao: Doacao):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO doacoes 
        (doador_id, abrigo_id, item, categoria, quantidade, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        doacao.doador_id,
        doacao.abrigo_id,
        doacao.item,
        doacao.categoria,
        doacao.quantidade,
        doacao.status
    ))

    conexao.commit()
    conexao.close()

    return {
        "mensagem": "Doação registrada com sucesso!"
    }


@app.get("/doacoes")
def listar_doacoes():
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT 
            doacoes.id,
            doadores.nome AS doador,
            abrigos.nome AS abrigo,
            doacoes.item,
            doacoes.categoria,
            doacoes.quantidade,
            doacoes.status
        FROM doacoes
        INNER JOIN doadores
        ON doacoes.doador_id = doadores.id
        INNER JOIN abrigos
        ON doacoes.abrigo_id = abrigos.id
    """)

    dados = cursor.fetchall()
    conexao.close()

    lista = []

    for item in dados:
        lista.append(dict(item))

    return lista