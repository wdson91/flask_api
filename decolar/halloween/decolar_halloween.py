import re
import pandas as pd
from flask import jsonify

from decolar.salvardadosdecolar import salvar_dados_decolar

def clean_price(string):
    if isinstance(string, str):  # Verificar se é uma string válida
        last_three_chars = string[-6:].rstrip()  # Pegar os últimos três caracteres da string
        #if last_three_chars.isdigit():  # Verificar se os últimos três caracteres são dígitos
        last_three_chars = re.sub(r'[^\d]', '', last_three_chars)
        return int(last_three_chars)
    return None

def decolar_halloween(dados,data_atual):
    
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
    
    parques_mapping = {
    ' Ingresso para Noites de Terror de Halloween ':'Universal Halloween Horror Nights',
    " Ingresso ao evento de Halloween: Mickey's Not so Scary Halloween Party ":"Mickey’s Not–So–Scary Halloween",
}
    
    # Iterar sobre os dados originais e converter para o formato desejado
    for dado in dados_originais:
        data_viagem = dado['Data_viagem']
        Preco_Parcelado = dado['Preco_Parcelado']
        
        # Mapear o nome do parque
        Parque = None
        for nome_parque, nome_parque_mapeado in parques_mapping.items():
            if nome_parque in dado['Parque']:
                Parque = nome_parque_mapeado
                break
        if Parque is None:
            Parque = dado['Parque']  # Usar o nome original do parque se não houver mapeamento

        Hora_coleta = dados_originais[0]['Hora_coleta']
        dados_formatados.append({
            
            'Data_viagem': data_viagem,
            'Parque': Parque,
            'Preco_Parcelado': Preco_Parcelado,
            # Removendo o arredondamento do preço à vista
            'Preco_Avista': float(Preco_Parcelado) * 0.97
        })


    df = pd.DataFrame(dados_formatados)
    
    # Ordenar o DataFrame pelo campo 'Data_viagem' e 'Parque'
    df = df.sort_values(by=['Data_viagem', 'Parque'])
    
    # Remover duplicatas mantendo apenas a primeira ocorrência
    df.drop_duplicates(subset=['Data_viagem', 'Parque'], inplace=True)
    
    # Agrupar os dados por data_viagem e converter em formato de lista
    grouped_data = df.groupby('Data_viagem').apply(lambda x: x.to_dict(orient='records')).reset_index(
        name='Dados')

    # Formatar os dados conforme especificado
    formatted_data = []
    for index, row in grouped_data.iterrows():
        formatted_data.extend(row['Dados'])
    
    # Obter a hora de coleta
    hora = dados_originais[0]['Hora_coleta']
    
    # Nome do arquivo
    nome_arquivo = f'halloween_decolar_{data_atual}.json'
    #df.to_json(nome_arquivo, orient='records')
    # Salvar os dados
    salvar_dados_decolar(formatted_data, nome_arquivo, 'halloween/decolar', str(hora))
    
    return jsonify({"message": "Dados salvos com sucesso!"})
