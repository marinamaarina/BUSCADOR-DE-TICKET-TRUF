import streamlit as st
import pandas as pd
import plotly.express as px
from thefuzz import fuzz, process

# Configuração da página
st.set_page_config(page_title="Dashboard de Tickets", layout="wide", page_icon="📊")

# Estilo CSS personalizado
st.markdown("""
    <style>
        .card {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .metric-card {
            background-color: #ffffff;
            border-left: 4px solid #4e73df;
            border-radius: 5px;
            padding: 15px;
            margin: 5px;
        }
        .header {
            color: #2e59a7;
        }
    </style>
""", unsafe_allow_html=True)

# Título do dashboard
st.markdown("<h1 class='header'>📊 Dashboard de Análise de Tickets</h1>", unsafe_allow_html=True)

# Upload do arquivo
uploaded_file = st.file_uploader("Carregue seu arquivo de tickets (CSV ou Excel)", type=["csv", "xlsx"])

if uploaded_file:
    # Carregar dados
    @st.cache_data
    def load_data(file):
        if file.name.endswith('.csv'):
            return pd.read_csv(file)
        else:
            return pd.read_excel(file)
    
    df = load_data(uploaded_file)

    # Verificar colunas necessárias
    if all(col in df.columns for col in ['Tipo', 'Análise']):
        # Sidebar com filtros
        with st.sidebar:
            st.header("🔍 Filtros Avançados")
            
            # Campo de busca para Tipo
            tipo_search = st.text_input("Buscar por Tipo:")
            tipos = df['Tipo'].dropna().unique()
            
            if tipo_search:
                matches = process.extract(tipo_search, tipos, scorer=fuzz.token_set_ratio, limit=5)
                tipos_filtrados = [match[0] for match in matches]
            else:
                tipos_filtrados = tipos
            
            tipo_selecionado = st.selectbox("Selecione o Tipo:", tipos_filtrados)
            
            # Campo de busca para Análise
            analise_search = st.text_input("Buscar por Análise:")
            analises = df['Análise'].dropna().unique()
            
            if analise_search:
                matches = process.extract(analise_search, analises, scorer=fuzz.token_set_ratio, limit=5)
                analises_filtradas = [match[0] for match in matches]
            else:
                analises_filtradas = analises
            
            analise_selecionada = st.selectbox("Selecione a Análise:", analises_filtradas)
        
        # Aplicar filtros
        filtered_df = df[(df['Tipo'] == tipo_selecionado) & (df['Análise'] == analise_selecionada)]
        
        # Seção de métricas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <h3>Total de Tickets</h3>
                    <h2>{len(filtered_df)}</h2>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <h3>Tipo Selecionado</h3>
                    <h2>{tipo_selecionado}</h2>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <h3>Análise Selecionada</h3>
                    <h2>{analise_selecionada}</h2>
                </div>
            """, unsafe_allow_html=True)
        
        # Gráficos
        tab1, tab2, tab3 = st.tabs(["📊 Distribuição", "📈 Tendência", "🔍 Dados"])
        
        with tab1:
            if 'Data' in df.columns:
                fig = px.histogram(filtered_df, x='Data', title=f"Distribuição por Data - {tipo_selecionado}")
                st.plotly_chart(fig, use_container_width=True)
            else:
                fig = px.pie(filtered_df, names='Status', title=f"Distribuição por Status - {tipo_selecionado}")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            if 'Data' in df.columns and 'Quantidade' in df.columns:
                fig = px.line(filtered_df, x='Data', y='Quantidade', title=f"Tendência - {tipo_selecionado}")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("Dados insuficientes para mostrar tendência temporal")
        
        with tab3:
            st.dataframe(filtered_df, use_container_width=True)
        
        # Botão de download
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Baixar dados filtrados (CSV)",
            data=csv,
            file_name=f"tickets_{tipo_selecionado}_{analise_selecionada}.csv",
            mime="text/csv"
        )
    
    else:
        st.error("O arquivo precisa conter as colunas 'Tipo' e 'Análise'")
else:
    st.info("Por favor, carregue um arquivo para começar a análise")


