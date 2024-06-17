from imports import *
from webdriver_setup import get_webdriver

# Inicialize o driver do Selenium (certifique-se de ter o WebDriver correspondente instalado)

#from atualizar_calibragem import atualizar_calibragem

async def coletar_precos_voupra_paris(hora_global,array_datas,data_atual):
    datas = [datetime.now().date() + timedelta(days=d) for d in array_datas]

    driver = get_webdriver()
    all_data_set = set()
    # Mapeamento dos nomes dos parques
    mapeamento_nomes = {
        329431: "1 Dia 1 Parque - Disney Paris",
        329472: "1 Dia 2 Parques - Disney Paris",
        329476: "2 Dias 2 Parques - Disney Paris",
        369974: "3 Dias 2 Parques - Disney Paris",
        369978: "4 Dias 2 Parques - Disney Paris",
    }

    for data in datas:
        url = f"https://shopapp-montagem.azurewebsites.net/europa/franca/disneyland-paris?Id=56310&Busca=true&DataTemporada={data}&dump=true"
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

    nome_arquivo = f'paris_voupra_{data_atual}.json'
    salvar_dados(df, nome_arquivo, 'paris/voupra', hora_global)
    
    #atualizar_calibragem(20)
    logging.info("Coleta de preços Voupra Paris  finalizada.")
    return

if __name__ == "__main__":
    # Hora global
    hora_global = datetime.now(pytz.timezone('America/Sao_Paulo'))
    data_atual = datetime.now().date()
    array_datas = [7, 14, 21, 28]
    asyncio.run(coletar_precos_voupra_sea(hora_global,array_datas,data_atual))
    #atualizar_calibragem(20)