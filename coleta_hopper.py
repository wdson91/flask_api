from imports import *

from classes.junta_dados_classe import JuntarJsons
from outros_parques.hopper.ml_hopper import coletar_precos_ml_hopper
from outros_parques.hopper.vmz_disney_hopper import coletar_precos_vmz_hopper, coletar_precos_vmz_hopper_basicos, coletar_precos_vmz_hopper_disneydias
from outros_parques.hopper.vmz_disney_hopper_plus import coletar_precos_vmz_disneydias_hopperplus, coletar_precos_vmz_hopper_plus, coletar_precos_vmz_hopperplus_basicos
from outros_parques.hopper.voupra_hopper import coletar_precos_voupra_hopper
#from .vmzdisney.teste import coletar_precos_vmz

async def bloco01_hopper(hora_global,array_datas,data_atual):

    try:
        await coletar_precos_ml_hopper(hora_global, array_datas, data_atual)  # Executa a função main_voupra com o argumento hora_global
        logging.info("main_voupra concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar main_voupra: {e}")  # Registra uma mensagem de log de erro
        
    try:
        await coletar_precos_vmz_hopperplus_basicos(hora_global, array_datas, data_atual)  # Executa a função main_ml com o argumento hora_global
        logging.info("main_ml concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar main_ml: {e}")  # Registra uma mensagem de log de erro
    try:
        await coletar_precos_vmz_hopper_basicos(hora_global, array_datas, data_atual)  # Executa a função main_ml com o argumento hora_global
        logging.info("main_ml concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar main_ml: {e}")  # Registra uma mensagem de log de erro
    
    try:
        await coletar_precos_voupra_hopper(hora_global, array_datas, data_atual)
        logging.info("main_ml concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar main_ml: {e}")
        
    return

async def bloco02_hopper(hora_global,array_datas,data_atual):

        try:
            await coletar_precos_vmz_disneydias_hopperplus(hora_global, array_datas, data_atual)  # Executa a função main_vmz com o argumento hora_global
            logging.info("main_vmz concluída.")  # Registra uma mensagem de log
        except Exception as e:
            logging.error(f"Erro ao executar main_vmz: {e}")  # Registra uma mensagem de log de erro

        try:
            await coletar_precos_vmz_hopper_plus(hora_global, array_datas, data_atual)
            logging.info("main_ml concluída.")  # Registra uma mensagem de log
        except Exception as e:
            logging.error(f"Erro ao executar main_ml: {e}")
        
        
        return

async def bloco03_hopper(hora_global,array_datas,data_atual):

    try:
        await coletar_precos_vmz_hopper_disneydias(hora_global, array_datas, data_atual)  # Executa a função main_vmz com o argumento hora_global
        logging.info("main_vmz concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar main_vmz: {e}")  # Registra uma mensagem de log de erro
        
    try:
        await coletar_precos_vmz_hopper(hora_global, array_datas, data_atual)
        logging.info("main_ml concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar main_ml: {e}")    
    
    return


async def juntar(data_atual):
        try:
            empresas = ['voupra', 'vmz', 'decolar','ml']
            parques = ['hopper','hopperplus']
            
            juntar_json = JuntarJsons(data_atual, empresas, parques, 'hopper')
            
            await juntar_json.executar()
        
        except Exception as e:
            logging.error(f"Erro durante a junção dos arquivos: {e}")
                
if __name__ == "__main__":
    # Crie um loop de eventos e execute a função principal
    asyncio.run(bloco01())
