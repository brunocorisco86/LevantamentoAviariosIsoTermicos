import pandas as pd

class DataManager:
    def __init__(self, base_path):
        self.base_path = base_path
        self.classificacao_aviario_path = f"{base_path}/data/classificacao_aviario.csv"
        self.indicadores_fomento_path = f"{base_path}/data/Indicadores_Fomento_2025.csv"
        self.remuneracao_lotes_path = f"{base_path}/data/remuneracao_lotes.csv"
        self.tipo_aviario_path = f"{base_path}/data/tipo_aviario.csv"
        self.df_classificacao = None
        self.df_indicadores = None
        self.df_remuneracao = None
        self.df_tipo_aviario = None
        self.df_merged = None

    def load_data(self):
        self.df_classificacao = pd.read_csv(self.classificacao_aviario_path, sep=';')
        self.df_indicadores = pd.read_csv(self.indicadores_fomento_path, sep=';')
        self.df_remuneracao = pd.read_csv(self.remuneracao_lotes_path, sep=';')
        self.df_tipo_aviario = pd.read_csv(self.tipo_aviario_path, sep=';')
        print("All dataframes loaded.")

    def clean_data(self):
        # Clean 'tipo_aviario' column in df_indicadores
        if self.df_indicadores is not None:
            self.df_indicadores['tipo_aviario'] = self.df_indicadores['tipo_aviario'].str.strip()
            print("Cleaned 'tipo_aviario' column in df_indicadores.")
        
        # Clean 'tipo_aviario_classificacao' column in df_tipo_aviario
        if self.df_tipo_aviario is not None:
            self.df_tipo_aviario['tipo_aviario_classificacao'] = self.df_tipo_aviario['tipo_aviario_classificacao'].str.strip()
            print("Cleaned 'tipo_aviario_classificacao' column in df_tipo_aviario.")


    def print_unique_values(self):
        if self.df_indicadores is not None:
            print(f"Unique values in df_indicadores['tipo_aviario']: {self.df_indicadores['tipo_aviario'].unique()}")
        if self.df_tipo_aviario is not None:
            print(f"Unique values in df_tipo_aviario['tipo_aviario_classificacao']: {self.df_tipo_aviario['tipo_aviario_classificacao'].unique()}")

    def merge_data(self):
        # Merge indicadores_fomento with remuneracao_lotes
        self.df_merged = pd.merge(self.df_indicadores, self.df_remuneracao, 
                                  left_on=['aviario', 'lote_composto'], right_on=['aviario', 'lote_composto'], 
                                  how='left', suffixes=('_indic', '_remun'))

        # Merge with classificacao_aviario
        self.df_merged = pd.merge(self.df_merged, self.df_classificacao, 
                                  left_on='aviario', right_on='aviario', how='left')

        # Merge with tipo_aviario
        self.df_merged = pd.merge(self.df_merged, self.df_tipo_aviario, 
                                  left_on='aviario', right_on='aviario', how='left', suffixes=('_merged', '_tipo'))
        
        print("All dataframes merged.")

    def filter_data(self):
        # Filter out 'Convencional' poultry houses
        if self.df_merged is not None:
            self.df_merged = self.df_merged[self.df_merged['tipo_aviario_classificacao'] != 'Convencional']
            print("Filtered out 'Convencional' poultry houses.")
        
        # Filter out rows where 'remuneracao_ave' or 'remuneracao_area' are null
        if self.df_merged is not None:
            initial_rows = len(self.df_merged)
            self.df_merged.dropna(subset=['remuneracao_ave', 'remuneracao_area'], inplace=True)
            rows_dropped = initial_rows - len(self.df_merged)
            print(f"Filtered out {rows_dropped} rows where 'remuneracao_ave' or 'remuneracao_area' were null.")

    def get_merged_data(self):
        return self.df_merged

    def save_to_sqlite(self, db_name="aviarios.db", table_name="dados_consolidados"):
        if self.df_merged is not None:
            import sqlite3
            conn = sqlite3.connect(db_name)
            
            self.df_merged.to_sql(table_name, conn, if_exists='replace', index=False)
            conn.close()
            print(f"Data successfully saved to {db_name} in table {table_name}.")

            # Verify the schema created in SQLite
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            schema_info = cursor.fetchall()
            conn.close()
            print("\nActual SQLite schema for dados_consolidados:")
            for col_info in schema_info:
                print(col_info)

        else:
            print("No merged data to save.")

    def transform_data(self):
        if self.df_merged is None:
            print("No merged data available for transformation.")
            return

        print("Starting data transformations...")

        # Convert 'positivo_salmonella' to boolean
        if 'positivo_salmonella' in self.df_merged.columns:
            self.df_merged['positivo_salmonella'] = self.df_merged['positivo_salmonella'].astype(bool)
            print("Converted 'positivo_salmonella' to boolean.")

        # Convert all string columns to uppercase
        for col in self.df_merged.select_dtypes(include=['object']).columns:
            self.df_merged[col] = self.df_merged[col].str.upper()
        print("Converted all string columns to uppercase.")

        # Extract data before comma in 'lote_matriz'
        if 'lote_matriz' in self.df_merged.columns:
            self.df_merged['lote_matriz'] = self.df_merged['lote_matriz'].astype(str).apply(lambda x: x.split(',')[0].strip() if ',' in x else x.strip())
            print("Extracted data before comma in 'lote_matriz'.")

        # Convert relevant columns to numeric, coercing errors to NaN
        numeric_cols = [
            'mortalidade_prim_semana', 'feed_conversion_rate', 'gmd', 
            'mortalidade', 'peso_medio', 'valor_lote', 'remuneracao_ave', 
            'remuneracao_area', 'aquecimento_BTU_square_meter', 'velocidade_ar',
            'entrada_ar_falso', 'nota_aquecimento', 'nota_velocidade_ar', 
            'nota_resfriamento', 'nota_vedacao', 'nota_obtida_total',
            'condenacao_patologica_total', 'condenacao_patologica_parcial',
            'idade_matriz', 'idade_abate', 'aves_abatidas', 'aves_alojadas', 
            'cama', 'densidade', 'iep', 'year'
        ]
        for col in numeric_cols:
            # Replace comma with dot for decimal conversion
            if col in self.df_merged.columns and self.df_merged[col].dtype == 'object':
                self.df_merged[col] = self.df_merged[col].str.replace(',', '.', regex=False)
            self.df_merged[col] = pd.to_numeric(self.df_merged[col], errors='coerce')

        print("Data transformations complete.")

    def analyze_performance(self):
        if self.df_merged is None:
            print("No merged data available for analysis.")
            return

        print("Starting performance analysis...")

        # Group by poultry house type and calculate mean for key indicators
        performance_summary = self.df_merged.groupby('tipo_aviario_classificacao').agg(
            # Zootechnical Indicators
            CA_media=('feed_conversion_rate', 'mean'),
            GPD_media=('gmd', 'mean'),
            Mortalidade_media=('mortalidade', 'mean'),
            IEP_media=('iep', 'mean'),

            # Financial Indicators
            Valor_Lote_media=('valor_lote', 'mean'),
            Remuneracao_Ave_mean=('remuneracao_ave', 'mean'),
            Remuneracao_Area_mean=('remuneracao_area', 'mean'),

            # Technological/Quality Indicators (example, can add more)
            Aquecimento_BTU_media=('aquecimento_BTU_square_meter', 'mean'),
            Condenacao_Total_media=('condenacao_patologica_total', 'mean')
        )

        print("Performance Analysis Complete:")
        print(performance_summary)
        return performance_summary

if __name__ == "__main__":
    data_manager = DataManager("/home/brunoconter/Code/Git/LevantamentoIsopainel")
    data_manager.load_data()
    data_manager.clean_data()
    data_manager.print_unique_values()
    data_manager.merge_data()
    data_manager.transform_data()
    data_manager.filter_data()
    data_manager.save_to_sqlite()
    performance_summary = data_manager.analyze_performance()
    
    df = data_manager.get_merged_data()
    if df is not None:
        print("Merged and filtered data head:")
        print(df.head())
        print("\nMerged and filtered data info:")
        print(df.info())
    else:
        print("No data to display.")
