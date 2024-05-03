# Importando os módulos necessários
from imports import *
from junta_dados_furafila import juntarjsons_furafila

from outros_parques.fura_fila.ml.ml import coletar_precos_ml_fura_fila
from outros_parques.fura_fila.voupra.voupra_furafila import coletar_precos_voupra_fura_fila

array_datas =  [5,10,20,47,65,126]

async def coleta_furafila(hour, array_datas, data_atual):
    try:
        await coletar_precos_voupra_fura_fila(hour, array_datas,data_atual)  # Executa a função main_voupra com o argumento hour
        logging.info("main_voupra concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar main_voupra: {e}")  # Registra uma mensagem de log de erro
    
    try:
        await coletar_precos_ml_fura_fila(hour,array_datas,data_atual)  # Executa a função main_vmz com o argumento hour
        logging.info("main_vmz concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar main_vmz: {e}")  # Registra uma mensagem de log de erro
    
    # try:
    #     await juntarjsons_outros_parques(hour, data_atual)  # Executa a função main_ml com o argumento hour
    #     logging.info("main_ml concluída.")  # Registra uma mensagem de log
    # except Exception as e:
        #logging.error(f"Erro ao executar main_ml: {e}")  # Registra uma mensagem de log de erro

    return  
# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    asyncio.run(executar_ambos_teste(hora_global,array_datas,'2024-03-25'))  # Executa a função principal 'main' usando asyncio
