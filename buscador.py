import streamlit as st
import pandas as pd
from fuzzywuzzy import fuzz, process

st.set_page_config(page_title="Análise de Tickets", layout="wide")

# Configuração de estilo
st.markdown("""
    <style>
        .stSelectbox, .stTextInput, .stMultiSelect {
            margin-bottom: 1rem;
        }
        .stDataFrame {
            border: 1px solid #e1e4e8;
            border-radius: 5px;
        }
        .css-1aumxhk {
            background-color: #f0f2f6;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🔍 Buscador Inteligente de Tickets")

# Upload do arquivo Excel
arquivo = st.file_uploader("📤 Envie sua planilha (.xlsx ou .csv)", type=["xlsx", "csv"], help="Planilha deve conter colunas 'Tipo' e 'Análise'")

if arquivo:
    # Carrega os dados com cache para melhor performance
    @st.cache_data
    def load_data(file):
        if file.name.endswith('.csv'):
            return pd.read_csv(file)
        else:
            return pd.read_excel(file)
    
    df = load_data(arquivo)

    # Exibe prévia com abas
    preview_tab, stats_tab = st.tabs(["📋 Prévia dos Dados", "📊 Estatísticas"])
    
    with preview_tab:
        st.dataframe(df.head(), use_container_width=True)
    
    with stats_tab:
        st.write(f"Total de registros: {len(df)}")
        if 'Tipo' in df.columns:
            st.write("Distribuição por Tipo:")
            st.bar_chart(df['Tipo'].value_counts())
        if 'Análise' in df.columns:
            st.write("Distribuição por Análise:")
            st.bar_chart(df['Análise'].value_counts())

    # Verifica se colunas esperadas existem
    colunas_necessarias = ['Tipo', 'Análise']
    if all(col in df.columns for col in colunas_necessarias):
        
        # Sidebar para filtros avançados
        with st.sidebar:
            st.header("🔎 Filtros Avançados")
            
            # Busca fuzzy para tipos
            tipos_disponiveis = df['Tipo'].dropna().unique()
            tipo_pesquisa = st.text_input("Pesquisar Tipo:")
            if tipo_pesquisa:
                matches = process.extract(tipo_pesquisa, tipos_disponiveis, scorer=fuzz.token_set_ratio, limit=5)
                tipos_filtrados = [match[0] for match in matches]
            else:
                tipos_filtrados = tipos_disponiveis
            
            tipo_escolhido = st.selectbox("Selecione o Tipo:", tipos_filtrados)
            
            # Busca fuzzy para análises
            analises_disponiveis = df['Análise'].dropna().unique()
            analise_pesquisa = st.text_input("Pesquisar Análise:")
            if analise_pesquisa:
                matches = process.extract(analise_pesquisa, analises_disponiveis, scorer=fuzz.token_set_ratio, limit=5)
                analises_filtradas = [match[0] for match in matches]
            else:
                analises_filtradas = analises_disponiveis
            
            analise_escolhida = st.selectbox("Selecione a Análise:", analises_filtradas)
            
            # Filtros adicionais
            outras_colunas = [col for col in df.columns if col not in colunas_necessarias]
            coluna_filtro_extra = st.selectbox("Filtrar por outra coluna:", ['Nenhum'] + outras_colunas)
            
            if coluna_filtro_extra != 'Nenhum':
                valores_filtro = df[coluna_filtro_extra].dropna().unique()
                valor_selecionado = st.selectbox(f"Selecione {coluna_filtro_extra}:", valores_filtro)
        
        # Aplica o filtro
        filtro = df[(df['Tipo'] == tipo_escolhido) & (df['Análise'] == analise_escolhida)]
        
        if coluna_filtro_extra != 'Nenhum':
            filtro = filtro[filtro[coluna_filtro_extra] == valor_selecionado]
        
        # Exibe resultados
        st.subheader(f"🎯 Resultados Encontrados: {len(filtro)} registros")
        
        # Mostra métricas rápidas
        col1, col2, col3 = st.columns(3)
        col1.metric("Total de Registros", len(filtro))
        if 'Data' in filtro.columns:
            col2.metric("Período", f"{filtro['Data'].min().date()} a {filtro['Data'].max().date()}")
        
        # Visualização dos dados
        st.dataframe(filtro, use_container_width=True)
        
        # Opções de exportação
        export_col1, export_col2 = st.columns(2)
        
        with export_col1:
            csv_export = filtro.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Baixar como CSV", data=csv_export, 
                             file_name="filtro_tickets.csv", mime="text/csv")
        
        with export_col2:
            excel_export = filtro.to_excel(index=False)
            st.download_button("⬇️ Baixar como Excel", data=excel_export, 
                             file_name="filtro_tickets.xlsx", mime="application/vnd.ms-excel")
        
    else:
        st.warning("⚠️ A planilha precisa ter as colunas 'Tipo' e 'Análise'.")

