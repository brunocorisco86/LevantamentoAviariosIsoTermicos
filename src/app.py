import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

st.set_page_config(layout="wide")

st.title("Comparativo de Desempenho de Aviários")

# Connect to the SQLite database
conn = sqlite3.connect('aviarios.db')

# Load the consolidated data into a pandas DataFrame
df = pd.read_sql_query("SELECT * FROM dados_consolidados", conn)

# Close the connection
conn.close()

# Ensure numeric columns are correctly typed
numeric_cols = [
    'mortalidade_prim_semana', 'feed_conversion_rate', 'gmd', 
    'mortalidade', 'peso_medio', 'valor_lote', 'remuneracao_ave', 
    'remuneracao_area', 'aquecimento_BTU_square_meter', 'velocidade_ar',
    'entrada_ar_falso', 'nota_aquecimento', 'nota_velocidade_ar', 
    'nota_resfriamento', 'nota_vedacao', 'nota_obtida_total',
    'condenacao_patologica_total', 'condenacao_patologica_parcial',
    'aves_alojadas', 'area', 'iep', 'aves_abatidas', 'aves',
    'idade_matriz', 'idade_abate', 'cama', 'densidade', 'year'
]
for col in numeric_cols:
    if col in df.columns and df[col].dtype == 'object':
        df[col] = df[col].str.replace(',', '.', regex=False)
    df[col] = pd.to_numeric(df[col], errors='coerce')


st.sidebar.header("Filtros")

# Filter by poultry house type
selected_tipo_aviario = st.sidebar.multiselect(
    "Tipo de Aviário",
    options=df['tipo_aviario_classificacao'].unique(),
    default=df['tipo_aviario_classificacao'].unique()
)

# Filter by Proprietario
selected_proprietario = st.sidebar.multiselect(
    "Proprietário",
    options=df['proprietario'].unique(),
    default=df['proprietario'].unique()
)

# Filter by Classificacao Aviario (categoria) - Added back
selected_categoria = st.sidebar.multiselect(
    "Classificação Aviário",
    options=df['categoria'].unique(),
    default=df['categoria'].unique()
)

# New Filters
selected_modelo_aviario = st.sidebar.multiselect(
    "Modelo Aviário",
    options=df['modelo_aviario'].unique(),
    default=df['modelo_aviario'].unique()
)

selected_posicionamento_pinteiro = st.sidebar.multiselect(
    "Posicionamento Pinteiro",
    options=df['posicionamento_pinteiro'].unique(),
    default=df['posicionamento_pinteiro'].unique()
)

selected_aquecimento_principal = st.sidebar.multiselect(
    "Aquecimento Principal",
    options=df['aquecimento_principal'].unique(),
    default=df['aquecimento_principal'].unique()
)

selected_modelo_aquecedor = st.sidebar.multiselect(
    "Modelo Aquecedor",
    options=df['modelo_aquecedor'].unique(),
    default=df['modelo_aquecedor'].unique()
)

selected_fornecedor_ovo = st.sidebar.multiselect(
    "Fornecedor Ovo",
    options=df['fornecedor_ovo'].unique(),
    default=df['fornecedor_ovo'].unique()
)

selected_fornecedor_pinto = st.sidebar.multiselect(
    "Fornecedor Pinto",
    options=df['fornecedor_pinto'].unique(),
    default=df['fornecedor_pinto'].unique()
)


# Sliders
st.sidebar.subheader("Filtros por Intervalo")

idade_matriz_min, idade_matriz_max = float(df['idade_matriz'].min()), float(df['idade_matriz'].max())
selected_idade_matriz = st.sidebar.slider(
    "Idade Matriz",
    min_value=idade_matriz_min,
    max_value=idade_matriz_max,
    value=(idade_matriz_min, idade_matriz_max)
)

idade_abate_min, idade_abate_max = float(df['idade_abate'].min()), float(df['idade_abate'].max())
selected_idade_abate = st.sidebar.slider(
    "Idade Abate",
    min_value=idade_abate_min,
    max_value=idade_abate_max,
    value=(idade_abate_min, idade_abate_max)
)

nota_aquecimento_min, nota_aquecimento_max = float(df['nota_aquecimento'].min()), float(df['nota_aquecimento'].max())
selected_nota_aquecimento = st.sidebar.slider(
    "Nota Aquecimento",
    min_value=nota_aquecimento_min,
    max_value=nota_aquecimento_max,
    value=(nota_aquecimento_min, nota_aquecimento_max)
)

nota_velocidade_ar_min, nota_velocidade_ar_max = float(df['nota_velocidade_ar'].min()), float(df['nota_velocidade_ar'].max())
selected_nota_velocidade_ar = st.sidebar.slider(
    "Nota Velocidade Ar",
    min_value=nota_velocidade_ar_min,
    max_value=nota_velocidade_ar_max,
    value=(nota_velocidade_ar_min, nota_velocidade_ar_max)
)

nota_resfriamento_min, nota_resfriamento_max = float(df['nota_resfriamento'].min()), float(df['nota_resfriamento'].max())
selected_nota_resfriamento = st.sidebar.slider(
    "Nota Resfriamento",
    min_value=nota_resfriamento_min,
    max_value=nota_resfriamento_max,
    value=(nota_resfriamento_min, nota_resfriamento_max))

nota_vedacao_min, nota_vedacao_max = float(df['nota_vedacao'].min()), float(df['nota_vedacao'].max())
selected_nota_vedacao = st.sidebar.slider(
    "Nota Vedação",
    min_value=nota_vedacao_min,
    max_value=nota_vedacao_max,
    value=(nota_vedacao_min, nota_vedacao_max)
)

nota_obtida_total_min, nota_obtida_total_max = float(df['nota_obtida_total'].min()), float(df['nota_obtida_total'].max())
selected_nota_obtida_total = st.sidebar.slider(
    "Nota Obtida Total",
    min_value=nota_obtida_total_min,
    max_value=nota_obtida_total_max,
    value=(nota_obtida_total_min, nota_obtida_total_max)
)


filtered_df = df[
    (df['tipo_aviario_classificacao'].isin(selected_tipo_aviario)) &
    (df['proprietario'].isin(selected_proprietario)) &
    (df['categoria'].isin(selected_categoria)) &
    (df['modelo_aviario'].isin(selected_modelo_aviario)) &
    (df['posicionamento_pinteiro'].isin(selected_posicionamento_pinteiro)) &
    (df['aquecimento_principal'].isin(selected_aquecimento_principal)) &
    (df['modelo_aquecedor'].isin(selected_modelo_aquecedor)) &
    (df['fornecedor_ovo'].isin(selected_fornecedor_ovo)) &
    (df['fornecedor_pinto'].isin(selected_fornecedor_pinto)) &
    (df['idade_matriz'] >= selected_idade_matriz[0]) & (df['idade_matriz'] <= selected_idade_matriz[1]) &
    (df['idade_abate'] >= selected_idade_abate[0]) & (df['idade_abate'] <= selected_idade_abate[1]) &
    (df['nota_aquecimento'] >= selected_nota_aquecimento[0]) & (df['nota_aquecimento'] <= selected_nota_aquecimento[1]) &
    (df['nota_velocidade_ar'] >= selected_nota_velocidade_ar[0]) & (df['nota_velocidade_ar'] <= selected_nota_velocidade_ar[1]) &
    (df['nota_resfriamento'] >= selected_nota_resfriamento[0]) & (df['nota_resfriamento'] <= selected_nota_resfriamento[1]) &
    (df['nota_vedacao'] >= selected_nota_vedacao[0]) & (df['nota_vedacao'] <= selected_nota_vedacao[1]) &
    (df['nota_obtida_total'] >= selected_nota_obtida_total[0]) & (df['nota_obtida_total'] <= selected_nota_obtida_total[1])
]

if filtered_df.empty:
    st.warning("Nenhum dado encontrado com os filtros selecionados.")
    st.stop()

# Download button for filtered data
st.download_button(
    label="Baixar Dados Filtrados (.csv)",
    data=filtered_df.to_csv(index=False, sep=';', encoding='utf-8').encode('utf-8'),
    file_name="dados_filtrados.csv",
    mime="text/csv",
)


st.header("Análise de Desempenho por Tipo de Aviário")

performance_summary = filtered_df.groupby('tipo_aviario_classificacao').agg(
    CA_mean=('feed_conversion_rate', 'mean'),
    GPD_mean=('gmd', 'mean'),
    Mortalidade_mean=('mortalidade', 'mean'),
    IEP_mean=('iep', 'mean'),
    Valor_Lote_mean=('valor_lote', 'mean'),
    Remuneracao_Ave_mean=('remuneracao_ave', 'mean'),
    Remuneracao_Area_mean=('remuneracao_area', 'mean'),
    Aquecimento_BTU_mean=('aquecimento_BTU_square_meter', 'mean'),
    Condenacao_Total_mean=('condenacao_patologica_total', 'mean')
).reset_index()

st.dataframe(performance_summary)


st.header("Comparativo Visual")

# Mapping for display names
indicator_display_names = {
    'CA_mean': 'CA Média',
    'GPD_mean': 'GPD Média',
    'Mortalidade_mean': 'Mortalidade Média',
    'IEP_mean': 'IEP Média',
    'Valor_Lote_mean': 'Valor Lote Média',
    'Remuneracao_Ave_mean': 'Remuneração Ave Média',
    'Remuneracao_Area_mean': 'Remuneração Área Média',
    'Aquecimento_BTU_mean': 'Aquecimento BTU Média',
    'Condenacao_Total_mean': 'Condenação Total Média'
}

# Bar chart for key indicators
selected_indicator_display_name = st.selectbox(
    "Selecione o Indicador para Comparar",
    options=list(indicator_display_names.values())
)

# Get the actual column name from the display name
indicator_to_compare = [key for key, value in indicator_display_names.items() if value == selected_indicator_display_name][0]

fig = px.bar(
    performance_summary,
    x='tipo_aviario_classificacao',
    y=indicator_to_compare,
    title=f'Comparativo de {selected_indicator_display_name} por Tipo de Aviário',
    labels={'tipo_aviario_classificacao': 'Tipo de Aviário', indicator_to_compare: selected_indicator_display_name}
)
st.plotly_chart(fig, use_container_width=True)


# Radar Chart
st.subheader("Gráfico Radar de Notas de Ambiência")

radar_data = filtered_df.groupby('tipo_aviario_classificacao')[[
    'nota_aquecimento', 'nota_velocidade_ar', 'nota_resfriamento', 'nota_vedacao'
]].mean().reset_index()

if not radar_data.empty:
    fig_radar = go.Figure()

    for index, row in radar_data.iterrows():
        fig_radar.add_trace(go.Scatterpolar(
            r=[row['nota_aquecimento'], row['nota_velocidade_ar'], row['nota_resfriamento'], row['nota_vedacao']],
            theta=['Aquecimento', 'Velocidade Ar', 'Resfriamento', 'Vedação'],
            fill='toself',
            name=row['tipo_aviario_classificacao']
        ))

    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 30] # Set max limit to 30 as requested
            )),
        showlegend=True,
        title="Notas de Ambiência por Tipo de Aviário"
    )
    st.plotly_chart(fig_radar, use_container_width=True)
else:
    st.info("Dados insuficientes para gerar o Gráfico Radar.")


st.header("Análise Estatística")

# T-tests
st.subheader("Teste T sobre Indicadores por Tipo de Aviário")

poultry_types = filtered_df['tipo_aviario_classificacao'].unique()

if len(poultry_types) > 1:
    type1_data = filtered_df[filtered_df['tipo_aviario_classificacao'] == poultry_types[0]]
    type2_data = filtered_df[filtered_df['tipo_aviario_classificacao'] == poultry_types[1]]

    indicators_for_ttest = [
        'remuneracao_ave', 'remuneracao_area', 'iep', 'feed_conversion_rate'
    ]

    for indicator in indicators_for_ttest:
        st.write(f"### {indicator.replace('_', ' ').title()} ")
        
        # Drop NaN values for t-test
        data1 = type1_data[indicator].dropna()
        data2 = type2_data[indicator].dropna()

        if not data1.empty and not data2.empty:
            t_stat, p_val = stats.ttest_ind(data1, data2, equal_var=False) # Welch's t-test
            st.write(f"**{poultry_types[0]} vs {poultry_types[1]}**")
            st.write(f"T-statistic: {t_stat:.3f}")
            st.write(f"P-value: {p_val:.3f}")
            if p_val < 0.05:
                st.write("Há uma diferença estatisticamente significativa entre os tipos de aviário para este indicador.")
            else:
                st.write("Não há diferença estatisticamente significativa entre os tipos de aviário para este indicador.")
        else:
            st.write("Dados insuficientes para realizar o Teste T para este indicador.")
else:
    st.info("Selecione pelo menos dois tipos de aviário para realizar o Teste T.")


# Correlation Matrix
st.subheader("Matriz de Correlação")

# Select only numeric columns for correlation
numeric_df = filtered_df.select_dtypes(include=['number'])

# Columns to exclude from the correlation matrix
exclude_cols = ['aviario', 'lote', 'lote_composto', 'aves', 'aves_alojadas', 'aves_abatidas']
numeric_df = numeric_df.drop(columns=[col for col in exclude_cols if col in numeric_df.columns])

# Add a print statement to check columns before correlation
# st.write(f"Columns in correlation matrix: {numeric_df.columns.tolist()}")

if not numeric_df.empty:
    corr_matrix = numeric_df.corr()
    
    # Filter correlations above 0.1 absolute value
    filtered_corr_df = corr_matrix.stack().reset_index()
    filtered_corr_df.columns = ['Variavel 1', 'Variavel 2', 'Correlacao']
    filtered_corr_df = filtered_corr_df[filtered_corr_df['Correlacao'].abs() > 0.1]
    filtered_corr_df = filtered_corr_df[filtered_corr_df['Variavel 1'] != filtered_corr_df['Variavel 2']]

    if not filtered_corr_df.empty:
        fig_corr = go.Figure(data=go.Heatmap(
            z=filtered_corr_df['Correlacao'],
            x=filtered_corr_df['Variavel 1'],
            y=filtered_corr_df['Variavel 2'],
            colorscale='Viridis',
            colorbar=dict(title='Correlação')
        ))
        fig_corr.update_layout(title='Matriz de Correlação (Abs > 0.1)')
        st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.info("Nenhuma correlação absoluta maior que 0.1 encontrada.")
else:
    st.info("Não há dados numéricos para calcular a matriz de correlação.")


# Feature Importance for remuneracao_area (Placeholder - requires a model)
st.subheader("Importância das Features para Remuneração por Área")
st.info("A importância das features para 'remuneracao_area' requer a construção e treinamento de um modelo preditivo (ex: Regressão Linear, Random Forest). Esta funcionalidade será implementada em uma etapa futura.")