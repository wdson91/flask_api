from imports import *



from classes.junta_dados_classe import JuntarJsons
from tioorlando.sea_tio import coleta_tio_sea
from tioorlando.disney_tio import coleta_tio_orlando
from tioorlando.universal_tio import coleta_tio_universal


async def main_tio(hour,array_datas,data_atual):
    
        
        logging.info("Iniciando a coleta de preços de Tio Orlando.")
        try:
            # Execute as funções assíncronas em sequência
            await coleta_tio_orlando(hour,array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços da Disney: {e}")

        # try:
        #     await coleta_tio_universal(hour,array_datas,data_atual)
            
        # except Exception as e:
        #     logging.error(f"Erro durante a coleta de preços do SeaWorld: {e}")
            
        # try:
        #     await coleta_tio_sea(hour,array_datas,data_atual)
            
        # except Exception as e:
        #     logging.error(f"Erro durante a coleta de preços da Universal: {e}")
        
        return 
if __name__ == "__main__":
    # Crie um loop de eventos e execute a função principal
    asyncio.run(main_tio())
