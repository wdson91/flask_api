import pandas as pd

# Carregar o arquivo CSV
df = pd.read_csv('precos_organizados.csv')

# Função para ajustar o ano com base no mês
def ajustar_ano(data):
    mes = int(data[5:7])
    if mes >= 1 and mes <= 4:
        return data.replace('2025', '2025')
    else:
        return data.replace('2025', '2024')

# Aplicar a função a cada linha da coluna 'Data'
df['Data'] = df['Data'].apply(ajustar_ano)

# Salvar o DataFrame modificado em um novo arquivo CSV
df.to_csv('precos_organizados.csv', index=False)

# Verificar se a substituição foi bem-sucedida
print("Anos substituídos com sucesso!")
