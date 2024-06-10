import pandas as pd

# Carregar o arquivo xlsx
df = pd.read_excel('arquivo_concatenado.xlsx')

# Adicionar o símbolo de dólar ($) a todas as colunas numéricas
for column in df.columns:
    if df[column].dtype == 'float64':
        df[column] = df[column].map(lambda x: f'${x:.2f}')

# Salvar o DataFrame atualizado em um novo arquivo xlsx
df.to_excel('preco_3dias.xlsx', index=False)

print("Valores atualizados e arquivo salvo com sucesso!")
