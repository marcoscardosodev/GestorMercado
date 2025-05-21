import tkinter as tk
from tkinter import messagebox
from dados import produtos as produtos_disponiveis

class ClientePage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cliente - Mercado")
        self.geometry("600x750") 
        self.configure(bg="#e8f5e9")
        self.resizable(False, False)

        # Frame principal para organização
        self.main_frame = tk.Frame(self, bg="#e8f5e9")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(self.main_frame, text="Faça suas compras", font=("Helvetica", 16, "bold"), bg="#e8f5e9", fg="#2e7d32").pack(pady=15)

        # Seção de produtos disponíveis
        tk.Label(self.main_frame, text="Produtos Disponíveis:", bg="#e8f5e9", font=("Arial", 12, "bold"), fg="#388e3c").pack()
        self.lista_produtos = tk.Listbox(self.main_frame, font=("Arial", 12), height=7, bg="#c8e6c9", fg="#1b5e20", relief=tk.SOLID, borderwidth=1)
        self.lista_produtos.pack(padx=20, pady=5, fill=tk.X)
        self.atualizar_lista()

        # Seção de quantidade
        tk.Label(self.main_frame, text="Quantidade:", bg="#e8f5e9", font=("Arial", 12)).pack(pady=(15, 0))
        self.entry_quantidade = tk.Entry(self.main_frame, font=("Arial", 12), width=10)
        self.entry_quantidade.pack(pady=5)

        # Botão de adicionar ao carrinho
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
        tk.Label(self.main_frame, text="Carrinho:", bg="#e8f5e9", font=("Arial", 12, "bold"), fg="#2e7d32").pack(pady=(10,0))
        self.lista_carrinho = tk.Listbox(self.main_frame, font=("Arial", 12), height=7, bg="#c8e6c9", fg="#1b5e20", relief=tk.SOLID, borderwidth=1)
        self.lista_carrinho.pack(padx=20, pady=5, fill=tk.X)

        # Frame para os botões de ação do carrinho
        self.frame_botoes_carrinho = tk.Frame(self.main_frame, bg="#e8f5e9")
        self.frame_botoes_carrinho.pack(pady=10)

        # Botão Remover Item Selecionado
        self.btn_remover = tk.Button(
            self.frame_botoes_carrinho, 
            text="Remover Item", 
            font=("Arial", 12, "bold"), 
            bg="#ff7043",  # Laranja para ação de remoção
            fg="white", 
            command=self.remover_item
        )
        self.btn_remover.pack(side=tk.LEFT, padx=5)

        # Botão Limpar Carrinho
        self.btn_limpar = tk.Button(
            self.frame_botoes_carrinho, 
            text="Limpar Carrinho", 
            font=("Arial", 12, "bold"), 
            bg="#ef5350",  # Vermelho para ação destrutiva
            fg="white", 
            command=self.limpar_carrinho
        )
        self.btn_limpar.pack(side=tk.LEFT, padx=5)

        # Botão Finalizar Compra
        self.btn_finalizar = tk.Button(
            self.frame_botoes_carrinho, 
            text="Finalizar Compra", 
            font=("Arial", 12, "bold"), 
            bg="#388e3c", 
            fg="white", 
            command=self.finalizar_compra
        )
        self.btn_finalizar.pack(side=tk.LEFT, padx=5)

        # Frame para o botão Voltar
        self.frame_botoes = tk.Frame(self.main_frame, bg="#e8f5e9")
        self.frame_botoes.pack(fill=tk.X, pady=10)

        # Botão Voltar ao Login
        self.btn_voltar = tk.Button(
            self.frame_botoes,
            text="Voltar ao Login",
            font=("Arial", 12, "bold"), 
            bg="#c62828",  # Vermelho escuro
            fg="white",
            command=self.voltar_login
        )
        self.btn_voltar.pack(pady=5)

        self.carrinho = {}

    def voltar_login(self):
        """Fecha a janela atual e retorna para a página de login"""
        self.destroy()
        from login import LoginPage
        LoginPage().mainloop()

    def atualizar_lista(self):
        self.lista_produtos.delete(0, tk.END)
        for produto, info in produtos_disponiveis.items():
            self.lista_produtos.insert(tk.END, f"{produto} - R${info['preco']:.2f} - Estoque: {info['estoque']}")

    def adicionar_carrinho(self):
        selecionado = self.lista_produtos.curselection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um produto!")
            return

        produto = list(produtos_disponiveis.keys())[selecionado[0]]
        try:
            quantidade = int(self.entry_quantidade.get())
            if quantidade <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Informe uma quantidade válida!")
            return

        estoque_atual = produtos_disponiveis[produto]['estoque']
        if quantidade > estoque_atual:
            messagebox.showerror("Erro", f"Quantidade indisponível. Estoque atual: {estoque_atual}")
            return

        if produto in self.carrinho:
            self.carrinho[produto] += quantidade
        else:
            self.carrinho[produto] = quantidade

        self.atualizar_carrinho()
        self.entry_quantidade.delete(0, tk.END)

    def atualizar_carrinho(self):
        self.lista_carrinho.delete(0, tk.END)
        for produto, qtd in self.carrinho.items():
            preco_unit = produtos_disponiveis[produto]['preco']
            total = preco_unit * qtd
            self.lista_carrinho.insert(tk.END, f"{produto} - Quantidade: {qtd} - Total: R${total:.2f}")

    def finalizar_compra(self):
        if not self.carrinho:
            messagebox.showinfo("Carrinho Vazio", "Adicione produtos antes de finalizar a compra.")
            return

        valor_total = 0
        for produto, qtd in self.carrinho.items():
            preco = produtos_disponiveis[produto]['preco']
            valor_total += preco * qtd
            produtos_disponiveis[produto]['estoque'] -= qtd

        messagebox.showinfo("Compra Finalizada", f"Obrigado pela compra! \nValor total: R${valor_total:.2f}")
        self.limpar_carrinho()
        self.atualizar_lista()

    def limpar_carrinho(self):
        """Limpa o carrinho sem finalizar a compra"""
        self.carrinho.clear()
        self.atualizar_carrinho()
        messagebox.showinfo("Carrinho Limpo", "Seu carrinho foi esvaziado.")

    def remover_item(self):
        """Remove o item selecionado do carrinho"""
        selecionado = self.lista_carrinho.curselection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um item para remover!")
            return

        # Obtém o nome do produto a partir do texto no carrinho
        texto_item = self.lista_carrinho.get(selecionado[0])
        produto = texto_item.split(" - ")[0]  # Extrai o nome do produto

        if produto in self.carrinho:
            del self.carrinho[produto]
            self.atualizar_carrinho()
            messagebox.showinfo("Item Removido", f"{produto} foi removido do carrinho.")
        else:
            messagebox.showerror("Erro", "Item não encontrado no carrinho!")


if __name__ == "__main__":
    app = ClientePage()
    app.mainloop()