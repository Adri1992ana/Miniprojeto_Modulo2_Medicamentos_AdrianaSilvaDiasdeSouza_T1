# Mini-Projeto Avaliativo — Banco de Preços em Saúde (BPS)

### Visualização de Dados e Business Intelligence — Módulo 2, Semana 07

**Aluna:** Adriana | **Turma:** T1

---

## 1. Objetivo do projeto

Desenvolver, individualmente, um dashboard analítico em Power BI para acompanhar as compras de medicamentos e dispositivos médicos registradas no Banco de Preços em Saúde (BPS) entre 2020 e 2026. O dashboard permite explorar a evolução temporal dos valores, a distribuição geográfica das compras, os produtos e fornecedores/fabricantes mais relevantes, a variação de preços unitários e as modalidades de compra utilizadas, por meio de KPIs, gráficos e filtros interativos.

## 2. Contextualização do problema

A gestão eficiente dos recursos públicos é um desafio central para os órgãos de saúde: a aquisição de medicamentos e dispositivos médicos envolve grande volume financeiro, múltiplos fornecedores, diferentes modalidades de compra e ampla variedade de produtos. Este projeto usa os dados públicos do Banco de Preços em Saúde (BPS), do Ministério da Saúde, para construir um dashboard que apoie a comparação de preços entre instituições e fornecedores, a identificação de variações relevantes nos preços unitários, a distribuição das compras entre estados/municípios/instituições e o acompanhamento da evolução das compras ao longo dos anos.

Importante: a análise de diferenças de preços apresentada neste projeto **não deve ser interpretada automaticamente como comprovação de economia, sobrepreço ou irregularidade** — variações podem decorrer de fatores como fabricante, apresentação, unidade de fornecimento, quantidade adquirida, localidade, modalidade de compra e características específicas de cada negociação.

## 3. Fonte dos dados

- Banco de Preços em Saúde (BPS) — Ministério da Saúde
- Portal: https://dadosabertos.saude.gov.br/dataset/bps
- Arquivos anuais em CSV, referentes aos anos de 2020 a 2026
- Observação: durante a coleta, o portal principal apresentou instabilidade (erro 500). Os arquivos foram obtidos com sucesso via link direto dos arquivos no repositório S3 do Ministério da Saúde.

## 4. Procedimentos utilizados para baixar e concatenar as bases anuais

- Download manual dos arquivos `.csv` de 2020 a 2026, organizados em `BPS_20_26_AdrianaSilvaDiasdeSouza_T1/Dados/Original/`
- Concatenação e tratamento da base usada no **dashboard** realizados via **Power Query (Power BI)**, usando "Obter Dados > Pasta" apontando para `dados/original/`, com a função "Combinar e Transformar" para unir os 7 arquivos automaticamente
- Criada a coluna **`ano_compra`** (tipo Número Inteiro) a partir do nome de cada arquivo de origem, permitindo identificar a que ano cada registro pertence
- Para gerar o **arquivo de entrega consolidado** (`BPS_20_26_AdrianaSilvaDiasdeSouza.csv`), foi usado um script em **Python (pandas)**, replicando os mesmos tratamentos aplicados no Power Query (coluna ano_compra, colunas de CNPJ/ANVISA como texto, preco_unitario/preco_total como decimal, remoção de duplicados) — usado apenas para a exportação do CSV final, já que o Power BI Desktop não permite exportar tabelas grandes (342 mil+ linhas) diretamente sem ferramentas externas.

## 5. Tratamentos e transformações realizados nos dados

- **CNPJ da instituição:** mantido como tipo **Texto**, pois é um código identificador (não uma quantidade) — evita perda de formatação (pontos/traços) e conversões incorretas.
- **Código ANVISA:** a coluna havia sido convertida automaticamente para tipo Número, o que gerava exibição em notação científica (ex: `1,0311E+12`). Corrigido para tipo **Texto**, restaurando a exibição correta do código completo.
- **Valores nulos na coluna ANVISA:** identificados como nulos legítimos — nem toda compra registrada no BPS possui código ANVISA vinculado (ex: itens sem registro ou pendência de cadastro). Não foram removidos nem preenchidos.
- **Verificação da consulta combinada:** confirmado, via a coluna `Nome da Origem` (7 valores distintos) e `ano_compra` (7 valores distintos), que a consulta final "Original" contém os 7 anos combinados corretamente.
- **Qualidade das colunas (base completa):** `nome_instituicao` com <1% de valores vazios; demais colunas analisadas (esfera, cnpj_instituicao, municipio_instituicao) sem erros e sem vazios relevantes.
- **Duplicados:** aplicado "Remover Duplicadas" considerando todas as colunas na consulta combinada. Total caiu de 342.716 para **342.697 linhas** (19 duplicatas reais removidas). Casos de registros aparentemente repetidos (ex: mesma instituição em linhas seguidas) foram verificados e confirmados como compras distintas (diferiam em outras colunas, como produto/valor/data), portanto não foram removidos.
- **Valores monetários (preco_unitario, preco_total):** a conversão padrão para Número Decimal usava a configuração regional pt-BR, interpretando o ponto do CSV original como separador de milhar em vez de decimal (ex: `1500.00` virava `150000`). Corrigido usando "Tipo de Dados > Usando Local > Inglês (Estados Unidos)", que interpreta corretamente o ponto como separador decimal. Conferido manualmente que `qtd_itens_comprados × preco_unitario = preco_total` após a correção.
- **Base final:** carregada no modelo do Power BI com **342.697 linhas** (2020–2026), tipos padronizados e duplicados tratados.

## 6. Descrição das principais colunas utilizadas

| Coluna                                                                  | Descrição                                                                                                         |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| `ano_compra`                                                          | Ano da compra, criado a partir do nome do arquivo de origem                                                         |
| `nome_instituicao` / `cnpj_instituicao`                             | Nome e CNPJ da instituição compradora                                                                             |
| `esfera`                                                              | Esfera administrativa da instituição (Municipal, Estadual etc.)                                                   |
| `municipio_instituicao` / `uf_compra`                               | Município e estado da instituição compradora                                                                     |
| `codigo_br` / `descricao_catmat`                                    | Código e descrição do produto (CATMAT); descricao_catmat contém HTML bruto em parte dos registros (ver item 11) |
| `unidade_fornecimento_generico` / `unidade_medida` / `capacidade` | Unidade e apresentação do produto                                                                                 |
| `anvisa`                                                              | Código de registro ANVISA do produto (texto, contém nulos legítimos)                                             |
| `modalidade_compra` / `tipo_compra`                                 | Modalidade e tipo do processo de compra (ex: Pregão, Dispensa de Licitação)                                      |
| `cnpj_fornecedor` / `fornecedor`                                    | Identificação de quem forneceu/entregou o produto                                                                 |
| `cnpj_fabricante` / `fabricante`                                    | Identificação do fabricante do produto                                                                            |
| `qtd_itens_comprados`                                                 | Quantidade de itens adquiridos no registro                                                                          |
| `preco_unitario` / `preco_total`                                    | Preço unitário e valor total da compra (decimal)                                                                  |

## 7. Definição dos KPIs e das métricas

```DAX
Valor Total Registrado = SUM('Original'[preco_total])
Quantidade Total de Itens Comprados = SUM('Original'[qtd_itens_comprados])
Número de Registros de Compra = COUNTROWS('Original')
Instituições Compradoras = DISTINCTCOUNT('Original'[cnpj_instituicao])
Fornecedores = DISTINCTCOUNT('Original'[cnpj_fornecedor])
Preço Unitário Médio Ponderado = DIVIDE([Valor Total Registrado], [Quantidade Total de Itens Comprados])
```

- **Instituições Compradoras** e **Fornecedores** usam o CNPJ (não o nome) como chave de contagem distinta, para evitar duplicidade por grafias diferentes do mesmo nome.
- **Preço Unitário Médio Ponderado** usa `DIVIDE()` (não o operador `/`) para tratar divisão por zero automaticamente quando os filtros deixarem a base vazia. Deve ser interpretado com cautela quando os filtros incluírem produtos, unidades ou apresentações diferentes.

## 8. Link ou imagens do dashboard

- Arquivo do dashboard: `dashboard/BPS_20_26_AdrianaSilvaDiasdeSouza.pbix`
- Print da página final: *(inserir aqui a imagem salva em `imagens/dashboard_final.png` depois de exportar o print do Power BI)*
- Link do repositório no GitHub: *(inserir aqui após a publicação na Pasta Oficial de Projetos da Turma)*

**Design do dashboard:** página única (16:9), com fundo customizado definindo as zonas de KPIs, filtros e os 7 visuais, garantindo consistência visual e hierarquia clara. Títulos dos visuais vêm do fundo customizado (títulos nativos do Power BI desativados), evitando repetição. Filtros interativos (segmentações de dados): `ano_compra`, `uf_compra`, `modalidade_compra`, `esfera`.

**Visuais do dashboard:**

1. Gráfico de linhas — evolução do Valor Total Registrado por `ano_compra`
2. Barras horizontais — ranking de `uf_compra` por Valor Total Registrado (Top 10)
3. Barras — Top 15 `descricao_catmat` por Quantidade Total de Itens Comprados
   4a/4b. Barras — Top 10 `fornecedor` e Top 10 `fabricante` por Valor Total Registrado
4. Dispersão — variação de `preco_unitario` por `codigo_br` (Top 20), valores exatos disponíveis via tooltip
5. Barras — Número de Registros de Compra por `modalidade_compra`

## 9. Principais análises e descobertas

- **Evolução temporal:** valores sobem de 2020 (~5 Bi) até um pico em 2022 (~22 Bi), recuam em 2023 (~8 Bi), atingem o maior pico em 2025 (~32 Bi) e caem para ~2 Bi em 2026. A queda de 2026 reflete dado parcial (ano corrente, ainda em andamento), não uma redução real de compras.
- **Concentração geográfica:** PR (~30 Bi) e SP (~27 Bi) lideram amplamente o volume financeiro, muito à frente do terceiro colocado (CE) — indício de concentração geográfica relevante nas compras registradas.
- **Padrão volume x valor:** os medicamentos mais adquiridos em quantidade são itens essenciais de baixo custo e uso crônico (Losartana, Hidroclorotiazida, Metformina, Dipirona, Omeprazol, dietas enterais). Já os fornecedores líderes em valor financeiro são dominados por medicamentos de alto custo unitário — especialidades e oncológicos (AstraZeneca, Novartis, Janssen-Cilag, Onco Prod, Oncovit) — com destaque para o fornecedor Agille Comercio, que lidera isoladamente (~23 Bi), bem à frente dos demais.
- No visual de dispersão (Top 20 `codigo_br` por Quantidade Total de Itens Comprados), o código **332849** se destaca com preço unitário médio ponderado de **0,91**, bem acima dos demais códigos do grupo (maioria entre 0,01 e 0,32) — candidato a investigação mais aprofundada (sem conclusão de irregularidade, conforme orientação do desafio). O código **404992** tem a maior quantidade adquirida do grupo (4,36 Bi de itens) a preço muito baixo (0,01), consistente com um insumo básico comprado em escala.
- **Modalidades de compra:** Pregão domina amplamente, com ~315 mil registros (≈92% do total de 342.697), seguido de longe por Dispensa de Licitação (~13 mil) e Registro de Preços (~11 mil). As demais modalidades (Tomada de Preços, Concorrência, Inexigibilidade, Concurso, Convite, Leilão) somadas representam menos de 1% dos registros.
- **Varredura ampla de outliers de preço (script Python, método IQR por produto):** de 342.697 registros, 5.580 produtos tinham base suficiente (5+ compras) para comparação. **14.863 registros (≈4,3% da base)** ficaram fora do padrão esperado de preço para o próprio produto (limite de 3x IQR). A maior parte provavelmente reflete variação legítima (fabricante, apresentação, negociação), mas os casos mais extremos — com preço unitário entre ~4.000 e ~30.000 vezes a mediana do mesmo produto — sugerem fortemente **erro de digitação na fonte** (possível troca entre preço unitário e preço total em compras de quantidade pequena), não apenas variação de mercado. Exemplos: código 305494 (Didrogesterona) a R$ 55.776,00 contra mediana de R$ 1,85 (30.149x); código 415898 (Nebulizador) a R$ 1.439.000,00 contra mediana de R$ 135,30 (10.636x). Lista completa salva em `outliers_preco_unitario.csv`.

## 10. Recomendações baseadas nos dados

- Investigar com mais profundidade o código de produto 332849 (comparar unidade de fornecimento, fabricante e apresentação com produtos similares antes de qualquer conclusão).
- Avaliar a concentração de compras no fornecedor Agille Comercio — entender se decorre de contratos consolidados legítimos ou representa risco de dependência de fornecedor único.
- Como o Pregão é quase a modalidade exclusiva (~92%), garantir que as demais modalidades continuem sendo usadas nos casos em que são tecnicamente mais adequadas.
- Comparar preços de medicamentos de alto volume (genéricos essenciais) entre estados/fornecedores para identificar oportunidades de economia de escala nas compras.
- Implementar validações automáticas de faixa de preço no momento do lançamento dos dados (ex: alertar quando o preço unitário foge muito da mediana histórica do mesmo produto), para reduzir erros de digitação como os identificados na varredura de outliers (item 9) antes que entrem na base pública.

## 11. Limitações identificadas na base ou na análise

- **descricao_catmat contém HTML bruto e entidades codificadas** (ex: `&#193;`, `<BR><TABLE...>`, `<LABEL>`) em parte dos registros, herdados da fonte original. Isso impede o uso direto dessa coluna como categoria em visuais (gera categorias falsas por variação de formatação). Optou-se por usar `codigo_br` como identificador de produto nos gráficos, mantendo descricao_catmat apenas como detalhe/tooltip.
- **Ano de 2026 incompleto:** por ser o ano corrente, a base contém apenas dados parciais de 2026, o que faz a evolução temporal aparentar uma queda brusca no último ponto — não deve ser lida como redução real de compras.
- **Diferenças de preço não implicam irregularidade:** conforme orientação do próprio desafio, variações de preço podem decorrer de fabricante, apresentação, unidade de fornecimento, quantidade, localidade, modalidade de compra e características da negociação — os pontos destacados no item 9 são indicativos para investigação, não conclusões.
- **Possíveis erros de digitação na base pública:** a varredura de outliers (item 9) identificou uma minoria de registros com preço unitário milhares de vezes acima do padrão do próprio produto, provavelmente decorrentes de erro de lançamento na fonte (não de variação real de preço) — qualquer KPI financeiro calculado sobre `preco_unitario`/`preco_total` sem filtrar esses casos pode estar distorcido por eles.

## 12. Instruções para reprodução do projeto

1. Clone o repositório ou baixe a pasta `BPS_20_26_AdrianaSilvaDiasdeSouza_T1/` completa.
2. Os dados brutos estão em `Dados/Original/` (BPS_2020.csv a BPS_2026.csv) e a base já consolidada em `Dados/Processado/BPS_20_26_AdrianaSilvaDiasdeSouza.csv` — **compactada em .zip no repositório** (o CSV puro tem ~130 MB, acima do limite do GitHub); extraia o .zip antes de usar.
3. Para reproduzir a consolidação a partir do zero: rode o script `concatenar_bps.py` com Python 3 e a biblioteca `pandas` instalada (`pip install pandas`), ajustando as variáveis `PASTA_ORIGINAL`/`SAIDA` conforme a pasta onde o script estiver.
4. Para o dashboard: abra `dashboard/BPS_20_26_AdrianaSilvaDiasdeSouza.pbix` no Power BI Desktop.
5. Se o Power BI pedir para atualizar o caminho da pasta de origem (Transformar Dados > Configurações da Fonte de Dados), aponte para a pasta `Dados/Original/` no seu computador e clique em Atualizar.
6. Todas as medidas DAX e visuais já estão configurados na página única do relatório.

---

*README em construção — atualizado a cada etapa concluída do desenvolvimento.*
