from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QListWidget, QVBoxLayout
from PyQt6.QtGui import QPixmap, QColor, QPalette
from PyQt6.QtCore import Qt
import sys
import os
from sqlalchemy.orm import Session, aliased
from sqlalchemy import or_
from matriculas_app.app.config.database import SessionLocal
from matriculas_app.app.models.curso import Curso
from matriculas_app.app.models.instituicao import Instituicao
from matriculas_app.app.models.localizacao import Localizacao
from matriculas_app.app.models.matricula import Matricula


class NewWindow(QWidget):
    def __init__(self, lista, selected1):
        super().__init__()

        self.setWindowTitle("")
        self.setFixedSize(367, 461)

        self.background = QLabel(self)
        self.background.setGeometry(0, 0, 382, 464)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        if selected1 == 'Ranking de cursos em 2022':
            pixmap = QPixmap(os.path.join(BASE_DIR, "resources", "RankingCurso.png"))
        elif selected1 == 'Total de alunos matriculados (no Brasil) por ano':
            pixmap = QPixmap(os.path.join(BASE_DIR, "resources", "ListaAlunos.png"))

        self.background.setPixmap(pixmap)
        self.background.setScaledContents(True)

        self.list_widget = QListWidget(self)
        self.list_widget.setGeometry(60, 60, 272, 374)

        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: rgba(0, 0, 0, 0);
                color: #5c5a68;
                font-size: 14px;
                border: none;
            }
            QListWidget::item {
                padding: 8px;
            }
        """)

        self.list_widget.addItems(lista)

    # Aqui vai ser a conexão com o Controller
def consultar_nomes(ano, estado):
    session: Session = SessionLocal()
    try:
        # Alianças entre as tabelas
        instituicoes = aliased(Instituicao)
        cursos = aliased(Curso)
        matriculas = aliased(Matricula)
        localizacoes = aliased(Localizacao)

        # Realizando a consulta
        query = session.query(instituicoes.nome, cursos.nome).\
            join(matriculas, matriculas.curso_id == cursos.id).\
            join(localizacoes, localizacoes.id == matriculas.localizacao_id).\
            join(instituicoes, instituicoes.id == matriculas.instituicao_id).\
            filter(matriculas.ano == ano, localizacoes.estado == estado)

        # Executando a consulta e retornando os resultados
        resultados = query.all()

        # Criando a lista com os nomes
        lista_nomes = [f"{instituicao} - {curso}" for instituicao, curso in resultados]
        return lista_nomes

    except Exception as e:
        print(f"Erro na consulta: {e}")
    finally:
        session.close()


resultado = consultar_nomes('2022', 'SÃO PAULO')

def buscarLista(selected1, selected2, selected3):
    if selected3 == 'Todos':
        return resultado
    elif selected3 == 'Modalidade EAD':
        return ["Curso A", "Curso B"]
    elif selected3 == 'Modalidade Presencial':
        return ["Curso C", "Curso D"]
    return ["Nenhum resultado encontrado."]


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.consultas = []
        self.setMinimumSize(674, 410)
        self.setMaximumSize(674, 410)
        self.setup_ui()

    def setup_ui(self):
        # Background Imagem
        self.background = QLabel(self)

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(BASE_DIR, "resources", "Main.png")
        pixmap = QPixmap(image_path)
        self.background.setPixmap(pixmap)
        self.background.setScaledContents(True)

        self.list_widget = QListWidget(self)
        self.list_widget.setGeometry(445, 308, 184, 64)
        # Tornar o fundo transparente
        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: #859987;
                color: #5c5a68;
                font-size: 14px;
                border: 2px solid #5c5a68;
            }
        """)
        self.list_widget.itemClicked.connect(self.consulta_clicada)

        # ChoiceBoxes
        self.list1 = self.create_list(["Total de alunos matriculados (no Brasil) por ano", "Ranking de cursos em 2022"])
        self.list2 = self.create_list(
            ["TODOS", "ACRE", "ALAGOAS", "AMAZONAS", "BAHIA", "CEARÁ", "DISTRITO FEDERAL", "ESPÍRITO SANTO", "GOIÁS",
             "MARANHÃO",
             "MATO GROSSO", "MATO GROSSO DO SUL", "MINAS GERAIS", "PARÁ", "PARAÍBA", "PERNAMBUCO", "PIAUÍ",
             "RIO DE JANEIRO", "RIO GRANDE DO NORTE",
             "RIO GRANDE DO SUL", "RONDÔNIA", "RR", "SANTA CATARINA", "SÃO PAULO", "SERGIPE", "TOCANTINS"]
        )
        self.list3 = self.create_list(["Todos", "Modalidade EAD", "Modalidade Presencial"])
        self.button = QPushButton("Pesquisar", self)
        self.button.clicked.connect(self.handle_search)
        self.button.setVisible(True)  # Tornando o botão visível
        self.style_button()
        self.list_widget.addItems(self.consultas)

    def consulta_clicada(self, item):
        texto = item.text()
        partes = texto.split(" | ")
        if len(partes) == 3:
            selected1, selected2, selected3 = partes
            lista = buscarLista(selected1, selected2, selected3)
            item.setBackground(QColor(100, 150, 200))  # Cor de fundo para destaque
            item.setForeground(QColor(255, 255, 255))
            self.open_new_window(lista, selected1)

    def adicionar_consulta(self, consulta_str):
        if consulta_str in self.consultas:
            self.consultas.remove(consulta_str)
        self.consultas.insert(0, consulta_str)
        self.consultas = self.consultas[:10]  # Limita a 10

        self.list_widget.clear()
        self.list_widget.addItems(self.consultas)

    def style_button(self):
        # Estilo do botão
        self.button.setStyleSheet("""
               QPushButton {
                   background-color: #4a4857;
                   color: #86c28b;
                   font-size: 25px;
                   width: 191.2px;
                   height: 68.6px;
                   border-radius: 10px;
                   border: none;
               }
               QPushButton:hover {
                   background-color: #5c5a68;  /* Mudança de cor no hover */
               }
           """)

    def create_list(self, items):
        list_widget = QListWidget(self)
        list_widget.addItems(items)
        list_widget.setWordWrap(True)
        palette = list_widget.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor(0, 0, 0, 0))
        list_widget.setPalette(palette)
        list_widget.setStyleSheet("""
            QListWidget {
                background: transparent;
                border: none;
                color: #5c5a68;
                font-size: 14px;
            }
        """)
        list_widget.setFrameShape(QListWidget.Shape.NoFrame)

        return list_widget

    def resizeEvent(self, event):
        w = self.width()
        h = self.height()

        self.background.setGeometry(0, 0, w, h)

        self.list1.setGeometry(int(w * 0.095), int(h * 0.32), int(w * 0.25), 140)
        self.list2.setGeometry(int(w * 0.4), int(h * 0.32), int(w * 0.25), 140)
        self.list3.setGeometry(int(w * 0.7), int(h * 0.39), int(w * 0.22), 80)

        self.button.setGeometry(int(w * 0.35), int(h * 0.76), int(w * 0.29), int(h * 0.15))

        super().resizeEvent(event)

    def handle_search(self):
        selected1 = self.list1.currentItem().text() if self.list1.currentItem() else None
        selected2 = self.list2.currentItem().text() if self.list2.currentItem() else None
        selected3 = self.list3.currentItem().text() if self.list3.currentItem() else None

        if not (selected1 and selected2 and selected3):
            return

        consulta_str = f"{selected1} | {selected2} | {selected3}"
        lista = buscarLista(selected1, selected2, selected3)
        self.adicionar_consulta(consulta_str)
        self.open_new_window(lista, selected1)

    def open_new_window(self, lista, selected1):
        self.new_window = NewWindow(lista, selected1)
        self.new_window.show()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
