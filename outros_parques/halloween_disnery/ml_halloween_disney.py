from imports import *

# Function to calculate future dates
def get_future_date(days):
    return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

async def coletar_precos_ml_halloween(hour, array_datas,data_atual):
    # Configurações do WebDriver Selenium
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    # WebDriver remoto
    #driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options)
    #driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub', options=options)
    dados = []
    wait = WebDriverWait(driver, 5)
    logging.info("Iniciando a coleta de preços ML halloween")
    datas = [f'2024-08-30',f'2024-09-06',f'2024-09-22',f'2024-10-04',f'2024-10-11',f'2024-10-31']
    
    try:
        for days in datas:
            #future_date = get_future_date(days)
            url = f"https://www.vamonessa.com.br/ingressos/MICKEY'S%20NOT%20SO%20SCARY%20HALLOWEEN%20PARTY/570?destination=Orlando&destinationCode=2&destinationState=&destinationStateCode=&date={days}&provider=0"
            driver.get(url)
            await asyncio.sleep(3)  # Aguardar o carregamento da página
            logging.info(f"Coletando preços para {days}")

            # Pares de XPaths para botões e elementos de preço correspondentes
            xpath_pairs = [
                 ( '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div/div[2]/div[1]/button',
                  '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[2]/span/span',
                  '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[1]/span',
                  'Disney Halloween Horror Nights')
            ]
            
            for button_xpath,price_xpath, cash_price_xpath, park_name in xpath_pairs:
                try:
                    button = wait.until(EC.presence_of_element_located((By.XPATH, button_xpath)))
                    driver.execute_script("arguments[0].scrollIntoView();", button)
                    time.sleep(2)
                    button.click()
                except TimeoutException:
                    logging.error(f"Tempo esgotado ao tentar localizar o botão para {park_name}")
                    dados.append({
                        'Data_viagem': days,
                        'Parque': park_name,
                        'Preco_Avista': '-',
                        'Preco_Parcelado':  '-'
                    })
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
                    'Data_viagem': days,
                    'Parque': park_name,
                    'Preco_Parcelado': float(multiplied_price),
                    'Preco_Avista': cash_price_number
                })
                
    except TimeoutException as e:
            print("Erro: Elemento não encontrado ou tempo de espera excedido", e)    
    finally:
        driver.quit()
        df = pd.DataFrame(dados)
        nome_arquivo = f'halloweenDisney_ml_{data_atual}.json'
        
        salvar_dados(df, nome_arquivo, 'halloween/ml', hour)
        logging.info("Coleta de preços ML halloween concluída")
        #atualizar_calibragem(85)
        return
if __name__ == '__main__':
    array_datas = [5,10,20,47,65,126]
    hora_global = datetime.now(pytz.timezone('America/Sao_Paulo'))
    asyncio.run(coletar_precos_ml_halloween(hora_global,array_datas,'2024-03-25')) 