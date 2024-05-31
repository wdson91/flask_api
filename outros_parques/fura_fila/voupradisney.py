import asyncio
import time
from urllib.parse import parse_qs, urlparse

import pandas as pd
#from helpers.atualizar_calibragem import atualizar_calibragem
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import logging
from selenium.webdriver.chrome.service import Service as ChromeService
import schedule
from flask_cors import CORS
from bs4 import BeautifulSoup
import json
from threading import Thread

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
    #datas = [datetime.now().date() + timedelta(days=d) for d in array_datas]

    # URL base
    base_url = "https://shopapp-montagem.azurewebsites.net/estados-unidos/orlando/universal-express---fura-fila?Id=57594&DataIngresso="

    xpath_pairs = [
                ('/html/body/div[3]/div/div[1]/div[2]/div[8]/div/div/div[3]/div[1]/div[1]','/html/body/div[3]/div/div[1]/div[2]/div[8]/div/div/div[3]/div[1]/div[5]','Ingresso 1 Dia Universal Express Pass'),
                ('/html/body/div[3]/div/div[1]/div[2]/div[13]/div/div/div[3]/div[1]/div[1]','/html/body/div[3]/div/div[1]/div[2]/div[13]/div/div/div[3]/div[1]/div[5]','Ingresso 1 Dia Universal Express Unlimited')]
    dados = []  # Inicializa os dados dentro do loop
    
    # Iniciar o loop pelas datas
    for day in array_datas:
        try:
            future_date = get_future_date(day)
            logging.info(f"Coletando preços para {future_date}...")
            # Montar a URL com a data atual do loop
            url = f'{base_url + future_date}&dump=true'
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
                    html_content = driver.page_source

                    # Use BeautifulSoup to parse the HTML
                    soup = BeautifulSoup(html_content, 'html.parser')

                    # Find the script that contains the data
                    script_tags = soup.find_all('script')

                    # Counter to track the position of dumps
                    dump_count = 0

                    # Iterate over all scripts on the page
                    for script in script_tags:
                        # Check if the script contains the desired dump pattern
                        if '[DUMP]' in script.text:
                            # Increment the dump counter
                            dump_count += 1

                            # Check if it is the third desired dump
                            if dump_count == 4:
                                # Extract the data from the dump
                                dump_data = script.text.strip()

                                # Save the data to a txt file
                                with open('dados_dump.txt', 'w') as file:
                                    file.write(dump_data)

                                break  # Exit the loop after finding the third dump

                    # Open the text file with the data
                    with open('dados_dump.txt', 'r') as file:
                        data = file.read()

                    # Find the index of the start of the JSON data
                    start_index = data.find('{')

                    # Extract only the JSON data
                    json_data = data[start_index:]

                    # Find the index of the last closing brace
                    last_brace_index = json_data.rfind('}') + 1

                    # Cut the JSON string to contain only valid data
                    json_data = json_data[:last_brace_index]

                    # Parse the JSON data
                    parsed_data = json.loads(json_data)

                    # Access the products
                    #produtos = parsed_data['Produtos']

                    # Extract the date from the URL and convert the format
                    parsed_url = urlparse(url)
                    query_params = parse_qs(parsed_url.query)
                    data_insercao = query_params['DataIngresso'][0]
                    data_viagem = "-".join(data_insercao.split('/')[::-1])

                    # Iterate over the products and add the data to the set
                    
                        
                    margem = parsed_data['Margem']
                    
                    margem_categoria = parsed_data['MargemCategoria']
                    # Verificar se 'Margem' é um número válido
                    try:
                            # Tentar converter 'Margem' para float
                            margem = float(margem)
                    except (ValueError, TypeError):
                            # Se não puder ser convertido, atribuir um valor padrão
                            margem = '-'
                            margem_categoria = '-'
                        # Verifique se o parque está no mapeamento
                    # Adiciona os dados ao array
                    dados.append({
                        'Data_viagem': (datetime.now() + timedelta(days=day)).strftime("%Y-%m-%d"),
                        'Parque': park_name,
                        'Margem': margem,
                        'MargemCategoria': margem_categoria,
                        'Preco_Avista': price_number_vista if price_number_vista != '-' else '-',
                        'Preco_Parcelado': multiplied_price_parcelado if multiplied_price_parcelado != '-' else '-'
                    })
                    
                except TimeoutException:
                    logging.error(f"Tempo esgotado ao tentar obter o preço para {park_name}")
                    # Se houver um timeout, adicione valores padrão
                    dados.append({
                        'Data_viagem': (datetime.now() + timedelta(days=day)).strftime("%Y-%m-%d"),
                        'Parque': park_name,
                        'Margem': margem,
                        'MargemCategoria': margem_categoria,
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
    array_datas=[5,10, 20, 47, 65, 126]
    asyncio.run(coletar_precos_voupra_fura_fila('hour',array_datas, 'data_atual'))
