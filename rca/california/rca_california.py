
from imports import *
from salvardados import salvar_dados

porcentagem_parcelado = 1.1417 # 14,17% de acréscimo
porcentagem_avista = 0.97 # 3% de desconto
async def coletar_precos_california_rca(hour, array_datas,data_atual):
    
    array_datas = [5,10,20,47,65,126]

    df1 = await coletar_precos_california_rca1(array_datas)
    df2 = await coletar_precos_california_rca2(array_datas)
    
    df = pd.DataFrame(df1 + df2)
    
    df = df.drop_duplicates()
    df = df.sort_values(by=['Data_viagem', 'Parque'])
    
    
    # Exibir o DataFrame mesclado
    nome_arquivo = f'california_rca_{data_atual}.json'
    #df.to_json('california_rca2.json', orient='records', lines=True)
    
    salvar_dados(df, nome_arquivo,'california/rca',hour)



async def coletar_precos_california_rca2(array_datas):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    urls = [
        ("2 Dias - Disney California", "https://www.ingressosrca.com.br/parques-tematicos/disneyland-california/disneyland-california-2-dias-basico-2015.html"),
        ("3 Dias - Disney California", "https://www.ingressosrca.com.br/parques-tematicos/disneyland-california/disneyland-california-3-dias-basico-ingresso-eletronico.html"),
        ("4 Dias - Disney California", "https://www.ingressosrca.com.br/parques-tematicos/disneyland-california/disneyland-california-4-dias-basico-ingresso-eletronico.html"),
        ("5 Dias - Disney California", "https://www.ingressosrca.com.br/parques-tematicos/disneyland-california/disneyland-california-5-dias-basico-ingresso-eletronico.html")
    ]

    all_data = []

    for park_name, url in urls:
        driver.get(url)
        time.sleep(2)
        
        element = driver.find_element(By.XPATH, '//*[@id="datautilizacao-container"]/tbody/tr/td[3]/script')
        script_text = element.get_attribute("textContent")
        
        # Procurar o padrão do preço no script
        price_pattern = r'"base_price":\s*(\d+\.\d+)'
        match = re.search(price_pattern, script_text)
        if match:
            desired_price = float(match.group(1))  # Convertendo a string para um número float
        else:
            desired_price = None

        # Datas desejadas
        today = datetime.now().date()
        desired_days = [today + timedelta(days=offset) for offset in array_datas]

        # Verificando se o preço foi encontrado antes de criar os dados
        if desired_price is not None:
            # Criar o JSON com as datas desejadas e o preço coletado
            data = [{'Data_viagem': str(date), 
                    'Parque': park_name, 
                    'Preco_Parcelado': round(desired_price * porcentagem_parcelado, 2), 
                    'Preco_Avista': round(desired_price * porcentagem_avista, 2)} for date in desired_days]

            all_data.extend(data)
        else:
            print("Preço desejado não encontrado.")


    return all_data

def serialize_datetime(obj):
    """Função de serialização personalizada para objetos datetime."""
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d')  # Formatar apenas a data
    raise TypeError(f"Type {type(obj)} not serializable")

def convert_timestamp_to_datetime(timestamp: int) -> datetime:
    """Função para converter timestamp em objeto datetime."""
    return datetime.fromtimestamp(timestamp / 1000)

async def coletar_precos_california_rca1(array_datas):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    urls = [
        ("1 Dia - Disney California", "https://www.ingressosrca.com.br/parques-tematicos/disneyland-california/disneyland-california-1-dia-basico-eletronico.html"),
        ("1 Dia - Disney California", "https://www.ingressosrca.com.br/parques-tematicos/disneyland-california/disneyland-california-1-dia-basico-tier-1.html"),
        ("1 Dia - Disney California", "https://www.ingressosrca.com.br/parques-tematicos/disneyland-california/disneyland-california-1-dia-basico-nivel-2.html"),
        ("1 Dia - Disney California", "https://www.ingressosrca.com.br/parques-tematicos/disneyland-california/disneyland-california-1-dia-basico-nivel-3.html"),
        ("1 Dia - Disney California", "https://www.ingressosrca.com.br/parques-tematicos/disneyland-california/disneyland-california-1-dia-basico-nivel-4.html"),
        ("1 Dia - Disney California", "https://www.ingressosrca.com.br/parques-tematicos/disneyland-california/disneyland-california-1-dia-basico-nivel-5.html"),
        ("1 Dia - Disney California", "https://www.ingressosrca.com.br/parques-tematicos/disneyland-california/disneyland-california-1-dia-basico-nivel-6.html")
    ]

    # Datas desejadas
    today = datetime.now().date()
    desired_days = [today + timedelta(days=offset) for offset in array_datas]

    all_rules = []
    for park_name, url in urls:
            driver.get(url)
            
            time.sleep(2)
            
            element = driver.find_element(By.XPATH, '//*[@id="datautilizacao-container"]/tbody/tr/td[3]/script')
            script_text = element.get_attribute("textContent")
            
            regex_pattern = r"dateRestrinctionsDate\[\d+\] = ({.*?});"
            matches = re.findall(regex_pattern, script_text)
            
            for match in matches:
                match_json = json.loads(match)
                for key, value in match_json.items():
                    if 'datePrice' in value:
                        for rule in value['datePrice']['rules']:
                            
                            rule_date = rule['final_date'] / 1000
                            rule_date = datetime.fromtimestamp(rule_date)  # Converter timestamp para datetime
                            rule_date_mais_um_dia = rule_date + timedelta(days=1)
                            all_rules.append({
                                'Data_viagem': rule_date_mais_um_dia.strftime('%Y-%m-%d'),  # Converter a data para timestamp
                                'Parque': park_name,
                                'Preco_Parcelado': round(float(rule['base_price']* porcentagem_parcelado)),
                                'Preco_Avista': round(float(rule['base_price'] * porcentagem_avista))
                            })

    driver.quit()
    return all_rules


if __name__ == "__main__":
    import asyncio
    asyncio.run(coletar_precos_california_rca(1, [5,10,20,47,65,126], '2022-12-31'))
