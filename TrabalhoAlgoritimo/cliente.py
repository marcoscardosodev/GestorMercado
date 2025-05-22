import tkinter as tk
from tkinter import messagebox
from dados import produtos as produtos_disponiveis

class ClientePage(tk.Tk):
    def __init__(self):
        super().__init__()
        # Configurações da janela
        self.title("Cliente - Mercado")
        self.geometry("600x750")
        self.configure(bg="#e8f5e9")

        # Frame principal
        self.main_frame = tk.Frame(self, bg="#e8f5e9")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Label de título
        tk.Label(self.main_frame, text="Faça suas compras", font=("Helvetica", 16, "bold"), 
                bg="#e8f5e9", fg="#2e7d32").pack(pady=15)

        # Lista de produtos
        tk.Label(self.main_frame, text="Produtos Disponíveis:", bg="#e8f5e9", 
                font=("Arial", 12, "bold"), fg="#388e3c").pack()
        
        self.lista_produtos = tk.Listbox(self.main_frame, font=("Arial", 12), height=7, 
                                       bg="#c8e6c9", fg="#1b5e20", relief=tk.SOLID, borderwidth=1)
        self.lista_produtos.pack(padx=20, pady=5, fill=tk.X)
        self.atualizar_lista()  # Preenche a lista com produtos

        # Campo de quantidade
        tk.Label(self.main_frame, text="Quantidade:", bg="#e8f5e9", font=("Arial", 12)).pack(pady=(15, 0))
        self.entry_quantidade = tk.Entry(self.main_frame, font=("Arial", 12), width=10)
        self.entry_quantidade.pack(pady=5)

        # Botão para adicionar ao carrinho
        self.btn_comprar = tk.Button(
            self.main_frame, 
            text="Adicionar ao Carrinho", 
            font=("Arial", 12, "bold"), 
            bg="#66bb6a", 
            fg="white", 
            command=self.adicionar_carrinho
        )
        self.btn_comprar.pack(pady=15)

        # Seção do carrinho
        tk.Label(self.main_frame, text="Carrinho:", bg="#e8f5e9", 
                font=("Arial", 12, "bold"), fg="#2e7d32").pack(pady=(10,0))
        
        self.lista_carrinho = tk.Listbox(self.main_frame, font=("Arial", 12), height=7, 
                                       bg="#c8e6c9", fg="#1b5e20", relief=tk.SOLID, borderwidth=1)
        self.lista_carrinho.pack(padx=20, pady=5, fill=tk.X)

        # Frame para botões do carrinho
        self.frame_botoes_carrinho = tk.Frame(self.main_frame, bg="#e8f5e9")
        self.frame_botoes_carrinho.pack(pady=10)

        # Botões de ação do carrinho
        self.btn_remover = tk.Button(
            self.frame_botoes_carrinho, 
            text="Remover Item", 
            font=("Arial", 12, "bold"), 
            bg="#ff7043", 
            fg="white", 
            command=self.remover_item
        )
        self.btn_remover.pack(side=tk.LEFT, padx=5)

        self.btn_limpar = tk.Button(
            self.frame_botoes_carrinho, 
            text="Limpar Carrinho", 
            font=("Arial", 12, "bold"), 
            bg="#ef5350", 
            fg="white", 
            command=self.limpar_carrinho
        )
        self.btn_limpar.pack(side=tk.LEFT, padx=5)

        self.btn_finalizar = tk.Button(
            self.frame_botoes_carrinho, 
            text="Finalizar Compra", 
            font=("Arial", 12, "bold"), 
            bg="#388e3c", 
            fg="white", 
            command=self.finalizar_compra
        )
        self.btn_finalizar.pack(side=tk.LEFT, padx=5)

        # Botão para voltar ao login
        self.btn_voltar = tk.Button(
            self.main_frame,
            text="Voltar ao Login",
            font=("Arial", 12, "bold"), 
            bg="#c62828", 
            fg="white",
            command=self.voltar_login
        )
        self.btn_voltar.pack(pady=5)

        self.carrinho = {}  # Dicionário para armazenar os itens do carrinho

    def voltar_login(self):
        """Fecha a janela atual e retorna para a página de login"""
        self.destroy()
        from login import LoginPage
        LoginPage().mainloop()

    def atualizar_lista(self):
        """Atualiza a lista de produtos disponíveis"""
        self.lista_produtos.delete(0, tk.END)  # Limpa a lista
        # Adiciona cada produto com suas informações
        for produto, info in produtos_disponiveis.items():
            self.lista_produtos.insert(tk.END, f"{produto} - R${info['preco']:.2f} - Estoque: {info['estoque']}")

    def adicionar_carrinho(self):
        """Adiciona um item selecionado ao carrinho"""
        selecionado = self.lista_produtos.curselection()  # Obtém o item selecionado
        if not selecionado:  # Verifica se há seleção
            messagebox.showwarning("Aviso", "Selecione um produto!")
            return

        produto = list(produtos_disponiveis.keys())[selecionado[0]]  # Obtém o nome do produto
        
        try:  # Valida a quantidade
            quantidade = int(self.entry_quantidade.get())
            if quantidade <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Informe uma quantidade válida!")
            return

        # Verifica estoque
        estoque_atual = produtos_disponiveis[produto]['estoque']
        if quantidade > estoque_atual:
            messagebox.showerror("Erro", f"Quantidade indisponível. Estoque atual: {estoque_atual}")
            return

        # Adiciona ao carrinho ou incrementa quantidade
        if produto in self.carrinho:
            self.carrinho[produto] += quantidade
        else:
            self.carrinho[produto] = quantidade

        self.atualizar_carrinho()  # Atualiza a exibição
        self.entry_quantidade.delete(0, tk.END)  # Limpa o campo de quantidade

    def atualizar_carrinho(self):
        """Atualiza a visualização do carrinho"""
        self.lista_carrinho.delete(0, tk.END)
        for produto, qtd in self.carrinho.items():
            preco_unit = produtos_disponiveis[produto]['preco']
            total = preco_unit * qtd
            self.lista_carrinho.insert(tk.END, f"{produto} - Quantidade: {qtd} - Total: R${total:.2f}")

    def finalizar_compra(self):
        """Processa a compra e atualiza o estoque"""
        if not self.carrinho:  # Verifica se o carrinho está vazio
            messagebox.showinfo("Carrinho Vazio", "Adicione produtos antes de finalizar a compra.")
            return

        valor_total = 0
        for produto, qtd in self.carrinho.items():
            preco = produtos_disponiveis[produto]['preco']
            valor_total += preco * qtd
            produtos_disponiveis[produto]['estoque'] -= qtd  # Atualiza estoque

        messagebox.showinfo("Compra Finalizada", f"Obrigado pela compra! \nValor total: R${valor_total:.2f}")
        self.limpar_carrinho()  # Limpa o carrinho
        self.atualizar_lista()  # Atualiza a lista de produtos

    def limpar_carrinho(self):
        """Limpa o carrinho"""
        self.carrinho.clear()
        self.atualizar_carrinho()
        messagebox.showinfo("Carrinho Limpo", "Seu carrinho foi esvaziado.")

    def remover_item(self):
        """Remove um item específico do carrinho"""
        selecionado = self.lista_carrinho.curselection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um item para remover!")
            return

        texto_item = self.lista_carrinho.get(selecionado[0])
        produto = texto_item.split(" - ")[0]  # Extrai o nome do produto

        if produto in self.carrinho:
            del self.carrinho[produto]
            self.atualizar_carrinho()
            messagebox.showinfo("Item Removido", f"{produto} foi removido do carrinho.")