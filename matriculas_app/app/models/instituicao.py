from sqlalchemy import Column, Integer, String
from matriculas_app.app.config.database import Base

class Instituicao(Base):
    __tablename__ = "instituicoes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    sigla = Column(String(50))
    organizacao = Column(String(100))
    categoria_administrativa = Column(String(100))
