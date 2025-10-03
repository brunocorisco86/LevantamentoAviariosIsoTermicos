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
*   **Estimativa de Payback** do investimento inicial

### Tecnológico/Qualidade (Agregação de Valor)
*   **Estabilidade de Ambiência** (uso de sensores, como o DOL 53)
*   **Redução de emissões (ESG)**
*   **Impacto na bonificação do módulo Remunera** (Fidelidade & Benefícios) da plataforma AgroCenter.

## 🛠️ Tecnologia

O desenvolvimento da análise (ETL/Modelagem) será iniciado utilizando **Python**. A documentação e os resultados serão formatados neste arquivo `README.md`, utilizando **Markdown**.

## ➡️ Próximas Ações (Desenvolvimento Inicial)

Como o foco agora é iniciar o desenvolvimento, este `README.md` servirá como a estrutura inicial do projeto. As próximas etapas incluirão:

1.  **Estruturação do Projeto:** Organização de pastas e arquivos para o código Python e dados.
2.  **ETL (Extract, Transform, Load):**
    *   Leitura e tratamento dos dados brutos (`classificacao_aviario.csv`, `Indicadores_Fomento_2025.csv`, `remuneracao_lotes.csv`, `tipo_aviario.csv`).
    *   Limpeza, transformação e padronização dos dados usando funções Python.
3.  **Modelagem de Dados:** Criação de um banco de dados unificado (SQLite) com tabelas para armazenar os dados tratados.
4.  **Análise Exploratória de Dados (EDA):** Desenvolvimento de notebooks em `/notebooks` para explorar os dados e identificar padrões.
5.  **Desenvolvimento do Comparativo:** Implementação da lógica de comparação entre os tipos de aviários, calculando os indicadores zootécnicos e financeiros.
6.  **Visualização e Relatório:**
    *   Criação de um dashboard interativo (Streamlit) para apresentação dos resultados.
    *   Geração do relatório final em Markdown, incorporando gráficos e insights.
7.  **Deploy:** Publicação do dashboard no Streamlit Community Cloud.
8.  **Documentação:** Refinamento contínuo deste `README.md` e adição de documentação técnica.
