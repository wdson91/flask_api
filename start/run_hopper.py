# Importando os módulos necessários
from classes.junta_dados_classe import JuntarJsons
from imports import *



array_datas =  [5,10,20,47,65,126]

async def coleta_hopper_aquaticos(hour, array_datas, data_atual):
    
    await coletar_precos_vmz_hopper(hour, array_datas, data_atual)
    # try:
    #     await main_voupra(hour, array_datas, data_atual, run_once=True)  # Executa a função main_voupra com o argumento hour
    #     logging.info("main_voupra concluída.")  # Registra uma mensagem de log
    # except Exception as e:
    #     logging.error(f"Erro ao executar main_voupra: {e}")  # Registra uma mensagem de log de erro
    
    # try:
    #     await main_vmz(hour, array_datas, data_atual, run_once=True)  # Executa a função main_vmz com o argumento hour
    #     logging.info("main_vmz concluída.")  # Registra uma mensagem de log
    # except Exception as e:
    #     logging.error(f"Erro ao executar main_vmz: {e}")  # Registra uma mensagem de log de erro
    
    # try:
    #     await main_ml(hour, array_datas, data_atual, run_once=True)  # Executa a função main_ml com o argumento hour
    #     logging.info("main_ml concluída.")  # Registra uma mensagem de log
    # except Exception as e:
    #     logging.error(f"Erro ao executar main_ml: {e}")  # Registra uma mensagem de log de erro

    # try:
    #         empresas = ['voupra', 'vmz', 'decolar','ml']
    #         parques = ['disney', 'universal', 'seaworld']
            
    #         juntar_json = JuntarJsons(data_atual, empresas, parques, 'orlando')
            
    #         await juntar_json.executar()
              
    # except Exception as e:
    #         logging.error(f"Erro durante a junção dos arquivos: {e}")

# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    asyncio.run(coleta_hopper_aquaticos(hora_global,array_datas,'2024-03-25'))  # Executa a função principal 'main' usando asyncio
