from imports import *
from vmz.vmzdisney.vmz_disney import coletar_precos_vmz_disneybasicos, coletar_precos_vmz_disneydias

#from .vmzdisney.teste import coletar_precos_vmz

dias_para_processar = [2,3,4,5]
async def main_parques(hour,array_datas,data_atual):

        global calibragem
        logging.info("Iniciando coleta de preços Vmz Disney.")
        try:
            await coletar_precos_vmz_disneybasicos(array_datas,hour,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços da Disney: {e}")
        try:
            # Execute as funções assíncronas em sequência
            await coletar_precos_voupra_disney(hour, array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços Disney: {e}")
        try:
            await coletar_precos_voupra_sea(hour, array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços SeaWorld: {e}")
            
        try:
            await coletar_precos_voupra_universal(hour, array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços Universal: {e}")
        try:
            await coletar_precos_vmz_seaworld(hour,array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços do SeaWorld: {e}")
        try:
            await coletar_precos_vmz_universal(hour,array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços da Universal: {e}")
        try:
            # Execute as funções assíncronas em sequência
            await coletar_precos_ml_disney(hour,array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços da Disney: {e}")

        try:
            await coletar_precos_ml_seaworld(hour,array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços do SeaWorld: {e}")

        try:
            await coletar_precos_ml_universal(hour,array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços da Universal: {e}")
        
        return

if __name__ == "__main__":
    # Crie um loop de eventos e execute a função principal
    asyncio.run(main_parques())
