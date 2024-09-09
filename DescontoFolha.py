print("\nCálculo de Descontos")
nome = str(input("Digite seu nome completo: "))
salario = float(input("Digite o valor bruto do seu salário: "))
novoSalario = salario - (0.75*100) - (0.75*100) - (0.8*100) - (0.5*100) - (1.0*100)
#descontos de INSS, IRRF, FGTS, vale-transporte, vr/va

print("\nO funcionário", nome) 
print("tem seu salário com descontos de: ", novoSalario)
