import tkinter as tk
from tkinter import ttk, messagebox
from crud import busca_preco, busca_produto, registrar_venda
from editar_produto import abrir_janela

def atualizar_valores(event=None):
    produto_selecionado = produto.get()
    try:
        if produto_selecionado:
            preco = float(busca_preco(produto_selecionado))
            unidades = int(qtd.get())
            if preco is not None:
                valor_unit.config(state="normal")
                valor_unit.delete(0, tk.END)
                valor_unit.insert(0, f"R${preco:.2f}")
                valor_unit.config(state="readonly")
                valor_total.config(state="normal")
                valor_total.delete(0, tk.END)
                total = preco * unidades
                valor_total.insert(0, f"R${total:.2f}")
                valor_total.config(state="readonly")
            else:
                messagebox.showwarning("Não encontrado", "Ocorreu um erro ao procurar o produto.")
    except Exception as e:
        print(e)
        pass

janela = tk.Tk()
janela.title("Vendas")
janela.geometry('500x200')

janela.columnconfigure(0, weight=0)
janela.columnconfigure(1, weight=1)
janela.columnconfigure(2, weight=0)
janela.rowconfigure(4, weight=1)

#Menu de produtos
tk.Label(janela, text="Produto").grid(column=0, row=0, sticky="e", padx=20)
produtos = busca_produto()
produto = ttk.Combobox(janela, values=produtos)
produto.grid(column=1, row=0, sticky='ew')
#Entrada de quantidade
tk.Label(janela, text="Quantidade").grid(column=0, row=1, sticky="e", padx=20)
qtd = tk.Entry(janela)
qtd.insert(0, "1")
qtd.grid(column=1, row=1, sticky="ew")
#Exibe o valor
tk.Label(janela, text="Valor Unitário").grid(column=0, row=2, sticky="e", padx=20)
valor_unit = tk.Entry(janela, state="readonly")
valor_unit.grid(column=1, row=2, sticky="ew")
tk.Label(janela, text="Valor Total").grid(column=0, row=3, sticky="e", padx=20)
valor_total = tk.Entry(janela, state="readonly")
valor_total.grid(column=1, row=3, sticky="ew")

#Botões
tk.Button(janela, text="Editar Produtos", command = lambda: abrir_janela()).grid (pady= 20, column=0, row=4, sticky="ew")
tk.Button(janela, text="Ok", command = lambda: registrar()).grid (column=1, row=4, sticky="ew")
tk.Button(janela, text="Encerrar", command= lambda: fechar_programa()).grid(column=2, row=4, sticky="ew")

def registrar():
    item = produto.get()
    quantidade = qtd.get()
    if item and quantidade:
        try:
            total = valor_total.get()
            registrar_venda(item, quantidade, total)
        except Exception as e:
            messagebox.showwarning("Erro", "Erro ao registrar produto")
        finally:
            messagebox.showinfo("Sucesso", "Venda Registrada")
    else:
        messagebox.showwarning("Erro", "Insira o produto e a quantidade")

def fechar_programa():
    janela.quit()


qtd.bind("<KeyRelease>", atualizar_valores)
produto.bind("<<ComboboxSelected>>", atualizar_valores)
janela.mainloop()

