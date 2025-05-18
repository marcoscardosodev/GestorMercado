"""
Módulo para armazenamento centralizado dos dados da aplicação
"""

# Dicionário de produtos disponíveis na loja
produtos = {
    "Arroz": {"preco": 5.50, "estoque": 10},
    "Feijão": {"preco": 7.00, "estoque": 8},
    "Macarrão": {"preco": 4.00, "estoque": 15},
    "Leite": {"preco": 3.20, "estoque": 15},
    "Pão": {"preco": 1.50, "estoque": 20},
    "Refrigerante": {"preco": 4.00, "estoque": 12},
    "Sabão": {"preco": 2.00, "estoque": 8}
}

# Carrinho de compras (inicialmente vazio)
carrinho = {}

# Senha do administrador
ADMIN_CREDENCIAIS = {
    "usuario": "admin",
    "senha": "1234"
}