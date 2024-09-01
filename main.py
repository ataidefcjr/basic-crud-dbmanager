import tkinter as tk
from tkinter import messagebox
from ttkwidgets.autocomplete import AutocompleteCombobox
from crud import busca_preco, busca_produto, registrar_venda, verificar_db
from editar_produto import editar_produtos, exportar_vendas

def atualizar_valores(event=None):
    produto_selecionado = produto.get()
    try:
        if not qtd.get():
            valor_unit.config(state="normal")
            valor_unit.delete(0, tk.END)
            valor_unit.config(state="readonly")
            valor_total.config(state="normal")
            valor_total.delete(0, tk.END)
            valor_total.config(state="readonly")
        if produto_selecionado in produtos and qtd.get():
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

verificar_db() 

janela = tk.Tk()
janela.title("Vendas")
janela.geometry('500x220')
janela.resizable(False, False)

janela.columnconfigure(0, weight=0)
janela.columnconfigure(1, weight=1)
janela.columnconfigure(2, weight=0)
janela.rowconfigure(4, weight=1)

#Menu de produtos
tk.Label(janela, text="Produto").grid(column=0, row=0, sticky="e", padx=20)
produtos = sorted(busca_produto())
produto = AutocompleteCombobox(janela, completevalues=produtos)
produto.grid(column=1, row=0, sticky='ew')

#Entrada de quantidade
tk.Label(janela, text="Quantidade").grid(column=0, row=1, sticky="e", padx=20)
qtd = tk.Entry(janela)
qtd.insert(0, "1")
qtd.grid(column=1, row=1, sticky="ew")

#Exibe o valor
tk.Label(janela, text="Valor Unitário").grid(column=0, row=2, sticky="e", padx=20)
valor_unit = tk.Entry(janela, state="readonly", textvariable='')
valor_unit.grid(column=1, row=2, sticky="ew")
tk.Label(janela, text="Valor Total").grid(column=0, row=3, sticky="e", padx=20)
valor_total = tk.Entry(janela, state="readonly", textvariable='')
valor_total.grid(column=1, row=3, sticky="ew")

#Botões
tk.Button(janela, text="Editar Produtos", command = lambda: janela_editar()).grid ( column=0, row=4, sticky="ew", padx=5, pady=5)
tk.Button(janela, text="Ok", command = lambda: registrar()).grid (column=1, row=4, sticky="ew", padx=5, pady=5)
tk.Button(janela, text="Encerrar", command= lambda: fechar_programa()).grid(column=2, row=4, sticky="ew", padx=5, pady=5)
tk.Button(janela, text="Exportar Vendas", command= lambda: janela_exportar()).grid(column=0, columnspan=3, row=5, sticky="ew", padx=5, pady=10)

def produtos_update(combobox): ##atualiza a lista de produtos
    combobox['values'] = sorted(busca_produto())
    global produtos
    produtos = sorted(busca_produto())

def registrar():
    item = produto.get()
    quantidade = qtd.get()
    quantidade = int(quantidade)
    if quantidade > 0:
        if item in produtos:
            try:
                atualizar_valores()
                total = valor_total.get()
                registrar_venda(item, quantidade, total)
                messagebox.showinfo("Sucesso", "Venda Registrada")
            except Exception as e:
                messagebox.showwarning("Erro", "Erro ao registrar produto")
            finally:
                produto.set('')
                qtd.delete(0, 'end')
                qtd.insert(0, '1')
                valor_total.config(state="normal")
                valor_unit.config(state="normal")
                valor_unit.delete(0, 'end')
                valor_total.delete(0, 'end')  
                valor_total.config(state="readonly")
                valor_unit.config(state='readonly')
                atualizar_valores()
        else:
            messagebox.showwarning("Erro", "Produto não cadastrado na base de dados.")

    else:
        messagebox.showwarning("Erro", "Insira a quantidade.")

def fechar_programa():
    janela.quit()

def janela_editar():
    editar = editar_produtos()
    if editar:
        janela.withdraw()
        editar.wait_window()
        janela.deiconify()
        produtos_update(produto)
        
def janela_exportar():
    exportar = exportar_vendas()
    if exportar:
        janela.withdraw()
        exportar.wait_window()
        janela.deiconify()

qtd.bind("<KeyRelease>", atualizar_valores)
produto.bind("<<ComboboxSelected>>", atualizar_valores)
janela.mainloop()

