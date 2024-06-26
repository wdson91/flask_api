
from imports import *


from helpers.atualizar_calibragem import atualizar_calibragem
from webdriver_setup import get_webdriver

# Function to calculate future dates
def get_future_date(days):
    return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

async def coletar_precos_fastPass_seaworld(hora_global, array_datas,data_atual):
    driver = get_webdriver()
    dados = []
    wait = WebDriverWait(driver, 5)
    logging.info("Iniciando a coleta de preços fastPass SeaWorld")
    try:
        for days in array_datas:
            future_date = get_future_date(days)
            url = f"https://ingressos.orlandofastpass.com.br/ingressos/Orlando/8?destination=Orlando&destinationCode=2&destinationState=&destinationStateCode=&date={future_date}"
            driver.get(url)
            time.sleep(3)  # Aguardar o carregamento da página
            logging.info(f"Coletando preços para fastPass SeaWorld {future_date}")

            # Pares de XPaths para botões e elementos de preço correspondentes
            xpath_pairs = [
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[1]/div[2]/div[1]/button[1]', 
                 '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span',
                 '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/span',
                 '1 Dia 1 Parque - SeaWorld Orlando'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[1]/div[2]/div[1]/button[3]', 
                 '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span',
                 '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/span',
                 '3 Dias 3 Parques - SeaWorld Orlando'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[3]/div[2]/div/button', 
                 '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span',
                 '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/div[1]/span',
                 '14 Dias 3 Parques - SeaWorld Orlando'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[2]/div[2]/div[1]/button[2]',
                 '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span',
                 '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/span',
                '3 Dias 3 Parques com Refeições - SeaWorld Orlando')
                # Adicionar outros pares conforme necessário
            ]
            
            for button_xpath, price_xpath, cash_price_xpath, park_name in xpath_pairs:
                try:
                    button = wait.until(EC.presence_of_element_located((By.XPATH, button_xpath)))
                    driver.execute_script("arguments[0].scrollIntoView();", button)
                    time.sleep(2)  # Permitir tempo para quaisquer elementos carregados preguiçosos
                    button.click()
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
    try:    
        for days in array_datas:
            future_date = get_future_date(days)
            url = f"https://ingressos.orlandofastpass.com.br/ingressos/Orlando/9?destination=Orlando&destinationCode=2&destinationState=&destinationStateCode=&date={future_date}"
            driver.get(url)
            time.sleep(3)  # Aguardar o carregamento da página
            logging.info(f"Coletando preços para fastPass SeaWorld {future_date}")
            
           # Pares de XPaths para botões e elementos de preço correspondentes
            xpath_pairs = [
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div/div[2]/div[1]/button', 
                 '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[2]/span/span',
                 '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[1]/span',
                 '1 Dia 1 Parque - Busch Gardens'),
                # Adicionar outros pares conforme necessário
            ]
            
            for button_xpath, price_xpath, cash_price_xpath, park_name in xpath_pairs:
                try:
                    button = wait.until(EC.presence_of_element_located((By.XPATH, button_xpath)))
                    driver.execute_script("arguments[0].scrollIntoView();", button)
                    time.sleep(2)  # Permitir tempo para quaisquer elementos carregados preguiçosos
                    button.click()
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

                
                if "R$ " in price_text:
                    try:
                        price_number_str = price_text.replace("R$", "").replace(",", ".").strip()
                        price_number = float(price_number_str)
                        multiplied_price = price_number * 10
                    
                        cash_price_number_str = cash_price_text.replace("R$", "").replace(".","").replace(",", ".").strip()
                        cash_price_number = float(cash_price_number_str)
                        
                    except ValueError:
                        print(f"Erro ao converter preço para {park_name}: {price_text}")
                # Adicionando dados
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
        nome_arquivo = f'seaworld_fastPass_{data_atual}.json'
        salvar_dados(df, nome_arquivo, 'orlando/fastPass', hora_global)
        logging.info("Coleta de preços fastPass SeaWorld concluída")
        atualizar_calibragem(85)
        return
if __name__ == '__main__':
    asyncio.run(coletar_precos_fastPass_seaworld()) 