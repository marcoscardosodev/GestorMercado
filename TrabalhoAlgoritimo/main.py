import tkinter as tk
from tkinter import messagebox
from dados import produtos, carrinho

def limpar_tela():
    for widget in root.winfo_children():
        widget.destroy()

def mostrar_tela_inicial():
    limpar_tela()
    titulo = tk.Label(root, text="Loja Virtual", font=("Helvetica", 20, "bold"))
    titulo.pack(pady=20)
    
    btn_admin = tk.Button(root, text="Administrador", width=20, command=mostrar_login_admin)
    btn_admin.pack(pady=10)
    
    btn_cliente = tk.Button(root, text="Cliente", width=20, command=mostrar_tela_cliente)
    btn_cliente.pack(pady=10)

def mostrar_login_admin():
    limpar_tela()
    
    tk.Label(root, text="Login Administrador", font=("Helvetica", 16, "bold")).pack(pady=20)
    
    tk.Label(root, text="Usuário:").pack()
    entry_user = tk.Entry(root)
    entry_user.pack()
    
    tk.Label(root, text="Senha:").pack()
    entry_senha = tk.Entry(root, show="*")
    entry_senha.pack()
    
    def tentar_login():
        user = entry_user.get()
        senha = entry_senha.get()
        if user == "admin" and senha == "1234":
            mostrar_tela_admin()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")
    
    tk.Button(root, text="Entrar", command=tentar_login).pack(pady=10)
    tk.Button(root, text="Voltar", command=mostrar_tela_inicial).pack()

def mostrar_tela_admin():
    limpar_tela()
    
    tk.Label(root, text="Área do Administrador", font=("Helvetica", 16, "bold")).pack(pady=20)
    
    lista_produtos = tk.Listbox(root, width=50)
    lista_produtos.pack(pady=10)
    
    def atualizar_lista():
        lista_produtos.delete(0, tk.END)
        for nome, info in produtos.items():
            lista_produtos.insert(tk.END, f"{nome} - R${info['preco']:.2f} - Estoque: {info['estoque']}")
    atualizar_lista()
    
    frame_form = tk.Frame(root)
    frame_form.pack(pady=10)
    
    tk.Label(frame_form, text="Nome:").grid(row=0, column=0)
    entry_nome = tk.Entry(frame_form)
    entry_nome.grid(row=0, column=1)
    
    tk.Label(frame_form, text="Preço:").grid(row=1, column=0)
    entry_preco = tk.Entry(frame_form)
    entry_preco.grid(row=1, column=1)
    
    tk.Label(frame_form, text="Estoque:").grid(row=2, column=0)
    entry_estoque = tk.Entry(frame_form)
    entry_estoque.grid(row=2, column=1)
    
    def adicionar_produto():
        nome = entry_nome.get().strip()
        preco = entry_preco.get().strip()
        estoque = entry_estoque.get().strip()
        
        if not nome or not preco or not estoque:
            messagebox.showwarning("Aviso", "Preencha todos os campos.")
            return
        try:
            preco = float(preco)
            estoque = int(estoque)
        except:
            messagebox.showwarning("Aviso", "Preço deve ser número e estoque inteiro.")
            return
        
        produtos[nome] = {"preco": preco, "estoque": estoque}
        atualizar_lista()
        entry_nome.delete(0, tk.END)
        entry_preco.delete(0, tk.END)
        entry_estoque.delete(0, tk.END)
    
    def remover_produto():
        selecionado = lista_produtos.curselection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um produto para remover.")
            return
        item = lista_produtos.get(selecionado)
        nome = item.split(" - ")[0]
        del produtos[nome]
        atualizar_lista()
    
    tk.Button(root, text="Adicionar Produto", command=adicionar_produto).pack(pady=5)
    tk.Button(root, text="Remover Produto", command=remover_produto).pack(pady=5)
    tk.Button(root, text="Logout", command=mostrar_tela_inicial).pack(pady=20)

def mostrar_tela_cliente():
    limpar_tela()
    
    tk.Label(root, text="Área do Cliente", font=("Helvetica", 16, "bold")).pack(pady=20)
    
    lista_itens = tk.Listbox(root, width=50)
    lista_itens.pack()
    
    def atualizar_lista_itens():
        lista_itens.delete(0, tk.END)
        for nome, info in produtos.items():
            lista_itens.insert(tk.END, f"{nome} - R${info['preco']:.2f} - Estoque: {info['estoque']}")
    atualizar_lista_itens()
    
    tk.Label(root, text="Quantidade:").pack(pady=5)
    entry_quant = tk.Entry(root)
    entry_quant.pack()
    
    lista_carrinho = tk.Listbox(root, width=50)
    lista_carrinho.pack(pady=10)
    
    def atualizar_carrinho():
        lista_carrinho.delete(0, tk.END)
        for nome, quant in carrinho.items():
            preco = produtos[nome]["preco"]
            subtotal = preco * quant
            lista_carrinho.insert(tk.END, f"{nome} x{quant} = R${subtotal:.2f}")
    
    def adicionar_ao_carrinho():
        try:
            idx = lista_itens.curselection()[0]
        except IndexError:
            messagebox.showwarning("Aviso", "Selecione um produto para adicionar.")
            return
        item = lista_itens.get(idx)
        nome = item.split(" - ")[0]
        
        quant_str = entry_quant.get().strip()
        if not quant_str.isdigit() or int(quant_str) <= 0:
            messagebox.showwarning("Aviso", "Informe uma quantidade válida.")
            return
        
        quant = int(quant_str)
        if quant > produtos[nome]["estoque"]:
            messagebox.showwarning("Aviso", f"Estoque insuficiente. Temos {produtos[nome]['estoque']} unidades.")
            return
        
        if nome in carrinho:
            carrinho[nome] += quant
        else:
            carrinho[nome] = quant
        
        atualizar_carrinho()
        entry_quant.delete(0, tk.END)
    
    def remover_do_carrinho():
        try:
            idx = lista_carrinho.curselection()[0]
        except IndexError:
            messagebox.showwarning("Aviso", "Selecione um item do carrinho para remover.")
            return
        item = lista_carrinho.get(idx)
        nome = item.split(" x")[0]
        del carrinho[nome]
        atualizar_carrinho()
    
    def finalizar_compra():
        if not carrinho:
            messagebox.showwarning("Aviso", "Seu carrinho está vazio!")
            return
        
        total = 0
        for nome, quant in carrinho.items():
            if quant > produtos[nome]["estoque"]:
                messagebox.showerror("Erro", f"Estoque insuficiente para {nome}. Ajuste a quantidade.")
                return
            total += produtos[nome]["preco"] * quant
        
        confirmar = messagebox.askyesno("Confirmar Compra", f"O total é R${total:.2f}. Deseja finalizar?")
        if confirmar:
            for nome, quant in carrinho.items():
                produtos[nome]["estoque"] -= quant
            messagebox.showinfo("Compra Finalizada", "Obrigado pela compra!")
            carrinho.clear()
            atualizar_carrinho()
            atualizar_lista_itens()
    
    frame_botoes = tk.Frame(root)
    frame_botoes.pack(pady=10)
    
    tk.Button(frame_botoes, text="Adicionar ao Carrinho", command=adicionar_ao_carrinho).grid(row=0, column=0, padx=5)
    tk.Button(frame_botoes, text="Remover do Carrinho", command=remover_do_carrinho).grid(row=0, column=1, padx=5)
    tk.Button(frame_botoes, text="Finalizar Compra", command=finalizar_compra).grid(row=0, column=2, padx=5)
    tk.Button(root, text="Voltar", command=mostrar_tela_inicial).pack(pady=20)

root = tk.Tk()
root.title("Loja Virtual")
root.geometry("500x600")

mostrar_tela_inicial()

root.mainloop()