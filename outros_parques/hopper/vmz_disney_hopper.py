from imports import *

pasta = 'outros/vmz'

async def coletar_precos_vmz_hopper(hour,array_datas,data_atual):
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Defina sua lógica para baixar os arquivos e esperar por eles
    baixar_blob_se_existir('disney_vmz_hopper_basicos_parcial.json', pasta)
    baixar_blob_se_existir('disney_vmz_hopper_dias_parcial.json', pasta)
    
    # Carregue os dados do JSON baixado
    disney_basicos = carregar_dados_json('disney_vmz_hopper_basicos_parcial.json')
    disney_dias = carregar_dados_json('disney_vmz_hopper_dias_parcial.json')


    # Combine os dados de disney_basicos e disney_dias
    dados_combinados = disney_basicos[-1]["Dados"] + disney_dias[-1]["Dados"]


    df = pd.DataFrame(dados_combinados)
    
    df_sorted = df.sort_values(by=['Data_viagem', 'Parque'], ignore_index=True)

    nome_arquivo = f'hopper_vmz_{data_atual}.json'
    
    salvar_dados(df_sorted, nome_arquivo, pasta, hour)
    
    logging.info("Coleta finalizada.")
    #atualizar_calibragem(65)
    return 


async def coletar_precos_vmz_hopper_basicos(array_datas,hour,data_atual):
    
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    #driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options)
    #driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub', options=options)
    
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    sites = [
    ("https://www.vmzviagens.com.br/ingressos/orlando/disney-world-ingresso/1-dia-hopper-disney?", '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/span[1]', '1 Dia - Disney Park Hopper'),
    
]

    # Definindo as datas
    datas = [datetime.now().date() + timedelta(days=d) for d in array_datas]

    # Lista para armazenar os dados
    dados = []

    # Percorrer cada site e coletar preços
    for site_url, xpath_selector, parque_nome in sites:
        for data in datas:
            logging.info(f"Coletando preços para {parque_nome} na data: {data}")
            url_com_data = f"{site_url}&data={data.strftime('%Y-%m-%d')}"
            driver.get(url_com_data)
            
            try:
                
                # Tente localizar o elemento com o preço
                wait = WebDriverWait(driver, 10)
                elemento_preco = driver.find_element(By.XPATH, xpath_selector)
                preco_texto = elemento_preco

                # Multiplicar o preço por 10
                price_text = preco_texto.text
                price_decimal = float(price_text.replace('R$', '').replace('.', '').replace(',', '.').strip())
                new_price = round(price_decimal , 2)
                preco_parcelado = round(price_decimal * 1.08, 2)
            except NoSuchElementException:
                # Se o elemento não for encontrado, atribua um traço "-" ao valor
                new_price = "-"
                preco_parcelado = "-"
            # Adicionar os dados coletados à lista
            dados.append({
                'Data_viagem': data.strftime("%Y-%m-%d"),
                'Parque': parque_nome,
                'Preco_Parcelado': preco_parcelado,
                'Preco_Avista': new_price
            })

    logging.info("Coleta de preços finalizada.")
    
    # Criando um DataFrame
    df = pd.DataFrame(dados)
    salvar_dados(df, 'disney_vmz_hopper_basicos_parcial.json',pasta,hour)
    driver.quit()
    
    
    return

async def coletar_precos_vmz_hopper_disneydias(array_datas, hour, data_atual):
    waiter = 2
    dias_para_processar = [2,3,4,5,6,7,8,9,10]
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 60)

    nome_pacotes = {
        2: "2 Dias - Disney Park Hopper",
        3: "3 Dias - Disney Park Hopper",
        4: "4 Dias - Disney Park Hopper",
        5: "5 Dias - Disney Park Hopper",
        6: "6 Dias - Disney Park Hopper",
        7: "7 Dias - Disney Park Hopper",
        8: "8 Dias - Disney Park Hopper",
        9: "9 Dias - Disney Park Hopper",
        10: "10 Dias - Disney Park Hopper",
    }

    def fechar_popups(driver):
        try:
            botao_fechar_selector = '.dinTargetFormCloseButtom'
            botao_fechar = WebDriverWait(driver, waiter + 3).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, botao_fechar_selector))
            )
            botao_fechar.click()
            botao_cookies = WebDriverWait(driver, waiter + 3).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[3]/div/div/div[2]/button'))
            )
            botao_cookies.click()

            logging.info("Pop-up fechado.")
        except Exception as e:
            logging.warning(f"Popup não encontrada")

    def encontrar_preco_data(driver, data):
        try:
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'fc-content')))
            elementos_fc_content = driver.find_elements(By.CLASS_NAME, 'fc-content')
            for elemento in elementos_fc_content:
                fc_date = elemento.find_element(By.CLASS_NAME, 'fc-date').text
                if fc_date == str(data.day):
                    calendar_event_price = elemento.find_element(By.CLASS_NAME, 'calendar-event-price')
                    price_text = calendar_event_price.text.strip()
                    preco_avista = float(price_text.replace('R$', '').replace('.', '').replace(',', '.').strip())
                    preco_parcelado = round(preco_avista * 1.08, 2)

                    return preco_avista, preco_parcelado
        except Exception as e:
            logging.error(f"Erro ao encontrar preço para data {data}: {e}")
            return None

    def processar_dias(driver, dias, array_datas):
        base_url = "https://www.vmzviagens.com.br/ingressos/orlando/walt-disney-orlando/ticket-disney-hopper"
        dados = []

        for dia in dias:
            logging.info(f"Coletando preços para {dia} dias.")
            nome_pacote = nome_pacotes.get(dia, f"{dia} Dias - Desconhecido")
            url_com_dias = f"{base_url}?mes=2024-01&dias={dia}"
            driver.get(url_com_dias)
            fechar_popups(driver)

            data_objeto = datetime.strptime(data_atual, "%Y-%m-%d")
            mes_extenso = data_objeto.strftime("%B").lower()

            mes_atual = driver.find_element(By.XPATH, "//*[@id='custom-month']").text.lower()

            for data in array_datas:
                if mes_extenso != mes_atual:
                    while mes_extenso != mes_atual:
                        botao_next = driver.find_element(By.XPATH, '//*[@id="custom-next"]')
                        wait.until(EC.element_to_be_clickable(botao_next))
                        botao_next.click()
                        mes_atual = driver.find_element(By.CSS_SELECTOR, "#custom-next").text.lower()
                else:
                    logging.warning(f"Preço não encontrado para {nome_pacote} em {data}")
                    continue

                preco = encontrar_preco_data(driver, data)
                if preco is not None:
                    preco_avista, preco_parcelado = preco
                    dados.append({
                        'Data_viagem': data.strftime("%Y-%m-%d"),
                        'Parque': nome_pacote,
                        'Preco_Parcelado': preco_parcelado,
                        'Preco_Avista': preco_avista
                    })
                else:
                    logging.warning(f"Preço não encontrado para {nome_pacote} em {data}")

        return dados

    dias_para_processar = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    resultados = processar_dias(driver, dias_para_processar, array_datas)

    df = pd.DataFrame(resultados)
    
    salvar_dados(df,'disney_vmz_hopper_dias_parcial.json',pasta,hour)
    driver.quit()

    return 

if __name__ == "__main__":
    
    dias_para_processar = [2,3,4,5,6,7,8,9,10]
    array_datas = [5,10,20,47,65,126]
    hour = datetime.now().hour
    data_atual = datetime.now().strftime('%Y-%m-%d')
    
    
    df_final = asyncio.run(coletar_precos_vmz_hopper_disneydias(dias_para_processar,array_datas,hour,data_atual))
