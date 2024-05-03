# Importando os módulos necessários
from imports import *
from outros_parques.discovery_cove.ml_cove import coletar_precos_ml_cove
from outros_parques.discovery_cove.vmz_cove import coletar_precos_vmz_cove
from outros_parques.discovery_cove.voupra_cove import coletar_precos_voupra_cove


array_datas =  [5,10,20,47,65,126]

async def coleta_cove(hour, array_datas, data_atual):
    try:
        await coletar_precos_voupra_cove(hour, array_datas,data_atual)  # Executa a função main_voupra com o argumento hour
        logging.info("main_voupra concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar main_voupra: {e}")  # Registra uma mensagem de log de erro
    
    
    try:
        await coletar_precos_ml_cove(hour,array_datas,data_atual)  # Executa a função main_vmz com o argumento hour
        logging.info("main_vmz concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar main_vmz: {e}")  # Registra uma mensagem de log de erro
    
    try:
        await coletar_precos_vmz_cove(hour, array_datas, data_atual)  # Executa a função main_ml com o argumento hour
        logging.info("main_ml concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar main_ml: {e}")  # Registra uma mensagem de log de erro
    
    return
# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    asyncio.run(coleta_cove(hora_global,array_datas,'2024-03-25'))  # Executa a função principal 'main' usando asyncio
