# Importando os módulos necessários
from imports import *
from outros_parques.nasa.ml_nasa import coletar_precos_ml_nasa
from outros_parques.nasa.vmz_nasa import coletar_precos_vmz_nasa
from outros_parques.nasa.voupra_nasa import coletar_precos_voupra_nasa



array_datas =  [5,10,20,47,65,126]

async def coleta_nasa(hour, array_datas, data_atual):
    try:
        await coletar_precos_voupra_nasa(hour, array_datas,data_atual)  # Executa a função coletar_precos_voupra_nasa com o argumento hour
        logging.info("coletar_precos_voupra_nasa concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar coletar_precos_voupra_nasa: {e}")  # Registra uma mensagem de log de erro
    
    
    try:
        await coletar_precos_ml_nasa(hour,array_datas,data_atual)  # Executa a função coletar_precos_ml_nasacom o argumento hour
        logging.info("coletar_precos_ml_nasa concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar coletar_precos_ml_nasa: {e}")  # Registra uma mensagem de log de erro
    
    try:
        await coletar_precos_vmz_nasa(hour, array_datas, data_atual)  # Executa a função coleta coletar_precos_vmz_nasacom o argumento hour
        logging.info("coleta coletar_precos_vmz_nasa concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar coletar_precos_vmz_nasa: {e}")  # Registra uma mensagem de log de erro
    
    return
# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    asyncio.run(coleta_nasa(hora_global,array_datas,'2024-03-25'))  # Executa a função principal 'main' usando asyncio
