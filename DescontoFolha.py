from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Função para conectar ao banco
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

# Rota para enviar dados
@app.route('/enviar', methods=['POST'])
def enviar_dados():
    # Capturar os dados enviados pelo formulário
    nome = request.form.get('name')
    data_nascimento = request.form.get('dataNascimento')
    cpf = request.form.get('cpf')
    salario = request.form.get('salario')
    data_contratacao = request.form.get('dataContratacao')

    # Verificar se todos os campos foram preenchidos
    if not nome or not data_nascimento or not cpf or not salario or not data_contratacao:
        return jsonify({'erro': 'Por favor, preencha todos os campos.'}), 400

    # Verificação de formato de data (ex: YYYY-MM-DD)
    try:
        datetime.strptime(data_nascimento, '%Y-%m-%d')
        datetime.strptime(data_contratacao, '%Y-%m-%d')
    except ValueError:
        return jsonify({'erro': 'Formato de data inválido. Use YYYY-MM-DD.'}), 400

    print(f"Dados recebidos: Nome={nome}, Data Nascimento={data_nascimento}, CPF={cpf}, Salário={salario}, Data Contratação={data_contratacao}")

    # Conectar ao banco
    conexao = conectar_banco()
    if not conexao:
        print("Erro ao conectar ao banco de dados.")
        return jsonify({'erro': 'Erro ao conectar ao banco de dados.'}), 500

    cursor = conexao.cursor()

    try:
        # Inserir os dados na tabela Funcionario
        sql_funcionario = "INSERT INTO funcionario (Nome, Dt_nascimento, Cpf, Dt_contratacao) VALUES (%s, %s, %s, %s)"
        valores_funcionario = (nome, data_nascimento, cpf, data_contratacao)
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

        # Consulta para retornar os dados inseridos
        cursor.execute("SELECT * FROM funcionario WHERE Cpf = %s", (cpf,))
        funcionario = cursor.fetchone()
    except mysql.connector.Error as erro:
        print(f"Erro ao inserir dados: {erro}")
        return jsonify({'erro': f'Erro ao inserir dados: {erro}'}), 500
    finally:
        cursor.close()
        conexao.close()

    # Retornar os dados como JSON para exibição no front-end
    if funcionario:
        return jsonify({
            'nome': funcionario[1],
            'data_nascimento': funcionario[2],
            'cpf': funcionario[3],
            'data_contratacao': funcionario[4]
        })
    else:
        print("Funcionário não encontrado.")
        return jsonify({'erro': 'Funcionário não encontrado.'}), 404

if __name__ == '__main__':
    app.run(debug=True)
