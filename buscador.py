import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Análise de Tickets", layout="wide")
st.title("📊 Dashboard Interativo de Análise de Tickets")

# Upload do arquivo Excel
arquivo = st.file_uploader("📎 Envie seu arquivo Excel com os dados", type=["xlsx"])

if arquivo:
    # Leitura do Excel
    df = pd.read_excel(arquivo, sheet_name="Dados")
    df.columns = df.columns.str.strip()  # limpa os nomes das colunas

    st.sidebar.header("🔎 Filtros Interativos")

    # 🔍 Campo de busca livre para filtrar a coluna "Análise"
    analise_busca = st.sidebar.text_input(
        "Buscar Análise (ex: ideal, não)", value=""
    ).strip().upper()

    # Filtra a coluna "Análise" por texto
    df_busca = df[df["Análise"].str.upper().str.contains(analise_busca)] if analise_busca else df

    # 🎯 Tipos disponíveis com base na busca de Análise
    tipos_disponiveis = df_busca["Tipo"].unique()
    tipo_selecionado = st.sidebar.multiselect(
        "Filtrar por Tipos",
        options=sorted(tipos_disponiveis),
        default=sorted(tipos_disponiveis)
    )

    # 📌 Filtro final
    df_filtrado = df_busca[df_busca["Tipo"].isin(tipo_selecionado)]

    # 🧠 Insight automático
    st.subheader("🧠 Insight Inteligente")
    if not df_filtrado.empty:
        tipo_top = df_filtrado["Tipo"].value_counts().idxmax()
        qtde_top = df_filtrado["Tipo"].value_counts().max()
        total_filtrado = len(df_filtrado)
        percentual = (qtde_top / total_filtrado) * 100
        st.info(f"⚠️ O tipo **{tipo_top}** representa **{percentual:.1f}%** dos tickets filtrados.")
    else:
        st.warning("Nenhum dado encontrado com os filtros atuais.")

    # 📊 Métricas
    col1, col2 = st.columns(2)
    col1.metric("Tickets Filtrados", len(df_filtrado))
    col2.metric("Tipos Únicos", df_filtrado["Tipo"].nunique())

    # 📈 Gráficos
    if not df_filtrado.empty:
        st.subheader("📊 Distribuição por Tipo")
        fig_pizza = px.pie(df_filtrado, names="Tipo", title="Participação dos Tipos", hole=0.4)
        st.plotly_chart(fig_pizza, use_container_width=True)

        st.subheader("📈 Frequência por Tipo")
        fig_bar = px.bar(
            df_filtrado["Tipo"].value_counts().reset_index(),
            x="index", y="Tipo",
            labels={"index": "Tipo", "Tipo": "Quantidade"},
            title="Tickets por Tipo",
            color="index"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # 📄 Tabela de dados
    st.subheader("📄 Tabela com Dados Filtrados")
    st.dataframe(df_filtrado, use_container_width=True)

else:
    st.warning("⚠️ Envie o arquivo Excel para iniciar a análise.")

