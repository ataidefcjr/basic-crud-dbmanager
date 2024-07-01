import sqlite3
import tkinter as tk

def conectar_bd():
    return sqlite3.connect('produtos.db')

def listar_produtos(tree):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    rows = cursor.fetchall()
    tree.delete(*tree.get_children())  # Limpar a Treeview
    for row in rows:
        tree.insert("", tk.END, values=row)
    conn.close()

def atualizar_produto(id, produto, valor):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("UPDATE produtos SET produto = ?, valor = ? WHERE id = ?", (produto, valor, id))
    conn.commit()
    conn.close()

def excluir_produto(id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def inserir_produto(produto, valor):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produtos (produto, valor) VALUES (?, ?)", (produto, valor))
    listar_produtos
    conn.commit()
    conn.close()
