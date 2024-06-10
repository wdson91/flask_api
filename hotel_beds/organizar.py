import pandas as pd

# Ler o CSV
df = pd.read_csv('precos_parques.csv')

# Adicionar o ano atual às datas
current_year = pd.Timestamp.now().year+1
df['Data'] = pd.to_datetime(df['data'] + ' ' + str(current_year), format='%a, %d %b %Y')

# Remover a coluna 'data' original
df.drop(columns=['data'], inplace=True)

# Transformar os dados no formato desejado
df_pivot = df.pivot_table(index=['Data'], columns='tipo', values=' 3 Parques 3 Dias - Entrada Parque a Parque com data + Promo 2 dias gratis ')

# Renomear a coluna para 'preco'
df_pivot.rename(columns={' 3 Parques 3 Dias - Entrada Parque a Parque com data + Promo 2 dias gratis ': 'preco'}, inplace=True)

# Resetar o índice
df_pivot.reset_index(inplace=True)

# Salvar o DataFrame resultante em um novo CSV
df_pivot.to_csv('precos_organizados.csv', index=False)

