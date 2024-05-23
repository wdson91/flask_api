from imports import *
from salvardados import *
from helpers.atualizar_calibragem import atualizar_calibragem





async def coletar_precos_vmz_halloween(hour,array_datas,data_atual):
    logging.info("Iniciando coleta de preços do Vmz halloween.")
    
    # Configuração inicial do Selenium
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    #driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options)
    #driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub', options=options)
    # Lista de sites e nomes de parques
    sites = [
        ("https://www.vmzviagens.com.br/ingressos/orlando/universal-halloween-horror-nights/universal-halloween-horror-nights?data=", 'Universal Halloween Horror Nights'),
        ("https://www.vmzviagens.com.br/ingressos/orlando/mickeys-not-so-scary-halloween-party/disney-mickeys-not-so-scary-halloween-party?data=","Mickey’s Not–So–Scary Halloween")
        
    ]

    datas = [f'2024-08-30',f'2024-09-06',f'2024-09-22',f'2024-10-04',f'2024-10-11',f'2024-10-31']
    
        # Definindo as datas
        #datas = [datetime.now().date() + timedelta(days=d) for d in array_datas]
        
        # Lista para armazenar os dados
    dados = []
    try:
        for url, parque in sites:    
            for data in datas:
                #for url, parque in sites:
                    logging.info(f"Coletando precos do parque")

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
                        'Data_viagem': data,
                        'Parque': parque,
                        'Preco_Parcelado': preco_float,
                        'Preco_Avista': preco_final_avista
                    })
            # Criando um DataFrame
        df = pd.DataFrame(dados)
            
        nome_arquivo = f'halloween_vmz_{data_atual}.json'
        salvar_dados(df, nome_arquivo,'halloween/vmz',hour)
            
        logging.info("Coleta finalizada Site Vmz - halloween")
        
    finally:
        driver.quit()
        #atualizar_calibragem(70)
        return
        
    
if __name__ == "__main__":
    asyncio.run(coletar_precos_vmz_halloween())
