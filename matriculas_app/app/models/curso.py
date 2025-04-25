from sqlalchemy import Column, Integer, String
from matriculas_app.app.config.database import Base

class Curso(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    nome_detalhado = Column(String(255))
    modalidade = Column(String(20))
    grau = Column(String(50))
