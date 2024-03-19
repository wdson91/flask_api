from imports import *



async def disney_decolar(data,data_hora):
    data_list = data  # Recebe a lista de objetos JSON enviada na solicitação

    # Trim 'Parque' field in each item
    for item in data_list:
        item['Parque'] = item['Parque'].strip()
    
    # Mapeamento dos nomes dos parques
    mapping = {
        "Ingresso de 1 dia Magic Kingdom Park - 2024": "1 Dia - Disney Basico Magic Kingdom",
        "Ingresso de 1 dia Disney Park Hollywood Studios 2024": "1 Dia - Disney Basico Hollywood Studios",
        "Ingresso de 1 dia para o Disney Animal Kingdom Park - 2024": "1 Dia - Disney Basico Animal Kingdom",
        "Ingresso de 1 dia EPCOT Park - 2024": "1 Dia - Disney Basico Epcot",
        "Ingresso de 2 dias - 2024": "2 Dias - Disney World Basico",
        "Bilhete de 3 dias - 2024": "3 Dias - Disney World Basico",
        "Ingresso Mágico 4 dias - 4 parques": "4 Dias - Disney Promocional",
        "Ingresso de 4 dias - 2024": "4 Dias - Disney World Basico",
        "Ingresso de 5 dias - 2024": "5 Dias - Disney World Basico"
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

    nome_arquivo = f'disney_decolar_{datetime.now().strftime("%Y-%m-%d")}.json'
    salvar_dados_decolar(formatted_data, nome_arquivo ,'decolar',str(hora))
    
    return jsonify({"message": "Dados salvos com sucesso!"})