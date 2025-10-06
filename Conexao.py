import mysql.connector
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Estabelece conexão com o banco de dados MySQL
def conectar():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )

# Busca veículo na tabela 'validacao' pelo modelo
def buscar_veiculo_por_modelo(conexao, modelo):
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM validacao WHERE LOWER(modelo) = %s", (modelo,))
    resultado = cursor.fetchone()
    cursor.fetchall()  # Limpa o buffer de resultados
    cursor.close()
    return resultado

# Insere dados validados na tabela 'validacoes_aprovadas'
def inserir_dados_validados(conexao, dados):
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO validacoes_aprovadas (marca, modelo, ano, potencia, carroceria)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        dados['marca'],
        dados['modelo'],
        dados['ano'],
        dados['potencia'],
        dados['carroceria']
    ))
    conexao.commit()
    cursor.close()

# Insere novo carro na tabela 'carros'
def inserir_carro(conexao, dados):
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO carros (marca, modelo, ano, potencia, carroceria)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        dados['marca'],
        dados['modelo'],
        dados['ano'],
        dados['potencia'],
        dados['carroceria']
    ))
    conexao.commit()
    cursor.close()

# Verifica se o modelo já existe na tabela 'carros'
def modelo_ja_existe(conexao, modelo):
    cursor = conexao.cursor()
    cursor.execute("SELECT COUNT(*) FROM carros WHERE LOWER(modelo) = %s", (modelo.lower(),))
    existe = cursor.fetchone()[0] > 0
    cursor.close()
    return existe
