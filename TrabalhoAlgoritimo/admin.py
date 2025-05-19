import tkinter as tk
from tkinter import messagebox
from dados import produtos as produtos_disponiveis

class AdminPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Área do Administrador")
        self.geometry("600x700")  # Aumentei a altura para 700 para acomodar o botão Voltar
        self.configure(bg="#fce4ec")
        self.resizable(False, False)

        # Frame principal para organização
        self.main_frame = tk.Frame(self, bg="#fce4ec")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(self.main_frame, text="Gerenciamento de Produtos", font=("Helvetica", 16, "bold"), bg="#fce4ec").pack(pady=15)

        # Frame da lista de produtos
        self.frame_lista = tk.Frame(self.main_frame, bg="#f8bbd0", relief=tk.RIDGE, borderwidth=2)
        self.frame_lista.pack(fill=tk.BOTH, expand=True, pady=10)

        self.lista_produtos = tk.Listbox(self.frame_lista, font=("Arial", 12), bg="#fce4ec", fg="#880e4f", height=8)
        self.lista_produtos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10,0), pady=10)
        self.atualizar_lista()

        self.scrollbar = tk.Scrollbar(self.frame_lista, command=self.lista_produtos.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        self.lista_produtos.config(yscrollcommand=self.scrollbar.set)

        # Frame de edição
        self.frame_edicao = tk.Frame(self.main_frame, bg="#fce4ec")
        self.frame_edicao.pack(pady=10)

        # Labels e Entrys
        tk.Label(self.frame_edicao, text="Produto:", bg="#fce4ec", font=("Arial", 12)).grid(row=0, column=0, sticky="e", pady=5)
        self.entry_produto = tk.Entry(self.frame_edicao, font=("Arial", 12), width=20)
        self.entry_produto.grid(row=0, column=1, pady=5)

        tk.Label(self.frame_edicao, text="Preço:", bg="#fce4ec", font=("Arial", 12)).grid(row=1, column=0, sticky="e", pady=5)
        self.entry_preco = tk.Entry(self.frame_edicao, font=("Arial", 12), width=20)
        self.entry_preco.grid(row=1, column=1, pady=5)

        tk.Label(self.frame_edicao, text="Estoque:", bg="#fce4ec", font=("Arial", 12)).grid(row=2, column=0, sticky="e", pady=5)
        
        # Frame para o Spinbox e botão de atualização
        self.frame_estoque = tk.Frame(self.frame_edicao, bg="#fce4ec")
        self.frame_estoque.grid(row=2, column=1, pady=5)
        
        # Spinbox para ajuste do estoque
        self.spin_estoque = tk.Spinbox(self.frame_estoque, from_=0, to=1000, width=5, font=("Arial", 12))
        self.spin_estoque.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botão para aplicar o ajuste
        self.btn_aplicar_estoque = tk.Button(
            self.frame_estoque, 
            text="Aplicar", 
            command=self.aplicar_ajuste_estoque,
            bg="#ec407a", 
            fg="white", 
            font=("Arial", 10, "bold")
        )
        self.btn_aplicar_estoque.pack(side=tk.LEFT)

        # Botão principal
        self.btn_adicionar = tk.Button(
            self.frame_edicao, 
            text="Adicionar / Atualizar", 
            command=self.adicionar_atualizar_produto, 
            bg="#ec407a", 
            fg="white", 
            font=("Arial", 12, "bold")
        )
        self.btn_adicionar.grid(row=3, column=0, columnspan=2, pady=15)

        # Frame para o botão Voltar
        self.frame_botoes = tk.Frame(self.main_frame, bg="#fce4ec")
        self.frame_botoes.pack(fill=tk.X, pady=10)

        # Botão Voltar
        self.btn_voltar = tk.Button(
            self.frame_botoes,
            text="Voltar ao Login",
            command=self.voltar_login,
            bg="#c62828",  # Vermelho escuro para destaque
            fg="white",
            font=("Arial", 12, "bold"),
            width=15
        )
        self.btn_voltar.pack(pady=5)

        # Vincular evento de seleção na lista
        self.lista_produtos.bind("<<ListboxSelect>>", self.preencher_campos)

    def voltar_login(self):
        """Fecha a janela atual e retorna para a página de login"""
        self.destroy()
        from login import LoginPage
        LoginPage().mainloop()

    def atualizar_lista(self):
        self.lista_produtos.delete(0, tk.END)
        for produto, info in produtos_disponiveis.items():
            self.lista_produtos.insert(tk.END, f"{produto} - R${info['preco']:.2f} - Estoque: {info['estoque']}")

    def preencher_campos(self, event):
        if not self.lista_produtos.curselection():
            return
            
        index = self.lista_produtos.curselection()[0]
        produto = list(produtos_disponiveis.keys())[index]
        info = produtos_disponiveis[produto]
        
        self.entry_produto.delete(0, tk.END)
        self.entry_produto.insert(0, produto)
        
        self.entry_preco.delete(0, tk.END)
        self.entry_preco.insert(0, str(info['preco']))
        
        # Configura o Spinbox com o valor atual do estoque
        self.spin_estoque.delete(0, tk.END)
        self.spin_estoque.insert(0, str(info['estoque']))

    def aplicar_ajuste_estoque(self):
        if not self.lista_produtos.curselection():
            messagebox.showwarning("Aviso", "Selecione um produto primeiro!")
            return
            
        try:
            novo_estoque = int(self.spin_estoque.get())
            if novo_estoque < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "O estoque deve ser um número inteiro positivo!")
            return
            
        produto = self.entry_produto.get().strip()
        if produto not in produtos_disponiveis:
            messagebox.showerror("Erro", "Produto não encontrado!")
            return
            
        produtos_disponiveis[produto]['estoque'] = novo_estoque
        self.atualizar_lista()
        messagebox.showinfo("Sucesso", f"Estoque de {produto} atualizado para {novo_estoque}")

    def adicionar_atualizar_produto(self):
        produto = self.entry_produto.get().strip()
        preco = self.entry_preco.get().strip()
        estoque = self.spin_estoque.get().strip()

        if not produto or not preco or not estoque:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
            
        try:
            preco = float(preco)
            estoque = int(estoque)
            if preco <= 0 or estoque < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Preço deve ser número positivo e estoque deve ser inteiro não negativo!")
            return

        produtos_disponiveis[produto] = {'preco': preco, 'estoque': estoque}
        self.atualizar_lista()
        messagebox.showinfo("Sucesso", f"Produto '{produto}' adicionado/atualizado com sucesso!")
        
        # Limpa os campos após a operação
        self.entry_produto.delete(0, tk.END)
        self.entry_preco.delete(0, tk.END)
        self.spin_estoque.delete(0, tk.END)
        self.spin_estoque.insert(0, "0")

if __name__ == "__main__":
    app = AdminPage()
    app.mainloop()