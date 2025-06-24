import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard de Tickets", layout="wide")
st.title("📊 Dashboard Interativo para Análise de Tickets")

st.markdown("""
Bem-vindo! Aqui você pode enviar seu arquivo CSV com os tickets para analisar os dados de forma fácil e rápida.

**O arquivo deve conter as colunas:**  
- `Ticket`: identificador único  
- `Tipo`: categoria do ticket (ex: Liveness, Outros)  
- `Análise`: classificação do ticket (ex: IDEAL, NÃO IDEAL)

Use os filtros abaixo para explorar os dados de acordo com seus interesses!
""")

uploaded_file = st.file_uploader("⬆️ Envie seu arquivo CSV aqui", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    col_necessarias = ["Ticket", "Tipo", "Análise"]
    if not all(col in df.columns for col in col_necessarias):
        st.error(f"Oops! O arquivo precisa conter as colunas: {', '.join(col_necessarias)}")
    else:
        st.markdown("### 👀 Visualização dos dados carregados")
        st.dataframe(df)

        # Filtros
        tipos = df['Tipo'].dropna().unique().tolist()
        analises = df['Análise'].dropna().unique().tolist()

        col1, col2 = st.columns(2)
        with col1:
            tipo_selecionado = st.multiselect(
                "Filtrar por Tipo de Ticket:", 
                options=tipos, 
                default=tipos,
                help="Selecione um ou mais tipos de ticket para visualizar"
            )
        with col2:
            analise_selecionada = st.multiselect(
                "Filtrar por Classificação:", 
                options=analises, 
                default=analises,
                help="Selecione as classificações dos tickets para filtrar"
            )

        df_filtrado = df[(df['Tipo'].isin(tipo_selecionado)) & (df['Análise'].isin(analise_selecionada))]

        st.markdown(f"### ✅ Tickets após filtragem: **{len(df_filtrado)}**")
        st.dataframe(df_filtrado)

        # Estatísticas
        st.markdown("## 📈 Estatísticas Rápidas")

        total_tickets = len(df_filtrado)
        ideal_count = len(df_filtrado[df_filtrado['Análise'] == 'IDEAL'])
        nao_ideal_count = len(df_filtrado[df_filtrado['Análise'] == 'NÃO IDEAL'])

        col1, col2, col3 = st.columns(3)
        col1.metric("Total de Tickets", total_tickets)
        col2.metric("Tickets IDEAL", ideal_count, delta=f"{(ideal_count / total_tickets * 100 if total_tickets else 0):.1f}%")
        col3.metric("Tickets NÃO IDEAL", nao_ideal_count, delta=f"{(nao_ideal_count / total_tickets * 100 if total_tickets else 0):.1f}%")

        # Gráfico de barras: Tickets por Tipo
        st.markdown("### 📊 Distribuição de Tickets por Tipo")
        tipo_counts = df_filtrado['Tipo'].value_counts()

        fig1, ax1 = plt.subplots()
        tipo_counts.plot(kind='bar', ax=ax1, color='cornflowerblue')
        ax1.set_xlabel("Tipo de Ticket")
        ax1.set_ylabel("Quantidade")
        ax1.set_title("Número de Tickets por Tipo")
        ax1.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig1)

        # Gráfico pizza: proporção Análise
        st.markdown("### 🥧 Proporção de Classificação dos Tickets")
        analise_counts = df_filtrado['Análise'].value_counts()

        fig2, ax2 = plt.subplots()
        colors = ['#4CAF50', '#F44336']
        ax2.pie(
            analise_counts, 
            labels=analise_counts.index, 
            autopct='%1.1f%%', 
            startangle=140, 
            colors=colors, 
            textprops={'fontsize': 12}
        )
        ax2.axis('equal')
        st.pyplot(fig2)

else:
    st.info("📂 Por favor, envie um arquivo CSV para começar a análise.")



