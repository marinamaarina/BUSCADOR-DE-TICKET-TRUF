import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard Tickets", layout="wide")
st.title("Dashboard e Análise de Tickets")

# Upload do arquivo CSV
uploaded_file = st.file_uploader("Envie o arquivo CSV com os tickets", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    col_necessarias = ["Ticket", "Tipo", "Análise"]
    if not all(col in df.columns for col in col_necessarias):
        st.error(f"O arquivo precisa conter as colunas: {', '.join(col_necessarias)}")
    else:
        st.markdown("### Dados Originais")
        st.dataframe(df)

        # Filtros
        tipos = df['Tipo'].dropna().unique().tolist()
        analises = df['Análise'].dropna().unique().tolist()

        col1, col2 = st.columns(2)
        with col1:
            tipo_selecionado = st.multiselect("Filtrar por Tipo", tipos, default=tipos)
        with col2:
            analise_selecionada = st.multiselect("Filtrar por Análise", analises, default=analises)

        # Dados filtrados
        df_filtrado = df[(df['Tipo'].isin(tipo_selecionado)) & (df['Análise'].isin(analise_selecionada))]

        st.markdown(f"### Tickets filtrados: {len(df_filtrado)}")
        st.dataframe(df_filtrado)

        # Estatísticas rápidas
        st.markdown("## Estatísticas")

        total_tickets = len(df_filtrado)
        ideal_count = len(df_filtrado[df_filtrado['Análise'] == 'IDEAL'])
        nao_ideal_count = len(df_filtrado[df_filtrado['Análise'] == 'NÃO IDEAL'])

        col1, col2, col3 = st.columns(3)
        col1.metric("Total de Tickets", total_tickets)
        col2.metric("Tickets IDEAL", ideal_count)
        col3.metric("Tickets NÃO IDEAL", nao_ideal_count)

        # Gráfico de barras: Tickets por Tipo
        st.markdown("### Distribuição por Tipo")
        tipo_counts = df_filtrado['Tipo'].value_counts()

        fig1, ax1 = plt.subplots()
        tipo_counts.plot(kind='bar', ax=ax1, color='skyblue')
        ax1.set_xlabel("Tipo")
        ax1.set_ylabel("Quantidade")
        ax1.set_title("Quantidade de Tickets por Tipo")
        st.pyplot(fig1)

        # Gráfico pizza: proporção Análise
        st.markdown("### Proporção de Análise")
        analise_counts = df_filtrado['Análise'].value_counts()

        fig2, ax2 = plt.subplots()
        ax2.pie(analise_counts, labels=analise_counts.index, autopct='%1.1f%%', startangle=140, colors=['#4CAF50', '#F44336'])
        ax2.axis('equal')
        st.pyplot(fig2)

else:
    st.info("Por favor, envie o arquivo CSV para começar.")

