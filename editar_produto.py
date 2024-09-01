# editar_produto.py
import tkinter as tk
from tkinter import ttk, messagebox
from crud import listar_produtos, inserir_produto, atualizar_produto, excluir_produto, on_click_exportar
from tkcalendar import DateEntry


#Janela Editar Produtos
def editar_produtos():
    def show_error(mensagem):
        janela.destroy()
        messagebox.showerror("Erro", mensagem)
    def inserir():
        try:
            if not produto_entry.get() and valor_entry.get():
                show_error(f"Insira o nome do produto")
            elif not valor_entry.get() and produto_entry.get():
                show_error("Insira o valor")
            elif not produto_entry.get() and not valor_entry.get():
                show_error("Insira o nome do produto e o valor")
            else:
                inserir_produto(produto_entry.get(), valor_entry.get())
                listar_produtos(tree)
        except Exception as e:
            show_error(f"Ocorreu um erro: {e}")

    def atualizar():
        try:
            if id_entry.get() and produto_entry.get() and valor_entry.get():
                atualizar_produto(id_entry.get(), produto_entry.get(), valor_entry.get())
                listar_produtos(tree)
            else:
                show_error("Preencha todos os dados.")
        except Exception as e:
            show_error(f"Ocorreu um erro: {e}")

    def excluir():
        try:
            if id_entry.get():
                excluir_produto(id_entry.get())
                listar_produtos(tree)
            else:
                show_error("Insira o ID do produto que deseja excluir.")
        except Exception as e:
            show_error(f"Ocorreu um erro: {e}")

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

    ttk.Button(janela, text="Inserir", command=inserir).grid(pady=20, column=0, row=3, sticky="ew", padx=10)
    ttk.Button(janela, text="Atualizar", command=atualizar).grid(column=1, row=3, sticky="ew", padx=10)
    ttk.Button(janela, text="Excluir", command=excluir).grid(column=2, row=3, sticky="ew", padx=10)

    colunas = ('ID', 'Produto', 'Valor')
    tree = ttk.Treeview(janela, columns=colunas, show='headings')
    tree.column('ID', width=40)
    tree.column('Valor', width=70)
    tree.heading('ID', text='ID')
    tree.heading('Produto', text='Produto')
    tree.heading('Valor', text='Valor')
    tree.grid(column=0, row=4, columnspan=3, sticky='nsew', pady=10, padx=20)
    scrollbar = ttk.Scrollbar(janela, orient='vertical', command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(column=3, row=4, sticky='ns')

    listar_produtos(tree)
    tree.bind('<<TreeviewSelect>>', selecionado)
    return janela

#Janela Exportar Vendas
def exportar_vendas():
    def show_error(mensagem):
        janela.destroy() 
        messagebox.showerror("Erro", mensagem)
    def on_click(opcao):
        try: 
            if opcao == 1:
                inicio = data_inicio.get_date()
                fim = data_fim.get_date()
                if inicio > fim:
                    show_error("A data de início não pode ser superior à data final.")
                    janela.destroy()
                else:
                    on_click_exportar(inicio, fim, opcao)
                    messagebox.showinfo("Exportado", "Verifique se o arquivo foi exportado corretamente.")
                    janela.destroy()
            else:
                on_click_exportar(None, None, opcao)
                messagebox.showinfo("Exportado", "Verifique se o arquivo foi exportado corretamente.")
                janela.destroy()
        except Exception as e:
            show_error(e)


    janela = tk.Toplevel()
    janela.title("Exportar")
    janela.geometry('360x250')
    janela.resizable(False, False)

    for i in range(5):
        janela.rowconfigure(i, weight=1)
    for i in range(2):
        janela.columnconfigure(i, weight=1)

    tk.Label(janela, text="Data Inicial").grid(column=0, row=0, sticky="e", padx=15, pady=10)
    tk.Label(janela, text="Data Final").grid(column=0, row=1, sticky="e", padx=15)
 
    data_inicio = DateEntry(janela, width=18, background='black', foreground='white', borderwidth=2, locale='pt_BR')
    data_inicio.grid(column=1, row=0, padx=10, sticky='ew')
    data_fim = DateEntry(janela, width=18, background='black', foreground='white', borderwidth=2, locale='pt_BR')
    data_fim.grid(column=1, row=1, padx=10, sticky='ew')

    botao_exportar_selecionado = ttk.Button(janela, text="Exportar Período", command=lambda: on_click(1))
    botao_exportar_selecionado.grid(columnspan=2, row=2, pady=10, padx=10, sticky='ew')
    botao_exportar_dia = ttk.Button(janela, text="Exportar Vendas de Hoje", command=lambda: on_click(3))
    botao_exportar_dia.grid(columnspan=2, row=3, pady=10, padx=10, sticky='ew')
    botao_exportar_tudo = ttk.Button(janela, text="Exportar Tudo", command=lambda: on_click(2))
    botao_exportar_tudo.grid(columnspan=2, row=4, pady=10, padx=10, sticky='ew')

    return janela