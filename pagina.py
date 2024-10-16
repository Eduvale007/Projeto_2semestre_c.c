from flask import Flask, request, jsonify, render_template
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
def home():
    return render_template('form.html')

@app.route('/enviar', methods=['POST'])
def enviar_dados():
    
    nome = request.form.get('name')
    data_nascimento = request.form.get('dataNascimento')
    cpf = request.form.get('cpf')
    salario = request.form.get('salario')
    data_contratacao = request.form.get('dataContratacao')

    
    if not nome or not data_nascimento or not cpf or not salario or not data_contratacao:
        return jsonify({'erro': 'Por favor, preencha todos os campos.'}), 400

    
    try:
        datetime.strptime(data_nascimento, '%Y-%m-%d')
        datetime.strptime(data_contratacao, '%Y-%m-%d')
    except ValueError:
        return jsonify({'erro': 'Formato de data inválido. Use YYYY-MM-DD.'}), 400

    
    try:
        salario = float(salario)  
        novo_salario = salario - (0.75 * 100) - (0.75 * 100) - (0.8 * 100) - (0.5 * 100) - (1.0 * 100)
        
        if novo_salario >= 0:  
            return jsonify({'mensagem': f'Salário calculado com sucesso! Novo salário: {novo_salario:.2f}'}), 200
        else:
            return jsonify({'erro': 'O cálculo do salário resultou em um valor negativo.'}), 400
    except Exception as e:
        return jsonify({'erro': f'Erro ao calcular o salário: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
