from imports import *
from webdriver_setup import get_webdriver




# Function to calculate future dates
def get_future_date(days):
    return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

async def coletar_precos_ml_california(hora_global, array_datas,data_atual):
    # Configurações do WebDriver Selenium
    driver = get_webdriver()
    dados = []
    wait = WebDriverWait(driver, 5)
    logging.info("Iniciando a coleta de preços ML California")
    try:
        for days in array_datas:
            future_date = get_future_date(days)
            url = f"https://www.vamonessa.com.br/ingressos/Entrada%20para%20o%20Disneyland%20Resort/E-U10-DISNEY1PAK?destination=Los+Angeles&destinationCode=123&destinationState=California&destinationStateCode=47&date={future_date}&provider=0&provider=2"
            driver.get(url)
            await asyncio.sleep(3)  # Aguardar o carregamento da página
            logging.info(f"Coletando preços para {future_date}")

            # Pares de XPaths para botões e elementos de preço correspondentes
            xpath_pairs = [
                # ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[1]/div[2]/div[1]/button', 
                #  '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span',
                #  '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/span',
                #  '1 Dia - Disney California'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[1]/div[2]/div[1]/button', 
                 '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span',
                 '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/span',
                 '2 Dias - Disney California'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[2]/div[2]/div[1]/button', 
                 '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span',
                 '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/span',
                 '3 Dias - Disney California'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[3]/div[2]/div[1]/button',
                 '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span',
                 '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/div[1]/span',
                '4 Dias - Disney California'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[4]/div[2]/div[1]/button',
                 '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[4]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span',
                 '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[4]/div[2]/div[2]/div[2]/div[1]/div[1]/span',
                '5 Dias - Disney California'),
                # Adicionar outros pares conforme necessário
            ]
            
            for button_xpath, price_xpath, cash_price_xpath, park_name in xpath_pairs:
                try:
                    button = wait.until(EC.presence_of_element_located((By.XPATH, button_xpath)))
                    driver.execute_script("arguments[0].scrollIntoView();", button)
                    await asyncio.sleep(2)  # Permitir tempo para quaisquer elementos carregados preguiçosos
                    #button.click()
                except TimeoutException:
                    print("Timeout ao esperar pelo botão:", button_xpath)
                    continue
                except ElementClickInterceptedException:
                    print("Clique interceptado para o botão:", button_xpath)
                    continue
                
                try:
                    price_element = wait.until(EC.presence_of_element_located((By.XPATH, price_xpath)))
                    cash_price_element = wait.until(EC.presence_of_element_located((By.XPATH, cash_price_xpath)))
                    
                    driver.execute_script("arguments[0].scrollIntoView();", price_element)
                    
                    price_text = price_element.text
                    cash_price_text = cash_price_element.text
                    
                except TimeoutException:
                    price_text = '-'
                    cash_price_text = '-'

                
                if "R$" in price_text:
                    try:
                        price_number_str = price_text.replace("R$", "").replace(",", ".").strip()
                        price_number = float(price_number_str)
                        multiplied_price = price_number * 10
                    
                        cash_price_number_str = cash_price_text.replace("R$", "").replace(".","").replace(",", ".").strip()
                        cash_price_number = float(cash_price_number_str)
                        
                    except ValueError:
                        print(f"Erro ao converter preço para {park_name}: {price_text}")

                #Adicionando dados
                data_hora_atual = datetime.now()
                
                dados.append({
                    'Data_viagem': (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d"),
                    'Parque': park_name,
                    'Preco_Parcelado': float(multiplied_price),
                    'Preco_Avista': cash_price_number
                })
                
    except TimeoutException as e:
            print("Erro: Elemento não encontrado ou tempo de espera excedido", e)    
    finally:
        driver.quit()
        df = pd.DataFrame(dados)
        nome_arquivo = f'california_ml_{data_atual}.json'
        
        salvar_dados(df, nome_arquivo, 'california/ml', hora_global)
        logging.info("Coleta de preços ML California concluída")
        #atualizar_calibragem(85)
        
if __name__ == '__main__':
    array_datas = [5,10,20,47,65,126]
    hora_global = datetime.now(pytz.timezone('America/Sao_Paulo'))
    asyncio.run(coletar_precos_ml_california(hora_global,array_datas,'2024-03-25')) 