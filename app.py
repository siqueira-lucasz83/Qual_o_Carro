import os
from flask import Flask, session
from Conexao import conectar
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializa o Flask e configura a chave de sessão
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'uma-chave-secreta-padrao')

# Estabelece conexão com o banco de dados
try:
    conexao = conectar()
    if not conexao:
        raise ConnectionError("Não foi possível conectar ao banco de dados.")
    app.conexao = conexao
except Exception as e:
    print(f"Erro ao conectar ao banco de dados: {e}")
    app.conexao = None

# Importa rotas após a criação do app para evitar importações circulares
from routes import *

# Executa o servidor Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
