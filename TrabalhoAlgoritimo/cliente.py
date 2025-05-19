import tkinter as tk
from tkinter import messagebox
from dados import produtos as produtos_disponiveis

class ClientePage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cliente - Mercado")
        self.geometry("600x650")
        self.configure(bg="#e8f5e9")
        self.resizable(False, False)

        tk.Label(self, text="Faça suas compras", font=("Helvetica", 16, "bold"), bg="#e8f5e9", fg="#2e7d32").pack(pady=15)

        tk.Label(self, text="Produtos Disponíveis:", bg="#e8f5e9", font=("Arial", 12, "bold"), fg="#388e3c").pack()
        self.lista_produtos = tk.Listbox(self, font=("Arial", 12), height=7, bg="#c8e6c9", fg="#1b5e20", relief=tk.SOLID, borderwidth=1)
        self.lista_produtos.pack(padx=20, pady=5, fill=tk.X)
        self.atualizar_lista()

        tk.Label(self, text="Quantidade:", bg="#e8f5e9", font=("Arial", 12)).pack(pady=(15, 0))
        self.entry_quantidade = tk.Entry(self, font=("Arial", 12), width=10)
        self.entry_quantidade.pack(pady=5)

        self.btn_comprar = tk.Button(self, text="Adicionar ao Carrinho", font=("Arial", 12, "bold"), bg="#66bb6a", fg="white", command=self.adicionar_carrinho)
        self.btn_comprar.pack(pady=15)

        tk.Label(self, text="Carrinho:", bg="#e8f5e9", font=("Arial", 12, "bold"), fg="#2e7d32").pack(pady=(10,0))
        self.lista_carrinho = tk.Listbox(self, font=("Arial", 12), height=7, bg="#c8e6c9", fg="#1b5e20", relief=tk.SOLID, borderwidth=1)
        self.lista_carrinho.pack(padx=20, pady=5, fill=tk.X)

        self.btn_finalizar = tk.Button(self, text="Finalizar Compra", font=("Arial", 12, "bold"), bg="#388e3c", fg="white", command=self.finalizar_compra)
        self.btn_finalizar.pack(pady=10)

        # Botão Voltar adicionado aqui
        self.btn_voltar = tk.Button(self, text="Voltar ao Login", font=("Arial", 12, "bold"), 
                                   bg="#c62828", fg="white", command=self.voltar_login)
        self.btn_voltar.pack(pady=10)

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
        self.carrinho.clear()
        self.atualizar_carrinho()
        self.atualizar_lista()


if __name__ == "__main__":
    app = ClientePage()
    app.mainloop()