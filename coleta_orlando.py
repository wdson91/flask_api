from imports import *
from tioorlando.sea_tio import coleta_tio_sea
from tioorlando.universal_tio import coleta_tio_universal
from vmz.vmzdisney.vmz_disney import coletar_precos_vmz_disneybasicos, coletar_precos_vmz_disneydias
from classes.junta_dados_classe import JuntarJsons
#from .vmzdisney.teste import coletar_precos_vmz

dias_para_processar = [2,3,4,5]

async def bloco01(hora_global,array_datas,data_atual):

        try:
            await coletar_precos_vmz_disneybasicos(array_datas,hora_global,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços da Disney: {e}")
        try:
            await coletar_precos_vmz_universal(hora_global,array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços da Universal: {e}")
        
        try:
            # Execute as funções assíncronas em sequência
            await coletar_precos_voupra_disney(hora_global, array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços Disney: {e}")
            
        try:
            await coletar_precos_voupra_sea(hora_global, array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços SeaWorld: {e}")
        
        try:
            await coletar_precos_voupra_universal(hora_global, array_datas,data_atual)
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços Universal: {e}")
            
        try:
            await coletar_precos_vmz_seaworld(hora_global,array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços do SeaWorld: {e}")
            
        return

async def bloco02(hora_global,array_datas,data_atual):

        try:
            await coleta_tio_universal(hora_global,array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços do Tio Orlando Universal: {e}")
            

        try:
            await coleta_tio_sea(hora_global,array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços do Tio Orlando Seaworld: {e}")
        
        
        return

async def bloco03(hora_global,array_datas,data_atual):

        try:
            # Execute as funções assíncronas em sequência
            await coletar_precos_ml_disney(hora_global,array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços da Disney: {e}")

        
        try:
            await coletar_precos_ml_seaworld(hora_global,array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços do SeaWorld: {e}")

        
        try:
            await coletar_precos_ml_universal(hora_global,array_datas,data_atual)
            
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços da Universal: {e}")
        
        
        
        return


async def juntar(data_atual):
        try:
            empresas = ['voupra', 'vmz', 'decolar','ml','tio','fastPass']
            parques = ['disney', 'universal', 'seaworld']
            
            juntar_json = JuntarJsons(data_atual, empresas, parques, 'orlando')
            
            await juntar_json.executar()
            return
        except Exception as e:
                logging.error(f"Erro durante a junção dos arquivos: {e}")
                
if __name__ == "__main__":
    # Crie um loop de eventos e execute a função principal
    asyncio.run(bloco01())
