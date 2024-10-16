from flask import Flask, request, redirect, url_for, render_template
import mysql.connector
from datetime import datetime

app = Flask(__name__)

def conectar_banco():
    try:
        conexao = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="Bololo@10",
            database="aposentadoriadb",
            port=3306
        )
        if conexao.is_connected():
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
    salario = request.form.get('salario')
    data_contratacao = request.form.get('dataContratacao')
    anos_contribuicao = request.form.get('tempoContribuicao')

    if not nome or not data_nascimento or not cpf or not salario or not data_contratacao or not anos_contribuicao:
        return redirect(url_for('index'))  # Redireciona se não preencher todos os campos

    try:
        # Verificar formato de data
        datetime.strptime(data_nascimento, '%Y-%m-%d')
        datetime.strptime(data_contratacao, '%Y-%m-%d')
    except ValueError:
        return redirect(url_for('index'))  # Redireciona se o formato da data for inválido

    # Conectar ao banco
    conexao = conectar_banco()
    if not conexao:
        print("Erro ao conectar ao banco de dados.")
        return redirect(url_for('index'))  # Redireciona em caso de erro

    cursor = conexao.cursor()
    try:
        # Inserir os dados na tabela Funcionario
        sql_funcionario = "INSERT INTO funcionario (Nome, Dt_nascimento, Cpf, Dt_contratacao, Anos_contribuicao) VALUES (%s, %s, %s, %s, %s)"
        valores_funcionario = (nome, data_nascimento, cpf, data_contratacao, anos_contribuicao)
        cursor.execute(sql_funcionario, valores_funcionario)
        conexao.commit()

        # Obter o ID do funcionário recém-inserido
        funcionario_id = cursor.lastrowid
        print(f"ID do funcionário inserido: {funcionario_id}")

        # Inserir o salário na tabela Salario
        sql_salario = "INSERT INTO salario (funcionario_id, Valor_Bruto, Dt_ajuste) VALUES (%s, %s, CURDATE())"
        valores_salario = (funcionario_id, salario)
        cursor.execute(sql_salario, valores_salario)
        conexao.commit()

        print("Dados de salário inseridos com sucesso!")

        # Calcular o valor estimado da aposentadoria
        fator = 0.8  # Defina seu fator aqui
        valor_estimado = float(salario) * float(anos_contribuicao) * fator

        # Inserir o valor estimado na tabela Aposentadoria
        sql_aposentadoria = "INSERT INTO aposentadoria (Funcionario_id, Valor_estimado, Dt_calculo) VALUES (%s, %s, CURDATE())"
        valores_aposentadoria = (funcionario_id, valor_estimado)
        cursor.execute(sql_aposentadoria, valores_aposentadoria)
        conexao.commit()

        print("Valor estimado da aposentadoria inserido com sucesso!")

    except mysql.connector.Error as erro:
        print(f"Erro ao inserir dados: {erro}")
        return redirect(url_for('index'))  # Redireciona em caso de erro
    finally:
        cursor.close()
        conexao.close()

    # Redireciona para a página inicial após a inserção
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
