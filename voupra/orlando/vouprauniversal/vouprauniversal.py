from imports import *

from helpers.atualizar_calibragem import atualizar_calibragem
from webdriver_setup import get_webdriver
        
async def coletar_precos_voupra_universal(hora_global,array_datas,data_atual):
    datas = [datetime.now().date() + timedelta(days=d) for d in array_datas]
    logging.info("Iniciando coleta de preços Voupra Universal.")
    # Inicialize o driver do Selenium (certifique-se de ter o WebDriver correspondente instalado)
    driver = get_webdriver()
    #driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options)
    #driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub', options=options)
    
    # Lista para armazenar os dados dos produtos
    all_data_set = set()  # Usando um conjunto para armazenar dados únicos

    # Mapeamento dos nomes dos parques
    mapeamento_nomes = {
        369879: "1 Dia 1 Parque - Universal Orlando",
        369881: "1 Dia 2 Parques - Universal Orlando",
        361016: "2 Dias 2 Parques - Universal Orlando",
        379814: "5 Dias 2 Parques - Universal Orlando",
        352939: "4 Dias 2 Parques - Universal Orlando",
        361018: "14 Dias 3 Parques - Universal Orlando"
    }

    for data in datas:
        url = f"https://shopapp-montagem.azurewebsites.net/estados-unidos/orlando/universal-orlando?Id=53458&DataIngresso={data}&dump=true"
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
                if '1321/Views/CompraExpressa/_RTabelaCusto.cshtml' in script.text:
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
        data_insercao = query_params['DataIngresso'][0]
        data_viagem = "-".join(data_insercao.split('/')[::-1])

        # Itere sobre os produtos e adicione os dados ao conjunto
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

    
    nome_arquivo = f'universal_voupra_{data_atual}.json'
    
    salvar_dados(df, nome_arquivo,'orlando/voupra',hora_global)
    atualizar_calibragem(15)
    return
# async def coletar_precos_voupra_universal(hora_global,array_datas):
    
    
#     extract_data_and_return_dataframe(array_datas, hora_global)
    
#     options = webdriver.ChromeOptions()
#     driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options)
#     #driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub', options=options)
#     # Lista de datas a serem consideradas
#     datas = [datetime.now().date() + timedelta(days=d) for d in array_datas]

#     # URL base
#     base_url = "https://www.voupra.com/estados-unidos/orlando/universal-orlando?Id=53458&DataIngresso="

#     # Mapeamento de nomes desejados
#     mapeamento_nomes = {
#         "Ingresso 1 Dia Universal Orlando com 1 Parque – Adulto": "1 Dia 1 Parque - Universal Orlando",
#         "Ingresso 1 Dia Universal Orlando com 2 Parques – Adulto": "1 Dia 2 Parques - Universal Orlando",
#         "Ingresso 2 Dias Universal Orlando com 2 Parques – Adulto": "2 Dias 2 Parques - Universal Orlando",
#         "Super Combo 4 Dias Universal até 60% OFF (POR DIA) – Livre Acesso ao Universal Studios e Islands of Adventure – Adulto": "4 Dias 2 Parques - Universal Orlando",
#         "Super Combo 14 Dias Universal até 90% OFF (POR DIA) – Livre Acesso ao Universal Studios, Islands of Adventure e Volcano Bay – Adulto": "14 Dias 3 Parques - Universal Orlando"
#     }

#     dados = []

#     # Iniciar o loop pelas datas
#     for data in datas:
#         try:
#             # Montar a URL com a data atual do loop
#             url = base_url + data.strftime('%d%%2F%m%%2F%Y')
#             driver.get(url)
#             logging.info(f"Iniciando o processamento para a data: {data}")
#             logging.info(url)
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
#                     titulo = produto.find_element(By.CLASS_NAME,"produto_titulo")
                    
#                     titulo_texto = titulo.text
#                     titulo_texto = titulo_texto.strip()
#                     # Extraindo o preço do produto
#                     preco = produto.find_element(By.CLASS_NAME,"produto_preco_padrao")
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

#                 except NoSuchElementException as e:
#                     logging.warning("Elemento não encontrado:", e)
#             # Loop pelos nomes desejados
#             for nome, nome_desejado in mapeamento_nomes.items():
#                 if nome in precos:
#                     preco = precos[nome]
#                     preco_avista = round(preco * 0.9,2)
#                 else:
#                     preco = ''
#                     preco_avista = ''
#                 # Adicionar os dados à lista
#                 dados.append({
#                     'Data_viagem': data.strftime("%Y-%m-%d"),
#                     'Parque': nome_desejado,
#                     'Preco_Parcelado': preco,
#                     'Preco_Avista': preco_avista
                    
#                 })

#         except Exception as e:
#             logging.error("Erro ao processar data:", e)

#     # Fechar o driver
#     driver.quit()
    
#     # Criar um DataFrame com os dados
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
    
#     nome_arquivo = f'universal_voupra_{datetime.now().strftime("%Y-%m-%d")}.json'
#     salvar_dados(df_merged, nome_arquivo,'voupra',hora_global)
    
    
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    asyncio.run(coletar_precos_voupra_universal())
