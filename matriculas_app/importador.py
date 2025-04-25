import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import text
from matriculas_app.app.config.database import engine, SessionLocal
from matriculas_app.app.models.instituicao import Instituicao
from matriculas_app.app.models.curso import Curso
from matriculas_app.app.models.localizacao import Localizacao
from matriculas_app.app.models.matricula import Matricula

csv_path = "data/matriculadosBrasil.csv"
df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
anos = [str(ano) for ano in range(2014, 2023)]

def safe(val):
    return val if pd.notna(val) else None

def testar_conexao():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Conexão com o banco de dados bem-sucedida!")
    except Exception as e:
        print(f"Falha na conexão com o banco de dados: {e}")

def importar_dados_em_lotes(tamanho_lote=1000):
    session: Session = SessionLocal()
    try:
        total = len(df)
        for inicio in range(0, total, tamanho_lote):
            fim = min(inicio + tamanho_lote, total)
            print(f"🔄 Processando linhas {inicio+1} até {fim} de {total}")

            for i, row in df.iloc[inicio:fim].iterrows():
                inst = session.query(Instituicao).filter_by(
                    nome=safe(row['IES']),
                    sigla=safe(row['Sigla'])
                ).first()
                if not inst:
                    inst = Instituicao(
                        nome=safe(row['IES']),
                        sigla=safe(row['Sigla']),
                        organizacao=safe(row['Organização']),
                        categoria_administrativa=safe(row['Categoria Administrativa'])
                    )
                    session.add(inst)
                    session.flush()

                curso = session.query(Curso).filter_by(
                    nome=safe(row['Nome do Curso']),
                    nome_detalhado=safe(row['Nome Detalhado do Curso']),
                    modalidade=safe(row['Modalidade']),
                    grau=safe(row['Grau'])
                ).first()
                if not curso:
                    curso = Curso(
                        nome=safe(row['Nome do Curso']),
                        nome_detalhado=safe(row['Nome Detalhado do Curso']),
                        modalidade=safe(row['Modalidade']),
                        grau=safe(row['Grau'])
                    )
                    session.add(curso)
                    session.flush()

                local = session.query(Localizacao).filter_by(
                    estado=safe(row['Estado']),
                    cidade=safe(row['Cidade'])
                ).first()
                if not local:
                    local = Localizacao(
                        estado=safe(row['Estado']),
                        cidade=safe(row['Cidade'])
                    )
                    session.add(local)
                    session.flush()

                for ano in anos:
                    if pd.notna(row[ano]):
                        matricula = Matricula(
                            curso_id=curso.id,
                            instituicao_id=inst.id,
                            localizacao_id=local.id,
                            ano=ano,
                            quantidade=int(row[ano])
                        )
                        session.add(matricula)

            session.commit()
            print(f"Lote {inicio+1}-{fim} inserido com sucesso!")

        print("Importação finalizada com sucesso")

    except Exception as e:
        session.rollback()
        import traceback
        print(f"Erro durante importação: {e}")
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    testar_conexao()
    importar_dados_em_lotes()