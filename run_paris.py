# Importando os módulos necessários
from imports import *
from voupra.paris.index_paris import main_voupra_paris


array_datas =  [5,10,20,47,65,126]

async def executar_paris(hour, array_datas, data_atual):
    try:
        await main_voupra_paris(hour, array_datas, data_atual, run_once=True)  # Executa a função main_voupra com o argumento hour
        logging.info("main_voupra concluída.")  # Registra uma mensagem de log
    except Exception as e:
        logging.error(f"Erro ao executar main_voupra: {e}")  # Registra uma mensagem de log de erro

# Verifica se o script está sendo executado diretamente
if __name__ == "__main__":
    asyncio.run(executar_paris(hora_global,array_datas,'2024-03-25'))  # Executa a função principal 'main' usando asyncio
