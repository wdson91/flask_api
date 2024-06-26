from imports import *



from classes.junta_dados_classe import JuntarJsons
from ml.orlando.mldisney.ml_disney import coletar_precos_ml_disney
from ml.orlando.mlsea.mlsea import coletar_precos_ml_seaworld
from ml.orlando.ml_universal.ml_universal import coletar_precos_ml_universal

async def main_ml(hour,array_datas,data_atual):
    
        logging.info("Iniciando coleta de preços.")
        
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
    asyncio.run(main_ml())
