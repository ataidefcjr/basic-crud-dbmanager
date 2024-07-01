import tkinter as tk
from tkinter import ttk
from crud import listar_produtos, inserir_produto, atualizar_produto, excluir_produto

janela = tk.Tk()
janela.title("Editar Produtos")
janela.geometry('600x400')

janela.columnconfigure(0, weight=1)
janela.columnconfigure(1, weight=1)
janela.columnconfigure(2, weight=1)
janela.rowconfigure(4, weight=1)

#Inputs
ttk.Label(janela, text="ID").grid(column=0, row=0, sticky="e")
id = tk.Entry(janela)
id.grid(column=1,row=0, sticky="ew")
ttk.Label(janela, text="Produto").grid(column=0, row=1, sticky="e")
produto = tk.Entry(janela)
produto.grid(column=1, row=1, sticky="ew")
ttk.Label(janela, text="Valor").grid(column=0, row=2, sticky="e")
valor = tk.Entry(janela)
valor.grid(column=1, row=2, sticky="ew")
#Botões
ttk.Button(janela, text="Inserir", command = lambda: inserir()).grid (pady= 20, column=0, row=3, sticky="ew")
ttk.Button(janela, text="Atualizar", command = lambda: atualizar()).grid(column=1, row=3, sticky="ew")
ttk.Button(janela, text="Excluir", command= lambda: excluir()).grid(column=2, row=3, sticky="ew")
#Lista dos produtos
colunas = ('ID', 'Produto', 'Valor')
tree = ttk.Treeview(janela, columns=colunas, show='headings')
tree.heading('ID', text='ID')
tree.heading('Produto', text='Produto')
tree.heading('Valor', text='Valor')
tree.grid(column=0, row=4, columnspan=3, sticky='nsew')
treechildrens = tree.get_children()
#Atualiza a lista dos produtos
listar_produtos(tree)

#Funções dos Botões
def inserir():
    inserir_produto(produto.get(), valor.get())
    listar_produtos(tree)

def atualizar():
    atualizar_produto(id.get(), produto.get(), valor.get())
    listar_produtos(tree)

def excluir():
    excluir_produto(id.get())
    listar_produtos(tree)

#Função para preencher o entry com os dados da tree
def selecionado(event):
    try:
        item_selecionado = tree.selection()[0]
        valor_item = tree.item(item_selecionado, 'values')
        id.delete(0, tk.END)
        id.insert(0, valor_item[0])
        produto.delete(0, tk.END)
        produto.insert(0, valor_item[1])
        valor.delete(0, tk.END)
        valor.insert(0, valor_item[2])
    except:
        pass
    

tree.bind('<<TreeviewSelect>>', selecionado)
janela.mainloop()
