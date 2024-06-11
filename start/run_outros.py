# Importando os módulos necessários
from classes.junta_dados_classe import JuntarJsons
from imports import *
from junta_dados_furafila import juntarjsons_furafila
from outros_parques.discovery_cove.ml_cove import coletar_precos_ml_cove
from outros_parques.discovery_cove.vmz_cove import coletar_precos_vmz_cove
from outros_parques.discovery_cove.voupra_cove import coletar_precos_voupra_cove

from outros_parques.fura_fila.ml import coletar_precos_ml_fura_fila
from outros_parques.fura_fila.voupra_furafila import coletar_precos_voupra_fura_fila
from outros_parques.halloween.ml_halloween import coletar_precos_ml_halloween
from outros_parques.halloween.vmz_halloween import coletar_precos_vmz_halloween
from outros_parques.halloween.voupra_halloween import coletar_precos_voupra_halloween
from outros_parques.legoland.ml_legoland import coletar_precos_ml_lego
from outros_parques.legoland.vmz_legoland import coletar_precos_vmz_lego
from outros_parques.legoland.voupra_legoland import coletar_precos_voupra_lego
from outros_parques.nasa.ml_nasa import coletar_precos_ml_nasa
from outros_parques.nasa.vmz_nasa import coletar_precos_vmz_nasa
from outros_parques.nasa.voupra_nasa import coletar_precos_voupra_nasa



array_datas =  [5,10,20,47,65,126]

async def coleta_outros_parques(hora_global, array_datas, data_atual):
    
    try:
        await coletar_precos_voupra_nasa(hora_global, array_datas,data_atual)  # Executa a função coletar_precos_voupra_nasa com o argumento hora_global
        logging.info("coletar_precos_voupra_nasa concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar coletar_precos_voupra_nasa: {e}")  # Registra uma mensagem de log de erro
    
    try:
        await coletar_precos_ml_nasa(hora_global,array_datas,data_atual)  # Executa a função coletar_precos_ml_nasacom o argumento hora_global
        logging.info("coletar_precos_ml_nasa concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar coletar_precos_ml_nasa: {e}")  # Registra uma mensagem de log de erro
    
    try:
        await coletar_precos_vmz_nasa(hora_global, array_datas, data_atual)  # Executa a função coleta coletar_precos_vmz_nasacom o argumento hora_global
        logging.info("coleta coletar_precos_vmz_nasa concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar coletar_precos_vmz_nasa: {e}")  # Registra uma mensagem de log de erro
    
    try:
        await coletar_precos_voupra_cove(hora_global, array_datas,data_atual)  # Executa a função main_voupra com o argumento hora_global
        logging.info("main_voupra concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar main_voupra: {e}")  # Registra uma mensagem de log de erro
    
    try:
        await coletar_precos_ml_cove(hora_global,array_datas,data_atual)  # Executa a função main_vmz com o argumento hora_global
        logging.info("main_vmz concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar main_vmz: {e}")  # Registra uma mensagem de log de erro
    
    try:
        await coletar_precos_vmz_cove(hora_global, array_datas, data_atual)  # Executa a função main_ml com o argumento hora_global
        logging.info("main_ml concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar main_ml: {e}")  # Registra uma mensagem de log de erro
   
    try:
        await coletar_precos_voupra_lego(hora_global, array_datas,data_atual)  # Executa a função coletar_precos_voupra_lego com o argumento hora_global
        logging.info("coletar_precos_voupra_lego concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar coletar_precos_voupra_lego: {e}")  # Registra uma mensagem de log de erro
    
    try:
        await coletar_precos_ml_lego(hora_global,array_datas,data_atual)  # Executa a função coletar_precos_ml_legocom o argumento hora_global
        logging.info("coletar_precos_ml_lego concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar coletar_precos_ml_lego: {e}")  # Registra uma mensagem de log de erro
    
    try:
        await coletar_precos_vmz_lego(hora_global, array_datas, data_atual)  # Executa a função coleta coletar_precos_vmz_legocom o argumento hora_global
        logging.info("coleta coletar_precos_vmz_lego concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar coletar_precos_vmz_lego: {e}")  # Registra uma mensagem de log de erro
    try:
        await coletar_precos_voupra_fura_fila(hora_global, array_datas,data_atual)  # Executa a função main_voupra com o argumento hora_global
        logging.info("main_voupra concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar main_voupra: {e}")  # Registra uma mensagem de log de erro
    try:
        await coletar_precos_ml_fura_fila(hora_global,array_datas,data_atual)  # Executa a função main_vmz com o argumento hora_global
        logging.info("main_vmz concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar main_vmz: {e}")  # Registra uma mensagem de log de erro
    # try:
    #     await juntarjsons_furafila(hora_global,data_atual)
    #     logging.info("juntarjsons_furafila concluída.")  # Registra uma mensagem de log
    # except Exception as e:
    #     logging.error(f"Erro ao executar juntarjsons_furafila: {e}")
 
  
    return
# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    asyncio.run(coleta_outros(hora_global,array_datas,'2024-03-25'))  # Executa a função principal 'main' usando asyncio
