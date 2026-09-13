"""
Varredura de outliers de preço unitário, por produto (codigo_br).

Para cada produto, calcula a mediana e o intervalo interquartil (IQR) do
preco_unitario entre TODAS as compras registradas daquele produto, e sinaliza
registros cujo preço foge muito do padrão do próprio produto (método IQR,
com margem de 3x — mais conservador que o padrão de 1.5x, pra focar só nos
desvios mais extremos).

Isso NÃO significa irregularidade — é só um ponto de partida para investigação,
igual orientado no desafio.
"""

import pandas as pd
import numpy as np
from pathlib import Path


ARQUIVO = Path("Dados/Processado/BPS_20_26_AdrianaSilvaDiasdeSouza.csv")
SAIDA = Path("Dados/Processado/outliers_preco_unitario.csv")
MIN_AMOSTRAS_POR_PRODUTO = 5   # produtos com poucas compras não têm base de comparação confiável
MULTIPLICADOR_IQR = 3          # 3x = outlier "extremo"; 1.5x pegaria mais casos (mais sensível)

df = pd.read_csv(ARQUIVO, low_memory=False)
df["preco_unitario"] = pd.to_numeric(df["preco_unitario"], errors="coerce")

colunas_contexto = [c for c in [
    "codigo_br", "descricao_catmat", "preco_unitario", "qtd_itens_comprados",
    "fornecedor", "fabricante", "nome_instituicao", "uf_compra", "ano_compra",
] if c in df.columns]

resultados = []
for codigo, grupo in df.groupby("codigo_br"):
    precos = grupo["preco_unitario"].dropna()
    if len(precos) < MIN_AMOSTRAS_POR_PRODUTO:
        continue

    q1, q3 = precos.quantile([0.25, 0.75])
    iqr = q3 - q1
    if iqr == 0:
        continue  # produto com preço sempre igual, nada a comparar

    limite_superior = q3 + MULTIPLICADOR_IQR * iqr
    limite_inferior = max(q1 - MULTIPLICADOR_IQR * iqr, 0)
    mediana = precos.median()

    outliers = grupo[
        (grupo["preco_unitario"] > limite_superior) | (grupo["preco_unitario"] < limite_inferior)
    ].copy()

    if outliers.empty:
        continue

    outliers["mediana_produto"] = mediana
    outliers["razao_vs_mediana"] = outliers["preco_unitario"] / mediana
    resultados.append(outliers[colunas_contexto + ["mediana_produto", "razao_vs_mediana"]])

if resultados:
    saida_df = pd.concat(resultados, ignore_index=True)
    saida_df = saida_df.sort_values("razao_vs_mediana", ascending=False)
else:
    saida_df = pd.DataFrame(columns=colunas_contexto + ["mediana_produto", "razao_vs_mediana"])

SAIDA.parent.mkdir(parents=True, exist_ok=True)
saida_df.to_csv(SAIDA, index=False, encoding="utf-8")

print(f"Total de registros na base: {len(df):,}")
print(f"Produtos avaliados (>= {MIN_AMOSTRAS_POR_PRODUTO} compras): {df.groupby('codigo_br').filter(lambda g: len(g) >= MIN_AMOSTRAS_POR_PRODUTO)['codigo_br'].nunique():,}")
print(f"Registros sinalizados como outlier: {len(saida_df):,}")
print(f"\nArquivo salvo em: {SAIDA.resolve()}")

if not saida_df.empty:
    print("\nTop 15 outliers (maior razão vs. mediana do próprio produto):")
    print(saida_df.head(15).to_string(index=False))