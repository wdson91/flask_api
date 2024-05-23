# Importando os módulos necessários


from classes.junta_dados_classe import JuntarJsons
from helpers.atualizar_calibragem import finalizar_halloween
from imports import *

from outros_parques.halloween.ml_halloween import coletar_precos_ml_halloween
from outros_parques.halloween.vmz_halloween import coletar_precos_vmz_halloween
from outros_parques.halloween.voupra_halloween import coletar_precos_voupra_halloween
from outros_parques.halloween_disnery.voupra_halloween_disney import coletar_precos_voupra_halloween_disney


# Importa os módulos necessários, incluindo funções definidas em 'imports'


array_datas =  [5,10,20,47,65,126]

async def executar_halloween(hour, array_datas, data_atual):
    try:
        await coletar_precos_ml_halloween(hour, array_datas, data_atual)  # Executa a função coleta coletar_precos_vmz_legocom o argumento hour
        logging.info("coleta coletar_precos_vmz_halloween concluída.")  # Registra uma mensagem de log
    except Exception as e:
         logging.error(f"Erro ao executar coletar_precos_vmz_halloween: {e}")  # Registra uma mensagem de log de erro
    try:
        await coletar_precos_vmz_halloween(hour, array_datas, data_atual)  # Executa a função coleta coletar_precos_vmz_halloweencom o argumento hour
        logging.info("coleta coletar_precos_vmz_halloween concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar coletar_precos_vmz_halloween: {e}")  # Registra uma mensagem de log de erro
    try:
        await coletar_precos_voupra_halloween(hour, array_datas, data_atual)  # Executa a função coleta coletar_precos_vmz_halloweencom o argumento hour
        logging.info("coleta coletar_precos_vmz_halloween concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar coletar_precos_vmz_halloween: {e}")  # Registra uma mensagem de log de erro
    
    
    await finalizar_halloween()
    
    # try:
    #         empresas = ['voupra', 'vmz', 'ml', 'decolar']
    #         parques = ['halloween','halloweenDisney']
            
    #         juntar_json = JuntarJsons(data_atual, empresas, parques, 'halloween')
            
    #         await juntar_json.executar()
    
    # except Exception as e:
    #         logging.error(f"Erro durante a junção dos arquivos: {e}")
    return
        
# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    asyncio.run(executar_halloween('hora_global',array_datas,'2024-03-25'))  # Executa a função principal 'main' usando asyncio
