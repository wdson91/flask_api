from imports import *
from webdriver_setup import get_webdriver


async def coleta_tio_universal(hora,array_datas,data_atual):# Inicializar o driver do Selenium
    logging.info("Iniciando coleta de preços Tio Orlando Universal.")
    driver = get_webdriver()
    # Lista de datas para a coleta de dados
    array_datas = [10, 20, 47, 65, 126]
    datas = [datetime.now().date() + timedelta(days=d) for d in array_datas]
    dados = []
    # Função para fechar elemento bloqueador, se existir
    def fechar_elemento_bloqueador(driver):
        try:
            botao_fechar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="jivo_close_button"]/jdiv'))
            )
            botao_fechar.click()
        except TimeoutException:
            logging.error("Elemento bloqueador não encontrado ou não clicável - Universal Tio Orlando.")

    # Mapeamento dos nomes dos parques
    mapeamento_parques = {
        "Universal 1-Dia 1-Park Base": "1 Dia 1 Parque - Universal Orlando",
        "Universal 1-Dia 2-Parks Park-to-Park": "1 Dia 2 Parques - Universal Orlando",
        "Universal 2-Dias 2-Parks Park-to-Park": "2 Dias 2 Parques - Universal Orlando",
        "PROMO: Universal 2-Park Play 4-Dias": "4 Dias 2 Parques - Universal Orlando",
        "Universal 14-Dias 3-Park Explorer Park-to-Park – 2024":"14 Dias 3 Parques - Universal Orlando",
        "PROMO: Universal 2-Park 3-Dias + 2-Dias GRÁTIS!":"5 Dias 2 Parques - Universal Orlando"
    }

    # Mapeamento dos meses em português
    nomes_meses_pt_BR = {
        1: "janeiro",
        2: "fevereiro",
        3: "março",
        4: "abril",
        5: "maio",
        6: "junho",
        7: "julho",
        8: "agosto",
        9: "setembro",
        10: "outubro",
        11: "novembro",
        12: "dezembro"
    }
    
    async def coleta(datas):
        # Aguardar a presença do elemento do mês atual
        mes_atual = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "react-datepicker__current-month"))
        )
        
        for data in datas:
            mes = nomes_meses_pt_BR[data.month]
            ano = data.year
            
            dia = data.day
            if dia < 10:
                dia = f"0{dia}"
            mes_desejado = f'{mes} {ano}'
            
            # Verificar se o mês atual é diferente do desejado
            while mes_desejado not in mes_atual.text:
                try:
                    # Se não for, clicar no botão de navegação "next"
                    botao_next = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "react-datepicker__navigation--next"))
                    )
                    try:
                        # Tenta clicar no botão de navegação
                        botao_next.click()
                    except ElementClickInterceptedException:
                        # Se o clique for interceptado, usa JavaScript para clicar
                        driver.execute_script("arguments[0].click();", botao_next)
                    
                    # Aguardar a atualização do mês atual
                    mes_atual = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "react-datepicker__current-month"))
                    )
                except TimeoutException:
                    logging.error("Não foi possível encontrar o botão de navegação ou clicar nele. - Universal Tio Orlando.")
                    break

            time.sleep(5)

            seletor_dia = f".react-datepicker__day--0{dia}"
            try:
                # Aguardar até que o elemento correspondente ao dia desejado esteja clicável na página
                elemento_dia = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, seletor_dia))
                )

                # Clicar no elemento correspondente ao dia desejado
                elemento_dia.click()
                
            except TimeoutException:
                logging.error(f"Não foi possível clicar no dia {dia} - Universal Tio Orlando.")
                continue

            time.sleep(7)
            
            # Encontrar todos os elementos com a classe 'MuiBox-root mui-7ulwng'
            elementos = driver.find_elements(By.CLASS_NAME, 'MuiBox-root.mui-7ulwng')

            # Iterar sobre os elementos
            for elemento in elementos:
                # Encontrar o título dentro do elemento atual
                titulo = elemento.find_element(By.CLASS_NAME, 'MuiTypography-root.MuiTypography-body2.mui-1sgqvsm').text
                # Encontrar o preço dentro do elemento atual
                preco_a_vista = elemento.find_element(By.CLASS_NAME, 'MuiBox-root.mui-1ahotr9').text
               
                preco_a_vista = float(preco_a_vista.replace("R$", "").replace(".", "").replace(",", ".").strip())
                preco = elemento.find_elements(By.CLASS_NAME, 'MuiBox-root.mui-sw026l')
                # Dividir a string pelo espaço em branco
                partes = preco[2].text.split()
                
                # Remover o valor desejado
                preco_parcelado = float(partes[-1].replace('R$', '').replace(',', '.'))
                # Calcula o preço parcelado
                parque = titulo.split(' - ', 1)[0]
               
                # Mapear o nome do parque para o nome completo
                parque = mapeamento_parques.get(parque, titulo)

                dados.append({
                    'Data_viagem': data.strftime('%Y-%m-%d'),
                    'Parque': parque,
                    "Preco_Avista": preco_a_vista,
                    "Preco_Parcelado": preco_parcelado * 12
                })
                
    #Lista para armazenar os dados
    

    driver.get('https://www.tioorlando.com.br/promo-universal-orlando')
    logging.info("Coletando dados do site Tio Orlando - Universal Orlando.")
    time.sleep(5)
    
    await coleta(datas)
    
    for i in range(1, 5):
        logging.info(f"Coletando dados do site Tio Orlando - Universal Orlando dia {i}.")
        driver.get('https://www.tioorlando.com.br/ingressos-universal-orlando')

        # Aguardar o carregamento do elemento
        elemento = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f'//*[@id="page-content"]/div[2]/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[{i}]/button'))
        )

        # Clicar no botão
        elemento.click()
        
        time.sleep(5)
        
        await coleta(datas)    
    #Fechar o navegador após processar todos os dados
    driver.quit()
    # Salvar os dados em um arquivo JSON
  
    df = pd.DataFrame(dados)
    
    nome_arquivo = f'universal_tio_{data_atual}.json'
    
    salvar_dados(df, nome_arquivo, 'orlando/tio', hora)
    
    logging.info("Coleta finalizada Site Tio Orlando - Universal Orlando.")
    return
    
if __name__ == '__main__':
    coleta_tio_universal()
    logging.info("Coleta de dados finalizada com sucesso.")