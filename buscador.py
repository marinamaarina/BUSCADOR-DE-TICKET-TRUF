import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Dashboard de Tickets", layout="wide")
st.title("📊 Dashboard Interativo para Análise de Tickets")

st.markdown("""
Envie seu arquivo CSV e use os filtros para explorar os tickets rapidamente.
""")

# Layout em 2 colunas: esquerda maior para gráficos, direita menor para controles
col_esq, col_dir = st.columns([3,1])

with col_dir:
    uploaded_file = st.file_uploader("⬆️ Envie seu arquivo CSV aqui", type=["csv"])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        
        col_necessarias = ["Ticket", "Tipo", "Análise"]
        if not all(col in df.columns for col in col_necessarias):
            st.error(f"⚠️ O arquivo precisa conter as colunas: {', '.join(col_necessarias)}")
        else:
            st.markdown("### 🔍 Filtros e Busca")
            
            # Campo de busca por ticket
            busca_ticket = st.text_input("Pesquisar Ticket (ID):", "")
            
            # Filtros para Tipo e Análise
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
            
            # Aplicar filtros e busca
            df_filtrado = df[
                (df['Tipo'].isin(tipo_selecionado)) & 
                (df['Análise'].isin(analise_selecionada))
            ]
            if busca_ticket.strip():
                df_filtrado = df_filtrado[df_filtrado['Ticket'].str.contains(busca_ticket.strip(), case=False)]
            
            st.markdown(f"### Tickets encontrados: {len(df_filtrado)}")
            
            st.dataframe(df_filtrado)
    else:
        st.info("📂 Por favor, envie um arquivo CSV para começar.")

with col_esq:
    if uploaded_file and 'df_filtrado' in locals():
        st.markdown("## 📈 Estatísticas e Gráficos")

        total_tickets = len(df_filtrado)
        ideal_count = len(df_filtrado[df_filtrado['Análise'] == 'IDEAL'])
        nao_ideal_count = len(df_filtrado[df_filtrado['Análise'] == 'NÃO IDEAL'])

        c1, c2, c3 = st.columns(3)
        c1.metric("Total de Tickets", total_tickets)
        c2.metric("Tickets IDEAL", ideal_count, delta=f"{(ideal_count / total_tickets * 100 if total_tickets else 0):.1f}%")
        c3.metric("Tickets NÃO IDEAL", nao_ideal_count, delta=f"{(nao_ideal_count / total_tickets * 100 if total_tickets else 0):.1f}%")

        st.markdown("### 📊 Tickets por Tipo")
        tipo_counts = df_filtrado['Tipo'].value_counts()

        fig1, ax1 = plt.subplots()
        tipo_counts.plot(kind='bar', ax=ax1, color='cornflowerblue')
        ax1.set_xlabel("Tipo")
        ax1.set_ylabel("Quantidade")
        ax1.set_title("Quantidade de Tickets por Tipo")
        ax1.grid(axis='y', linestyle='--', alpha=0.7)
        st.pyplot(fig1)

        st.markdown("### 🥧 Proporção de Análise")
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
        st.markdown("⚠️ Faça o upload de um arquivo CSV válido para visualizar estatísticas e gráficos.")


