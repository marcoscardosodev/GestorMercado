import tkinter as tk
from tkinter import messagebox
from dados import produtos as produtos_disponiveis

class AdminPage(tk.Tk):
    def __init__(self):
        super().__init__()
        # Configuração inicial da janela
        self.title("Área do Administrador")  # Título da janela
        self.geometry("600x750")  # Define tamanho fixo da janela
        self.configure(bg="#fce4ec")  # Cor de fundo rosa claro

        # Frame principal que organiza todo o conteúdo
        self.main_frame = tk.Frame(self, bg="#fce4ec")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Label com título da página
        tk.Label(self.main_frame, text="Gerenciamento de Produtos", 
                font=("Helvetica", 16, "bold"), bg="#fce4ec").pack(pady=15)

        # Frame que contém a lista de produtos e scrollbar
        self.frame_lista = tk.Frame(self.main_frame, bg="#f8bbd0", relief=tk.RIDGE, borderwidth=2)
        self.frame_lista.pack(fill=tk.BOTH, expand=True, pady=10)

        # Listbox que mostra todos os produtos disponíveis
        self.lista_produtos = tk.Listbox(self.frame_lista, font=("Arial", 12), 
                                       bg="#fce4ec", fg="#880e4f", height=8)
        self.lista_produtos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10,0), pady=10)
        self.atualizar_lista()  # Preenche a lista com os produtos

        # Scrollbar para navegar na lista de produtos
        self.scrollbar = tk.Scrollbar(self.frame_lista, command=self.lista_produtos.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        self.lista_produtos.config(yscrollcommand=self.scrollbar.set)

        # Frame que contém os campos de edição
        self.frame_edicao = tk.Frame(self.main_frame, bg="#fce4ec")
        self.frame_edicao.pack(pady=10)

        # Label e Entry para o nome do produto
        tk.Label(self.frame_edicao, text="Produto:", bg="#fce4ec", 
                font=("Arial", 12)).grid(row=0, column=0, sticky="e", pady=5)
        self.entry_produto = tk.Entry(self.frame_edicao, font=("Arial", 12), width=20)
        self.entry_produto.grid(row=0, column=1, pady=5)

        # Label e Entry para o preço do produto
        tk.Label(self.frame_edicao, text="Preço:", bg="#fce4ec", 
                font=("Arial", 12)).grid(row=1, column=0, sticky="e", pady=5)
        self.entry_preco = tk.Entry(self.frame_edicao, font=("Arial", 12), width=20)
        self.entry_preco.grid(row=1, column=1, pady=5)

        # Label para o estoque
        tk.Label(self.frame_edicao, text="Estoque:", bg="#fce4ec", 
                font=("Arial", 12)).grid(row=2, column=0, sticky="e", pady=5)
        
        # Frame que contém o spinbox e botão para ajuste de estoque
        self.frame_estoque = tk.Frame(self.frame_edicao, bg="#fce4ec")
        self.frame_estoque.grid(row=2, column=1, pady=5)
        
        # Spinbox para ajustar o estoque (valores de 0 a 1000)
        self.spin_estoque = tk.Spinbox(self.frame_estoque, from_=0, to=1000, width=5, font=("Arial", 12))
        self.spin_estoque.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botão para aplicar o ajuste de estoque
        self.btn_aplicar_estoque = tk.Button(
            self.frame_estoque, 
            text="Aplicar", 
            command=self.aplicar_ajuste_estoque,
            bg="#ec407a",  # Cor rosa
            fg="white", 
            font=("Arial", 10, "bold")
        )
        self.btn_aplicar_estoque.pack(side=tk.LEFT)

        # Frame para os botões principais (Adicionar/Remover)
        self.frame_botoes_acao = tk.Frame(self.frame_edicao, bg="#fce4ec")
        self.frame_botoes_acao.grid(row=3, column=0, columnspan=2, pady=15)

        # Botão para adicionar ou atualizar produto
        self.btn_adicionar = tk.Button(
            self.frame_botoes_acao, 
            text="Adicionar / Atualizar", 
            command=self.adicionar_atualizar_produto, 
            bg="#ec407a", 
            fg="white", 
            font=("Arial", 12, "bold"),
            width=15
        )
        self.btn_adicionar.pack(side=tk.LEFT, padx=5)

        # Botão para remover produto
        self.btn_remover = tk.Button(
            self.frame_botoes_acao, 
            text="Remover", 
            command=self.remover_produto, 
            bg="#c62828",  # Cor vermelha
            fg="white", 
            font=("Arial", 12, "bold"),
            width=15
        )
        self.btn_remover.pack(side=tk.LEFT, padx=5)

        # Frame para o botão de voltar
        self.frame_botoes = tk.Frame(self.main_frame, bg="#fce4ec")
        self.frame_botoes.pack(fill=tk.X, pady=10)

        # Botão para voltar à tela de login
        self.btn_voltar = tk.Button(
            self.frame_botoes,
            text="Voltar ao Login",
            command=self.voltar_login,
            bg="#c62828",  # Vermelho escuro
            fg="white",
            font=("Arial", 12, "bold"),
            width=15
        )
        self.btn_voltar.pack(pady=5)

        # Vincula o evento de seleção na lista à função preencher_campos
        self.lista_produtos.bind("<<ListboxSelect>>", self.preencher_campos)

    def voltar_login(self):
        """Fecha a janela atual e abre a tela de login"""
        self.destroy()  # Fecha a janela do admin
        from login import LoginPage
        LoginPage().mainloop()  # Abre a tela de login

    def atualizar_lista(self):
        """Atualiza a lista de produtos com os dados atuais"""
        self.lista_produtos.delete(0, tk.END)  # Limpa a lista
        # Para cada produto no dicionário, adiciona na lista formatado
        for produto, info in produtos_disponiveis.items():
            self.lista_produtos.insert(tk.END, f"{produto} - R${info['preco']:.2f} - Estoque: {info['estoque']}")

    def preencher_campos(self, event):
        """Preenche os campos de edição quando um produto é selecionado"""
        if not self.lista_produtos.curselection():  # Se nada estiver selecionado
            return
            
        # Obtém o índice e nome do produto selecionado
        index = self.lista_produtos.curselection()[0]
        produto = list(produtos_disponiveis.keys())[index]
        info = produtos_disponiveis[produto]  # Informações do produto
        
        # Preenche os campos com os valores do produto
        self.entry_produto.delete(0, tk.END)
        self.entry_produto.insert(0, produto)  # Nome
        
        self.entry_preco.delete(0, tk.END)
        self.entry_preco.insert(0, str(info['preco']))  # Preço
        
        # Configura o spinbox com o valor atual do estoque
        self.spin_estoque.delete(0, tk.END)
        self.spin_estoque.insert(0, str(info['estoque']))

    def aplicar_ajuste_estoque(self):
        """Aplica o ajuste de estoque para o produto selecionado"""
        if not self.lista_produtos.curselection():  # Verifica se há produto selecionado
            messagebox.showwarning("Aviso", "Selecione um produto primeiro!")
            return
            
        try:
            # Converte e valida o valor do estoque
            novo_estoque = int(self.spin_estoque.get())
            if novo_estoque < 0:  # Não permite estoque negativo
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "O estoque deve ser um número inteiro positivo!")
            return
            
        produto = self.entry_produto.get().strip()  # Obtém o nome do produto
        if produto not in produtos_disponiveis:  # Verifica se o produto existe
            messagebox.showerror("Erro", "Produto não encontrado!")
            return
            
        # Atualiza o estoque e a lista
        produtos_disponiveis[produto]['estoque'] = novo_estoque
        self.atualizar_lista()
        messagebox.showinfo("Sucesso", f"Estoque de {produto} atualizado para {novo_estoque}")

    def adicionar_atualizar_produto(self):
        """Adiciona um novo produto ou atualiza um existente"""
        # Obtém os valores dos campos
        produto = self.entry_produto.get().strip()
        preco = self.entry_preco.get().strip()
        estoque = self.spin_estoque.get().strip()

        # Valida se todos os campos foram preenchidos
        if not produto or not preco or not estoque:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
            
        try:
            # Converte e valida os valores
            preco = float(preco)  # Converte para float
            estoque = int(estoque)  # Converte para inteiro
            if preco <= 0 or estoque < 0:  # Valida valores positivos
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Preço deve ser número positivo e estoque deve ser inteiro não negativo!")
            return

        # Adiciona/atualiza o produto no dicionário
        produtos_disponiveis[produto] = {'preco': preco, 'estoque': estoque}
        self.atualizar_lista()  # Atualiza a lista
        messagebox.showinfo("Sucesso", f"Produto '{produto}' adicionado/atualizado com sucesso!")
        
        # Limpa os campos após a operação
        self.entry_produto.delete(0, tk.END)
        self.entry_preco.delete(0, tk.END)
        self.spin_estoque.delete(0, tk.END)
        self.spin_estoque.insert(0, "0")  # Define valor padrão

    def remover_produto(self):
        """Remove um produto do sistema"""
        if not self.lista_produtos.curselection():  # Verifica seleção
            messagebox.showwarning("Aviso", "Selecione um produto para remover!")
            return
            
        produto = self.entry_produto.get().strip()  # Obtém nome do produto
        if produto not in produtos_disponiveis:  # Verifica existência
            messagebox.showerror("Erro", "Produto não encontrado!")
            return
            
        # Pede confirmação antes de remover
        resposta = messagebox.askyesno("Confirmar", f"Tem certeza que deseja remover o produto '{produto}'?")
        if resposta:
            del produtos_disponiveis[produto]  # Remove o produto
            self.atualizar_lista()  # Atualiza a lista
            messagebox.showinfo("Sucesso", f"Produto '{produto}' removido com sucesso!")
            
            # Limpa os campos
            self.entry_produto.delete(0, tk.END)
            self.entry_preco.delete(0, tk.END)
            self.spin_estoque.delete(0, tk.END)
            self.spin_estoque.insert(0, "0")

if __name__ == "__main__":
    app = AdminPage()
    app.mainloop()