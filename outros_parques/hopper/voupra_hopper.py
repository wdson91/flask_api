from imports import *
from webdriver_setup import get_webdriver




async def coletar_precos_voupra_hopper_plus(hora_global,array_datas,data_atual):

    datas = [datetime.now().date() + timedelta(days=d) for d in array_datas]

    # Initialize the Selenium driver (make sure to have the corresponding WebDriver installed)
    driver = get_webdriver()

    # List to store product data
    all_data_set = set()  # Using a set to store unique data

   
    # Mapping of park names
    mapeamento_nomes = {
       
        283807: "1 Dia - Disney Parques Aquaticos",
        283809: "2 Dias - Disney Parques Aquaticos",
        283812: "3 Dias - Disney Parques Aquaticos",
        283814: "4 Dias - Disney Parques Aquaticos",
        283817: "5 Dias - Disney Parques Aquaticos",
        283821: "6 Dias - Disney Parques Aquaticos",
        283823: "7 Dias - Disney Parques Aquaticos",
        283825: "8 Dias - Disney Parques Aquaticos",
        283828: "9 Dias - Disney Parques Aquaticos",
        283830: "10 Dias - Disney Parques Aquaticos",
    }

    for data in datas:
        url = f"https://www.voupra.com/estados-unidos/orlando/disney-world---parques-aquaticos?Id=58167&DataIngresso={data}&dump=true"
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
                if '1321/Views/CompraExpressa/_RTabelaCusto.cshtml' in script.text:
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
   
    return df 

async def coletar_precos_voupra_hopper(hora_global,array_datas,data_atual):

    datas = [datetime.now().date() + timedelta(days=d) for d in array_datas]

    # Initialize the Selenium driver (make sure to have the corresponding WebDriver installed)
    driver = get_webdriver()

    # List to store product data
    all_data_set = set()  # Using a set to store unique data

    df_disney = await coletar_precos_voupra_hopper_plus(hora_global, array_datas, data_atual) 
    # Mapping of park names
    mapeamento_nomes = {
       
        283756: "1 Dia - Disney Park Hopper",
        283757: "2 Dias - Disney Park Hopper",
        283763: "3 Dias - Disney Park Hopper",
        283766: "4 Dias - Disney Park Hopper",
        283769: "5 Dias - Disney Park Hopper",
        283772: "6 Dias - Disney Park Hopper",
        283775: "7 Dias - Disney Park Hopper",
        283778: "8 Dias - Disney Park Hopper",
        283781: "9 Dias - Disney Park Hopper",
        283784: "10 Dias - Disney Park Hopper",
    }

    for data in datas:
        url = f"https://shopapp-montagem.azurewebsites.net/estados-unidos/orlando/disney-world---park-hopper?Id=54914&DataIngresso={data}&dump=true"
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
                if '1321/Views/CompraExpressa/_RTabelaCusto.cshtml' in script.text:
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
       
    
    merged_df = pd.concat([df, df_disney], ignore_index=True)
    
    # Exibir o DataFrame mesclado
    merged_df = merged_df.drop_duplicates()
    merged_df['Margem'].fillna('-', inplace=True)
    merged_df['MargemCategoria'].fillna('-', inplace=True)
    merged_df = merged_df.sort_values(by=['Data_viagem', 'Parque'])

    nome_arquivo = f'hopper_voupra_{data_atual}.json'
    salvar_dados(merged_df, nome_arquivo, 'hopper/voupra', hora_global)
    
    
    logging.info("Coleta de preços Voupra Disney finalizada.")
    return