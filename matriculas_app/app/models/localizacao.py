from sqlalchemy import Column, Integer, String
from matriculas_app.app.config.database import Base

class Localizacao(Base):
    __tablename__ = "localizacoes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    estado = Column(String(50), nullable=False)
    cidade = Column(String(100), nullable=False)
