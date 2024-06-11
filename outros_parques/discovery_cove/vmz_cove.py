from imports import *
from salvardados import *
from helpers.atualizar_calibragem import atualizar_calibragem
from webdriver_setup import get_webdriver





async def coletar_precos_vmz_cove(hour,array_datas,data_atual):
    logging.info("Iniciando coleta de preços do Discovery Cove Vmz.")
    
    driver = get_webdriver()
    # Lista de sites e nomes de parques
    sites = [
        ("https://www.vmzviagens.com.br/ingressos/orlando/discovery-cove-orlando/1-dia-de-discovery-cove-sem-nado?data=", '1 Dia Discovery Cove'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/discovery-cove-orlando/1-dia-de-discovery-cove-com-nado-com-golfinhos?data=", '1 Dia Discovery Cove com Nado com Golfinhos'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/discovery-cove-orlando/discovery-cove-package-sem-nado?data=", '1 Dia Discovery Cove + 14 Dias SeaWorld Orlando e Aquatica'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/discovery-cove-orlando/discovery-cove-ultimate-sem-nado?data=", '1 Dia Discovery Cove + 14 Dias SeaWorld, Busch Gardens, e Aquatica'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/discovery-cove-orlando/discovery-cove-package-com-nado-com-golfinhos?data=",'1 Dia Discovery Cove Com Nado com Golfinhos + 14 Dias SeaWorld Orlando e Aquatica'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/discovery-cove-orlando/discovery-cove-ultimate-com-nado-com-golfinhos?data=",'1 Dia Discovery Cove Com Nado com Golfinhos + 14 Dias SeaWorld, Busch Gardens e Aquatica'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/discovery-cove-orlando/seaventure-at-discovery-cove?data=",'SeaVenture - Passeio Subaquático no Discovery Cove')
    ]

    
    try:
        # Definindo as datas
        datas = [datetime.now().date() + timedelta(days=d) for d in array_datas]

        # Lista para armazenar os dados
        dados = []

        for data in datas:
            for url, parque in sites:
                logging.info(f"Coletando precos do parque {parque}.")

                driver.get(f'{url}{data}')
                
                
                try:
                    preco_parcelado_element = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[1]/b')
                    preco_avista_element = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[1]/span[1]')

                    # Multiplicar o preço parcelado por 10
                    preco_parcelado = preco_parcelado_element.text.replace('R$ ', '').replace(',', '.')
                    preco_float = float(preco_parcelado) * 10
                    #preco_final_parcelado = f"R$ {preco_float:    
                    
                    preco_final_avista = float(preco_avista_element.text.replace('R$ ', '').replace('.','').replace(',', '.'))
                    
                except NoSuchElementException:
                    
                    preco_final_avista = preco_float = "-"
                dados.append({
                    'Data_viagem': data.strftime("%Y-%m-%d"),
                    'Parque': parque,
                    'Preco_Parcelado': preco_float,
                    'Preco_Avista': preco_final_avista
                })
        # Criando um DataFrame
        df = pd.DataFrame(dados)
        
        nome_arquivo = f'discovery_cove_vmz_{data_atual}.json'
        salvar_dados(df, nome_arquivo,'outros/vmz',hour)
        
        logging.info("Coleta finalizada Site Vmz- Discovery Cove")
        
    finally:
        driver.quit()
        #atualizar_calibragem(70)
        return
        
    
if __name__ == "__main__":
    asyncio.run(coletar_precos_vmz_cove())
