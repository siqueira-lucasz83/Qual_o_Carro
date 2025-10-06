import mysql.connector
import bcrypt

# Cadastra um novo jogador no banco de dados
def cadastrar_jogador(conexao, nome, sobrenome, usuario, email, senha):
    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    cursor = conexao.cursor()
    try:
        cursor.execute(
            "INSERT INTO jogadores (nome, sobrenome, usuario, email, senha) VALUES (%s, %s, %s, %s, %s)",
            (nome, sobrenome, usuario, email, senha_hash)
        )
        conexao.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Erro ao cadastrar jogador: {err}")
        return False
    finally:
        cursor.close()

# Realiza login verificando usuário e senha
def login_jogador(conexao, usuario, senha):
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM jogadores WHERE usuario = %s", (usuario,))
    jogador = cursor.fetchone()
    cursor.close()
    if jogador and bcrypt.checkpw(senha.encode('utf-8'), jogador['senha'].encode('utf-8')):
        return jogador
    return None

# Retorna o ranking dos jogadores ordenado por pontuação
def mostrar_ranking(conexao):
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT usuario, pontuacao FROM jogadores ORDER BY pontuacao DESC")
    ranking = cursor.fetchall()
    cursor.close()
    return ranking
