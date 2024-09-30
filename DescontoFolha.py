import mysql.connector

try:
    conexao = mysql.connector.connect(
        host="127.0.0.1",     # Porta de conexão
        user="root",          # Usuário MySQL
        password="Bololo@10", #Senha do MySQL
        database="aposentadoriadb", # Nome do banco
        port=3306             # Porta padrão do MySQL
    )
    if conexao.is_connected():
        print("Conexão estabelecida com sucesso!")
except mysql.connector.Error as erro:
    print(f"Erro ao conectar: {erro}")
finally:
    if (conexao.is_connected()):
        conexao.close()
        print("Conexão encerrada")



'''print("\nCálculo de Descontos")
nome = str(input("Digite seu nome completo: "))
cpf = int(input("Digite seu CPF\n(sem espaços e pontos entre os números): "))
dataN = str(input("Digite sua data de nascimento\n(no formato: dd/mm/aaaa): "))
dataC = str(input("Digite sua data de contratação\n(no formato: dd/mm/aaaa): "))
salario = float(input("Digite o valor bruto do seu salário: "))
novoSalario = salario - (0.75*100) - (0.75*100) - (0.8*100) - (0.5*100) - (1.0*100)
#descontos de INSS, IRRF, FGTS, vale-transporte, vr/va

print("\nO funcionário", nome)
print("do CPF", cpf)
print("nascido em", dataN)
print("contratado em", dataC)
print("tem seu salário com descontos de R${:.2f}".format(novoSalario))
'''
