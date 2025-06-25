import streamlit as st
import pandas as pd

# ======== Configuração inicial ========
st.set_page_config(page_title="Dashboard de Tickets", layout="wide")

# ======== Carregamento dos dados ========
df = pd.read_csv("Dashboard_Analise - Dados.csv")

# ======== Título principal ========
st.markdown("## 🧾 Dashboard de Tickets")
st.markdown("Use os filtros abaixo para encontrar rapidamente os tickets IDEAL ou NÃO IDEAL por tipo.")

# ======== Layout dos filtros ========
col1, col2, col3 = st.columns([2, 2, 2])

with col1:
    ticket_busca = st.text_input("🔍 Buscar por código do Ticket")

with col2:
    tipo_selecionado = st.selectbox("📂 Filtrar por Tipo:", ["Todos"] + sorted(df["Tipo"].dropna().unique()))

with col3:
    analise_selecionada = st.radio("⚙️ Filtrar por Análise:", ["Todos", "IDEAL", "NÃO IDEAL"], horizontal=True)

# ======== Aplicar filtros ========
df_filtrado = df.copy()

if ticket_busca:
    df_filtrado = df_filtrado[df_filtrado["Ticket"].str.contains(ticket_busca, case=False, na=False)]

if tipo_selecionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Tipo"] == tipo_selecionado]

if analise_selecionada != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Análise"] == analise_selecionada]

# ======== Métricas resumo ========
col4, col5, col6 = st.columns(3)
col4.metric("🎫 Total de Tickets", len(df_filtrado))
col5.metric("✅ IDEAL", (df_filtrado["Análise"] == "IDEAL").sum())
col6.metric("❌ NÃO IDEAL", (df_filtrado["Análise"] == "NÃO IDEAL").sum())

# ======== Tabela com dados ========
st.markdown("---")
st.subheader("📋 Resultados")
st.dataframe(df_filtrado, use_container_width=True)
