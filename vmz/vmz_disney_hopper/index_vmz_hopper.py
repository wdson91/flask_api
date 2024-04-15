from imports import *

from vmz.vmz_disney_hopper.vmz_disney_hopper_plus import coletar_precos_vmz_disneydias_hopperplus, coletar_precos_vmz_hopper_plus, coletar_precos_vmz_hopperplus_basicos




#from .vmzdisney.teste import coletar_precos_vmz

dias_para_processar = [2,3,4,5]
async def main_vmz_hopper(hour,array_datas,data_atual,run_once=False):
    if run_once:
        global calibragem
        
        logging.info("Iniciando coleta de preços.")
        try:
            await coletar_precos_vmz_hopperplus_basicos(hour,array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços do SeaWorld: {e}")
        try:
            await coletar_precos_vmz_disneydias_hopperplus(array_datas,hour,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços da Disney: {e}")

        try: 
            await coletar_precos_vmz_hopper_plus(dias_para_processar,array_datas,hour,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços da Disney: {e}")
            
      
        return

if __name__ == "__main__":
    # Crie um loop de eventos e execute a função principal
    asyncio.run(main_vmz_hopper('hora_global',array_datas,'2024-03-25'))
