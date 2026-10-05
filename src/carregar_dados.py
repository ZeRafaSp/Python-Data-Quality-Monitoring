import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

df_carga = pd.read_csv(
    "data/transacoes.csv",
    dtype=str
)

df_carga["id_transacao"] = pd.to_numeric(
    df_carga["id_transacao"],
    errors="coerce"
)

df_carga["id_cliente"] = pd.to_numeric(
    df_carga["id_cliente"],
    errors="coerce"
)

df_carga["valor"] = pd.to_numeric(
    df_carga["valor"],
    errors="coerce"
)

print(df_carga)
print("\nQuantidade de registros:", len(df_carga))


engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

with engine.connect() as conexao:
    conexao.execute(text("TRUNCATE TABLE transacoes"))
    conexao.commit()

df_carga.to_sql(
    "transacoes",
    engine,
    if_exists="append",
    index=False
)

print("\nDados carregados no PostgreSQL com sucesso!")