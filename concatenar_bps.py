"""
Concatena os arquivos do BPS (2020 a 2026) em um único CSV.

Tratamentos:
- cria coluna ano_compra a partir do nome do arquivo
- mantém CNPJs e ANVISA como texto
- converte preco_unitario e preco_total para numérico
- remove duplicidades
"""

import pandas as pd
from pathlib import Path
import re

# ==========================================
# AJUSTE APENAS ESTES CAMINHOS SE NECESSÁRIO
# ==========================================

PASTA_ORIGINAL = Path(
    r"C:\Users\silva\Downloads\Miniprojeto_Modulo2_Medicamentos_AdrianaSilvaDiasdeSouza_T1\BPS_20_26_AdrianaSilvaDiasdeSouza_T1\Dados\Original"
)

SAIDA = Path(
    r"C:\Users\silva\Downloads\Miniprojeto_Modulo2_Medicamentos_AdrianaSilvaDiasdeSouza_T1\BPS_20_26_AdrianaSilvaDiasdeSouza_T1\Dados\Processado\BPS_20_26_AdrianaSilvaDiasdeSouza.csv"
)

SEPARADOR = ";"
ENCODING = "utf-8"

# ==========================================

colunas_texto = [
    "cnpj_instituicao",
    "cnpj_fornecedor",
    "cnpj_fabricante",
    "anvisa",
]

print("=" * 60)
print("PASTA ENCONTRADA:", PASTA_ORIGINAL.exists())
print("LOCAL:", PASTA_ORIGINAL)
print("=" * 60)

arquivos = list(PASTA_ORIGINAL.glob("*.csv"))

print(f"\nCSVs encontrados: {len(arquivos)}")

for arq in arquivos:
    print(" -", arq.name)

if len(arquivos) == 0:
    raise Exception(
        "Nenhum arquivo CSV encontrado na pasta informada."
    )

dfs = []

for arquivo in sorted(arquivos):

    try:

        print(f"\nLendo: {arquivo.name}")

        match = re.search(r"(20\d{2})", arquivo.stem)

        if match:
            ano = int(match.group(1))
        else:
            ano = None

        df = pd.read_csv(
            arquivo,
            sep=SEPARADOR,
            encoding=ENCODING,
            dtype={c: str for c in colunas_texto},
            low_memory=False,
        )

        df["ano_compra"] = ano

        dfs.append(df)

        print(f"OK -> {len(df):,} linhas")

    except Exception as erro:
        print(f"ERRO em {arquivo.name}")
        print(erro)

if len(dfs) == 0:
    raise Exception(
        "Nenhum DataFrame foi carregado. Verifique o separador e codificação."
    )

print("\nConcatenando arquivos...")

base = pd.concat(dfs, ignore_index=True)

print(f"Total antes dos duplicados: {len(base):,}")

for coluna in ["preco_unitario", "preco_total"]:

    if coluna in base.columns:

        base[coluna] = (
            base[coluna]
            .astype(str)
            .str.replace(",", ".", regex=False)
        )

        base[coluna] = pd.to_numeric(
            base[coluna],
            errors="coerce"
        )

base = base.drop_duplicates()

print(f"Total após remoção de duplicados: {len(base):,}")

SAIDA.parent.mkdir(parents=True, exist_ok=True)

base.to_csv(
    SAIDA,
    index=False,
    encoding="utf-8-sig"
)

print("\nArquivo criado com sucesso:")
print(SAIDA)

print("\nFim do processo.")