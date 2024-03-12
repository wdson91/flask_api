from imports import *

async def juntarjsons():
    # Lista de empresas e parques
    empresas = ['voupra', 'vmz', 'decolar', 'ml']
    parques = ['disney', 'universal', 'seaworld']

    # Obtém a data atual
    data_atual = datetime.now().strftime("%Y-%m-%d")

    # Baixa os arquivos JSON dos diferentes parques e empresas
    for empresa in empresas:
        for parque in parques:
            baixar_blob_se_existir(f'{parque}_{empresa}_{data_atual}.json', empresa)

    # Carrega os dados JSON baixados para cada empresa e parque
    dados = {}
    for empresa in empresas:
        dados[empresa] = {}
        for parque in parques:
            dados[empresa][parque] = carregar_dados_json(f'{parque}_{empresa}_{data_atual}.json')

    # Combina os dados de todas as empresas e parques
    dados_combinados = {
        empresa: {parque: dados[empresa][parque] for parque in parques} for empresa in empresas
    }

    # Cria um DataFrame a partir dos dados combinados
    df = pd.DataFrame(dados_combinados)

    # Nome do arquivo para salvar os dados
    nome_arquivo = f'dados_{datetime.now().strftime("%Y-%m-%d")}.json'

    # Salva os dados no Blob Storage e também localmente como um arquivo JSON
    salvar_dados_margem(df, nome_arquivo, 'dados')

    # Salva o JSON localmente como um arquivo
    with open(nome_arquivo, 'w') as f:
        json.dump(dados_combinados, f)

    for empresa in empresas:
        for parque in parques:
            arquivo_json = f'{parque}_{empresa}_{data_atual}.json'
            if os.path.exists(arquivo_json):
                os.remove(arquivo_json)

    logging.info("Arquivos JSON locais excluídos.")
    # Registra a finalização da coleta
    logging.info("Coleta finalizada.")

if __name__ == "__main__":
    # Crie um loop de eventos e execute a função principal
    asyncio.run(juntarjsons())