import sqlite3
import tkinter as tk
from datetime import datetime

def conectar_bd():
    return sqlite3.connect('produtos.db')

def listar_produtos(tree):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    rows = cursor.fetchall()
    tree.delete(*tree.get_children())   # Limpar a Treeview
    for row in rows:                    # Insere novamente na lista
        tree.insert("", tk.END, values=row)
    conn.close()
    return rows

def atualizar_produto(id, produto, valor):
    executar("UPDATE produtos SET produto = ?, valor = ? WHERE id = ?", (produto, valor, id))


def excluir_produto(id):
    executar("DELETE FROM produtos WHERE id = ?", (id,))

def busca_preco(produto):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT VALOR FROM PRODUTOS WHERE PRODUTO = ?", (produto,))
    valor = cursor.fetchone()
    if valor: 
        return valor[0]
    else:
        return None

def busca_produto():
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT PRODUTO FROM PRODUTOS")
    produtos = cursor.fetchall()
    return [produto[0] for produto in produtos]

def inserir_produto(produto, valor):
    executar("INSERT INTO produtos (produto, valor) VALUES (?, ?)", (produto, valor))

def registrar_venda(produto, quantidade, valortotal):
    try:
        data = datetime.now().strftime("%d/%m/%Y %H:%M")
        executar(("INSERT INTO VENDAS (PRODUTO, QUANTIDADE, VALOR, DATA) VALUES (?, ?, ?, ?)"), (produto, quantidade, valortotal, data))
    except:
        pass
    finally:
        return "Done"

def executar(comando, valores):
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute(comando, valores)
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)