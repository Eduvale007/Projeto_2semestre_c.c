from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)

# Função para conectar ao banco (mantenha a função existente)
# ...

# Rota para a página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para enviar dados (mantenha a função existente)
# ...

if __name__ == '__main__':
    app.run(debug=True)
