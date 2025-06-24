import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Análise de Tickets", layout="wide")
st.title("📊 Dashboard Interativo de Análise de Tickets")

# Upload do arquivo
arquivo = st.file_uploader("📎 Envie seu arquivo Excel com os dados", type=["xlsx"])

if arquivo:
    # Leitura do arquivo enviado
    df = pd.read_excel(arquivo, sheet_name="Dados")
    df.columns = df.columns.str.strip()  # limpa nomes de colunas

    # SIDEBAR COM FILTROS
    st.sidebar.header("🔎 Filtros")

    analise_selecionada = st.sidebar.selectbox(
        "Filtrar por Análise (IDEAL ou NÃO IDEAL)",
        options=sorted(df["Análise"].unique())
    )

    tipos_disponiveis = df[df["Análise"] == analise_selecionada]["Tipo"].unique()
    tipo_selecionado = st.sidebar.multiselect(
        "Filtrar por Tipos (relacionados à análise)",
        options=sorted(tipos_disponiveis),
        default=sorted(tipos_disponiveis)
    )

    # Aplica filtros
    df_filtrado = df[
        (df["Análise"] == analise_selecionada) &
        (df["Tipo"].isin(tipo_selecionado))
    ]

    # INSIGHT AUTOMÁTICO
    st.subheader("🧠 Insight Inteligente")
    if not df_filtrado.empty:
        tipo_top = df_filtrado["Tipo"].value_counts().idxmax()
        qtde_top = df_filtrado["Tipo"].value_counts().max()
        total_filtrado = len(df_filtrado)
        percentual = (qtde_top / total_filtrado) * 100
        st.info(f"⚠️ O tipo **{tipo_top}** representa **{percentual:.1f}%** dos tickets com análise **{analise_selecionada}**.")
    else:
        st.warning("Nenhum dado encontrado com os filtros selecionados.")

    # MÉTRICAS
    col1, col2 = st.columns(2)
    col1.metric("Tickets Filtrados", len(df_filtrado))
    col2.metric("Tipos Únicos", df_filtrado["Tipo"].nunique())

    # GRÁFICOS
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

    # TABELA
    st.subheader("📄 Tabela com Dados Filtrados")
    st.dataframe(df_filtrado, use_container_width=True)

else:
    st.warning("⚠️ Envie o arquivo Excel para iniciar a análise.")



