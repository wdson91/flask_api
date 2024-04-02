from datetime import datetime
import json
from flask import jsonify
import pandas as pd
import re

import pytz

from decolar.salvardadosdecolar import salvar_dados_decolar

def clean_price(price_str):
    cleaned_price = price_str.replace('R$', '').replace('\n', '').strip()
    return float(cleaned_price.replace('.', ''))

def decolar_paris2(dados):
    print(dados)
    dados_originais = dados
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
    formatted_data = []
    # Dicionário para mapear os nomes dos parques
    parques_mapping = {
        'Disneyland Paris Acesso a 2 parques em 1 dia 2024': '1 Dia 2 Parques - Disney Paris',
        'Disneyland Paris: 1 dia / 1 parque': '1 Dia 1 Parque - Disney Paris'
    }

    # Iterar sobre os dados originais e converter para o formato desejado
    for dado in dados_originais:
        data_viagem = f"2024-{meses[dado['mes']]:02d}-{int(dado['dia']):02d}"
        Preco_Parcelado = clean_price(dado['Preco_Parcelado'])
        preco_avista = Preco_Parcelado * 0.97  # Desconto de 3% para pagamento à vista
        Parque = parques_mapping.get(dado['Parque'], dado['Parque'])
        Hora_coleta = dado['hora']
        dados_formatados.append({
            'Hora_coleta': Hora_coleta,
            'Data_viagem': data_viagem,
            'Parque': Parque,
            'Preco_Parcelado': Preco_Parcelado,
            'Preco_Avista': preco_avista
        })

    df = pd.DataFrame(dados_formatados)
    
    hora= df['Hora_coleta'].iloc[0]
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
    print(formatted_data)
    nome_arquivo = f'disney_decolar_data_atual.json'
    #salvar_dados_decolar(formatted_data, nome_arquivo ,'decolar',str(hora))
    
    return jsonify({"message": "Dados salvos com sucesso!"})