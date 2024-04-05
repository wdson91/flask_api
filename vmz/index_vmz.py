from imports import *
from junta_dados import juntarjsons

from .vmzdisney.vmz_disney import coletar_precos_vmz, coletar_precos_vmz_disneybasicos, coletar_precos_vmz_disneydias
from .vmzsea.vmzsea import coletar_precos_vmz_seaworld
from .vmzuniversal.vmzuniversal import coletar_precos_vmz_universal
#from .vmzdisney.teste import coletar_precos_vmz

dias_para_processar = [2,3,4,5]
async def main_vmz(hour,array_datas,data_atual,run_once=False):
    if run_once:
        global calibragem
        
        logging.info("Iniciando coleta de preços.")
        try:
            await coletar_precos_vmz_seaworld(hour,array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços do SeaWorld: {e}")
        try:
            await coletar_precos_vmz_disneybasicos(array_datas,hour,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços da Disney: {e}")

        try: 
            await coletar_precos_vmz_disneydias(dias_para_processar,array_datas,hour,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços da Disney: {e}")
            
        try:
            await coletar_precos_vmz(hour,array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços da Disney: {e}")
            
        try:
            await coletar_precos_vmz_universal(hour,array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços da Universal: {e}")
        return

if __name__ == "__main__":
    # Crie um loop de eventos e execute a função principal
    asyncio.run(main_vmz())
