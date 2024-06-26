from classes.junta_dados_classe import JuntarJsons
from imports import *
from coleta_orlando import juntar


from .vmzdisney.vmz_disney import coletar_precos_vmz, coletar_precos_vmz_disneybasicos, coletar_precos_vmz_disneydias
from .vmzsea.vmzsea import coletar_precos_vmz_seaworld
from .vmzuniversal.vmzuniversal import coletar_precos_vmz_universal
#from .vmzdisney.teste import coletar_precos_vmz

dias_para_processar = [2,3,4,5]
async def main_vmz(hora_globa,array_datas,data_atual):

        global calibragem
        logging.info("Iniciando coleta de preços Vmz Disney.")
        # try:
        #     await coletar_precos_vmz_disneybasicos(array_datas,hora_globa,data_atual)
            
        # except Exception as e:
        #     logging.error(f"Erro durante a coleta de preços da Disney: {e}")

        try: 
            await coletar_precos_vmz_disneydias(dias_para_processar,array_datas,hora_globa,data_atual)
            #await coletar_precos_vmz(hora_globa,array_datas,data_atual)
        except Exception as e:
            logging.error(f"Erro durante a coleta de preços da Disney: {e}")
        
        # try:
        #     await coletar_precos_vmz(hora_globa,array_datas,data_atual)
            
        # except Exception as e:
        #     logging.error(f"Erro durante a coleta de preços da Disney: {e}")
        # try:
        #     await coletar_precos_vmz_seaworld(hora_globa,array_datas,data_atual)
            
        # except Exception as e:
        #     logging.error(f"Erro durante a coleta de preços do SeaWorld: {e}")
        # try:
        #     await coletar_precos_vmz_universal(hora_globa,array_datas,data_atual)
            
        # except Exception as e:
        #     logging.error(f"Erro durante a coleta de preços da Universal: {e}")
        try:
            empresas = ['voupra', 'vmz', 'decolar','ml','tio','fastPass']
            parques = ['disney', 'universal', 'seaworld']
            
            juntar_json = JuntarJsons(data_atual, empresas, parques, 'orlando')
            
            await juntar_json.executar()
        
        except Exception as e:
                logging.error(f"Erro durante a junção dos arquivos: {e}")
 
        return

if __name__ == "__main__":
    # Crie um loop de eventos e execute a função principal
    asyncio.run(main_vmz())
