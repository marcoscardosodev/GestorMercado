import tkinter as tk  # Importa a biblioteca tkinter para GUI
from tkinter import messagebox  # Importa o módulo messagebox para exibir alertas
from admin import AdminPage  # Importa a classe AdminPage
from cliente import ClientePage  # Importa a classe ClientePage
from dados import ADMIN_CREDENCIAIS  # Importa as credenciais do admin

class LoginPage(tk.Tk):  # Define a classe principal herdando de tk.Tk
    def __init__(self):  # Método construtor
        super().__init__()  # Chama o construtor da classe pai (tk.Tk)
        self.title("Login - Mercado")  # Define o título da janela
        self.geometry("600x400")  # Define o tamanho da janela
        self.configure(bg="#e3f2fd")  # Configura cor de fundo
        self.resizable(False, False)  # Impede redimensionamento

        # Frame principal para centralizar conteúdo
        self.main_frame = tk.Frame(self, bg="#e3f2fd")
        self.main_frame.pack(expand=True)

        # Label com texto de introdução
        self.label_intro = tk.Label(self.main_frame, text="Você é Administrador ou Cliente?", 
                                  bg="#e3f2fd", font=("Helvetica", 14, "bold"))
        self.label_intro.pack(pady=20)

        # Frame para os botões de escolha
        self.frame_buttons = tk.Frame(self.main_frame, bg="#e3f2fd")
        self.frame_buttons.pack(pady=10)

        # Botão para administrador
        btn_admin = tk.Button(self.frame_buttons, text="Administrador", width=15, command=self.show_login)
        btn_admin.grid(row=0, column=0, padx=10)

        # Botão para cliente
        btn_cliente = tk.Button(self.frame_buttons, text="Cliente", width=15, command=self.login_cliente)
        btn_cliente.grid(row=0, column=1, padx=10)

        # Frame para o formulário de login (inicialmente oculto)
        self.frame_login = tk.Frame(self.main_frame, bg="#bbdefb", padx=20, pady=20, relief=tk.RIDGE, borderwidth=2)
        
        # Label e Entry para usuário
        tk.Label(self.frame_login, text="Usuário:", bg="#bbdefb", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        self.entry_usuario = tk.Entry(self.frame_login, font=("Arial", 12))
        self.entry_usuario.grid(row=0, column=1, pady=5)

        # Label e Entry para senha
        tk.Label(self.frame_login, text="Senha:", bg="#bbdefb", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
        self.entry_senha = tk.Entry(self.frame_login, font=("Arial", 12), show="*")
        self.entry_senha.grid(row=1, column=1, pady=5)

        # Botão de login
        self.btn_login = tk.Button(self.frame_login, text="Entrar", width=15, command=self.verificar_login, 
                                   bg="#64b5f6", fg="white", font=("Arial", 12, "bold"))
        self.btn_login.grid(row=2, column=0, columnspan=2, pady=15)

    def show_login(self):  # Mostra o formulário de login
        self.frame_login.pack(pady=20)

    def verificar_login(self):  # Valida as credenciais
        usuario = self.entry_usuario.get()  # Obtém o usuário digitado
        senha = self.entry_senha.get()  # Obtém a senha digitada
        
        # Verifica se as credenciais são válidas
        if usuario == ADMIN_CREDENCIAIS["usuario"] and senha == ADMIN_CREDENCIAIS["senha"]:
            messagebox.showinfo("Login", "Login de administrador realizado com sucesso!")
            self.destroy()  # Fecha a janela atual
            AdminPage().mainloop()  # Abre a interface do admin
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos!")

    def login_cliente(self):  # Redireciona para a interface do cliente
        self.destroy()  # Fecha a janela atual
        ClientePage().mainloop()  # Abre a interface do cliente

if __name__ == "__main__":  # Execução direta do arquivo
    app = LoginPage()
    app.mainloop()