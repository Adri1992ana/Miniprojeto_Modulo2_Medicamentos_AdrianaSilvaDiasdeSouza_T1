Mini-Projeto Avaliativo --- Banco de Preços em Saúde (BPS)

Visualização de Dados e Business Intelligence --- Módulo 2, Semana 07

Aluna: Adriana Silva Dias de Souza | Turma: T1

1. Objetivo do projeto

Desenvolver, individualmente, um dashboard analítico em Power BI para
acompanhar as compras de medicamentos e dispositivos médicos registradas
no Banco de Preços em Saúde (BPS) entre 2020 e 2026. O dashboard permite
explorar a evolução temporal dos valores, a distribuição geográfica das
compras, os produtos e fornecedores/fabricantes mais relevantes, a
variação de preços unitários e as modalidades de compra utilizadas, por
meio de KPIs, gráficos e filtros interativos.

2. Contextualização do problema

A gestão eficiente dos recursos públicos é um desafio central para os
órgãos de saúde: a aquisição de medicamentos e dispositivos médicos
envolve grande volume financeiro, múltiplos fornecedores, diferentes
modalidades de compra e ampla variedade de produtos. Este projeto usa os
dados públicos do Banco de Preços em Saúde (BPS), do Ministério da
Saúde, para construir um dashboard que apoie a comparação de preços
entre instituições e fornecedores, a identificação de variações
relevantes nos preços unitários, a distribuição das compras entre
estados/municípios/instituições e o acompanhamento da evolução das
compras ao longo dos anos.

Importante: a análise de diferenças de preços apresentada neste projeto
não deve ser interpretada automaticamente como comprovação de
economia, sobrepreço ou irregularidade --- variações podem decorrer de
fatores como fabricante, apresentação, unidade de fornecimento,
quantidade adquirida, localidade, modalidade de compra e características
específicas de cada negociação.

3. Fonte dos dados

Banco de Preços em Saúde (BPS) --- Ministério da Saúde

Portal: https://dadosabertos.saude.gov.br/dataset/bps

Arquivos anuais em CSV, referentes aos anos de 2020 a 2026

Observação: durante a coleta, o portal principal apresentou
instabilidade (erro 500). Os arquivos foram obtidos com sucesso via
link direto dos arquivos no repositório S3 do Ministério da Saúde.

4. Procedimentos utilizados para baixar e concatenar as bases anuais

Download manual dos arquivos .csv de 2020 a 2026, organizados em
Dados/Original/

Concatenação e tratamento da base usada no dashboard realizados
via Power Query (Power BI), usando "Obter Dados > Pasta"
apontando para Dados/Original/, com a função "Combinar e
Transformar" para unir os 7 arquivos automaticamente

Criada a coluna ano_compra (tipo Número Inteiro) a partir do
nome de cada arquivo de origem, permitindo identificar a que ano
cada registro pertence

Para gerar o arquivo de entrega consolidado
(Dados/Processado/BPS_20_26_AdrianaSilvaDiasdeSouza.csv), foi
usado um script em Python (pandas), replicando os mesmos
tratamentos aplicados no Power Query (coluna ano_compra, colunas de
CNPJ/ANVISA como texto, preco_unitario/preco_total como decimal,
remoção de duplicados) --- usado apenas para a exportação do CSV
final, já que o Power BI Desktop não permite exportar tabelas
grandes (342 mil+ linhas) diretamente sem ferramentas externas.

5. Tratamentos e transformações realizados nos dados

CNPJ da instituição: mantido como tipo Texto, pois é um
código identificador (não uma quantidade) --- evita perda de
formatação (pontos/traços) e conversões incorretas.

Código ANVISA: a coluna havia sido convertida automaticamente
para tipo Número, o que gerava exibição em notação científica (ex:
1,0311E+12). Corrigido para tipo Texto, restaurando a exibição
correta do código completo.

Valores nulos na coluna ANVISA: identificados como nulos
legítimos --- nem toda compra registrada no BPS possui código ANVISA
vinculado (ex: itens sem registro ou pendência de cadastro). Não
foram removidos nem preenchidos.

Verificação da consulta combinada: confirmado, via a coluna
Nome da Origem (7 valores distintos) e ano_compra (7 valores
distintos), que a consulta final "Original" contém os 7 anos
combinados corretamente.

Qualidade das colunas (base completa): nome_instituicao com
<1% de valores vazios; demais colunas analisadas (esfera,
cnpj_instituicao, municipio_instituicao) sem erros e sem vazios
relevantes.

Duplicados: aplicado "Remover Duplicadas" considerando todas as
colunas na consulta combinada. Total caiu de 342.716 para 342.697
linhas (19 duplicatas reais removidas). Casos de registros
aparentemente repetidos (ex: mesma instituição em linhas seguidas)
foram verificados e confirmados como compras distintas (diferiam em
outras colunas, como produto/valor/data), portanto não foram
removidos.

Valores monetários (preco_unitario, preco_total): a conversão
padrão para Número Decimal usava a configuração regional pt-BR,
interpretando o ponto do CSV original como separador de milhar em
vez de decimal (ex: 1500.00 virava 150000). Corrigido usando
"Tipo de Dados > Usando Local > Inglês (Estados Unidos)", que
interpreta corretamente o ponto como separador decimal. Foi
realizada verificação da consistência entre quantidade, preço
unitário e preço total, incluindo análise de registros com
divergências.

Base final: carregada no modelo do Power BI com 342.697
linhas (2020--2026), tipos padronizados e duplicados tratados.

6. Descrição das principais colunas utilizadas

Coluna Descrição

ano_compra                        Ano da compra, criado a partir do
nome do arquivo de origem

nome_instituicao /                Nome e CNPJ da instituição
cnpj_instituicao                  compradora

esfera                            Esfera administrativa da instituição
(Municipal, Estadual etc.)

municipio_instituicao / uf      Município e estado (UF) da
instituição compradora

compra                            Identificador do processo de compra

insercao                          Data de inserção do registro na base

codigo_br / descricao_catmat    Código e descrição do produto
(CATMAT); descricao_catmat contém
HTML bruto em parte dos registros
(ver item 11)

unidade_fornecimento / generico Unidade, apresentação e indicação de
/ unidade_medida / capacidade / genérico do produto
unidade_fornecimento_capacidade

anvisa                            Código de registro ANVISA do produto
(texto, contém nulos legítimos)

modalidade_compra / tipo_compra Modalidade e tipo do processo de
compra (ex: Pregão, Dispensa de
Licitação)

cnpj_fornecedor / fornecedor    Identificação de quem
forneceu/entregou o produto

cnpj_fabricante / fabricante    Identificação do fabricante do
produto

qtd_itens_comprados               Quantidade de itens adquiridos no
registro

7. Definição dos KPIs e das métricas

Valor Total Registrado = SUM('Original'[preco_total])
Quantidade Total de Itens Comprados = SUM('Original'[qtd_itens_comprados])
Número de Registros de Compra = COUNTROWS('Original')
Instituições Compradoras = DISTINCTCOUNT('Original'[cnpj_instituicao])
Fornecedores = DISTINCTCOUNT('Original'[cnpj_fornecedor])
Preço Unitário Médio Ponderado = DIVIDE([Valor Total Registrado], [Quantidade Total de Itens Comprados])

Instituições Compradoras e Fornecedores usam o CNPJ (não o
nome) como chave de contagem distinta, para evitar duplicidade por
grafias diferentes do mesmo nome.

Preço Unitário Médio Ponderado usa DIVIDE() (não o operador
/) para tratar divisão por zero automaticamente quando os filtros
deixarem a base vazia. Deve ser interpretado com cautela quando os
filtros incluírem produtos, unidades ou apresentações diferentes.

8. Link ou imagens do dashboard

Arquivo do dashboard:
dashboard/BPS_20_26_AdrianaSilvaDiasdeSouza.pbix

Print da página final: imagens/dashboard_final.png 

Link do repositório no GitHub: https://github.com/Adri1992ana/Miniprojeto_Modulo2_Medicamentos_AdrianaSilvaDiasdeSouza_T1.git

Link para o vídeo: https://www.loom.com/share/f3c0133195aa4e68b3de9258ddf8e36e

Design do dashboard: página única (16:9), com fundo customizado
definindo as zonas de KPIs, filtros e os visuais, garantindo
consistência visual e hierarquia clara (6 blocos de visuais, totalizando
7 gráficos --- o bloco de Fornecedores/Fabricantes contém dois gráficos
lado a lado). Títulos dos visuais vêm do fundo customizado (títulos
nativos do Power BI desativados), evitando repetição. Filtros
interativos (segmentações de dados): ano_compra, uf,
modalidade_compra, esfera.

Visuais do dashboard:

Gráfico de linhas --- evolução do Valor Total Registrado por
ano_compra

Barras horizontais --- ranking de uf por Valor Total Registrado
(Top 10)

Barras --- Top 15 descricao_catmat por Quantidade Total de Itens
Comprados

Barras --- Fornecedores e fabricantes: Top 10 fornecedor e Top 10
fabricante por Valor Total Registrado, exibidos lado a lado

Dispersão --- variação de preco_unitario por codigo_br (Top 20),
valores exatos disponíveis via tooltip

Barras --- Número de Registros de Compra por modalidade_compra

9. Principais análises e descobertas

Evolução temporal: valores sobem de 2020 (~5 Bi) até um pico em
2022 (~22 Bi), recuam em 2023 (~8 Bi), atingem o maior pico em
2025 (~32 Bi) e caem para ~2 Bi em 2026. A queda de 2026 reflete
dado parcial (ano corrente, ainda em andamento), não uma redução
real de compras.

Concentração geográfica: PR (~30 Bi) e SP (~27 Bi) lideram
amplamente o volume financeiro, muito à frente do terceiro colocado
(CE) --- indício de concentração geográfica relevante nas compras
registradas.

Padrão volume x valor: os medicamentos mais adquiridos em
quantidade são itens essenciais de baixo custo e uso crônico
(Losartana, Hidroclorotiazida, Metformina, Dipirona, Omeprazol,
dietas enterais). Já os fornecedores líderes em valor financeiro são
dominados por medicamentos de alto custo unitário --- especialidades
e oncológicos (AstraZeneca, Novartis, Janssen-Cilag, Onco Prod,
Oncovit) --- com destaque para o fornecedor Agille Comercio, que
lidera isoladamente (~23 Bi), bem à frente dos demais.

No visual de dispersão (Top 20 codigo_br por Quantidade Total de
Itens Comprados), o código 332849 apresentou preço unitário
médio ponderado de aproximadamente R$ 0,91, acima dos demais
códigos selecionados no grupo (maioria entre 0,01 e 0,32),
justificando investigação adicional considerando unidade de
fornecimento, apresentação e características do produto. O código
404992 teve a maior quantidade adquirida do grupo (4,36 Bi de
itens) a preço unitário de R$ 0,01, consistente com um insumo
básico comprado em escala.

Modalidades de compra: Pregão domina amplamente, com ~315 mil
registros (≈92% do total de 342.697), seguido de longe por Dispensa
de Licitação (~13 mil) e Registro de Preços (~11 mil). As demais
modalidades (Tomada de Preços, Concorrência, Inexigibilidade,
Concurso, Convite, Leilão) somadas representam menos de 1% dos
registros.

Varredura ampla de outliers de preço (script Python, método IQR
por produto): de 342.697 registros, foram avaliados 5.580 produtos
com pelo menos 5 compras registradas. Usando o critério de 3x o
intervalo interquartil (IQR) do preço unitário de cada produto,
foram identificados 14.863 registros (≈4,3% da base) com preço
unitário discrepante em relação ao comportamento de preço do próprio
produto. Os casos mais extremos foram então ordenados pela razão
entre o preço registrado e a mediana do respectivo produto, chegando
a milhares de vezes a mediana em alguns casos (ex: código 305494 a
R$ 55.776,00 contra mediana de R$ 1,85; código 415898 a R$
1.439.000,00 contra mediana de R$ 135,30). Esses casos levantam a
hipótese de erro de lançamento na fonte (possível troca entre preço
unitário e preço total), mas a base sozinha não permite confirmar a
causa --- permanece como oportunidade de investigação, não
conclusão. Lista completa salva em outliers_preco_unitario.csv.

10. Recomendações baseadas nos dados

Investigar com mais profundidade o código de produto 332849
(comparar unidade de fornecimento, fabricante e apresentação com
produtos similares antes de qualquer conclusão).

Avaliar a concentração de compras no fornecedor Agille Comercio ---
entender se decorre de contratos consolidados legítimos ou
representa risco de dependência de fornecedor único.

Como o Pregão é quase a modalidade exclusiva (~92%), garantir que
as demais modalidades continuem sendo usadas nos casos em que são
tecnicamente mais adequadas.

Comparar preços de medicamentos de alto volume (genéricos
essenciais) entre estados/fornecedores para identificar
oportunidades de economia de escala nas compras.

Implementar validações automáticas de faixa de preço no momento do
lançamento dos dados (ex: alertar quando o preço unitário foge muito
da mediana histórica do mesmo produto), para reduzir erros de
digitação como os identificados na varredura de outliers (item 9)
antes que entrem na base pública.

11. Limitações identificadas na base ou na análise

descricao_catmat contém HTML bruto e entidades codificadas (ex:
&#193;, <BR><TABLE...>, <LABEL>) em parte dos registros,
herdados da fonte original. Isso pode gerar categorias
inconsistentes por variações de formatação. No dashboard, a coluna
foi utilizada no ranking de produtos, enquanto codigo_br foi
utilizado como identificador nos casos em que a padronização da
descrição poderia comprometer a análise.

Ano de 2026 incompleto: por ser o ano corrente, a base contém
apenas dados parciais de 2026, o que faz a evolução temporal
aparentar uma queda brusca no último ponto --- não deve ser lida
como redução real de compras.

Diferenças de preço não implicam irregularidade: conforme
orientação do próprio desafio, variações de preço podem decorrer de
fabricante, apresentação, unidade de fornecimento, quantidade,
localidade, modalidade de compra e características da negociação ---
os pontos destacados no item 9 são indicativos para investigação,
não conclusões.

Possíveis inconsistências de registro na base pública: a
varredura de outliers (item 9) identificou uma minoria de registros
com preço unitário milhares de vezes acima do padrão do próprio
produto, compatíveis com possíveis erros de lançamento ou outras
diferenças de registro, cuja causa não pode ser confirmada apenas
com os dados disponíveis. Por isso, esses casos foram tratados como
oportunidades de investigação, e não como erros confirmados.

12. Instruções para reprodução do projeto

Clone o repositório ou baixe a pasta
BPS_20_26_AdrianaSilvaDiasdeSouza_T1/ completa.

Os dados brutos estão em Dados/Original/ (BPS_2020.csv a
BPS_2026.csv) e a base já consolidada em
Dados/Processado/BPS_20_26_AdrianaSilvaDiasdeSouza.csv ---
compactada em .zip no repositório (o CSV puro tem ~130 MB,
acima do limite do GitHub); extraia o .zip antes de usar.

Para reproduzir a consolidação a partir do zero: rode o script
concatenar_bps.py com Python 3 e a biblioteca pandas instalada
(pip install pandas), ajustando as variáveis
PASTA_ORIGINAL/SAIDA conforme a pasta onde o script estiver.

Para o dashboard: abra
dashboard/BPS_20_26_AdrianaSilvaDiasdeSouza.pbix no Power BI
Desktop.

Se o Power BI pedir para atualizar o caminho da pasta de origem
(Transformar Dados > Configurações da Fonte de Dados), aponte para
a pasta Dados/Original/ no seu computador e clique em Atualizar.

Todas as medidas DAX e visuais já estão configurados na página única
do relatório.

README  --- atualizado a cada etapa concluída do
desenvolvimento.
