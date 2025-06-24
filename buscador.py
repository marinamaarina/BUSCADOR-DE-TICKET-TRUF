import pandas as pd

# 1. Carrega a planilha
arquivo = "tickets.xlsx"  # troque pelo nome do seu arquivo
df = pd.read_excel(arquivo)  # ou use pd.read_csv se for .csv

# 2. Exibe colunas disponíveis
print("Colunas disponíveis:", df.columns.tolist())

# 3. Filtra IDEAL e NÃO IDEAL
filtro_ideal = df[df['Análise'] == 'IDEAL']
filtro_nao_ideal = df[df['Análise'] == 'NÃO IDEAL']

# 4. Filtra por tipo (exemplo: “Liveness”)
tipo_especifico = "Liveness"
filtro_tipo = df[df['Tipo'] == tipo_especifico]

# 5. (Opcional) Filtrar por tipo + análise juntos
filtro_tipo_e_ideal = df[(df['Tipo'] == tipo_especifico) & (df['Análise'] == 'IDEAL')]

# 6. Mostrar os resultados
print("\n🔹 Tickets IDEAL:")
print(filtro_ideal)

print("\n🔹 Tickets NÃO IDEAL:")
print(filtro_nao_ideal)

print(f"\n🔹 Tickets do tipo '{tipo_especifico}':")
print(filtro_tipo)

print(f"\n🔹 Tickets do tipo '{tipo_especifico}' e IDEAL:")
print(filtro_tipo_e_ideal)
