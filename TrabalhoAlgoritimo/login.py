import tkinter as tk
from tkinter import messagebox
from admin import AdminPage
from cliente import ClientePage
from dados import ADMIN_CREDENCIAIS

class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login - Mercado")
        self.geometry("400x300")
        self.configure(bg="#e3f2fd")
        self.resizable(False, False)

        self.label_intro = tk.Label(self, text="Você é Administrador ou Cliente?", 
                                  bg="#e3f2fd", font=("Helvetica", 14, "bold"))
        self.label_intro.pack(pady=20)

        self.frame_buttons = tk.Frame(self, bg="#e3f2fd")
        self.frame_buttons.pack(pady=10)

        btn_admin = tk.Button(self.frame_buttons, text="Administrador", width=15, command=self.show_login)
        btn_admin.grid(row=0, column=0, padx=10)

        btn_cliente = tk.Button(self.frame_buttons, text="Cliente", width=15, command=self.login_cliente)
        btn_cliente.grid(row=0, column=1, padx=10)

        self.frame_login = tk.Frame(self, bg="#bbdefb", padx=20, pady=20, relief=tk.RIDGE, borderwidth=2)
        
        tk.Label(self.frame_login, text="Usuário:", bg="#bbdefb", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        self.entry_usuario = tk.Entry(self.frame_login, font=("Arial", 12))
        self.entry_usuario.grid(row=0, column=1, pady=5)

        tk.Label(self.frame_login, text="Senha:", bg="#bbdefb", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
        self.entry_senha = tk.Entry(self.frame_login, font=("Arial", 12), show="*")
        self.entry_senha.grid(row=1, column=1, pady=5)

        self.btn_login = tk.Button(self.frame_login, text="Entrar", width=15, command=self.verificar_login, bg="#64b5f6", fg="white", font=("Arial", 12, "bold"))
        self.btn_login.grid(row=2, column=0, columnspan=2, pady=15)

    def show_login(self):
        self.frame_login.pack(pady=20)

    def verificar_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        if usuario == ADMIN_CREDENCIAIS["usuario"] and senha == ADMIN_CREDENCIAIS["senha"]:
            messagebox.showinfo("Login", "Login de administrador realizado com sucesso!")
            self.destroy()
            AdminPage().mainloop()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos!")

    def login_cliente(self):
        self.destroy()
        ClientePage().mainloop()

if __name__ == "__main__":
    app = LoginPage()
    app.mainloop()