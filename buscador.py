import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard de Tickets", layout="wide")
st.title("📊 Dashboard Interativo para Análise de Tickets")

st.markdown("""
Envie seu arquivo CSV e use os filtros para explorar os tickets rapidamente.
""")

col_esq, col_dir = st.columns([4, 1])  # Dashboard maior

with col_dir:
    uploaded_file = st.file_uploader("⬆️ Envie seu arquivo CSV aqui", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        col_necessarias = ["Ticket", "Tipo", "Análise"]
        if not all(col in df.columns for col in col_necessarias):
            st.error(f"⚠️ O arquivo precisa conter as colunas: {', '.join(col_necessarias)}")
        else:
            # Limpar espaços e padronizar caixa
            df['Análise'] = df['Análise'].astype(str).str.strip().str.upper()
            df['Tipo'] = df['Tipo'].astype(str).str.strip()
            df['Ticket'] = df['Ticket'].astype(str).str.strip()

            st.markdown("### 🔍 Filtros e Busca")

            busca_ticket = st.text_input("Pesquisar Ticket (ID):", "")

            tipos = df['Tipo'].dropna().unique().tolist()
            analises = df['Análise'].dropna().unique().tolist()

            tipo_selecionado = st.multiselect(
                "Filtrar por Tipo:",
                options=tipos,
                default=tipos
            )
            analise_selecionada = st.multiselect(
                "Filtrar por Análise:",
                options=analises,
                default=analises
            )

            # Aplicar filtros
            df_filtrado = df[
                (df['Tipo'].isin(tipo_selecionado)) &
                (df['Análise'].isin(analise_selecionada))
            ]

            # Filtro busca ticket (case insensitive)
            if busca_ticket.strip():
                df_filtrado = df_filtrado[df_filtrado['Ticket'].str.contains(busca_ticket.strip(), case=False)]

            st.markdown(f"### Tickets encontrados: {len(df_filtrado)}")

            st.dataframe(df_filtrado)

    else:
        st.info("📂 Por favor, envie um arquivo CSV para começar.")

with col_esq:
    if uploaded_file and 'df_filtrado' in locals():
        st.markdown("## 📈 Estatísticas e Gráfico de Classificação")

        total_tickets = len(df_filtrado)
        ideal_count = len(df_filtrado[df_filtrado['Análise'] == 'IDEAL'])
        nao_ideal_count = len(df_filtrado[df_filtrado['Análise'] == 'NÃO IDEAL'])

        # Mostrar zero caso não tenha dados
        ideal_count = ideal_count if ideal_count > 0 else 0
        nao_ideal_count = nao_ideal_count if nao_ideal_count > 0 else 0

        c1, c2, c3 = st.columns(3)
        c1.metric("Total de Tickets", total_tickets)
        c2.metric(
            "Tickets IDEAL", ideal_count,
            delta=f"{(ideal_count / total_tickets * 100 if total_tickets else 0):.1f}%"
        )
        c3.metric(
            "Tickets NÃO IDEAL", nao_ideal_count,
            delta=f"{(nao_ideal_count / total_tickets * 100 if total_tickets else 0):.1f}%"
        )

        st.markdown("### 🥧 Proporção de Tickets IDEAL vs NÃO IDEAL")

        analise_counts = df_filtrado['Análise'].value_counts().reset_index()
        analise_counts.columns = ['Análise', 'Quantidade']

        fig = px.pie(
            analise_counts,
            values='Quantidade',
            names='Análise',
            color='Análise',
            color_discrete_map={'IDEAL': '#4CAF50', 'NÃO IDEAL': '#F44336'},
            hole=0.4,
            title="Proporção IDEAL x NÃO IDEAL"
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(margin=dict(t=40, b=40, l=40, r=40), height=350)

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown("⚠️ Faça o upload de um arquivo CSV válido para visualizar estatísticas e gráfico.")



