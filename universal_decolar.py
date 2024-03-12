from imports import *


async def universal_decolar(data,data_hora):
    data_list = data  # Recebe a lista de objetos JSON enviada na solicitação

    # Trim 'Parque' field in each item
    for item in data_list:
        item['Parque'] = item['Parque'].strip()
        
    # Mapeamento dos nomes dos parques
    mapping = {
        "Ingresso 1 Parque 1 Dia": "1 Dia 1 Parque - Universal Orlando",
        "Ingresso 2-Park 1-Day Park-to-Park": "1 Dia 2 Parques - Universal Orlando",
        "Ingresso 2 Parques 2 Dias (Parque a Parque)": "2 Dias 2 Parques - Universal Orlando",
        "Ingresso em 2 Parques 2 Dias (Parque a Parque) + 2 Dias Grátis": "4 Dias 2 Parques - Universal Orlando",
        "Ingresso Explorer 3 Parques 2024": "14 Dias 3 Parques - Universal Orlando"
    }

    filtered_data_list = [item for item in data_list if item['Parque'] in mapping]

    # Atualiza os nomes dos parques de acordo com o mapeamento
    for item in filtered_data_list:
        item['Parque'] = mapping[item['Parque']]
        
        
    # Criar um DataFrame pandas a partir da lista de dados filtrados
    df = pd.DataFrame(filtered_data_list)
    
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
        
    nome_arquivo = f'universal_decolar_{datetime.now().strftime("%Y-%m-%d")}.json'
    salvar_dados(formatted_data, nome_arquivo ,'decolar',"12:00")

    return jsonify({"message": "Dados salvos com sucesso!"})