from imports import *
from helpers.atualizar_calibragem import atualizar_calibragem
from webdriver_setup import get_webdriver

async def coletar_precos_voupra_sea(hora_global,array_datas,data_atual):
    datas = [datetime.now().date() + timedelta(days=d) for d in array_datas]

    logging.info("Iniciando coleta de preços Voupra SeaWorld.")
    driver = get_webdriver()
    #driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options)
    #driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub', options=options)

    # Lista para armazenar os dados dos produtos
    all_data_set = set()  # Usando um conjunto para armazenar dados únicos

    # Mapeamento dos nomes dos parques
    mapeamento_nomes = {
        376028: "1 Dia 1 Parque - SeaWorld Orlando",
        376029: "1 Dia 1 Parque - Busch Gardens",
        376030: "3 Dias 3 Parques - SeaWorld Orlando",
        376031: "3 Dias 3 Parques com Refeições - SeaWorld Orlando",
        376032: "14 Dias 3 Parques - SeaWorld Orlando",
        381252: "2 Dias 2 Parques com Refeição no Busch Gardens - SeaWorld Orlando",
        381352: "1 Dia SeaWorld Orlando com Refeições Inclusas",
        381353: "1 Dia Busch Gardens Tampa com Refeições Inclusas"
    }

    for data in datas:
        url = f"https://shopapp-montagem.azurewebsites.net/estados-unidos/orlando/seaworld?Id=58825&Busca=true&DataTemporada={data}&dump=true"
        driver.get(url)
        time.sleep(2)

        html_content = driver.page_source

        # Use BeautifulSoup para analisar o HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Encontre o script que contém os dados
        script_tags = soup.find_all('script')

        # Contador para rastrear a posição dos dumps
        dump_count = 0

        # Itere sobre todos os scripts na página
        for script in script_tags:
            # Verifique se o script contém o padrão de dump desejado
            if '[DUMP]' in script.text:
                # Incrementa o contador de dumps
                dump_count += 1

                # Verifica se é o terceiro dump desejado
                if '1321/Views/CompraExpressa/_RTemporada.cshtml' in script.text:
                    # Extraia os dados do dump
                    dump_data = script.text.strip()

                    # Salva os dados em um arquivo txt
                    with open('dados_dump.txt', 'w') as file:
                        file.write(dump_data)

                    break  # Saia do loop após encontrar o terceiro dump

        # Abra o arquivo de texto com os dados
        with open('dados_dump.txt', 'r') as file:
            data = file.read()

        # Encontre o índice do início dos dados JSON
        start_index = data.find('{')

        # Extraia apenas os dados JSON
        json_data = data[start_index:]

        # Encontre o índice do último fechamento de chaves
        last_brace_index = json_data.rfind('}') + 1

        # Corte a string JSON para conter apenas os dados válidos
        json_data = json_data[:last_brace_index]

        # Analise os dados JSON
        parsed_data = json.loads(json_data)

        # Acesse os produtos
        produtos = parsed_data['Produtos']

        # Extrair a data da URL e converter o formato
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        data_insercao = query_params['DataTemporada'][0]
        data_viagem = "-".join(data_insercao.split('/')[::-1])

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

    # Create a JSON from the collected data
    json_data = json.dumps(all_data)

    df = pd.DataFrame(all_data)

    # Exibir o DataFrame mesclado
    df = df.drop_duplicates()
    df['Margem'].fillna('-', inplace=True)
    df['MargemCategoria'].fillna('-', inplace=True)
    df = df.sort_values(by=['Data_viagem', 'Parque'])

    nome_arquivo = f'seaworld_voupra_{data_atual}.json'
    salvar_dados(df, nome_arquivo, 'orlando/voupra', hora_global)

    atualizar_calibragem(20)
    logging.info("Coleta de preços Voupra Seaworld  finalizada.")
    return

# async def coletar_precos_voupra_sea(hora_global,array_datas):
#     # Configuração do Selenium

#     extract_data_and_return_dataframe(array_datas, hora_global)

#     options = webdriver.ChromeOptions()
#     driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options)
#     #driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub', options=options)
#     #driver = webdriver.Chrome()

#     # Configuração de logs
#     log_format = '%(asctime)s - %(levelname)s - %(message)s'
#     logging.basicConfig(level=logging.INFO, format=log_format)

#     # Lista de datas a serem consideradas
#     datas = [datetime.now().date() + timedelta(days=d) for d in array_datas]

#     # URL base
#     base_url = "https://shopapp-montagem.azurewebsites.net/estados-unidos/orlando/seaworld?Id=58825&Busca=true&DataTemporada="

#     # Mapeamento de nomes desejados
#     mapeamento_nomes = {
#         "Ingresso 1 Dia SeaWorld - Adulto ou Criança": "1 Dia 1 Parque - SeaWorld Orlando",
#         "Super Combo Até 60% OFF (Por Dia) – 3 Dias de Parques – Escolha entre: SeaWorld, Busch Gardens e Aquatica – Adulto ou Criança": "3 Dias 3 Parques - SeaWorld Orlando",
#         "Super Combo Até 90% OFF – 14 Dias de Parques + Estacionamento Grátis – Escolha entre: SeaWorld, Busch Gardens e Aquatica – Adulto ou Criança": "14 Dias 3 Parques - SeaWorld Orlando"
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

#     nome_arquivo = f'seaworld_voupra_{datetime.now().strftime("%Y-%m-%d")}.json'
#     salvar_dados(df_merged, nome_arquivo, 'voupra', hora_global)

#     for filename in os.listdir('.'):
#         if filename.endswith(".json"):
#             os.remove(filename)
#             logging.info(f"Arquivo {filename} removido com sucesso.")

#     logging.info("Coleta de preços finalizada.")




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    asyncio.run(coletar_precos_voupra_sea())
