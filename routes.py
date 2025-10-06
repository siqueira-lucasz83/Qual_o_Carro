import random
from flask import request, jsonify, render_template, redirect, url_for, session, flash
from app import app
from Validar_carro import validar_carro_com_ia
from Conexao import buscar_veiculo_por_modelo
from Jogadores import login_jogador, cadastrar_jogador, mostrar_ranking

# Redireciona para a página inicial
@app.route('/')
def pagina_inicial():
    return redirect(url_for('inicio'))

# Renderiza a página inicial
@app.route('/inicio')
def inicio():
    return render_template('inicio.html')

# Renderiza a página "Saiba Mais"
@app.route('/saibamais')
def saibamais():
    return render_template('saibamais.html')

# Renderiza a página de tutorial
@app.route('/tutorial')
def tutorial():
    return render_template('tutorial.html')

# Gerencia login do jogador
@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        nome_usuario = request.form['nome_usuario']
        senha = request.form['senha']

        if not nome_usuario or not senha:
            return render_template('login.html', error="Por favor, preencha todos os campos.")

        jogador = login_jogador(app.conexao, nome_usuario, senha)

        if jogador:
            session['jogador_id'] = jogador['id']
            session['jogador_nome'] = jogador['nome']
            return redirect(url_for('menu_principal'))
        else:
            return render_template('login.html', error="Usuário ou senha incorretos.")

    return render_template('login.html')

# Gerencia cadastro de novo jogador
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro_page():
    if request.method == 'POST':
        nome_usuario = request.form['usuario']
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        email = request.form['email']
        senha = request.form['senha']

        if not all([nome_usuario, nome, sobrenome, email, senha]):
            return render_template('cadastro.html', error="Todos os campos são obrigatórios.")

        try:
            sucesso = cadastrar_jogador(app.conexao, nome, sobrenome, nome_usuario, email, senha)
            if sucesso:
                return render_template('login.html', success="Cadastro realizado com sucesso! Faça login.")
            else:
                return render_template('cadastro.html', error="Esse nome de usuário já existe ou outro erro ocorreu.")
        except Exception as e:
            return render_template('cadastro.html', error=f"Erro no cadastro: {e}")

    return render_template('cadastro.html')

# Renderiza o menu principal
@app.route('/menu')
def menu_principal():
    if 'jogador_id' not in session:
        return redirect(url_for('login_page'))

    nome_jogador = session.get('jogador_nome', 'Visitante')
    return render_template('menu.html', nome_jogador=nome_jogador)

# Inicia uma nova partida
@app.route('/jogar')
def jogar_web():
    if 'jogador_id' not in session:
        return redirect(url_for('login_page'))

    cursor = app.conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM carros")
    carros_do_banco = cursor.fetchall()
    cursor.close()

    if not carros_do_banco:
        return "Nenhum carro cadastrado no banco de dados."

    carro_escolhido = random.choice(carros_do_banco)
    session['carro_atual'] = carro_escolhido
    session['tentativas_restantes'] = 4
    return render_template('jogar.html', carro_escolhido=carro_escolhido)

# Processa o palpite do jogador
@app.route('/palpite', methods=['POST'])
def palpite():
    if 'jogador_id' not in session or 'carro_atual' not in session:
        return redirect(url_for('login_page'))

    try:
        palpite_usuario = request.form['palpite'].strip().lower()
        carro_escolhido = session['carro_atual']
        modelo_real = carro_escolhido.get("modelo", "Indefinido")

        tentativas = session.get('tentativas_restantes', 4)

        if palpite_usuario == modelo_real.lower():
            pontos = tentativas + 6
            cursor = app.conexao.cursor()
            cursor.execute("UPDATE jogadores SET pontuacao = pontuacao + %s WHERE id = %s", (pontos, session['jogador_id']))
            app.conexao.commit()
            cursor.close()
            return jsonify({"acertou": True, "carro": modelo_real, "pontos": pontos})
        else:
            tentativas -= 1
            session['tentativas_restantes'] = tentativas
            return jsonify({"acertou": False, "carro": modelo_real})
    except Exception as e:
        print(f"Erro no palpite: {e}")
        return jsonify({"acertou": False, "erro": "Ocorreu um erro no servidor.", "carro": "Indefinido"})

# Retorna os dados do carro atual
@app.route('/carro-dica')
def carro_dica():
    if 'carro_atual' not in session:
        return jsonify({})
    return jsonify(session['carro_atual'])

# Exibe o ranking dos jogadores
@app.route('/ranking')
def ranking_web():
    if 'jogador_id' not in session:
        return redirect(url_for('login_page'))

    ranking_data = mostrar_ranking(app.conexao)
    return render_template('ranking.html', ranking=ranking_data)

# Renderiza a página de validação de carro
@app.route('/adicionar-carro')
def adicionar_carro_web():
    if 'jogador_id' not in session:
        return redirect(url_for('login_page'))
    return render_template('validar_carro.html')

# Valida os dados do carro com IA
@app.route('/validar-carro', methods=['POST'])
def validar_carro_api():
    dados_carro = request.get_json()

    resposta_texto = validar_carro_com_ia(
        dados_carro['modelo'],
        dados_carro['marca'],
        dados_carro['ano'],
        dados_carro['potencia'],
        dados_carro['carroceria']
    )

    if "✅" in resposta_texto:
        salvar_carro_no_banco(dados_carro)

    return resposta_texto

# Salva o carro validado no banco de dados
def salvar_carro_no_banco(dados):
    try:
        cursor = app.conexao.cursor()
        cursor.execute("""
            INSERT INTO carros (modelo, marca, ano, potencia, carroceria)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            dados['modelo'],
            dados['marca'],
            dados['ano'],
            dados['potencia'],
            dados['carroceria']
        ))
        app.conexao.commit()
        cursor.close()
    except Exception as e:
        print(f"Erro ao salvar no banco: {e}")

# Encerra a sessão do jogador
@app.route('/logout')
def logout():
    session.pop('jogador_id', None)
    session.pop('jogador_nome', None)
    return redirect(url_for('inicio'))
