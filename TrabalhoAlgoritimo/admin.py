import tkinter as tk
from tkinter import messagebox
from dados import produtos as produtos_disponiveis

class AdminPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Área do Administrador")
        self.geometry("450x400")
        self.configure(bg="#fce4ec")
        self.resizable(False, False)

        tk.Label(self, text="Gerenciamento de Produtos", font=("Helvetica", 16, "bold"), bg="#fce4ec").pack(pady=15)

        self.frame_lista = tk.Frame(self, bg="#f8bbd0", relief=tk.RIDGE, borderwidth=2)
        self.frame_lista.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.lista_produtos = tk.Listbox(self.frame_lista, font=("Arial", 12), bg="#fce4ec", fg="#880e4f", height=10)
        self.lista_produtos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10,0), pady=10)
        self.atualizar_lista()

        self.scrollbar = tk.Scrollbar(self.frame_lista, command=self.lista_produtos.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=10)
        self.lista_produtos.config(yscrollcommand=self.scrollbar.set)

        self.frame_edicao = tk.Frame(self, bg="#fce4ec")
        self.frame_edicao.pack(pady=10)

        tk.Label(self.frame_edicao, text="Produto:", bg="#fce4ec", font=("Arial", 12)).grid(row=0, column=0, sticky="e", pady=5)
        self.entry_produto = tk.Entry(self.frame_edicao, font=("Arial", 12), width=20)
        self.entry_produto.grid(row=0, column=1, pady=5)

        tk.Label(self.frame_edicao, text="Preço:", bg="#fce4ec", font=("Arial", 12)).grid(row=1, column=0, sticky="e", pady=5)
        self.entry_preco = tk.Entry(self.frame_edicao, font=("Arial", 12), width=20)
        self.entry_preco.grid(row=1, column=1, pady=5)

        tk.Label(self.frame_edicao, text="Estoque:", bg="#fce4ec", font=("Arial", 12)).grid(row=2, column=0, sticky="e", pady=5)
        self.entry_estoque = tk.Entry(self.frame_edicao, font=("Arial", 12), width=20)
        self.entry_estoque.grid(row=2, column=1, pady=5)

        self.btn_adicionar = tk.Button(self.frame_edicao, text="Adicionar / Atualizar", command=self.adicionar_atualizar_produto, bg="#ec407a", fg="white", font=("Arial", 12, "bold"))
        self.btn_adicionar.grid(row=3, column=0, columnspan=2, pady=15)

        self.lista_produtos.bind("<<ListboxSelect>>", self.preencher_campos)

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
        self.entry_estoque.delete(0, tk.END)
        self.entry_estoque.insert(0, str(info['estoque']))

    def adicionar_atualizar_produto(self):
        produto = self.entry_produto.get().strip()
        preco = self.entry_preco.get().strip()
        estoque = self.entry_estoque.get().strip()

        if not produto or not preco or not estoque:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
        try:
            preco = float(preco)
            estoque = int(estoque)
        except ValueError:
            messagebox.showerror("Erro", "Preço deve ser número decimal e estoque deve ser inteiro!")
            return

        produtos_disponiveis[produto] = {'preco': preco, 'estoque': estoque}
        self.atualizar_lista()
        messagebox.showinfo("Sucesso", f"Produto '{produto}' adicionado/atualizado com sucesso!")
        self.entry_produto.delete(0, tk.END)
        self.entry_preco.delete(0, tk.END)
        self.entry_estoque.delete(0, tk.END)

if __name__ == "__main__":
    app = AdminPage()
    app.mainloop()