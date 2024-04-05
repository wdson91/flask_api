# Importando os módulos necessários
from imports import *
from junta_dados_paris import juntarjsons_paris
from ml.paris.ml_paris import coletar_precos_ml_paris
from voupra.paris.voupraparis import coletar_precos_voupra_paris

# Importa os módulos necessários, incluindo funções definidas em 'imports'


array_datas =  [5,10,20,47,65,126]

async def executar_paris(hour, array_datas, data_atual):
    try:
        await coletar_precos_voupra_paris(hour, array_datas, data_atual)  # Executa a função main_voupra com o argumento hour
        logging.info("voupra_paris concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar voupra_paris: {e}")  # Registra uma mensagem de log de erro
    try:
        await coletar_precos_ml_paris(hour, array_datas, data_atual)  # Executa a função main_ml_seaworld com o argumento hour
        logging.info("ml_paris concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar ml_paris: {e}")
    # try:
    #     await juntarjsons_paris(hour, data_atual)  # Executa a função main_vmz com o argumento hour
    #     logging.info("juntarjsons_paris concluída.")  # Registra uma mensagem de log
    # except Exception as e:
    #     logging.error(f"Erro ao executar juntarjsons_paris: {e}")
        
# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    asyncio.run(executar_paris('hora_global',array_datas,'2024-03-25'))  # Executa a função principal 'main' usando asyncio
