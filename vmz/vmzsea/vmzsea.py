from imports import *
from salvardados import *
from helpers.atualizar_calibragem import atualizar_calibragem
from webdriver_setup import get_webdriver





async def coletar_precos_vmz_seaworld(hora_global,array_datas,data_atual):
    logging.info("Iniciando coleta de preços Vmz Seaworld.")
    driver = get_webdriver()
    # Lista de sites e nomes de parques
    sites = [
        ("https://www.vmzviagens.com.br/ingressos/orlando/seaworld-orlando/seaworld-1-dia", '1 Dia 1 Parque - SeaWorld Orlando'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/seaworld-orlando/promocao-seaworld-busch-gardens-aquatica", '3 Dias 3 Parques - SeaWorld Orlando'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/seaworld-orlando/seaworld-14-dias-estacionamento", '14 Dias 3 Parques - SeaWorld Orlando'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/busch-gardens-tampa/busch-gardens-seaworld-aquatica-com-plano-alimentacao?data=2024-12-31", '3 Dias 3 Parques com Refeições - SeaWorld Orlando'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/busch-gardens-tampa/busch-gardens-1-dia?",'1 Dia 1 Parque - Busch Gardens'),
    ]

    
    try:
        # Definindo as datas
        datas = [datetime.now().date() + timedelta(days=d) for d in array_datas]

        # Lista para armazenar os dados
        dados = []

        for data in datas:
            for url, parque in sites:
                logging.info(f"Coletando precos do parque {parque} - Vmz Seaworld.")

                driver.get(url)

                
                try:
                    preco_parcelado_element = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div/div[1]/b')
                    preco_avista_element = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div/div[1]/span[1]')

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
        
        nome_arquivo = f'seaworld_vmz_{data_atual}.json'
        salvar_dados(df, nome_arquivo,'orlando/vmz',hora_global)
        
        logging.info("Coleta finalizada Site Vmz- SeaWorld")
        
    finally:
        driver.quit()
        atualizar_calibragem(70)
        return
        
    
if __name__ == "__main__":
    asyncio.run(coletar_precos_vmz_seaworld())
