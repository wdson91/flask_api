from imports import *

async def seaworld_decolar(json_data, data_hora,data_atual):
    # Mapeamento dos nomes dos parques
    mapping = {
        "Ingresso 3 parques pelo preço de 2": "3 Dias 3 Parques - SeaWorld Orlando",
        "Ingresso para 2 parques": "2 Dias 2 Parques - SeaWorld Orlando",
        "Ingresso para 1 parque": "1 Dia 1 Parque - SeaWorld Orlando",
        "Visitas ilimitadas + estacionamento gratuito": "14 Dias 3 Parques - SeaWorld Orlando",
        "Visite 3 parques ao preço de 2 com plano de refeições": "3 Dias 3 Parques com Refeições - SeaWorld Orlando",
        "Um dia no parque Busch Gardens": "1 Dia 1 Parque - Busch Gardens"
    }
    
    days_to_add = [5, 10, 20, 47, 65, 126]
    # Converter o JSON para um DataFrame pandas
    df = pd.DataFrame(json_data)
    
    # Remover duplicatas nos nomes dos parques e, em seguida, aplicar o trim
    df['Parque'] = df['Parque'].str.strip()
    df['Parque'] = df['Parque'].map(mapping)
    df = df.dropna(subset=['Parque'])
    hora= df['Hora_coleta'].iloc[0]
    # Obter a data atual
    sao_paulo_tz = pytz.timezone('America/Sao_Paulo')
    data = datetime.now(sao_paulo_tz).date()

    # Criar listas de datas de viagem
    datas_viagem = [data + timedelta(days=days) for days in days_to_add]

    # Criar um dicionário para armazenar os dados formatados
    formatted_data = []

    # Iterar sobre cada data de viagem e adicionar os dados formatados ao dicionário
    for data_viagem in datas_viagem:
        df_temp = df.copy()
        df_temp['Data_viagem'] = data_viagem.strftime("%Y-%m-%d")
        df_temp.drop_duplicates(subset=['Data_viagem', 'Parque'], inplace=True)
        df_temp = df_temp.sort_values(by=['Data_viagem', 'Parque'])
        df_temp['Preco_Avista'] = df_temp['Preco_Parcelado'] * 0.97
        df_temp = df_temp[['Data_viagem', 'Parque', 'Preco_Parcelado', 'Preco_Avista']]
        formatted_data.extend(df_temp.to_dict(orient='records'))
        
    nome_arquivo = f'seaworld_decolar_{data_atual}.json'
    
    salvar_dados_decolar(formatted_data, nome_arquivo ,'decolar', str(hora))
    
    return jsonify({"message": "Dados salvos com sucesso!"})
