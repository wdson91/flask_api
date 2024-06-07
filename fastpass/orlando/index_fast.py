from fastpass.orlando.fast_sea.fastsea import coletar_precos_fastPass_seaworld
from imports import *



from classes.junta_dados_classe import JuntarJsons
from fastpass.orlando.fastdisney.fast_disney import coletar_precos_fastPass_disney
from fastpass.orlando.fastuniversal.fast_universal import coletar_precos_fastPass_universal

async def main_fastPass(hour,array_datas,data_atual,):
        
        logging.info("Iniciando coleta de preços FastPass.")
        try:
            # Execute as funções assíncronas em sequência
            await coletar_precos_fastPass_disney(hour,array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços da Disney: {e}")

        try:
            await coletar_precos_fastPass_seaworld(hour,array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços do SeaWorld: {e}")

        try:
            await coletar_precos_fastPass_universal(hour,array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços da Universal: {e}")
            
        logging.info("Iniciando coleta de preços FastPass Finalizada.")
        return 
if __name__ == "__main__":
    # Crie um loop de eventos e execute a função principal
    asyncio.run(main_fastPass())
