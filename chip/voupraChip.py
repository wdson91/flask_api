from imports import *
from helpers.atualizar_calibragem import atualizar_calibragem
from webdriver_setup import get_webdriver

async def coletar_precos_voupra_chip(hora_global,data_atual):

    data_inicial  =  datetime.now().date()
    intervalos_de_dias = [5, 10,14,0]
    datas = [(data_inicial + timedelta(days=d)).strftime('%d-%m-%Y') for d in intervalos_de_dias]

    logging.info("Iniciando coleta de preços Chip Voupra.")
    driver = get_webdriver()
    #driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options)
    #driver = webdriver.Remote(command_executor='http://selenium-hub:4444/wd/hub', options=options)

    # Lista para armazenar os dados dos produtos
    all_data_set = set()  # Usando um conjunto para armazenar dados únicos

    # Mapeamento dos nomes dos parques
    mapeamento_nomes = {
        375472: "CHIP ILI EUA",
        375473: "CHIP ILI EUROPA",
        376828: "eSIM ILI EUA",
        376827: "eSIM ILI EUROPA",
    }


    for i in range(len(datas) -1 ):
      data_ida = data_inicial.strftime('%d-%m-%Y')
      data_retorno = datas[i]
      url_base = "https://shopapp-montagem.azurewebsites.net/chip-internacional?Id=55832"
      url = f"{url_base}&DataIda={data_ida}&DataRetorno={data_retorno}&dump=true"
      time.sleep(2)
      data_ida_calculo = datetime.strptime(data_ida, '%d-%m-%Y')
      data_retorno_calculo = datetime.strptime(data_retorno, '%d-%m-%Y')
      # Calcular a diferença em dias
      diferenca_dias = (data_retorno_calculo - data_ida_calculo).days
      print(f"Coletando preços para {diferenca_dias} dias.")
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
              if '1321/Views/CompraExpressa/_RCustoPorDia.cshtml' in script.text:
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
      data_insercao = query_params['DataIda'][0]
      #data_viagem = "-".join(data_insercao.split('/')[::-1])

      for produto in produtos:
          id = produto['Id']
          #margem = produto['Margem']
          preco_Avista = produto['ParcelaAVistaPadrao']['ValorTotal']
          preco_Parcelado = produto['ParcelasPadrao'][1]['ValorTotal']
          data_retorno = data_retorno
          # Verificar se 'Margem' é um número válido
          dias = f'{diferenca_dias} dias'
          # Verifique se o parque está no mapeamento
          if id in mapeamento_nomes:
              # Mapeie o nome do parque
              id = mapeamento_nomes[id]

              # Adicione os dados ao conjunto
              all_data_set.add(( id,data_ida,dias, preco_Avista, preco_Parcelado))

    # Feche o navegador
    driver.quit()

    # Converter o conjunto de tuplas em uma lista de dicionários
    all_data = [
        {

            'Chip': parque,
            'data_ativacao': data_ida,
            'dias':dias,
            "Preco_Avista": preco_Avista,
            "Preco_Parcelado": preco_Parcelado
        }
        for ( parque,data_ida,dias , preco_Avista, preco_Parcelado) in all_data_set
    ]

    # Create a JSON from the collected data
    #json_data = json.dumps(all_data)

    df = pd.DataFrame(all_data)

    # Exibir o DataFrame mesclado
    #df = df.drop_duplicates()


    nome_arquivo = f'chip_voupra_{data_atual}.json'
    salvar_dados(df, nome_arquivo, 'chip/voupra', hora_global)



    logging.info("Coleta de preços Voupra Chip  finalizada.")
    return



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    asyncio.run(coletar_precos_voupra_chip())
