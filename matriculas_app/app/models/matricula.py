from sqlalchemy import Column, Integer, ForeignKey, String
from matriculas_app.app.config.database import Base

class Matricula(Base):
    __tablename__ = "matriculas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    curso_id = Column(Integer, ForeignKey("cursos.id"), nullable=False)
    instituicao_id = Column(Integer, ForeignKey("instituicoes.id"), nullable=False)
    localizacao_id = Column(Integer, ForeignKey("localizacoes.id"), nullable=False)
    ano = Column(String(4), nullable=False)
    quantidade = Column(Integer, nullable=False)
