# editar_produto.py
import tkinter as tk
from tkinter import ttk, messagebox
from crud import listar_produtos, inserir_produto, atualizar_produto, excluir_produto

def abrir_janela():
    def inserir():
        try:
            inserir_produto(produto_entry.get(), valor_entry.get())
            listar_produtos(tree)
        except Exception as e:
            messagebox.showerror('ERRO', f'Ocorreu um erro: {e}')
            print(e)

    def atualizar():
        try:
            atualizar_produto(id_entry.get(), produto_entry.get(), valor_entry.get())
            listar_produtos(tree)
        except Exception as e:
            messagebox.showerror('ERRO', f'Ocorreu um erro: {e}')
            print(e)

    def excluir():
        try:
            excluir_produto(id_entry.get())
            listar_produtos(tree)
        except Exception as e:
            messagebox.showerror('ERRO', f'Ocorreu um erro: {e}')
            print(e)

    def selecionado(event):
        try:
            item_selecionado = tree.selection()[0]
            valor_item = tree.item(item_selecionado, 'values')
            id_entry.delete(0, tk.END)
            id_entry.insert(0, valor_item[0])
            produto_entry.delete(0, tk.END)
            produto_entry.insert(0, valor_item[1])
            valor_entry.delete(0, tk.END)
            valor_entry.insert(0, valor_item[2])
        except:
            pass

    janela = tk.Toplevel()
    janela.title("Editar Produtos")
    janela.geometry('600x400')

    janela.columnconfigure(0, weight=1)
    janela.columnconfigure(1, weight=1)
    janela.columnconfigure(2, weight=1)
    janela.rowconfigure(4, weight=1)

    ttk.Label(janela, text="ID").grid(column=0, row=0, sticky="e")
    id_entry = tk.Entry(janela)
    id_entry.grid(column=1, row=0, sticky="ew")
    ttk.Label(janela, text="Produto").grid(column=0, row=1, sticky="e")
    produto_entry = tk.Entry(janela)
    produto_entry.grid(column=1, row=1, sticky="ew")
    ttk.Label(janela, text="Valor").grid(column=0, row=2, sticky="e")
    valor_entry = tk.Entry(janela)
    valor_entry.grid(column=1, row=2, sticky="ew")

    ttk.Button(janela, text="Inserir", command=inserir).grid(pady=20, column=0, row=3, sticky="ew")
    ttk.Button(janela, text="Atualizar", command=atualizar).grid(column=1, row=3, sticky="ew")
    ttk.Button(janela, text="Excluir", command=excluir).grid(column=2, row=3, sticky="ew")

    colunas = ('ID', 'Produto', 'Valor')
    tree = ttk.Treeview(janela, columns=colunas, show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Produto', text='Produto')
    tree.heading('Valor', text='Valor')
    tree.grid(column=0, row=4, columnspan=3, sticky='nsew')

    listar_produtos(tree)
    tree.bind('<<TreeviewSelect>>', selecionado)

    janela.mainloop()
