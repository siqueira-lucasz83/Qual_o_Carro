from datetime import datetime
import requests
from Conexao import buscar_veiculo_por_modelo, modelo_ja_existe, inserir_carro
from app import app

# Consulta os dados reais diretamente do banco de dados
def consultar_dados_reais(modelo):
    modelo = modelo.strip().lower()
    print(f"Buscando modelo: '{modelo}'")
    return buscar_veiculo_por_modelo(app.conexao, modelo)

# Gera o prompt para a IA com base nos dados do jogador e os dados reais
def gerar_prompt(dados_usuario, dados_reais):
    return f"""
Compare os dados do carro fornecidos pelo usuário com os dados reais abaixo.

Se todos os campos coincidirem exatamente — incluindo modelo, marca, ano, potência e carroceria — responda em português com uma confirmação curta, começando com ✅. Diga que os dados estão aprovados para inserção.

Se houver qualquer diferença, responda em português com ❌ no início. Explique claramente quais campos estão incorretos. Não aprove os dados para inserção.

Evite termos técnicos como "string" ou "inteiro". Não mencione banco de dados. Use linguagem natural, amigável e direta. Responda apenas em português.

Dados do usuário:
Modelo: {dados_usuario['modelo']}
Marca: {dados_usuario['marca']}
Ano: {dados_usuario['ano']}
Potência: {dados_usuario['potencia']}
Carroceria: {dados_usuario['carroceria']}

Dados reais:
Modelo: {dados_reais['modelo']}
Marca: {dados_reais['marca']}
Ano: {dados_reais['ano']}
Potência: {dados_reais['potencia']}
Carroceria: {dados_reais['carroceria']}
"""

# Salva o resultado da validação em um log local
def salvar_log(modelo, marca, ano, resultado):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("log_validacoes.txt", "a", encoding="utf-8") as log:
        log.write(f"[{timestamp}] {modelo} - {marca} - {ano}: {resultado}\n")

# Remove emojis repetidos da resposta
def limpar_emojis_repetidos(texto):
    emojis_usados = set()
    resultado = []

    for palavra in texto.split():
        if palavra in ["✅", "❌", "ℹ️"]:
            if palavra not in emojis_usados:
                emojis_usados.add(palavra)
                resultado.append(palavra)
        else:
            resultado.append(palavra)

    return " ".join(resultado)

# Valida os dados do carro com a IA e trata a resposta
def validar_carro_com_ia(modelo, marca, ano, potencia, carroceria):
    dados_usuario = {
        "modelo": modelo,
        "marca": marca,
        "ano": ano,
        "potencia": potencia,
        "carroceria": carroceria,
    }

    dados_reais = consultar_dados_reais(modelo)
    if not dados_reais:
        return "❌ Modelo não encontrado na base de validação."

    prompt = gerar_prompt(dados_usuario, dados_reais)

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            },
        )
        response.raise_for_status()
        resposta_bruta = response.json().get("response", "").strip()

        if "✅" in resposta_bruta:
            resposta = "✅ " + resposta_bruta.split("✅", 1)[1].strip()

            if modelo_ja_existe(app.conexao, modelo):
                resposta += "\nℹ️ Este modelo já está registrado na base de dados."
            else:
                inserir_carro(app.conexao, dados_usuario)
                resposta += "\n✅ Modelo adicionado à base de dados com sucesso."

        elif "❌" in resposta_bruta:
            resposta = "❌ " + resposta_bruta.split("❌", 1)[1].strip()
        else:
            resposta = resposta_bruta

        print("Resposta da IA:")
        print(resposta)

        salvar_log(modelo, marca, ano, resposta)
        return resposta

    except Exception as e:
        print(f"Erro na validação com IA: {e}")
        return "❌ Erro ao validar o carro com a IA."
