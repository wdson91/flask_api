from app import *
from imports import *
from salvardados import baixar_blob_se_existir
arquivos = os.listdir()
from atualizar_calibragem import atualizar_calibragem, finalizar_calibragem, mudar_horarios

async def juntarjsons(hour,data_atual):
    
    # Lista de empresas e parques
    empresas = ['voupra', 'vmz', 'decolar', 'ml']
    parques = ['disney', 'universal', 'seaworld']
    
    # Dicionário para armazenar os dados modificados
    dados_modificados = {}

    # Obtém o horário atual
    hora_atual = datetime.now(pytz.timezone('America/Sao_Paulo'))

    # Subtrai 20 minutos
    #nova_hora = hora_atual - timedelta(minutes=25)

    # Formata a nova hora para o formato desejado (HH:MM)
    #nova_hora_formatada = nova_hora.strftime("%H:%M")
    nova_hora_formatada = hour
    # Baixa os arquivos JSON dos diferentes parques e empresas
    for empresa in empresas:
        for parque in parques:
            baixar_blob_se_existir(f'{parque}_{empresa}_{data_atual}.json', empresa)

            # Carrega os dados JSON baixados
            dados = carregar_dados_json(f'{parque}_{empresa}_{data_atual}.json')

            # Modifica o último dado para a hora global
            #if dados:
                #dados[-1]['Hora_coleta'] = nova_hora_formatada

            # Atualiza o dicionário de dados modificados
            if empresa not in dados_modificados:
                dados_modificados[empresa] = {}
            dados_modificados[empresa][parque] = dados

    # Nome do arquivo para salvar os dados
    nome_arquivo = f'dados_{data_atual}.json'
    
    # Salva os dados modificados no Blob Storage e também localmente como um arquivo JSON
    with open(nome_arquivo, 'w') as f:
        json.dump(dados_modificados, f)

    df = pd.read_json(nome_arquivo)
    df = pd.DataFrame(df)
    
    #Remova os arquivos JSON locais
    for arquivo in arquivos:
        if arquivo.endswith('.json'):
            os.remove(arquivo)
    
    logging.info("Arquivos JSON locais excluídos.")
    
    time.sleep(30)
    atualizar_calibragem(100)
    
    salvar_dados_margem(df, nome_arquivo, 'dados',nova_hora_formatada)
    time.sleep(30)
    finalizar_calibragem()


if __name__ == "__main__":
    # Hora global
    hour = datetime.now().strftime("%H:%M")
    
    # Crie um loop de eventos e execute a função principal
    asyncio.run(juntarjsons(hour))
