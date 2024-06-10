import pandas as pd

# Carregar os dois arquivos CSV
df1 = pd.read_csv('precos_organizados.csv')
df2 = pd.read_csv('precos_organizados_2024.csv')
df3 = pd.read_csv('precos_organizados_junho.csv')

# Concatenar os DataFrames
df_concatenado = pd.concat([df1, df2, df3], ignore_index=True)

# Salvar o DataFrame concatenado em um novo arquivo Excel (xlsx)
df_concatenado.to_excel('arquivo_concatenado.xlsx', index=False)

# Verificar se a concatenação foi bem-sucedida
print("Arquivos CSV foram concatenados e salvos como Excel (xlsx) com sucesso!")
