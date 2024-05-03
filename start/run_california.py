# Importando os módulos necessários
from imports import *
from ml.california.ml_california import coletar_precos_ml_california
from rca.california.rca_california import coletar_precos_california_rca
from vmz.california.vmzcalifornia import coletar_precos_vmz_california
from voupra.california.voupracalifornia import coletar_precos_voupra_california


# Importa os módulos necessários, incluindo funções definidas em 'imports'


array_datas =  [5,10,20,47,65,126]

async def executar_california(hour, array_datas, data_atual):
    try:
        await coletar_precos_voupra_california(hour, array_datas, data_atual)  # Executa a função main_voupra com o argumento hour
        logging.info("voupra_california concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar voupra_california: {e}")  # Registra uma mensagem de log de erro
    try:
        await coletar_precos_vmz_california(hour, array_datas, data_atual)  # Executa a função main_ml_seaworld com o argumento hour
        logging.info("ml_california concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar ml_california: {e}")
    try:
        await coletar_precos_ml_california(hour, array_datas, data_atual)  # Executa a função main_ml_seaworld com o argumento hour
        logging.info("ml_california concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar ml_california: {e}")
    try:
        await coletar_precos_california_rca(hour, array_datas,data_atual)
        logging.info("rca_california concluída.")
    except Exception as e:
        logging.error(f"Erro ao executar rca_california: {e}")
    # try:
    #     await juntarjsons_california(hour, data_atual)  # Executa a função main_vmz com o argumento hour
    #     logging.info("juntarjsons_california concluída.")  # Registra uma mensagem de log
    # except Exception as e:
    #     logging.error(f"Erro ao executar juntarjsons_california: {e}")
        
# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    asyncio.run(executar_california('hora_global',array_datas,'2024-03-25'))  # Executa a função principal 'main' usando asyncio
