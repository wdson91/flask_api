
from imports import *
from webdriver_setup import get_webdriver



def get_future_date(days):
    return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

# List of days to add to the current date

async def coletar_precos_ml_fura_fila(hour,array_datas,data_atual):
    options = webdriver.ChromeOptions()
    driver = get_webdriver()
    logging.info("Iniciando a coleta de preços ML Fura Fila")
    dados = []
    wait = WebDriverWait(driver, 5)
    
    
    xpath_pairs = [
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[10]/div[2]/div[1]/button', '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[10]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span','//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[10]/div[2]/div[2]/div[2]/div[1]/div[1]/span','Ingresso 1 Dia Universal Express Pass'),
                ('//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[11]/div[2]/div[1]/button', '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[11]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span','//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[11]/div[2]/div[2]/div[2]/div[1]/div[1]/span','Ingresso 1 Dia Universal Express Unlimited'),
               
                # Add other pairs as needed
            ]
    try:
    
        for days in array_datas:
            future_date = get_future_date(days)
            url = f"https://www.vamonessa.com.br/ingressos/Orlando/7?destination=Orlando&destinationCode=2&destinationState=&destinationStateCode=&date={future_date}&provider=0"
            driver.get(url)
            time.sleep(3)
            logging.info(f"Coletando preços para {future_date}")
            for button_xpath, preco_parcelado, preco_avista, park_name in xpath_pairs:
                # Scroll to button and click
                # button = wait.until(EC.presence_of_element_located((By.XPATH, button_xpath)))
                # driver.execute_script("arguments[0].scrollIntoView();", button)
                

                # try:
                #     button.click()
                # except ElementClickInterceptedException:
                    
                #     driver.execute_script("arguments[0].click();", button)

                try:
                    price1 = wait.until(EC.presence_of_element_located((By.XPATH, preco_parcelado)))
                    price2 = wait.until(EC.presence_of_element_located((By.XPATH, preco_avista)))
                    driver.execute_script("arguments[0].scrollIntoView();",  price1)
                    time.sleep(4)
                    price_text_1 =  price1.text
                    price_text_2 =  price2.text
                except TimeoutException:
                    price_text_1 = '-'
                    price_text_2= '-'
                if price_text_1 != '-':
                    price_number_str_1 = price_text_1.replace("R$", "").replace(",", ".").strip()
                    price_number_str_2 = price_text_2.replace("R$", "").replace(",", ".").strip()
                # Additional code to process and print the price
                if "R$" in price_text_1:
                    price_number_str_1 = price_text_1.replace("R$", "").replace(",", ".").strip()
                    price_number_str_2 = price_text_2.replace("R$", "").replace(",", ".").strip()
                    try:
                        price_number_1 = float(price_number_str_1)
                        
                        multiplied_price = price_number_1* 10
                        
                        price_number_2 = float(price_number_str_2.replace('.', ''))
                        
                    except ValueError:
                        print(f"Error converting price for {park_name}: {price_text_1}")
                    # ...       
                dados.append({

                        'Data_viagem': (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d"),
                        'Parque': park_name,
                        'Preco_Parcelado': float(multiplied_price),
                        'Preco_Avista': float(price_number_2) / 100,
                    })
                
    except TimeoutException as e:
        logging.error("Erro: Elemento não encontrado ou tempo de espera excedido", e)
    except Exception as e:
        logging.error("Erro inesperado:", e)
    finally:
                
                driver.quit()
                df = pd.DataFrame(dados)
                
                nome_arquivo = f'furafila_ml_{data_atual}.json'
                #df.to_json(nome_arquivo, orient='records', lines=True)
                salvar_dados(df, nome_arquivo,'outros/ml',hour)
                logging.info("Coleta de preços ML Disney finalizada")
               # atualizar_calibragem(95)
    return
if __name__ == '__main__':
    array_datas =  [5,10,20,47,65,126]
    asyncio.run(coletar_precos_ml_universal('hora_global',array_datas,'2024-03-25'))
