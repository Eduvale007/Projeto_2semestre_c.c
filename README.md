# Simulação de Aposentadoria

## Descrição
Este é um projeto desenvolvido por um grupo de estudantes da Faculdade Uninove. O objetivo do software é calcular a aposentadoria de uma pessoa com base nas informações fornecidas em um formulário. Após o preenchimento, o sistema processa os dados e retorna uma estimativa do valor da aposentadoria, considerando os critérios especificados no cálculo.

## Stack Utilizada
- **Front-end**: HTML, CSS, JavaScript
- **Back-end**: Python, Flask, MySQL

## Funcionalidades
- Coleta de dados como nome, CPF, data de nascimento, salário, data de contratação e anos de contribuição através de um formulário.
- Armazenamento seguro das informações no banco de dados.
- Cálculo do valor estimado da aposentadoria com base nos dados fornecidos.
- Exibição do valor da aposentadoria diretamente na interface do usuário.

## Endpoints

### 1. Página Inicial
- **URL**: `/`
- **Método**: `GET`
- **Descrição**: Exibe a página inicial com o formulário para inserir os dados do funcionário.
- **Resposta**:
  - **HTML**: Retorna a página `index.html`.

### 2. Enviar Dados para Cálculo de Aposentadoria
- **URL**: `/enviar`
- **Método**: `POST`
- **Descrição**: Recebe os dados do formulário, armazena no banco de dados e calcula o valor estimado da aposentadoria.

#### Parâmetros

| Parâmetro           | Tipo    | Descrição                                             |
|---------------------|---------|-------------------------------------------------------|
| `name`              | string  | Nome do funcionário.                                  |
| `dataNascimento`    | string  | Data de nascimento no formato `YYYY-MM-DD`.           |
| `cpf`               | string  | CPF do funcionário.                                   |
| `salario`           | float   | Salário atual do funcionário.                         |
| `dataContratacao`   | string  | Data de contratação no formato `YYYY-MM-DD`.          |
| `tempoContribuicao` | int     | Número de anos de contribuição.                       |

#### Exemplo de Request
```http
POST /enviar HTTP/1.1
Content-Type: application/x-www-form-urlencoded

name=João+Silva&dataNascimento=1980-01-15&cpf=123.456.789-00&salario=3500.50&dataContratacao=2005-03-10&tempoContribuicao=20
