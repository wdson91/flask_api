from imports import *
from salvardados import *
from helpers.atualizar_calibragem import atualizar_calibragem





async def coletar_precos_vmz_lego(hour,array_datas,data_atual):
    logging.info("Iniciando coleta de preços do Vmz lego.")
    
    # Configuração inicial do Selenium
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    #driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options)
    #driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub', options=options)
    # Lista de sites e nomes de parques
    sites = [
        ("https://www.vmzviagens.com.br/ingressos/orlando/legoland-florida/legoland-florida?data=", '1 Dia - Legoland Florida'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/legoland-florida/legoland-florida-1-dia-parque-aquatico?data=", '1 Dia - Legoland Florida com Parque Aquático'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/legoland-florida/peppa-piglegoland-1-dia?data=", '1 Dia - Peppa Pig Theme Park e Legoland'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/legoland-florida/legoland-florida-2-dias?data=", '2 Dias - Legoland Florida'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/legoland-florida/legoland-florida-2-dias-parque-aquatico?data=", '2 Dias - Legoland Florida com Parque Aquático'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/legoland-florida/peppa-piglegoland-2-dias?data=", '2 Dias - Peppa Pig Theme Park e Legoland'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/legoland-florida/peppa-piglegolandwater-park-2-dias?data=", '2 Dias - Peppa Pig Theme Park e Legoland com Parque Aquático'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/legoland-florida/peppa-piglegolandwater-park-3-dias?data=", '3 Dias - Peppa Pig Theme Park e Legoland com Parque Aquático')
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
                    preco_parcelado_element = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/b')
                    preco_avista_element = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/span[1]')

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
        
        nome_arquivo = f'lego_vmz_{data_atual}.json'
        salvar_dados(df, nome_arquivo,'outros/lego',hour)
        
        logging.info("Coleta finalizada Site Vmz - lego")
        
    finally:
        driver.quit()
        #atualizar_calibragem(70)
        return
        
    
if __name__ == "__main__":
    asyncio.run(coletar_precos_vmz_lego())
