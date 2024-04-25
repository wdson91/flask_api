from app import *
from excluir_json import apagar_arquivos_json_na_pasta_atual
from imports import *
from salvardados import baixar_blob_se_existir, carregar_dados_json, salvar_dados_margem
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
    nova_hora_formatada = hour
    
    # Baixa os arquivos JSON dos diferentes parques e empresas
    for empresa in empresas:
        for parque in parques:
            baixar_blob_se_existir(f'{parque}_{empresa}_{data_atual}.json', f'orlando/{empresa}')

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
    
    salvar_dados_margem(df, nome_arquivo, 'orlando/dados',nova_hora_formatada)
    
    finalizar_calibragem()
    
    apagar_arquivos_json_na_pasta_atual()
    time.sleep(30)
    atualizar_calibragem(100)
    
    
if __name__ == "__main__":
    # Hora global
    hora_global = datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%H:%M")
    data_atual = datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%Y-%m-%d")
    
    # Crie um loop de eventos e execute a função principal
    asyncio.run(juntarjsons(hora_global,data_atual))
