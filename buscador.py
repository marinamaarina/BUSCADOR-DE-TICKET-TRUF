import streamlit as st
import pandas as pd

st.title("Análise e Filtro de Tickets")

# Upload do arquivo CSV
uploaded_file = st.file_uploader("Envie o arquivo CSV com os tickets", type=["csv"])

if uploaded_file is not None:
    # Lendo o CSV para DataFrame
    df = pd.read_csv(uploaded_file)

    # Verifica se as colunas necessárias existem
    col_necessarias = ["Ticket", "Tipo", "Análise"]
    if not all(col in df.columns for col in col_necessarias):
        st.error(f"O arquivo precisa conter as colunas: {', '.join(col_necessarias)}")
    else:
        st.write("### Visualização dos dados originais")
        st.dataframe(df)

        # Criar filtros dinâmicos para Tipo e Análise
        tipos = df['Tipo'].dropna().unique().tolist()
        analises = df['Análise'].dropna().unique().tolist()

        tipo_selecionado = st.multiselect("Filtrar por Tipo", tipos, default=tipos)
        analise_selecionada = st.multiselect("Filtrar por Análise", analises, default=analises)

        # Filtrar dados
        df_filtrado = df[
            (df['Tipo'].isin(tipo_selecionado)) & 
            (df['Análise'].isin(analise_selecionada))
        ]

        st.write(f"### Tickets filtrados ({len(df_filtrado)})")
        st.dataframe(df_filtrado)
else:
    st.info("Por favor, envie o arquivo CSV para começar.")

