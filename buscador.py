import streamlit as st
import pandas as pd

st.set_page_config(page_title="Análise de Tickets", layout="centered")

st.title("🎫 Analisador de Tickets")

# Upload do arquivo Excel
arquivo = st.file_uploader("📤 Envie sua planilha (.xlsx ou .csv)", type=["xlsx", "csv"])

if arquivo:
    # Carrega os dados
    if arquivo.name.endswith('.csv'):
        df = pd.read_csv(arquivo)
    else:
        df = pd.read_excel(arquivo)

    # Exibe prévia
    st.subheader("🔍 Visualização da Tabela")
    st.dataframe(df.head())

    # Verifica se colunas esperadas existem
    colunas_necessarias = ['Tipo', 'Análise']
    if all(col in df.columns for col in colunas_necessarias):
        
        # Filtros
        tipos_disponiveis = df['Tipo'].dropna().unique()
        analises_disponiveis = df['Análise'].dropna().unique()

        tipo_escolhido = st.selectbox("📌 Escolha o tipo de ticket:", tipos_disponiveis)
        analise_escolhida = st.selectbox("✅ Escolha o tipo de análise:", analises_disponiveis)

        # Aplica o filtro
        filtro = df[(df['Tipo'] == tipo_escolhido) & (df['Análise'] == analise_escolhida)]

        st.subheader(f"📊 Resultados filtrados: {len(filtro)} linhas")
        st.dataframe(filtro)

        # Exportar como Excel
        csv_export = filtro.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Baixar resultados filtrados (CSV)", data=csv_export, file_name="filtro_tickets.csv", mime="text/csv")
    else:
        st.warning("⚠️ A planilha precisa ter as colunas 'Tipo' e 'Análise'.")

