import pandas as pd

# Lê o arquivo CSV existente
df = pd.read_csv('precos_parques.csv', index_col=[0, 1])

# Transpõe o DataFrame
df_transposed = df.transpose()

# Ordena as linhas do DataFrame pelo valor das datas
df_transposed = df_transposed.reindex(sorted(df_transposed.index, key=lambda x: pd.to_datetime(x, format='%d/%m')), axis=0)

# Salva o DataFrame transposto em um arquivo CSV
df_transposed.to_csv('precos_parques_ordenado.csv')

print("Dados transpostos e ordenados salvos em 'precos_parques_ordenado.csv'")
