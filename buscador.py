import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Dashboard de Tickets", layout="wide")

# Título
st.markdown("## 🧾 Dashboard de Tickets")
st.markdown("Antes de começar, envie o arquivo `.csv` com os dados dos tickets.")

# Upload do arquivo
arquivo = st.file_uploader("📁 Envie o arquivo CSV aqui", type="csv")

if arquivo is not None:
    # Carregar dados
    df = pd.read_csv(arquivo)

    # 🧼 Normaliza os dados da coluna 'Análise'
    df["Análise"] = df["Análise"].astype(str).str.strip().str.upper()

    # Interface de filtros
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        ticket_busca = st.text_input("🔍 Buscar por código do Ticket")
    with col2:
        tipo_selecionado = st.selectbox("📂 Filtrar por Tipo:", ["Todos"] + sorted(df["Tipo"].dropna().unique()))
    with col3:
        analise_selecionada = st.radio("⚙️ Filtrar por Análise:", ["Todos", "IDEAL", "NÃO IDEAL"], horizontal=True)

    # Aplicar filtros
    df_filtrado = df.copy()
    if ticket_busca:
        df_filtrado = df_filtrado[df_filtrado["Ticket"].str.contains(ticket_busca, case=False, na=False)]
    if tipo_selecionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Tipo"] == tipo_selecionado]
    if analise_selecionada != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Análise"] == analise_selecionada]

    # Métricas
    col4, col5, col6 = st.columns(3)
    col4.metric("📊 Total de Tickets", len(df_filtrado))
    col5.metric("✅ IDEAL", (df_filtrado["Análise"] == "IDEAL").sum())
    col6.metric("❌ NÃO IDEAL", (df_filtrado["Análise"] == "NÃO IDEAL").sum())

    # Exibição da tabela
    st.markdown("---")
    st.subheader("📋 Resultados filtrados")
    st.dataframe(df_filtrado, use_container_width=True)

else:
    st.warning("⛔ Nenhum arquivo enviado. Por favor, envie o arquivo CSV para iniciar o dashboard.")



