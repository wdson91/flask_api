from imports import *
from webdriver_setup import get_webdriver

# Function to calculate future dates
def get_future_date(days):
    return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

async def coletar_precos_ml_halloween(hora_global, array_datas,data_atual):
    # Configurações do WebDriver Selenium
    options = webdriver.ChromeOptions()
    driver = get_webdriver()
    dados = []
    wait = WebDriverWait(driver, 10)
    logging.info("Iniciando a coleta de preços ML halloween")
    datas = [f'2024-08-30',f'2024-09-06',f'2024-09-22',f'2024-10-04',f'2024-10-11',f'2024-10-31']
    
    urls= [('https://www.vamonessa.com.br/ingressos/HALLOWEEN%20HORROR%20NIGHTS%20UNIVERSAL/536?destination=Orlando&destinationCode=2&destinationState=Florida&destinationStateCode=2&date=','Universal Halloween Horror Nights'),("https://www.vamonessa.com.br/ingressos/MICKEY'S%20NOT%20SO%20SCARY%20HALLOWEEN%20PARTY/570?destination=Orlando&destinationCode=2&destinationState=&destinationStateCode=&date=","Mickey’s Not–So–Scary Halloween")]
    xpath_pairs = [
                    ( '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div/div[2]/div[1]/button',
                    '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[2]/span/span',
                    '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div/div[2]/div[2]/div[2]/div[1]/div[1]/span',
                    )
                ]
    for url ,park in urls:
        
            for days in datas:
                #future_date = get_future_date(days)
                url_atual = f"{url}{days}&provider=0"
                driver.get(url_atual)
                await asyncio.sleep(3)  # Aguardar o carregamento da página
                logging.info(f"Coletando preços para {days}")

                # Pares de XPaths para botões e elementos de preço correspondentes
               
                
                for button_xpath,price_xpath, cash_price_xpath in xpath_pairs:
                    try:
                        button = wait.until(EC.presence_of_element_located((By.XPATH, button_xpath)))
                        driver.execute_script("arguments[0].scrollIntoView();", button)
                        time.sleep(3)
                        button.click()
                    except TimeoutException:
                        logging.error(f"Tempo esgotado ao tentar localizar o botão para {park}")
                        dados.append({
                            'Data_viagem': days,
                            'Parque': park,
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
                            print(f"Erro ao converter preço para {park}: {price_text}")

                    #Adicionando dados
                    data_hora_atual = datetime.now()
                    
                    dados.append({
                        'Data_viagem': days,
                        'Parque': park,
                        'Preco_Parcelado': float(multiplied_price),
                        'Preco_Avista': cash_price_number
                    })
                    
       
    driver.quit()
    df = pd.DataFrame(dados)
    nome_arquivo = f'halloween_ml_{data_atual}.json'
            
    salvar_dados(df, nome_arquivo, 'halloween/ml', hora_global)
    logging.info("Coleta de preços ML halloween concluída")
    #atualizar_calibragem(85)
    return
if __name__ == '__main__':
    array_datas = [5,10,20,47,65,126]
    hora_global = datetime.now(pytz.timezone('America/Sao_Paulo'))
    asyncio.run(coletar_precos_ml_halloween(hora_global,array_datas,'2024-03-25')) 