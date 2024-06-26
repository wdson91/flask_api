from imports import *
from webdriver_setup import get_webdriver




# Function to calculate future dates
def get_future_date(days):
    return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")

async def coletar_precos_ml_cove(hour, array_datas,data_atual):
    driver = get_webdriver()
    dados = []
    wait = WebDriverWait(driver, 5)
    logging.info("Iniciando a coleta de preços ML Cove")
    try:
        for days in array_datas:
            future_date = get_future_date(days)
            url = f"https://www.vamonessa.com.br/ingressos/DISCOVERY%20COVE%20ORLANDO/11?destination=Orlando&destinationCode=2&destinationState=Florida&destinationStateCode=2&date={future_date}&provider=0"
            driver.get(url)
            await asyncio.sleep(3)  # Aguardar o carregamento da página
            logging.info(f"Coletando preços para {future_date}")

            # Pares de XPaths para botões e elementos de preço correspondentes
            xpath_pairs = [
                 ( 
                  '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span',
                  '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/span',
                  '1 Dia Discovery Cove'),
                (
                 '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span',
                 '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[1]/span',
                 '1 Dia Discovery Cove com Nado com Golfinhos'),
                ( 
                 '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span',
                 '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[3]/div[2]/div[2]/div[2]/div[1]/div[1]/span',
                 '1 Dia Discovery Cove + 14 Dias SeaWorld Orlando e Aquatica'),
                (
                 '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[4]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span',
                 '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[4]/div[2]/div[2]/div[2]/div[1]/div[1]/span',
                '1 Dia Discovery Cove Com Nado com Golfinhos + 14 Dias SeaWorld Orlando e Aquatica'),
                (
                 '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[5]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span',
                 '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[5]/div[2]/div[2]/div[2]/div[1]/div[1]/span',
                '1 Dia Discovery Cove + 14 Dias SeaWorld, Busch Gardens, e Aquatica'),
                (
                 '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[6]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span',
                 '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[6]/div[2]/div[2]/div[2]/div[1]/div[1]/span',
                '1 Dia Discovery Cove Com Nado com Golfinhos + 14 Dias SeaWorld, Busch Gardens e Aquatica'),
                (
                 '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[7]/div[2]/div[2]/div[2]/div[1]/div[2]/span/span',
                 '//*[@id="root"]/div[2]/div[1]/div[3]/div[4]/div[1]/div[7]/div[2]/div[2]/div[2]/div[1]/div[1]/span',
                'SeaVenture - Passeio Subaquático no Discovery Cove'),
              
                
                # Adicionar outros pares conforme necessário
            ]
            
            for price_xpath, cash_price_xpath, park_name in xpath_pairs:
               
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
        nome_arquivo = f'discovery_cove_ml_{data_atual}.json'
        
        salvar_dados(df, nome_arquivo, 'outros/ml', hour)
        logging.info("Coleta de preços ML Cove concluída")
        #atualizar_calibragem(85)
        return
if __name__ == '__main__':
    array_datas = [5,10,20,47,65,126]
    hora_global = datetime.now(pytz.timezone('America/Sao_Paulo'))
    asyncio.run(coletar_precos_ml_cove(hora_global,array_datas,'2024-03-25')) 