# 💰 Sistema de Controle Financeiro

Aplicativo desktop feito em Python com PySide6 para ajudar no controle de receitas e despesas pessoais. A ideia é ter um lugar simples onde eu consiga registrar o que entra e o que sai e ver, de forma rápida, como está a minha situação financeira.

## 📌 Sobre o projeto

Neste sistema é possível cadastrar, editar e excluir movimentações, classificar cada uma por categoria e acompanhar o saldo, que é calculado automaticamente. Também incluí um gráfico comparando receitas e despesas.

Fiz o projeto como aplicação desktop, com uma interface gráfica simples e fácil de usar.

## ✨ Funcionalidades

- ➕ Cadastro de receitas
- ➖ Cadastro de despesas
- ✏️ Edição de movimentações
- 🗑️ Exclusão de movimentações
- 🗂️ Categoria em cada movimentação (Salário, Alimentação, Moradia, Transporte, Lazer e Outros)
- 💰 Cálculo automático do total de receitas
- 💸 Cálculo automático do total de despesas
- 📊 Cálculo automático do saldo
- 📈 Gráfico de receitas x despesas
- 💾 Salvamento dos dados em arquivo JSON

## 🛠️ Tecnologias utilizadas

- Python 3.13
- PySide6 (interface gráfica)
- Matplotlib (gráficos)
- JSON (armazenamento dos dados)
- Git e GitHub (versionamento e compartilhamento)

## 📂 Estrutura do projeto

```
Controle-finceiro/
├── main.py            # ponto de entrada: é o arquivo que deve ser executado
├── app.py             # interface e lógica do aplicativo
├── dados.json         # arquivo onde os dados são salvos
├── requirements.txt   # dependências
├── .gitignore
└── README.md
```

A pasta `venv/` não é enviada ao GitHub, porque está no `.gitignore`.

## ▶️ Como executar

Testei o projeto no **Windows**, com **Python 3.13**.

**1. Clonar o repositório**

```
git clone https://github.com/thalliasilva3/Controle-finceiro.git
cd Controle-finceiro
```

**2. Criar o ambiente virtual**

```
py -3.13 -m venv venv
```

**3. Ativar o ambiente virtual** (PowerShell)

```
venv\Scripts\Activate.ps1
```

**4. Instalar as dependências**

```
pip install -r requirements.txt
```

**5. Executar o aplicativo**

```
python main.py
```

## 🗒️ Observações

- Os dados ficam salvos no `dados.json`, na mesma pasta do projeto, e são carregados automaticamente sempre que o app abre.
- Se o app não abrir, confira se o ambiente virtual está ativado e se as dependências foram instaladas.

## 🎓 Objetivo acadêmico

Desenvolvi este projeto para praticar programação em Python, criação de interfaces gráficas, armazenamento de dados, visualização de informações e organização de um projeto com controle de versão.

## 👩‍💻 Desenvolvedora

**Thallia Silva de Oliveira**
Estudante de Análise e Desenvolvimento de Sistemas, UniAnchieta.

Projeto desenvolvido para fins acadêmicos.
⸻

Sistema de Controle Financeiro — Python + PySide6
