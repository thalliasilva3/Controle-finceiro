import sys
import json
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.figure import Figure
from dotenv import load_dotenv
from openai import OpenAI

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QDialog,
    QFormLayout,
    QLineEdit,
    QComboBox,
    QDialogButtonBox,
    QMessageBox,
)

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPEN_aPI_KEY")
)

class LancamentoDialog(QDialog):

    def __init__(self, tipo, parent=None, dados=None):
        super().__init__(parent)

        self.setWindowTitle(f"Nova {tipo}" if dados is None else f"Editar {tipo}")
        self.resize(350, 200)

        layout = QFormLayout(self)

        self.descricao = QLineEdit()
        self.valor = QLineEdit()
        self.categoria = QComboBox()

        self.categoria.addItems([
            "Salario",
            "Alimentacao",
            "Moradia",
            "Transporte",
            "Lazer",
            "Outros"
        ])

        if dados:
            self.descricao.setText(dados["descricao"])
            self.valor.setText(str(dados["valor"]))

            indice = self.categoria.findText(dados["categoria"])

            if indice >= 0:
                self.categoria.setCurrentIndex(indice)

        layout.addRow("Descricao:", self.descricao)
        layout.addRow("Valor:", self.valor)
        layout.addRow("Categoria:", self.categoria)

        botoes = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        botoes.accepted.connect(self.accept)
        botoes.rejected.connect(self.reject)

        layout.addRow(botoes)


class ControleFinanceiro(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Controle Financeiro")
        self.resize(1100, 700)

        self.receitas = 0.0
        self.despesas = 0.0
        self.movimentacoes = []

        self.carregar_dados()

        central = QWidget()
        self.setCentralWidget(central)

        layout_principal = QVBoxLayout(central)
        layout_principal.setContentsMargins(30, 30, 30, 30)
        layout_principal.setSpacing(20)

        titulo = QLabel("CONTROLE FINANCEIRO")
        titulo.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #1F4E79;
            letter-spacing: 1px;
        """)

        subtitulo = QLabel(
            "Gerencie suas receitas e despesas"
        )

        subtitulo.setStyleSheet("""
            font-size: 14px;
            color: #666666;
""")

        layout_principal.addWidget(titulo)
        layout_principal.addWidget(subtitulo)

        cards = QHBoxLayout()

        self.card_receitas = self.criar_card(
            "RECEITAS",
            "R$ 0,00"
        )

        self.card_despesas = self.criar_card(
            "DESPESAS",
            "R$ 0,00"
        )

        self.card_saldo = self.criar_card(
            "SALDO",
            "R$ 0,00"
        )

        self.card_metas = self.criar_card(
            "METAS",
            "R$ 0,00"
        )

        cards.addWidget(self.card_receitas)
        cards.addWidget(self.card_despesas)
        cards.addWidget(self.card_saldo)
        cards.addWidget(self.card_metas)

        cards.setSpacing(15)

        layout_principal.addLayout(cards)

        botoes = QHBoxLayout()

        botao_receita = QPushButton("Nova Receita")
        botao_despesa = QPushButton("Nova Despesa")
        botao_editar = QPushButton("Editar Selecionado")
        botao_excluir = QPushButton("Excluir Selecionado")
        botao_ia = QPushButton("🤖 Assistente IA")

        botao_ia.setStyleSheet("""
    QPushButton {
        background-color: #1F4E79;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 10px;
        font-size: 14px;
        font-weight: bold;
    }

    QPushButton:hover {
        background-color: #163A5C;
    }
""")

        botao_receita.setStyleSheet("""
            QPushButton {
                background-color: #1F4E79;
                color: white;
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
     }
""")
        botao_despesa.setStyleSheet("""
            QPushButton { 
                background-color: #666666;
                color: white;
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
        }
""")

        botao_editar.setStyleSheet("""
            QPushButton {
                background-color: #1F4E79;
                color: white;
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
        }
""")

        botao_excluir.setStyleSheet("""
            QPushButton {
                background-color: #666666;
                color: white;
                padding: 8px 15px;
                border-radius: 6px;
                font-weight: bold;
        }
""")
            
        botao_receita.clicked.connect(
            lambda: self.novo_lancamento("Receita")
        )

        botao_despesa.clicked.connect(
            lambda: self.novo_lancamento("Despesa")
        )

        botao_editar.clicked.connect(
            self.editar_lancamento
        )

        botao_excluir.clicked.connect(
            self.excluir_lancamento
        )

        botao_ia.clicked.connect(
            self.abrir_assistente_ia
        )

        botoes.addWidget(botao_receita)
        botoes.addWidget(botao_despesa)
        botoes.addWidget(botao_editar)
        botoes.addWidget(botao_excluir)
        botoes.addWidget(botao_ia)

        layout_principal.addLayout(botoes)

        titulo_tabela = QLabel(
            "MOVIMENTACOES FINANCEIRAS"
        )

        titulo_tabela.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
        """)

        layout_principal.addWidget(titulo_tabela)

        self.tabela = QTableWidget()
        self.tabela.setAlternatingRowColors(True)
        self.tabela.setStyleSheet("""
            QTableWidget {
                border: 1px solid #D9E1E8;
                border-radius: 8px;
        }
""")
        self.tabela.verticalHeader().setDefaultSectionSize(35)

        self.tabela.setColumnCount(4)

        self.tabela.setHorizontalHeaderLabels([
            "Tipo",
            "Descricao",
            "Categoria",
            "Valor"
        ])

        self.tabela.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
            background-color: #1F4E79;
            color: white;
            font-weight: bold;
            padding: 6px;
        }
""")

        self.tabela.horizontalHeader().setStretchLastSection(True)

        self.tabela.setColumnWidth(0, 120)
        self.tabela.setColumnWidth(1, 300)
        self.tabela.setColumnWidth(2, 180)

        layout_principal.addWidget(self.tabela, 2)
        self.figure = Figure(figsize=(6, 2))
        self.canvas = FigureCanvas(self.figure)

        layout_principal.addWidget(self.canvas, 2)
        self.atualizar_grafico()
        
        self.ax.bar(
            ["Receitas", "Despesas"],
            [self.receitas, self.despesas]
        )

        self.ax.set_title("Receitas x Despesas")
        self.ax.set_ylabel("Valor (R$)")
       

        self.atualizar_tela()

    def criar_card(self, titulo, valor):

        card = QWidget()

        layout = QVBoxLayout(card)
        layout.setSpacing(8)

        label_titulo = QLabel(titulo)
        label_valor = QLabel(valor)

        label_titulo.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #1F4E79  ;
        """)

        label_valor.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            Color: #1F4E79;
""")

        layout.addWidget(label_titulo)
        layout.addWidget(label_valor)

        card.setStyleSheet("""
            QWidget {
                background-color: #F5F7FA;
                border: 1px solid #D9E1E8;
                border-radius: 12px;
                padding: 10px;
        }
""")

        return card

    def carregar_dados(self):

        if os.path.exists("dados.json"):

            try:

                with open(
                    "dados.json",
                    "r",
                    encoding="utf-8"
                ) as arquivo:

                    dados = json.load(arquivo)

                self.receitas = dados.get(
                    "receitas",
                    0.0
                )

                self.despesas = dados.get(
                    "despesas",
                    0.0
                )

                self.movimentacoes = dados.get(
                    "movimentacoes",
                    []
                )

            except (json.JSONDecodeError, OSError):

                self.receitas = 0.0
                self.despesas = 0.0
                self.movimentacoes = []

    def salvar_dados(self):

        dados = {
            "receitas": self.receitas,
            "despesas": self.despesas,
            "movimentacoes": self.movimentacoes
        }

        with open(
            "dados.json",
            "w",
            encoding="utf-8"
        ) as arquivo:

            json.dump(
                dados,
                arquivo,
                indent=4,
                ensure_ascii=False
            )

    def novo_lancamento(self, tipo):

        dialogo = LancamentoDialog(
            tipo,
            self
        )

        if dialogo.exec():

            descricao = (
                dialogo.descricao
                .text()
                .strip()
            )

            valor_texto = (
                dialogo.valor
                .text()
                .strip()
                .replace(",", ".")
            )

            if not descricao:
                return

            try:

                valor = float(valor_texto)

                if valor <= 0:
                    return

            except ValueError:

                return

            categoria = (
                dialogo.categoria
                .currentText()
            )

            self.movimentacoes.append({
                "tipo": tipo,
                "descricao": descricao,
                "categoria": categoria,
                "valor": valor
            })

            if tipo == "Receita":
                self.receitas += valor
            else:
                self.despesas += valor

            self.salvar_dados()
            self.atualizar_tela()

    def editar_lancamento(self):

        linha = self.tabela.currentRow()

        if linha < 0:

            QMessageBox.warning(
                self,
                "Editar",
                "Selecione um lancamento na tabela."
            )

            return

        item = self.movimentacoes[linha]

        dialogo = LancamentoDialog(
            item["tipo"],
            self,
            item
        )

        if dialogo.exec():

            descricao = (
                dialogo.descricao
                .text()
                .strip()
            )

            valor_texto = (
                dialogo.valor
                .text()
                .strip()
                .replace(",", ".")
            )

            if not descricao:
                return

            try:

                novo_valor = float(valor_texto)

                if novo_valor <= 0:
                    return

            except ValueError:

                return

            nova_categoria = (
                dialogo.categoria
                .currentText()
            )

            valor_antigo = item["valor"]

            if item["tipo"] == "Receita":

                self.receitas -= valor_antigo
                self.receitas += novo_valor

            else:

                self.despesas -= valor_antigo
                self.despesas += novo_valor

            item["descricao"] = descricao
            item["valor"] = novo_valor
            item["categoria"] = nova_categoria

            self.salvar_dados()
            self.atualizar_tela()

    def excluir_lancamento(self):

        linha = self.tabela.currentRow()

        if linha < 0:

            QMessageBox.warning(
                self,
                "Excluir",
                "Selecione um lancamento na tabela."
            )

            return

        item = self.movimentacoes[linha]

        resposta = QMessageBox.question(
            self,
            "Excluir lancamento",
            "Deseja realmente excluir este lancamento?",
            QMessageBox.Yes | QMessageBox.No
        )

        if resposta == QMessageBox.Yes:

            if item["tipo"] == "Receita":
                self.receitas -= item["valor"]
            else:
                self.despesas -= item["valor"]

            self.movimentacoes.pop(linha)

            self.salvar_dados()
            self.atualizar_tela()

    def abrir_assistente_ia(self):

        dialogo = QDialog(self)
        dialogo.setWindowTitle("Assistente Financeiro IA")
        dialogo.resize(500, 400)

        layout = QVBoxLayout(dialogo)

        titulo = QLabel("🤖 Assistente Financeiro")
        titulo.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
""")

        pergunta = QLineEdit()
        pergunta.setPlaceholderText(
            "Ex: Onde estou gastando mais?"
        )

        resposta = QLabel(
            "Digite uma perguntansobre suas finanças."
        )
        resposta.setWordWrap(True)

        botao_perguntar = QPushButton("Perguntar a IA")

        botao_perguntar.clicked.connect(
            lambda: self.perguntar_ia(
                pergunta,
                resposta
            )
        )

        layout.addWidget(titulo)
        layout.addWidget(pergunta)
        layout.addWidget(botao_perguntar)
        layout.addWidget(resposta)

        dialogo.exec()

    def perguntar_ia(self, pergunta, resposta):

        texto_pergunta = pergunta.text().strip().lower()

        if not texto_pergunta:
            resposta.setText("Digite uma pergunta primeiro.")
            return

        if not self.movimentacoes:
            resposta.setText(
                "🤖 Assistente Financeiro:\n\n"
                "Ainda não existem movimentações cadastradas. "
                "Adicione receitas ou despesas para que eu possa analisar seus dados."
            )
            return

        receitas = [
            item for item in self.movimentacoes
            if item["tipo"] == "Receita"
        ]

        despesas = [
            item for item in self.movimentacoes
            if item["tipo"] == "Despesa"
        ]

        total_receitas = sum(
            item["valor"] for item in receitas
        )

        total_despesas = sum(
            item["valor"] for item in despesas
        )

        saldo = total_receitas - total_despesas

        if "saldo" in texto_pergunta or "quanto tenho" in texto_pergunta:

            resposta.setText(
                f"🤖 Assistente Financeiro:\n\n"
                f"Seu saldo atual é de R$ {saldo:,.2f}.\n\n"
                f"💰 Receitas: R$ {total_receitas:,.2f}\n"
                f"💸 Despesas: R$ {total_despesas:,.2f}"
            )

            return

        if "receita" in texto_pergunta or "ganhei" in texto_pergunta:

            resposta.setText(
                f"🤖 Assistente Financeiro:\n\n"
                f"Você possui R$ {total_receitas:,.2f} "
                f"em receitas cadastradas."
            )

            return

        if "despesa" in texto_pergunta or "gasto" in texto_pergunta:

            if despesas:

                maior_despesa = max(
                    despesas,
                    key=lambda x: x["valor"]
                )

                resposta.setText(
                    f"🤖 Assistente Financeiro:\n\n"
                    f"Você possui R$ {total_despesas:,.2f} "
                    f"em despesas.\n\n"
                    f"Seu maior gasto individual é "
                    f"'{maior_despesa['descricao']}', "
                    f"no valor de R$ {maior_despesa['valor']:,.2f}."
                )

            else:

                resposta.setText(
                    "🤖 Assistente Financeiro:\n\n"
                    "Você ainda não possui despesas cadastradas."
                )

            return

        if "onde" in texto_pergunta and "gast" in texto_pergunta:

            categorias = {}

            for item in despesas:

                categoria = item["categoria"]

                categorias[categoria] = (
                    categorias.get(categoria, 0)
                    + item["valor"]
                )

            if categorias:

                maior_categoria = max(
                    categorias,
                    key=categorias.get
                )

                valor = categorias[maior_categoria]

                resposta.setText(
                    f"🤖 Assistente Financeiro:\n\n"
                    f"Sua maior categoria de gastos é "
                    f"'{maior_categoria}', com "
                    f"R$ {valor:,.2f}."
                )

            else:

                resposta.setText(
                    "🤖 Assistente Financeiro:\n\n"
                    "Ainda não existem despesas cadastradas "
                    "para fazer essa análise."
                )

            return

        if "econom" in texto_pergunta:

            if total_receitas > 0:

                percentual = (
                    saldo / total_receitas
                ) * 100

                resposta.setText(
                    f"🤖 Assistente Financeiro:\n\n"
                    f"Você está mantendo aproximadamente "
                    f"{percentual:.1f}% das suas receitas "
                    f"depois das despesas.\n\n"
                    f"Uma boa prática é acompanhar "
                    f"principalmente as categorias que "
                    f"concentram seus maiores gastos."
                )

            return

        resposta.setText(
            f"🤖 Assistente Financeiro:\n\n"
            f"Analisei seus dados financeiros.\n\n"
            f"💰 Receitas: R$ {total_receitas:,.2f}\n"
            f"💸 Despesas: R$ {total_despesas:,.2f}\n"
            f"📊 Saldo: R$ {saldo:,.2f}\n\n"
            f"Você pode perguntar:\n"
            f"• Onde estou gastando mais?\n"
            f"• Qual é meu saldo?\n"
            f"• Quanto tenho de despesas?\n"
            f"• Quanto recebi?\n"
            f"• Como posso economizar?"
        )

    def atualizar_grafico(self):

        self.figure.clear()

        self.ax = self.figure.add_subplot(111)

        self.ax.bar(
            ["Receitas", "Despesas"],
            [self.receitas, self.despesas]
        )

        self.ax.set_title("Receitas x Despesas")
        self.ax.set_ylabel("Valor (R$)")

        self.canvas.draw()
                
    def atualizar_grafico(self):

        self.figure.clear()

        self.ax = self.figure.add_subplot(111)

        self.ax.bar(
            ["Receitas", "Despesas"],
            [self.receitas, self.despesas]
        )

        self.ax.set_title("Receitas x Despesas")
        self.ax.set_ylabel("Valor (R$)")

        self.canvas.draw()
            
    def atualizar_tela(self):

        saldo = (
            self.receitas -
            self.despesas
        )

        receitas_formatadas = (
            f"R$ {self.receitas:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

        despesas_formatadas = (
            f"R$ {self.despesas:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

        saldo_formatado = (
            f"R$ {saldo:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

        self.card_receitas.layout().itemAt(1).widget().setText(
            receitas_formatadas
        )

        self.card_despesas.layout().itemAt(1).widget().setText(
            despesas_formatadas
        )

        self.card_saldo.layout().itemAt(1).widget().setText(
            saldo_formatado
        )

        self.tabela.setRowCount(
            len(self.movimentacoes)
        )

        for linha, item in enumerate(
            self.movimentacoes
        ):

            item_tipo = QTableWidgetItem(item["tipo"])
            item_tipo.setTextAlignment(Qt.AlignCenter)

            self.tabela.setItem(
                linha,
                0,
                item_tipo
            )

            self.tabela.setItem(
                linha,
                1,
                QTableWidgetItem(
                    item["descricao"]
                )
            )

            self.tabela.setItem(
                linha,
                2,
                QTableWidgetItem(
                    item["categoria"]
                )
            )

            valor = (
                f'R$ {item["valor"]:,.2f}'
                .replace(",", "X")
                .replace(".", ",")
                .replace("X", ".")
            )

            self.tabela.setItem(
                linha,
                3,
                QTableWidgetItem(valor)
            )

            self.atualizar_grafico()

if __name__ == "__main__":

    app = QApplication(sys.argv)

    janela = ControleFinanceiro()
    janela.show()

    sys.exit(app.exec())