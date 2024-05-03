# Importando os módulos necessários
from imports import *
from outros_parques.legoland.ml_legoland import coletar_precos_ml_lego
from outros_parques.legoland.vmz_legoland import coletar_precos_vmz_lego
from outros_parques.legoland.voupra_legoland import coletar_precos_voupra_lego




array_datas =  [5,10,20,47,65,126]

async def coleta_lego(hour, array_datas, data_atual):
    try:
        await coletar_precos_voupra_lego(hour, array_datas,data_atual)  # Executa a função coletar_precos_voupra_lego com o argumento hour
        logging.info("coletar_precos_voupra_lego concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar coletar_precos_voupra_lego: {e}")  # Registra uma mensagem de log de erro
    
    
    try:
        await coletar_precos_ml_lego(hour,array_datas,data_atual)  # Executa a função coletar_precos_ml_legocom o argumento hour
        logging.info("coletar_precos_ml_lego concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar coletar_precos_ml_lego: {e}")  # Registra uma mensagem de log de erro
    
    try:
        await coletar_precos_vmz_lego(hour, array_datas, data_atual)  # Executa a função coleta coletar_precos_vmz_legocom o argumento hour
        logging.info("coleta coletar_precos_vmz_lego concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar coletar_precos_vmz_lego: {e}")  # Registra uma mensagem de log de erro
    
    return
# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    asyncio.run(coleta_lego(hora_global,array_datas,'2024-03-25'))  # Executa a função principal 'main' usando asyncio
