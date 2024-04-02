from imports import *
from voupra.paris.voupraparis.voupraparis import coletar_precos_voupra_paris



async def main_voupra_paris(hour,array_datas,data_atual,run_once=False):
    if run_once:
        logging.info("Iniciando coleta de preços Voupra Disney.")
        try:
            # Execute as funções assíncronas em sequência
            await coletar_precos_voupra_paris(hour, array_datas,data_atual)
            
        except Exception as e:
                logging.error(f"Erro durante a coleta de preços Disney: {e}")
        return 
if __name__ == "__main__":
    # Crie um loop de eventos e execute a função principal
    asyncio.run(main_voupra_paris())
