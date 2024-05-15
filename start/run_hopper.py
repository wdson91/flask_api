# Importando os módulos necessários
from classes.junta_dados_classe import JuntarJsons
from imports import *
from outros_parques.hopper.ml_hopper import coletar_precos_ml_hopper
from outros_parques.hopper.vmz_disney_hopper import coletar_precos_vmz_hopper, coletar_precos_vmz_hopper_basicos, coletar_precos_vmz_hopper_disneydias
from outros_parques.hopper.vmz_disney_hopper_plus import coletar_precos_vmz_disneydias_hopperplus, coletar_precos_vmz_hopper_plus, coletar_precos_vmz_hopperplus_basicos
from outros_parques.hopper.voupra_hopper import coletar_precos_voupra_hopper



array_datas =  [5,10,20,47,65,126]

async def executar_hopper(hour, array_datas, data_atual):
    
    try:
        await coletar_precos_ml_hopper(hour, array_datas, data_atual)  # Executa a função main_voupra com o argumento hour
        logging.info("main_voupra concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar main_voupra: {e}")  # Registra uma mensagem de log de erro
    
    try:
        await coletar_precos_vmz_disneydias_hopperplus(hour, array_datas, data_atual)  # Executa a função main_vmz com o argumento hour
        logging.info("main_vmz concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar main_vmz: {e}")  # Registra uma mensagem de log de erro
    
    try:
        await coletar_precos_vmz_hopperplus_basicos(hour, array_datas, data_atual)  # Executa a função main_ml com o argumento hour
        logging.info("main_ml concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar main_ml: {e}")  # Registra uma mensagem de log de erro

    try:
        await coletar_precos_vmz_hopper_plus(hour, array_datas, data_atual)
        logging.info("main_ml concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar main_ml: {e}")
    try:
        await coletar_precos_vmz_hopper_disneydias(hour, array_datas, data_atual)  # Executa a função main_vmz com o argumento hour
        logging.info("main_vmz concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar main_vmz: {e}")  # Registra uma mensagem de log de erro
    
    try:
        await coletar_precos_vmz_hopper_basicos(hour, array_datas, data_atual)  # Executa a função main_ml com o argumento hour
        logging.info("main_ml concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar main_ml: {e}")  # Registra uma mensagem de log de erro

    try:
        await coletar_precos_vmz_hopper(hour, array_datas, data_atual)
        logging.info("main_ml concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar main_ml: {e}")    
    try:
        await coletar_precos_voupra_hopper(hour, array_datas, data_atual)
        logging.info("main_ml concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar main_ml: {e}")
    
    # try:
    #         empresas = ['voupra', 'vmz', 'decolar','ml']
    #         parques = ['hopper','hopperplus']
            
    #         juntar_json = JuntarJsons(data_atual, empresas, parques, 'hopper')
            
    #         await juntar_json.executar()
              
    # except Exception as e:
    #         logging.error(f"Erro durante a junção dos arquivos: {e}")

# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    asyncio.run(coleta_hopper_aquaticos(hora_global,array_datas,'2024-03-25'))  # Executa a função principal 'main' usando asyncio
