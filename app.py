from dotenv import load_dotenv
import os
from flask import Flask, request, redirect, url_for, render_template, jsonify
import mysql.connector
from datetime import datetime

load_dotenv()

app = Flask(__name__)

# Configurar o ambiente
app.config['ENV'] = os.getenv("FLASK_ENV", "development")

def conectar_banco():
    try:
        conexao = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT"))
        )
        if conexao.is_connected():
            print("Conexão com o banco de dados bem-sucedida")
            return conexao
    except mysql.connector.Error as erro:
        print(f"Erro ao conectar ao banco de dados: {erro}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def enviar_dados():
    nome = request.form.get('name')
    data_nascimento = request.form.get('dataNascimento')
    cpf = request.form.get('cpf')
    salario = float(request.form.get('salario'))
    data_contratacao = request.form.get('dataContratacao')
    anos_contribuicao = int(request.form.get('tempoContribuicao'))

    if not nome or not data_nascimento or not cpf or not salario or not data_contratacao or not anos_contribuicao:
        return redirect(url_for('index'))  # Redireciona se não preencher todos os campos

    try:
        datetime.strptime(data_nascimento, '%Y-%m-%d')
        datetime.strptime(data_contratacao, '%Y-%m-%d')
    except ValueError:
        return redirect(url_for('index'))  # Redireciona se o formato da data for inválido

    conexao = conectar_banco()
    if not conexao:
        return redirect(url_for('index'))  # Ou aqui você poderia exibir uma mensagem de erro na tela

    cursor = conexao.cursor()
    try:
        # Inserir os dados na tabela Funcionario
        sql_funcionario = "INSERT INTO funcionario (Nome, Dt_nascimento, Cpf, Dt_contratacao, Anos_contribuicao) VALUES (%s, %s, %s, %s, %s)"
        valores_funcionario = (nome, data_nascimento, cpf, data_contratacao, anos_contribuicao)
        cursor.execute(sql_funcionario, valores_funcionario)
        conexao.commit()

        funcionario_id = cursor.lastrowid

        # Inserir o salário na tabela Salario
        sql_salario = "INSERT INTO salario (funcionario_id, Valor_Bruto, Dt_ajuste) VALUES (%s, %s, CURDATE())"
        valores_salario = (funcionario_id, salario)
        cursor.execute(sql_salario, valores_salario)
        conexao.commit()

        # Calcular o valor estimado da aposentadoria
        fator = 0.08  # Valor do cálculo aqui 
        valor_estimado = (salario * fator) * anos_contribuicao

        # Inserir o valor estimado na tabela Aposentadoria
        sql_aposentadoria = "INSERT INTO aposentadoria (Funcionario_id, Valor_estimado, Dt_calculo) VALUES (%s, %s, CURDATE())"
        valores_aposentadoria = (funcionario_id, valor_estimado)
        cursor.execute(sql_aposentadoria, valores_aposentadoria)
        conexao.commit()

        return jsonify({'valorEstimado': valor_estimado})

    except mysql.connector.Error as erro:
        print(f"Erro ao inserir dados: {erro}")
        return redirect(url_for('index'))
    finally:
        cursor.close()
        conexao.close()

if __name__ == '__main__':
    # Adicionando configuração da porta dinâmica para produção
    port = int(os.environ.get("PORT", 5000))  # Obtém a porta de ambiente, se disponível
    app.run(host="0.0.0.0", port=port)  # Executa a aplicação na porta especificada
