from imports import *

from .voupradisney.voupradisney import coletar_precos_voupra_disney
from .vouprasea.vouprasea import coletar_precos_voupra_sea
from .vouprauniversal.vouprauniversal import coletar_precos_voupra_universal


async def main_voupra(hour,array_datas,data_atual,run_once=False):
    if run_once:
     
        
        logging.info("Iniciando coleta de preços Voupra Disney.")
        try:
            # Execute as funções assíncronas em sequência
            await coletar_precos_voupra_disney(hour, array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços Disney: {e}")

        logging.info("Iniciando coleta de preços Voupra Universal.")
        try:
            
            await coletar_precos_voupra_universal(hour, array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços Universal: {e}")

        logging.info("Iniciando coleta de preços Voupra SeaWorld.")
        try:
            await coletar_precos_voupra_sea(hour, array_datas,data_atual,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços SeaWorld: {e}")

        return 
    
if __name__ == "__main__":
    # Crie um loop de eventos e execute a função principal
    asyncio.run(main_voupra())
