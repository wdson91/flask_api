import re
import pandas as pd
from flask import jsonify

from decolar.salvardadosdecolar import salvar_dados_decolar

def clean_price(string):
    if isinstance(string, str):  # Verificar se é uma string válida
        last_three_chars = string[-7:].rstrip()  # Pegar os últimos três caracteres da string
        last_three_chars=last_three_chars.replace(".", "").replace(",", ".").replace("R$", "").strip()
        return int(float(last_three_chars))
    return None

def decolar_fura_fila(dados,data_atual):
    
    data_list = dados
    dados_formatados = []
   
    # Dicionário para mapear o mês
    meses = {
        'janeiro': 1,
        'fevereiro': 2,
        'março': 3,
        'abril': 4,
        'maio': 5,
        'junho': 6,
        'julho': 7,
        'agosto': 8,
        'setembro': 9,
        'outubro': 10,
        'novembro': 11,
        'dezembro': 12
    }
    
    # Dicionário para mapear os nomes dos parques
    parques_mapping = {
        " Ingresso Expresso Adicional Ilimitado para os 2 Parques ": 'Ingresso 1 Dia Universal Express Unlimited',
        " Passe Universal Express adicional para 2 parques ": 'Ingresso 1 Dia Universal Express Pass'
    }

    filtered_data_list = [item for item in data_list if item['Parque'] in parques_mapping ]

    # Atualiza os nomes dos parques de acordo com o mapeamento
    for item in filtered_data_list:
        item['Parque'] = parques_mapping [item['Parque']]
        
        
    # Criar um DataFrame pandas a partir da lista de dados filtrados
    df = pd.DataFrame(filtered_data_list)
    hora = df['Hora_coleta'].iloc[0]
    df = df.sort_values(by=['Data_viagem', 'Parque'])
    df['Preco_Avista'] = df['Preco_Parcelado'] * 0.97 
    df = df[['Data_viagem', 'Parque', 'Preco_Parcelado', 'Preco_Avista']]
    # Converter o DataFrame de volta para uma lista de dicionários

    # Agrupar os dados por data_viagem e converter em formato de lista
    grouped_data = df.groupby('Data_viagem').apply(lambda x: x.to_dict(orient='records')).reset_index(
        name='Dados')

    # Formatar os dados conforme especificado
    formatted_data = []
    for index, row in grouped_data.iterrows():
        formatted_data.extend(row['Dados'])
    
    # Nome do arquivo
    nome_arquivo = f'furafila_decolar_{data_atual}.json'
    #df.to_json(nome_arquivo, orient='records', lines=True)
    # Salvar os dados
    salvar_dados_decolar(formatted_data, nome_arquivo, 'outros/decolar', str(hora))
    
    return jsonify({"message": "Dados salvos com sucesso!"})
