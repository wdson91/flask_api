from imports import *


def get_future_date(days):
    return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")


async def coletar_precos_voupra_fura_fila(hour, array_datas,data_atual):
    # Configuração do Selenium
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 4)

    # Configuração de logs
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_format)

    # Lista de datas a serem consideradas
    datas = [datetime.now().date() + timedelta(days=d) for d in array_datas]

    # URL base
    base_url = "https://www.voupra.com/estados-unidos/orlando/universal-express---fura-fila?Id=57594&DataIngresso="

    xpath_pairs = [
                ('/html/body/div[3]/div/div[1]/div[2]/div[7]/div/div/div[3]/div[1]/div[1]','/html/body/div[3]/div/div[1]/div[2]/div[7]/div/div/div[3]/div[1]/div[5]','Ingresso 1 Dia Universal Express Pass'),
                ('/html/body/div[3]/div/div[1]/div[2]/div[13]/div/div/div[3]/div[1]/div[1]','/html/body/div[3]/div/div[1]/div[2]/div[13]/div/div/div[3]/div[1]/div[5]','Ingresso 1 Dia Universal Express Unlimited')]
    dados = []  # Inicializa os dados dentro do loop
    
    # Iniciar o loop pelas datas
    for day in array_datas:
        try:
            future_date = get_future_date(day)
            logging.info(f"Coletando preços para {future_date}...")
            # Montar a URL com a data atual do loop
            url = base_url + future_date
            driver.get(url)
           
            for price_xpath_parcelado, price_xpath_vista, park_name in xpath_pairs:
                try:
                    price_element_parcelado = wait.until(EC.presence_of_element_located((By.XPATH, price_xpath_parcelado)))
                    price_element_vista = wait.until(EC.presence_of_element_located((By.XPATH, price_xpath_vista)))
                    price_text_parcelado = price_element_parcelado.text
                    price_text_vista = price_element_vista.text
                    
                    if price_text_parcelado != '-':
                        price_number_str_parcelado = price_text_parcelado.replace("R$", "").replace(".", "").replace(",", ".").strip()
                        price_number_parcelado = float(price_number_str_parcelado)
                        multiplied_price_parcelado = price_number_parcelado
                    else:
                        multiplied_price_parcelado = '-'

                    if price_text_vista != '-':
                        price_number_str_vista = price_text_vista.replace("R$", "").replace(".", "").replace(",", ".").strip()
                        price_number_vista = float(price_number_str_vista)
                    else:
                        price_number_vista = '-'
                        
                    # Adiciona os dados ao array
                    dados.append({
                        'Data_viagem': (datetime.now() + timedelta(days=day)).strftime("%Y-%m-%d"),
                        'Parque': park_name,
                        'Preco_Avista': price_number_vista if price_number_vista != '-' else '-',
                        'Preco_Parcelado': multiplied_price_parcelado if multiplied_price_parcelado != '-' else '-'
                    })
                    
                except TimeoutException:
                    logging.error(f"Tempo esgotado ao tentar obter o preço para {park_name}")
                    # Se houver um timeout, adicione valores padrão
                    dados.append({
                        'Data_viagem': (datetime.now() + timedelta(days=day)).strftime("%Y-%m-%d"),
                        'Parque': park_name,
                        'Preco_Avista': '-',
                        'Preco_Parcelado': '-'
                    })
                    
            # Salvando os dados em um arquivo JSON após cada iteração do loop
            
                
        except Exception as e:
            logging.error(f"Erro inesperado: {e}")
    df = pd.DataFrame(dados)
    nome_arquivo = f'furafila_voupra_{data_atual}.json'
    #df.to_json(nome_arquivo, orient='records', lines=True)
    
     
    salvar_dados(df, nome_arquivo,'outros/voupra',hour)
    # Finalizando o WebDriver fora do loop
    driver.quit()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    array_datas=[5,10, 20, 47, 65, 126],
    asyncio.run(coletar_precos_voupra_disney('hour',array_datas, 'data_atual'))

