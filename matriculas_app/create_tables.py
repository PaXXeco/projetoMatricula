from matriculas_app.app.config.database import Base, engine
from matriculas_app.app.models import curso, instituicao, localizacao, matricula

Base.metadata.create_all(bind=engine)
print("Tabelas criadas com sucesso!")
