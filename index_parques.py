from imports import *
from tioorlando.sea_tio import coleta_tio_sea
from tioorlando.universal_tio import coleta_tio_universal
from vmz.vmzdisney.vmz_disney import coletar_precos_vmz_disneybasicos, coletar_precos_vmz_disneydias
from classes.junta_dados_classe import JuntarJsons
#from .vmzdisney.teste import coletar_precos_vmz

dias_para_processar = [2,3,4,5]
async def main_parques(hour,array_datas,data_atual):

        global calibragem
        
        try:
            await coletar_precos_vmz_disneybasicos(array_datas,hour,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços da Disney: {e}")
        
        try:
            # Execute as funções assíncronas em sequência
            await coletar_precos_voupra_disney(hour, array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços Disney: {e}")
            
        try:
            await coletar_precos_voupra_sea(hour, array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços SeaWorld: {e}")
        
        try:
            await coletar_precos_voupra_universal(hour, array_datas,data_atual)
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços Universal: {e}")
            
        try:
            await coletar_precos_vmz_seaworld(hour,array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços do SeaWorld: {e}")
            
        try:
            await coletar_precos_vmz_universal(hour,array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços da Universal: {e}")

        
        
        
        return

async def main_parques2(hour,array_datas,data_atual):

        global calibragem
        try:
            await coleta_tio_universal(hour,array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços do Tio Orlando Universal: {e}")
            

        try:
            await coleta_tio_sea(hour,array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços do Tio Orlando Seaworld: {e}")
        
        
        return

async def main_parques3(hour,array_datas,data_atual):

        global calibragem
        
        
        try:
            # Execute as funções assíncronas em sequência
            await coletar_precos_ml_disney(hour,array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços da Disney: {e}")

        
        try:
            await coletar_precos_ml_seaworld(hour,array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços do SeaWorld: {e}")

        
        try:
            await coletar_precos_ml_universal(hour,array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços da Universal: {e}")
        
        
        
        return



async def juntar(data_atual):
        try:
            empresas = ['voupra', 'vmz', 'decolar','ml','tio','fastPass']
            parques = ['disney', 'universal', 'seaworld']
            
            juntar_json = JuntarJsons(data_atual, empresas, parques, 'orlando')
            
            await juntar_json.executar()
        except Exception as e:
                logging.error(f"Erro durante a junção dos arquivos: {e}")
                
                
                
if __name__ == "__main__":
    # Crie um loop de eventos e execute a função principal
    asyncio.run(main_parques())
