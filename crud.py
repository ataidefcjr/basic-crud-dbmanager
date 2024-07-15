import sqlite3
import tkinter as tk
from datetime import datetime, timedelta
import csv
import os
import subprocess

banco_dados = 'produtos.db'

def verificar_db():
    conn = sqlite3.connect(banco_dados)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='PRODUTOS';")
    produto_existe = cursor.fetchone() is not None

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='VENDAS';")
    vendas_existe = cursor.fetchone() is not None

    if not produto_existe:
        cursor.execute("CREATE TABLE PRODUTOS (id INTEGER PRIMARY KEY AUTOINCREMENT, produto TEXT NOT NULL, valor REAL NOT NULL);")
        print("TABELA PRODUTOS CRIADA")
    if not vendas_existe:
        cursor.execute("CREATE TABLE VENDAS (id INTEGER PRIMARY KEY AUTOINCREMENT, quantidade INTEGER NOT NULL, produto TEXT NOT NULL, valor REAL NOT NULL, data DATE NOT NULL);")
        print("TABELA VENDAS CRIADA")

    conn.commit()
    conn.close()
    
def conectar_bd():
    return sqlite3.connect(banco_dados)

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
    valor = valor.replace(',', '.')
    valor = "{:.2f}".format(float(valor))
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
    valor = valor.replace(',', '.')
    valor = "{:.2f}".format(float(valor))
    executar("INSERT INTO produtos (produto, valor) VALUES (?, ?)", (produto, valor))

def registrar_venda(produto, quantidade, valortotal):
    try:
        data = datetime.now().strftime("%d/%m/%Y %H:%M")
        executar(("INSERT INTO VENDAS (PRODUTO, QUANTIDADE, VALOR, DATA) VALUES (?, ?, ?, ?)"), (produto, quantidade, valortotal, data))
    except:
        pass

def formatar_data(data):
    return data.strftime('%d-%m-%Y')

def exportar(inicio, fim):
    try: 
        if inicio == 'all' and fim == 'all':
            conn = conectar_bd()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM VENDAS")
            resultado = cursor.fetchall()
            conn.close()
            save_to_csv(resultado)
            return resultado
        elif inicio == 'today' and fim == 'today':
            conn = conectar_bd()
            cursor = conn.cursor()
            inicio = datetime.now()
            fim = inicio + timedelta(days=1)
            cursor.execute(("SELECT * FROM VENDAS WHERE DATA BETWEEN (?) AND (?)"), (formatar_data(inicio), formatar_data(fim),))
            resultado = cursor.fetchall()
            conn.close()
            save_to_csv(resultado)
            return resultado
        else:
            inicio = formatar_data(inicio)
            fim = fim + timedelta(days=1)
            fim = formatar_data(fim)
            conn = conectar_bd()
            cursor = conn.cursor()
            cursor.execute(("SELECT * FROM VENDAS WHERE DATA BETWEEN (?) AND (?)"), (inicio, fim))
            resultado = cursor.fetchall()
            conn.close()
            save_to_csv(resultado)
            return resultado
    except Exception as e:
        print(e)

def save_to_csv(resultado):
    if resultado:
        header = ['ID','Quantidade', 'Produtos', 'Valor', 'Data']
        filename = "Relatório - " + datetime.today().strftime('%d-%m-%Y %H-%M-%S') + ".csv"
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(header)

            for venda in resultado:
                writer.writerow(venda)
            
            if os.path.exists(filename):
                file_path = os.path.abspath(filename)
                try:
                    os.startfile(file_path)
                except AttributeError:
                    try:
                        subprocess.call(['xdg-open', file_path])
                    except:
                        pass
                except:
                    pass
        
def on_click_exportar(data_inicio, data_fim, opcao):
    if opcao == 1:
        inicio = data_inicio
        fim = data_fim
        exportar(inicio, fim)
    elif opcao == 2:
        inicio = 'all'
        fim = 'all'
        exportar(inicio, fim)
    elif opcao == 3:
        inicio = 'today'
        fim = 'today'
        exportar(inicio, fim)

def executar(comando, valores):
    try:
        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute(comando, valores)
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)