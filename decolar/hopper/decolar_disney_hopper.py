from imports import *



async def receive_disney_decolar_hopper(data,data_hora,data_atual):
    data_list = data  # Recebe a lista de objetos JSON enviada na solicitação
    
    # Trim 'Parque' field in each item
    for item in data_list:
        item['Parque'] = item['Parque'].strip()
    
    # Mapeamento dos nomes dos parques
    mapping = {
    "Ingresso de 1 dia Magic Kingdom Park + Adicional Park Hopper Plus": "1 Dia - Disney Parques Aquaticos",
    "Ingresso de 1 dia Magic Kingdom Park + Adicional Park Hopper": "1 Dia - Disney Park Hopper",
    "Ingresso de 2 dias + Adicional Park Hopper Plus": "2 Dias - Disney Parques Aquaticos",
    "Ingresso de 2 dias + Adicional Park Hopper": "2 Dias - Disney Park Hopper",
    "Ingresso de 3 dias + Adicional Park Hopper Plus": "3 Dias - Disney Parques Aquaticos",
    "Ingresso de 3 dias + Adicional Park Hopper": "3 Dias - Disney Park Hopper",
    "Ingresso de 4 dias + Adicional Park Hopper Plus": "4 Dias - Disney Parques Aquaticos",
    "Ingresso de 4 dias + Adicional Park Hopper": "4 Dias - Disney Park Hopper",
    "Ingresso de 5 dias + Adicional Park Hopper Plus": "5 Dias - Disney Parques Aquaticos",
    "Ingresso de 5 dias + Adicional Park Hopper": "5 Dias - Disney Park Hopper",
    "Bilhete de 6 dias + Adicional Park Hopper Plus": "6 Dias - Disney Parques Aquaticos",
    "Bilhete de 6 dias + Adicional Park Hopper": "6 Dias - Disney Park Hopper",
    "Ingresso de 7 dias + Adicional Park Hopper Plus": "7 Dias - Disney Parques Aquaticos",
    "Ingresso de 7 dias + Adicional Park Hopper": "7 Dias - Disney Park Hopper",
    "Ingresso de 8 dias + Adicional Park Hopper Plus": "8 Dias - Disney Parques Aquaticos",
    "Ingresso de 8 dias + Adicional Park Hopper": "8 Dias - Disney Park Hopper",
    "Ingresso de 9 dias + Adicional Park Hopper Plus": "9 Dias - Disney Parques Aquaticos",
    "Ingresso de 9 dias + Adicional Park Hopper": "9 Dias - Disney Park Hopper",
    "Ingresso de 10 dias + Adicional Park Hopper Plus": "10 Dias - Disney Parques Aquaticos",
    "Ingresso de 10 dias + Adicional Park Hopper": "10 Dias - Disney Park Hopper"
}


    filtered_data_list = [item for item in data_list if item['Parque'] in mapping]

    # Atualiza os nomes dos parques de acordo com o mapeamento
    for item in filtered_data_list:
        item['Parque'] = mapping[item['Parque']]

    # Criar um DataFrame pandas a partir da lista de dados filtrados
    df = pd.DataFrame(filtered_data_list)
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

    #df.to_json(f'hopper_decolar_{data_atual}.json', orient='records')
    nome_arquivo = f'hopper_decolar_{data_atual}.json'
    salvar_dados_decolar(formatted_data, nome_arquivo ,'hopper/decolar',str(hora))
    
    return jsonify({"message": "Dados salvos com sucesso!"})
