# Levantamento Comparativo: Aviários Isotérmicos vs. Convencionais

## 🎯 Contexto e Missão

Atuando como Analista de Negócios Sênior em Avicultura de Corte na C.Vale, minha missão é **refutar (ou validar)** a percepção de produtores parceiros de que o investimento em aviários de última tecnologia (Isotérmicos/Dark Houses) não compensa financeiramente, comparando-o com estruturas convencionais (ex: Convencional/Túnel).

## 🚀 Entrega Principal

Gerar um **comparativo consolidado (Dashboard/Relatório Markdown)** que demonstre a diferença no desempenho Zootécnico e Econômico-Financeiro entre os diferentes tipos de estrutura de aviários. O foco será no **Retorno sobre o Investimento (ROI)** a longo prazo e nos **benefícios de ESG/Bem-estar Animal**.

## 📊 Foco da Análise

### Zootécnico (Desempenho)
*   **Conversão Alimentar (CA)**
*   **Ganho de Peso Diário (GPD)**
*   **Taxa de Mortalidade**
*   **Desempenho (Escore de Produção ou similar)**

### Financeiro (Custo/Receita)
*   **Custo Operacional** (Energia Elétrica, Mão de Obra, Insumos)
*   **Remuneração por Lote** (Receita Bruta x Custos)
*   **Estimativa de Payback** do investimento inicial.

### Tecnológico/Qualidade (Agregação de Valor)
*   **Estabilidade de Ambiência** (uso de sensores, como o DOL 53)
*   **Redução de emissões (ESG)**
*   **Impacto na bonificação do módulo Remunera** (Fidelidade & Benefícios) da plataforma AgroCenter.

## 🛠️ Tecnologia e Estrutura do Projeto

O projeto utiliza **Python** para o ETL, modelagem de dados e desenvolvimento do dashboard interativo. Os resultados são apresentados através de um dashboard Streamlit e um relatório Markdown.

### Estrutura de Pastas

```
LevantamentoIsopainel/
├───database/             # Contém o banco de dados SQLite consolidado (aviarios.db)
├───data/                 # Dados brutos de entrada (CSVs)
├───docs/                 # Documentação adicional do projeto (prompt, próximos passos, tipos de aviários)
├───notebooks/            # Notebooks Jupyter para EDA e experimentação
├───src/                  # Código-fonte da aplicação (ETL, Streamlit app)
│   ├───app.py            # Aplicação Streamlit interativa
│   └───data_manager.py   # Script para ETL e processamento de dados
├───README.md             # Este arquivo
├───next_steps.md         # Próximos passos detalhados (agora incorporados aqui)
├───prompt.md             # Prompt original do projeto
└───tipos_aviarios.md     # Descrição dos tipos de aviários
```

## ⚙️ Processamento de Dados (ETL)

O script `src/data_manager.py` é responsável por:

1.  **Carregar Dados:** Lê os arquivos CSV brutos da pasta `data/`.
2.  **Limpeza e Transformação:**
    *   Remove espaços em branco de colunas categóricas.
    *   Converte todas as colunas de string para maiúsculas.
    *   Extrai a primeira parte da string na coluna `lote_matriz`.
    *   Converte colunas numéricas (como `feed_conversion_rate`, `remuneracao_ave`, `idade_matriz`, etc.) para tipos `float` ou `int`, tratando vírgulas como separadores decimais e valores não numéricos como `NaN`.
    *   Converte a coluna `positivo_salmonella` para booleano.
3.  **Merge de Dados:** Combina os diferentes DataFrames em um único DataFrame consolidado.
4.  **Filtragem:**
    *   Filtra aviários que não são do tipo 'Convencional' (este filtro foi removido do `data_manager.py` para permitir a seleção no Streamlit).
    *   Remove linhas onde `remuneracao_ave` ou `remuneracao_area` são nulas.
5.  **Persistência:** Salva o DataFrame processado no banco de dados SQLite `database/aviarios.db` na tabela `dados_consolidados`.
6.  **Análise de Performance:** Calcula indicadores médios (zootécnicos, financeiros, tecnológicos) agrupados por tipo de aviário.

Para reprocessar os dados e atualizar o banco de dados, execute:

```bash
python3 src/data_manager.py
```

## 📈 Dashboard Interativo (Streamlit)

A aplicação `src/app.py` fornece um dashboard interativo para explorar os dados e os resultados da análise.

### Funcionalidades:

*   **Filtros Dinâmicos:** Utilize a barra lateral para filtrar os dados por:
    *   Tipo de Aviário (`tipo_aviario_classificacao`)
    *   Proprietário (`proprietario`)
    *   Classificação Aviário (`categoria`)
    *   Modelo Aviário (`modelo_aviario`)
    *   Posicionamento Pinteiro (`posicionamento_pinteiro`)
    *   Aquecimento Principal (`aquecimento_principal`)
    *   Modelo Aquecedor (`modelo_aquecedor`)
    *   Fornecedor Ovo (`fornecedor_ovo`)
    *   Fornecedor Pinto (`fornecedor_pinto`)
*   **Sliders de Intervalo:** Filtre por faixas de valores para:
    *   Idade Matriz (`idade_matriz`)
    *   Idade Abate (`idade_abate`)
    *   Notas de Ambiência (`nota_aquecimento`, `nota_velocidade_ar`, `nota_resfriamento`, `nota_vedacao`, `nota_obtida_total`)
*   **Download de Dados:** Botão para baixar os dados filtrados em formato CSV (separador `;`, codificação `UTF-8`).
*   **Análise de Desempenho:** Tabela resumida com médias dos indicadores por tipo de aviário.
*   **Comparativo Visual (Gráfico de Barras):** Selecione um indicador para comparar visualmente entre os tipos de aviário.
*   **Gráfico Radar de Notas de Ambiência:** Visualiza as médias das notas de aquecimento, velocidade do ar, resfriamento e vedação para cada tipo de aviário, com um limite máximo de 30.
*   **Análise Estatística:**
    *   **Teste T:** Compara indicadores chave entre os tipos de aviário selecionados.
    *   **Matriz de Correlação:** Exibe correlações absolutas maiores que 0.1 entre variáveis numéricas, excluindo IDs e contagens.
*   **Importância das Features:** Placeholder para futura implementação de análise de importância de features para `remuneracao_area`.

### Como Executar o Dashboard:

Certifique-se de ter as dependências instaladas (`streamlit`, `pandas`, `plotly`, `scipy`). Em seguida, execute no terminal a partir da raiz do projeto:

```bash
streamlit run src/app.py
```

## ➡️ Próximos Passos

Este projeto é um protótipo funcional. As próximas etapas para aprimoramento incluem:

1.  **Desenvolvimento do Comparativo:**
    *   Cálculo de ROI (Retorno sobre o Investimento) e Payback mais detalhados.
    *   Análise de sensibilidade para variáveis chave.
    *   Identificação de padrões e correlações mais aprofundadas.
2.  **Relatório Final (Markdown):** Geração de um relatório detalhado com gráficos e insights do dashboard.
3.  **Deploy:** Publicação do dashboard interativo para acesso e compartilhamento (ex: Streamlit Community Cloud).
4.  **Documentação:** Refinamento contínuo da documentação técnica e de uso.
5.  **Feature Importance:** Implementação da análise de importância de features para `remuneracao_area` usando modelos preditivos.

## 📚 Documentação Adicional

*   `docs/prompt.md`: Contém o prompt original e a missão do projeto.
*   `docs/tipos_aviarios.md`: Detalhes sobre as características dos diferentes tipos de aviários climatizados.