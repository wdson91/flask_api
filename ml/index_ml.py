from imports import *
from junta_dados import juntarjsons

from ml.ml_universal.ml_universal import coletar_precos_ml_universal
from ml.mldisney.ml_disney import coletar_precos_ml_disney
from ml.mlsea.mlsea import coletar_precos_ml_seaworld




async def main_ml(hour,array_datas,run_once=False):
    if run_once:
        logging.info("Iniciando coleta de preços.")
        global calibragem
        
        try:
            # Execute as funções assíncronas em sequência
            await coletar_precos_ml_disney(hour,array_datas)
            calibragem = 90
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços da Disney: {e}")

        try:
            await coletar_precos_ml_seaworld(hour,array_datas)
            calibragem = 95
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços do SeaWorld: {e}")

        try:
            await coletar_precos_ml_universal(hour,array_datas)
            calibragem = 97
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços da Universal: {e}")
            
        try:
            await juntarjsons(hour)
            calibragem = 100
        except Exception as e:
            logging.error(f"Erro durante a junção dos arquivos: {e}")
        return 
if __name__ == "__main__":
    # Crie um loop de eventos e execute a função principal
    asyncio.run(main_ml())
