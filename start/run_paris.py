# Importando os módulos necessários

from civitatis.paris.civitatis_paris import coletar_precos_civitatis_paris

from get_your_guide.paris.get_your_guide_paris import coletar_precos_gyg_paris
from imports import *

from ml.paris.ml_paris import coletar_precos_ml_paris
from voupra.paris.voupraparis import coletar_precos_voupra_paris

# Importa os módulos necessários, incluindo funções definidas em 'imports'


array_datas =  [5,10,20,47,65,126]

async def executar_paris(hora_global, array_datas, data_atual):
    try:
        await coletar_precos_voupra_paris(hora_global, array_datas, data_atual)  # Executa a função main_voupra com o argumento hora_global
        logging.info("voupra_paris concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar voupra_paris: {e}")  # Registra uma mensagem de log de erro
    try:
        await coletar_precos_ml_paris(hora_global, array_datas, data_atual)  # Executa a função main_ml_seaworld com o argumento hora_global
        logging.info("ml_paris concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar ml_paris: {e}")
    try: 
        await coletar_precos_civitatis_paris(hora_global, array_datas, data_atual)
        logging.info("civitatis_paris concluída.")
    except Exception as e:
        logging.error(f"Erro ao executar civitatis_paris: {e}")
    try:
        await coletar_precos_gyg_paris(hora_global, array_datas, data_atual)  # Executa a função main_gyg com o argumento hora_global
        logging.info("gyr_paris concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar gyr_paris: {e}")
    return
        
# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    asyncio.run(executar_paris('hora_global',array_datas,'2024-03-25'))  # Executa a função principal 'main' usando asyncio
