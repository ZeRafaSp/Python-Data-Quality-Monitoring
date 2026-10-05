import pandas as pd
from datetime import datetime
import logging
import sys
import os
from sqlalchemy import create_engine 
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

logging.info("Conexão com PostgreSQL realizada com sucesso!")

query = "SELECT * FROM transacoes"

df = pd.read_sql(query, engine)

df["data_transacao"] = pd.to_datetime(
    df["data_transacao"],
    errors="coerce"
)

print(df)
print("\nQuantidade de registros:", len(df))


os.makedirs("logs", exist_ok=True)
os.makedirs("output", exist_ok=True)

logging.basicConfig(
    filename= "logs/monitoramento.log",
    level= logging.INFO,
    format= "%(asctime)s - %(levelname)s - %(message)s"
)

data_execucao = datetime.now()

logging.info("Inicio do monitoramento")

print("\n Data de execução: ", data_execucao)


colunas_obrigatorias = [
    "id_transacao",
    "id_cliente",
    "data_transacao",
    "valor",
    "status",
    "canal"
]

colunas_faltantes = [
    coluna
    for coluna in colunas_obrigatorias
    if coluna not in df.columns
]

if colunas_faltantes:
    logging.error(f"Colunas obrigatorias ausentes: {colunas_faltantes}")
    print("ERRO: Existem colunas obrigatórias ausentes.")
    print("Colunas faltantes:", colunas_faltantes)
    sys.exit()


print("primeiras linhas: ")
print(df.head())

print("\nInformações de base: ")
print(df.info())

print("\nlinhas e colunas: ")
print(df.shape)

total_registros = len(df)

print("\n valores nulos: ")
print(df.isnull().sum())

print("\n verificação de duplicidade: ")

duplicados = df.duplicated()
print("\n quantidade de linhas duplicacdas: ", duplicados.sum())

print("\n Registros duplicados: ")
print(df[duplicados])


print("\n verificando valores negativos: ")

valores_negativos = df[df["valor"] < 0]

print("\n Quantidade de valores negativos: ", len(valores_negativos))
print(valores_negativos)

limite = 10000

valores_suspeitos = df[df["valor"] > limite]

print("\n Quantidade de valores acima do limite: ", len(valores_suspeitos))
print(valores_suspeitos)


print("\n validação de status: ")

status_validos = ["aprovado", "recusado"]

status_invalidos = df[~df["status"].isin(status_validos)]

print("\n Quantidade de status invalidos", len(status_invalidos))
print(status_invalidos)

print("\n Validação de datas: ")

df["data_transacao"] = pd.to_datetime(
    df["data_transacao"],
    errors="coerce"
)

datas_invalidas = df[df["data_transacao"].isnull()]

print("\n Quantidade de datas nulas", len(datas_invalidas))
print(datas_invalidas)


quantidade_nulos = df.isnull().sum().sum()
quantidade_duplicados = df.duplicated().sum()
quantidade_negativos = len(valores_negativos)
quantidade_suspeitos = len(valores_suspeitos)
quantidade_status_invalidos = len(status_invalidos)
quantidade_datas_invalidas = len(datas_invalidas)

problemas = (
    quantidade_nulos
    + quantidade_duplicados
    + quantidade_negativos
    + quantidade_suspeitos
    + quantidade_status_invalidos
    + quantidade_datas_invalidas
)

percentual_problemas = (problemas / total_registros) * 100


problemas_criticos = []
problemas_alerta = []

if quantidade_datas_invalidas > 0:
    problemas_criticos.append(
        f"Datas invalidos: {quantidade_datas_invalidas}"
    )

if quantidade_status_invalidos > 0:
    problemas_criticos.append(
        f"Status invalidos: {quantidade_status_invalidos}"
    )

if quantidade_nulos > 0:
    problemas_alerta.append(
        f"Valores ausentes: {quantidade_nulos}"
    )

if quantidade_duplicados > 0:
    problemas_alerta.append(
        f"Duplicidades: {quantidade_duplicados}"
    )

if quantidade_negativos > 0:
    problemas_alerta.append(
        f"Valores negativos: {quantidade_negativos}"
    )

if quantidade_suspeitos > 0:
    problemas_alerta.append(
        f"Valores acima do limite: {quantidade_suspeitos}"
    )


if quantidade_status_invalidos > 0 or quantidade_datas_invalidas > 0:
    status_monitoramento = "FALHA"
   
elif problemas > 0:
    status_monitoramento = "ALERTA"

else:
    status_monitoramento = "OK"



if quantidade_nulos > 0:
    logging.warning(f"Valores ausentes encontrados: {quantidade_nulos}")

if quantidade_duplicados > 0:
    logging.warning(f"Valores duplicados encontrados: {quantidade_duplicados}")
    
if quantidade_negativos > 0:
    logging.warning(f"Valores negativos encontrados: {quantidade_negativos}")

if quantidade_suspeitos > 0:
    logging.warning(f"Valores acima do limite encontrados: {quantidade_suspeitos}")

if quantidade_status_invalidos > 0:
    logging.warning(f"Status invalidos encontrados: {quantidade_status_invalidos}")

if quantidade_datas_invalidas > 0:
    logging.warning(f"Datas invalidas encontradas: {quantidade_datas_invalidas}")

logging.info(f"Monitoramento finalizado com status: {status_monitoramento}")


relatorio =f"""
RELATÓRIO DE MONITORAMENTO
==========================

Data de execução: {data_execucao}

Registros analisados: {total_registros}
Quantidade de problema: {problemas}
Percentual de problemas: {percentual_problemas:.2f}%

Valores ausentes: {quantidade_nulos}
Duplicidades: {quantidade_duplicados}
Valores negativos: {quantidade_negativos}
Valores acima do limite: {quantidade_suspeitos}
Status inválidos: {quantidade_status_invalidos}
Datas inválidas: {quantidade_datas_invalidas}

STATUS: {status_monitoramento}

Problemas criticos: 
{chr(10).join(problemas_criticos) if problemas_criticos else "Nenhum"}

Problemas em alerta:
{chr(10).join(problemas_alerta) if problemas_alerta else "Nenhum"}

"""

print(relatorio)

with open("output/relatorio_monitoramento.txt", "w", encoding="utf-8") as arquivo:
    arquivo.write(relatorio)


duplicados_ = df.duplicated(keep=False)
df_problemas = df.copy()

df_problemas["tipo_problema"] = ""

df_problemas.loc[df_problemas["valor"] < 0, "tipo_problema"] += "Valor negativo; "

df_problemas.loc[df_problemas["valor"] > limite, "tipo_problema"] += "Valor acima do limite; "

df_problemas.loc[~df_problemas["status"].isin(status_validos), "tipo_problema"] += "Status invalido; "

df_problemas.loc[df_problemas["data_transacao"].isnull(), "tipo_problema"] += "Data invalida; "

df_problemas.loc[df_problemas["id_cliente"].isnull(), "tipo_problema"] += "Id do cliente ausente; "

df_problemas.loc[df_problemas["valor"].isnull(), "tipo_problema"] += "Valor ausente; "

df_problemas.loc[duplicados_, "tipo_problema"] += "Duplicidade; "

df_problemas["tipo_problema"] = df_problemas["tipo_problema"].str.rstrip("; ")

registro_com_problemas = df_problemas[
    df_problemas["tipo_problema"] != ""    
]

registro_com_problemas.to_csv("output/registro_com_problemas.csv", index=False)