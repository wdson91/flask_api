from imports import *
from webdriver_setup import get_webdriver

async def euro_price(driver):
    driver.get('https://www.google.com/search?client=firefox-b-d&q=euro')
    
    preco_euro = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]'))
    )
    preco_euro = preco_euro.text.replace(',', '.')
    return float(preco_euro)

async def coletar_precos_gyg_paris(hora_global, array_datas,data_atual):
    
    array_datas = [5,10,20,47,65,126]
    
    df1 = await coletar_precos_gyg_paris_1(hora_global, array_datas,data_atual)
    df2 = await coletar_precos_gyg_paris_2(hora_global, array_datas,data_atual)
    
    df = pd.DataFrame(df1 + df2)
    
    # Exibir o DataFrame mesclado
    df = df.drop_duplicates()
    df = df.sort_values(by=['Data_viagem', 'Parque'])
    
    # Salvar como JSON
    nome_arquivo = f'paris_gyg_{data_atual}.json'
    # Fechar o navegador

    salvar_dados(df, nome_arquivo, 'paris/gyg', hora_global)

async def coletar_precos_gyg_paris_1(hora_global, array_datas,data_atual):
    # Configurações do WebDriver Selenium
    options = webdriver.ChromeOptions()
    driver = get_webdriver()

    dados = []
    wait = WebDriverWait(driver, 5)
    # Lista de datas a serem verificadas
    array_datas = [datetime.now() + timedelta(days=d) for d in array_datas]
    euro = await euro_price(driver)
    # URL base
    url_base = "https://www.getyourguide.com/paris-l16/ingresso-disneyland-paris-1-dia-t395320?ranking_uuid=b6fc42b6-5c35-40dd-bf4a-0a9347d93925&date_from={}&_pc=1,1"

    try:
        for data in array_datas:
            data_formatada = data.strftime("%Y-%m-%d")
            # Construir a URL completa
            url = url_base.format(data_formatada)
            driver.get(url)


            # Pares de XPaths para botões e elementos de preço correspondentes
            xpath_pairs = [
                ('//*[@id="booking-assistant"]/div[2]/div/details[1]/summary/div[1]/h1', '//*[@id="booking-assistant"]/div[2]/div/details[1]/summary/section[2]/div/div[1]/span[2]'),
                ('//*[@id="booking-assistant"]/div[2]/div/details[2]/summary/div[1]/h1', '//*[@id="booking-assistant"]/div[2]/div/details[2]/summary/section/div/div[1]/span[2]')
            ]
            time.sleep(2)
            botao_disponibilidade = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="booking-assistant"]/div[1]/button'))
                )
            botao_disponibilidade.click()
            
            time.sleep(2)
            for title_xpath, price_xpath in xpath_pairs:
                try:
                    title_element = wait.until(EC.visibility_of_element_located((By.XPATH, title_xpath)))
                    price_element = wait.until(EC.visibility_of_element_located((By.XPATH, price_xpath)))
                    title = title_element.text
                    price = price_element.text.replace('€ ', '').replace(',', '.')
                    price = float(price) * euro
                    price = round(price, 2)
                    # Mapeamento condicional dos nomes dos parques
                    if '1 dia/1 parque' in title:
                        title = '1 Dia 1 Parque - Disney Paris'
                    elif '1 dia/2 parques' in title:
                        title = '1 Dia 2 Parques - Disney Paris'
                        
                    dados.append({
                        'Data_viagem': data_formatada,
                        'Parque': title,
                        'Preco_Parcelado': price,
                        'Preco_Avista': price
                    })
                except TimeoutException as e:
                    print(f"TimeoutException: Elemento não encontrado ou tempo de espera excedido: {e}")
    finally:
        
        driver.quit()
        return dados

async def coletar_precos_gyg_paris_2(hora_global, array_datas,data_atual):
    # Configurações do WebDriver Selenium
    options = webdriver.ChromeOptions()
    driver = get_webdriver()

    dados = []
    wait = WebDriverWait(driver, 5)
    # Lista de datas a serem verificadas
    array_datas = [datetime.now() + timedelta(days=d) for d in array_datas]
    euro = await euro_price(driver)
    # URL base
    url_base = "https://www.getyourguide.com/paris-l16/ingresso-disneyland-paris-para-multiplos-dias-t395319?ranking_uuid=b6fc42b6-5c35-40dd-bf4a-0a9347d93925&date_from={}&_pc=1,1"

    try:
        for data in array_datas:
            data_formatada = data.strftime("%Y-%m-%d")
            # Construir a URL completa
            url = url_base.format(data_formatada)
            driver.get(url)


            # Pares de XPaths para botões e elementos de preço correspondentes
            xpath_pairs = [
                ('//*[@id="booking-assistant"]/div[2]/div/details[1]/summary/div[1]/h1', '//*[@id="booking-assistant"]/div[2]/div/details[1]/summary/section[2]/div/div[1]/span[2]'),
                ('//*[@id="booking-assistant"]/div[2]/div/details[2]/summary/div[1]/h1', '//*[@id="booking-assistant"]/div[2]/div/details[2]/summary/section/div/div[1]/span[2]'),
                ('//*[@id="booking-assistant"]/div[2]/div/details[3]/summary/div[1]/h1', '//*[@id="booking-assistant"]/div[2]/div/details[3]/summary/section/div/div[1]/span[2]')
            ]
            time.sleep(2)
            botao_disponibilidade = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="booking-assistant"]/div[1]/button'))
                )
            botao_disponibilidade.click()
            
            time.sleep(2)
            for title_xpath, price_xpath in xpath_pairs:
                try:
                    title_element = wait.until(EC.visibility_of_element_located((By.XPATH, title_xpath)))
                    price_element = wait.until(EC.visibility_of_element_located((By.XPATH, price_xpath)))
                    title = title_element.text
                    price = price_element.text.replace('€ ', '').replace(',', '.')
                    price = float(price) * euro
                    price = round(price, 2)
                    
                    # Mapeamento condicional dos nomes dos parques
                    if '2 dias/2 parques' in title:
                        title = '2 Dias 2 Parques - Disney Paris'
                    elif '3 dias/2 parques ' in title:
                        title = '3 Dias 2 Parques - Disney Paris'
                    elif '4 dias/2 parques' in title:
                        title = '4 Dias 2 Parques - Disney Paris'
                    
                        
                    dados.append({
                        'Data_viagem': data_formatada,
                        'Parque': title,
                        'Preco_Parcelado': price,
                        'Preco_Avista':  price
                    })
                except TimeoutException as e:
                    print(f"TimeoutException: Elemento não encontrado ou tempo de espera excedido: {e}")
    finally:
        
        driver.quit()
        return dados
if __name__ == '__main__':
    array_datas = [5]
    hora_global = datetime.now(pytz.timezone('America/Sao_Paulo'))
    asyncio.run(coletar_precos_gyg_paris(hora_global,array_datas,'2024-03-25')) 