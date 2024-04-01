# Importando os módulos necessários
from imports import *
from ml.index_ml import main_ml
from vmz.index_vmz import main_vmz
from voupra.orlando.index_voupra import main_voupra  # Importa os módulos necessários, incluindo funções definidas em 'imports'

array_datas =  [5,10,20,47,65,126]

async def executar_ambos(hour, array_datas, data_atual):
    try:
        await main_voupra(hour, array_datas, data_atual, run_once=True)  # Executa a função main_voupra com o argumento hour
        logging.info("main_voupra concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar main_voupra: {e}")  # Registra uma mensagem de log de erro
    
    try:
        await main_vmz(hour, array_datas, data_atual, run_once=True)  # Executa a função main_vmz com o argumento hour
        logging.info("main_vmz concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar main_vmz: {e}")  # Registra uma mensagem de log de erro
    
    try:
        await main_ml(hour, array_datas, data_atual, run_once=True)  # Executa a função main_ml com o argumento hour
        logging.info("main_ml concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar main_ml: {e}")  # Registra uma mensagem de log de erro


# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    asyncio.run(executar_ambos(hora_global,array_datas,'2024-03-25'))  # Executa a função principal 'main' usando asyncio
