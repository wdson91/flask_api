from atualizar_calibragem import atualizar_calibragem
from imports import *

async def coletar_precos_disney_aquaticos(hour,array_datas,data_atual):
    
    datas = [datetime.now().date() + timedelta(days=d) for d in array_datas]

    # Initialize the Selenium driver (make sure to have the corresponding WebDriver installed)
    options = webdriver.ChromeOptions()
    #driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options)
    # driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub', options=options)

    # List to store product data
    all_data_set = []  # Using a set to store unique data

    # Mapping of park names
    mapeamento_nomes = {
        
        381001: "4 Dias - Disney Promocional com Aquatico e Esportes",
    }

    for data in datas:
        url = f"https://shopapp-montagem.azurewebsites.net/estados-unidos/orlando/disney-world---parques-aquaticos?Id=58167&DataIngresso={data}&dump=true"
        driver.get(url)
        time.sleep(2)

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
        produtos = parsed_data['Produtos']

        # Extract the date from the URL and convert the format
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        data_insercao = query_params['DataIngresso'][0]
        data_viagem = "-".join(data_insercao.split('/')[::-1])

        # Iterate over the products and add the data to the set
        for produto in produtos:
            id = produto['Id']
            margem = produto['Margem']
            preco_Avista = produto['ParcelaAVistaPadrao']['ValorTotal']
            preco_Parcelado = produto['ParcelasPadrao'][1]['ValorTotal']
            margem_categoria = produto['MargemCategoria']
            # Verificar se 'Margem' é um número válido
            try:
                # Tentar converter 'Margem' para float
                margem = float(margem)
            except (ValueError, TypeError):
                # Se não puder ser convertido, atribuir um valor padrão
                margem = '-'
                margem_categoria = '-'
            # Verifique se o parque está no mapeamento
            if id in mapeamento_nomes:
                # Mapeie o nome do parque
                id = mapeamento_nomes[id]

                # Adicione os dados ao conjunto
                all_data_set.append((data_viagem, id, margem, margem_categoria, preco_Avista, preco_Parcelado))

    # Feche o navegador
    driver.quit()

    # Converter o conjunto de tuplas em uma lista de dicionários
    all_data = [
        {
            'Data_viagem': data_viagem,
            'Parque': parque,
            'Margem': margem,
            'MargemCategoria': margem_categoria,
            "Preco_Avista": preco_Avista,
            "Preco_Parcelado": preco_Parcelado
        }
        for (data_viagem, parque, margem, margem_categoria, preco_Avista, preco_Parcelado) in all_data_set
    ]

    # Create a JSON from the collected data
    json_data = json.dumps(all_data)
    
    df = pd.DataFrame(all_data)

    # Exibir o DataFrame mesclado
    df = df.drop_duplicates()
    df['Margem'].fillna('-', inplace=True)
    df['MargemCategoria'].fillna('-', inplace=True)
    df = df.sort_values(by=['Data_viagem', 'Parque'])
    
    return df

async def coletar_precos_voupra_disney(hour,array_datas,data_atual):

    datas = [datetime.now().date() + timedelta(days=d) for d in array_datas]

    # Initialize the Selenium driver (make sure to have the corresponding WebDriver installed)
    options = webdriver.ChromeOptions()
    #driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options)
    # driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub', options=options)

    # List to store product data
    all_data_set = set()  # Using a set to store unique data

   
    # Mapping of park names
    mapeamento_nomes = {
        378149: "1 Dia - Disney Basico Magic Kingdom",
        378155: "1 Dia - Disney Basico Hollywood Studios",
        378158: "1 Dia - Disney Basico Animal Kingdom",
        378152: "1 Dia - Disney Basico Epcot",
        372961: "2 Dias - Disney World Basico",
        372963: "3 Dias - Disney World Basico",
        372965: "4 Dias - Disney World Basico",
        379851: "4 Dias - Disney Promocional",
        381001: "4 Dias - Disney Promocional com Aquatico e Esportes",
        372967: "5 Dias - Disney World Basico",
        283727: "6 Dias - Disney World Basico",
        283731: "7 Dias - Disney World Basico",
        283733: "8 Dias - Disney World Basico",
        283736: "9 Dias - Disney World Basico",
        283738: "10 Dias - Disney World Basico",
    }

    for data in datas:
        url = f"https://shopapp-montagem.azurewebsites.net/estados-unidos/orlando/disney-world?Id=49824&DataIngresso={data}&dump=true"
        driver.get(url)
        time.sleep(2)

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
        produtos = parsed_data['Produtos']

        # Extract the date from the URL and convert the format
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        data_insercao = query_params['DataIngresso'][0]
        data_viagem = "-".join(data_insercao.split('/')[::-1])

        # Iterate over the products and add the data to the set
        for produto in produtos:
            id = produto['Id']
            margem = produto['Margem']
            preco_Avista = produto['ParcelaAVistaPadrao']['ValorTotal']
            preco_Parcelado = produto['ParcelasPadrao'][1]['ValorTotal']
            margem_categoria = produto['MargemCategoria']
            # Verificar se 'Margem' é um número válido
            try:
                # Tentar converter 'Margem' para float
                margem = float(margem)
            except (ValueError, TypeError):
                # Se não puder ser convertido, atribuir um valor padrão
                margem = '-'
                margem_categoria = '-'
            # Verifique se o parque está no mapeamento
            if id in mapeamento_nomes:
                # Mapeie o nome do parque
                id = mapeamento_nomes[id]

                # Adicione os dados ao conjunto
                all_data_set.add((data_viagem, id, margem, margem_categoria, preco_Avista, preco_Parcelado))

    # Feche o navegador
    driver.quit()
    
    # Converter o conjunto de tuplas em uma lista de dicionários
    all_data = [
        {
            'Data_viagem': data_viagem,
            'Parque': parque,
            'Margem': margem,
            'MargemCategoria': margem_categoria,
            "Preco_Avista": preco_Avista,
            "Preco_Parcelado": preco_Parcelado
        }
        for (data_viagem, parque, margem, margem_categoria, preco_Avista, preco_Parcelado) in all_data_set
    ]

    # # Create a JSON from the collected data
    json_data = json.dumps(all_data)
    
    df = pd.DataFrame(all_data)
    df_disney = await coletar_precos_disney_aquaticos(hour, array_datas, data_atual)    
    
    merged_df = pd.concat([df, df_disney], ignore_index=True)
    
    # Exibir o DataFrame mesclado
    merged_df = merged_df.drop_duplicates()
    merged_df['Margem'].fillna('-', inplace=True)
    merged_df['MargemCategoria'].fillna('-', inplace=True)
    merged_df = merged_df.sort_values(by=['Data_viagem', 'Parque'])

    nome_arquivo = f'disney_voupra_{data_atual}.json'
    salvar_dados(merged_df, nome_arquivo, 'voupra', hour)
    
    # Define o novo valor para calibragem
    atualizar_calibragem(10)
    
    logging.info("Coleta de preços Voupra Disney finalizada.")
    return
# async def coletar_precos_voupra_disney(hour,array_datas):
#     # Configuração do Selenium
    
#     extract_data_and_return_dataframe(array_datas, hour)
    
#     options = webdriver.ChromeOptions()
#     driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options)
#     #driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub', options=options)
    

#     # Configuração de logs
#     log_format = '%(asctime)s - %(levelname)s - %(message)s'
#     logging.basicConfig(level=logging.INFO, format=log_format)

#     # Lista de datas a serem consideradas
#     datas = [datetime.now().date() + timedelta(days=d) for d in array_datas]

#     # URL base
#     base_url = "https://shopapp-montagem.azurewebsites.net/estados-unidos/orlando/disney-world?Id=49824&DataIngresso="

#     # Mapeamento de nomes desejados
#     mapeamento_nomes = {
#         "Ingresso 1 Dia Magic Kingdom Disney - Adulto": "1 Dia - Disney Basico Magic Kingdom",
#         "Ingresso 1 Dia Hollywood Studios Disney - Adulto": "1 Dia - Disney Basico Hollywood Studios",
#         "Ingresso 1 Dia Animal Kingdom Disney - Adulto": "1 Dia - Disney Basico Animal Kingdom",
#         "Ingresso 1 Dia Epcot Disney - Adulto": "1 Dia - Disney Basico Epcot",
#         "Ingresso 2 Dias Disney - Adulto": "2 Dias - Disney World Basico",
#         "Ingresso 3 Dias Disney - Adulto": "3 Dias - Disney World Basico",
#         "Ingresso 4 Dias Disney - Adulto": "4 Dias - Disney World Basico",
#         "Ingresso 4 Dias Disney para 4 Parques Diferentes - Adulto": "4 Dias - Disney Promocional",
#         "Super Combo 8 Dias de Experiências Disney - 4 Dias Parques Temáticos (1 Diferente por Dia) e 4 Dias Parques Aquáticos – Adulto":"4 Dias - Disney Promocional com Aquatico e Esportes",
#         "Ingresso 5 Dias Disney - Adulto": "5 Dias - Disney World Basico"
#     }

#     dados = []
    
#     # Iniciar o loop pelas datas
#     for data in datas:
#         try:
#             logging.info(f"Coletando preços para {data}...")
#             # Montar a URL com a data atual do loop
#             url = base_url + data.strftime('%d%%2F%m%%2F%Y') + '&dump=true'
#             driver.get(url)
            
#             # Usar WebDriverWait
#             wait = WebDriverWait(driver, 10)  # Esperar até 10 segundos

#             # Aguardar até que os elementos estejam presentes
#             produtos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "compra_expressa_item")))

#             # Inicializar um dicionário para armazenar os preços
#             precos = {}

#             # Loop pelos produtos
#             for produto in produtos:
#                 try:
#                     # Extraindo o título do produto
#                     titulo = produto.find_element(By.CLASS_NAME, "produto_titulo")
#                     titulo_texto = titulo.text

#                     # Extraindo o preço do produto
#                     preco = produto.find_element(By.CLASS_NAME, "produto_preco_padrao")
#                     driver.execute_script("arguments[0].classList.remove('d-none');", preco)
#                     preco_texto = preco.text

#                     # Removendo 'R$' e substituindo vírgulas por pontos
#                     preco_texto = preco_texto.replace('R$', '').replace(',', '.').strip()

#                     # Removendo pontos usados como separadores de milhar
#                     preco_texto = preco_texto.replace('.', '', preco_texto.count('.') - 1)

#                     # Convertendo para float e formatando
#                     preco_float = float(preco_texto)
                    
#                     preco_formatado = round(preco_float, 2)

#                     # Adicionando o preço ao dicionário
#                     precos[titulo_texto] = preco_formatado

#                 except Exception as e:
#                     logging.error("Erro ao processar produto:", e)

#             # Loop pelos nomes desejados
#             for nome, nome_desejado in mapeamento_nomes.items():
#                 if nome in precos:
#                     preco = precos[nome]
#                     preco_avista = round(preco * 0.9, 2)
#                 else:
#                     preco = '-'
#                     preco_avista = '-'
                    
#                 # Adicionar os dados à lista
#                 dados.append({
                    
#                     'Data_viagem': data.strftime("%Y-%m-%d"),
#                     'Parque': nome_desejado,
#                     'Preco_Parcelado': preco,
#                     'Preco_Avista': preco_avista
#                 })
            
            
# # Exibindo o DataFrame resultante
            
#         except Exception as e:
#             logging.error("Erro ao processar data:", e)

#     # Fechar o driver
#     driver.quit()
    
#     df = pd.DataFrame(dados)
    
#     all_data_json = baixar_blob_se_existir('dados.json', 'voupra')

#     # Carregar os dados do JSON baixado
#     dados_json = carregar_dados_json('dados.json')
#     # Converta os dados JSON em um DataFrame do Pandas
    
#     df_json = pd.DataFrame(dados_json)
    
#     df_json['Margem'].fillna('-', inplace=True)
#     df_json['MargemCategoria'].fillna('-', inplace=True)
#     # Mesclar os dois DataFrames com base nas colunas 'Data_viagem' e 'Parque'
#     df_merged = pd.merge(df, df_json, on=['Data_viagem', 'Parque'], how='left')

#     # Exibir o DataFrame mesclado
#     df_merged = df_merged.drop_duplicates()
#     df_merged['Margem'].fillna('-', inplace=True)
#     df_merged['MargemCategoria'].fillna('-', inplace=True)
    
#     nome_arquivo = f'disney_voupra_{datetime.now().strftime("%Y-%m-%d")}.json'
#     salvar_dados(df_merged, nome_arquivo, 'voupra', hour)

#     logging.info("Coleta de preços finalizada.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    asyncio.run(coletar_precos_voupra_disney())
