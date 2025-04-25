# app/config/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

USUARIO = 'root'
SENHA = ''
HOST = 'localhost'
PORTA = '3306'
BANCO = 'matriculas'

DATABASE_URL = f"mysql+pymysql://{USUARIO}:{SENHA}@{HOST}:{PORTA}/{BANCO}"

engine = create_engine(DATABASE_URL, echo=True, future=True)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

if __name__ == "__main__":
    try:
        with engine.connect() as conn:
            print("Conexão bem-sucedida")
    except Exception as e:
        print(f"Erro ao conectar: {e}")

