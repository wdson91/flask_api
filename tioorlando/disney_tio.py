from imports import *
from webdriver_setup import get_webdriver


async def coleta_tio_orlando(hora_global,array_datas,data_atual):# Inicializar o driver do Selenium
    driver = get_webdriver()
    # Lista de datas para a coleta de dados
    array_datas = [10, 20, 47, 65, 126]
    datas = [datetime.now().date() + timedelta(days=d) for d in array_datas]

    # Função para fechar elemento bloqueador, se existir
    def fechar_elemento_bloqueador(driver):
        try:
            botao_fechar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="jivo_close_button"]/jdiv'))
            )
            botao_fechar.click()
        except TimeoutException:
            logging.info("Elemento bloqueador não encontrado ou não clicável - Disney Tio Orlando.")

    # Mapeamento dos nomes dos parques
    mapeamento_parques = {
        "Disney 1-Dia 1-Parque Aquático": "Magic Kingdom",
        "Disney 1-Dia no Animal Kingdom": "1 Dia - Disney Basico Animal Kingdom",
        "Disney 1-Dia no Hollywood Studios": "1 Dia - Disney Basico Hollywood Studios",
        "Disney 1-Dia no EPCOT": "1 Dia - Disney Basico Epcot",
        "Disney 1-Dia no Magic Kingdom": "1 Dia - Disney Basico Magic Kingdom",
        "Disney 1-Dia Park Hopper":"1 Dia - Disney Park Hopper",
        "Disney 1-Dia Park Hopper Plus":"1 Dia - Disney Parques Aquaticos",
        "Disney 2-Dias Básico": "2 Dias - Disney World Basico",
        "Disney 2-Dias Básico com Parque Aquático e Esportes Aquáticos": "Disney 2-Dias Básico com Parque Aquático e Esportes Aquáticos",
        "Disney 2-Dias Park Hopper": "2 Dias - Disney Park Hopper",
        "Disney 2-Dias Park Hopper Plus": "2 Dias - Disney Parques Aquaticos",
        "Disney 3-Dias Básico": "3 Dias - Disney World Basico",
        "Disney 3-Dias Básico com Parque Aquático e Esportes Aquáticos": "Disney 3-Dias Básico com Parque Aquático e Esportes Aquáticos",
        "Disney 3-Dias Park Hopper": "3 Dias - Disney Park Hopper",
        "Disney 3-Dias Park Hopper Plus": "3 Dias - Disney Parques Aquaticos",
        "Disney 4-Dias Básico": "4 Dias - Disney World Basico",
        "Disney 4-Park Magic": "4 Dias - Disney Promocional",
        "Disney 4-Park Magic + Water Park and Sports":"4 Dias - Disney Promocional com Aquatico e Esportes",
        "Disney 4-Dias Básico com Parque Aquático e Esportes Aquáticos": "Disney 4-Dias Básico com Parque Aquático e Esportes Aquáticos",
        "Disney 4-Dias Park Hopper": "4 Dias - Disney Park Hopper",
        "Disney 4-Dias Park Hopper Plus": "4 Dias - Disney Parques Aquaticos",
        "Disney 5-Dias Básico": "5 Dias - Disney World Basico",
        "Disney 5-Dias Básico com Parque Aquático e Esportes Aquáticos": "Disney 5-Dias Básico com Parque Aquático e Esportes Aquáticos",
        "Disney 5-Dias Park Hopper": "5 Dias - Disney Park Hopper",
        "Disney 5-Dias Park Hopper Plus": "5 Dias - Disney Parques Aquaticos",
        "Disney 6-Dias Básico": "6 Dias - Disney World Basico",
        "Disney 6-Dias Básico com Parque Aquático e Esportes Aquáticos": "Disney 6-Dias Básico com Parque Aquático e Esportes Aquáticos",
        "Disney 6-Dias Park Hopper": "6 Dias - Disney Park Hopper",
        "Disney 6-Dias Park Hopper Plus": "6 Dias - Disney Parques Aquaticos",
        "Disney 7-Dias Básico": "7 Dias - Disney World Basico",
        "Disney 7-Dias Básico com Parque Aquático e Esportes Aquáticos": "Disney 7-Dias Básico com Parque Aquático e Esportes Aquáticos",
        "Disney 7-Dias Park Hopper": "7 Dias - Disney Park Hopper",
        "Disney 7-Dias Park Hopper Plus": "7 Dias - Disney Parques Aquaticos",
        "Disney 8-Dias Básico": "8 Dias - Disney World Basico",
        "Disney 8-Dias Básico com Parque Aquático e Esportes Aquáticos": "Disney 8-Dias Básico com Parque Aquático e Esportes Aquáticos",
        "Disney 8-Dias Park Hopper": "8 Dias - Disney Park Hopper",
        "Disney 8-Dias Park Hopper Plus": "8 Dias - Disney Parques Aquaticos",
        "Disney 9-Dias Básico": "9 Dias - Disney World Basico",
        "Disney 9-Dias Básico com Parque Aquático e Esportes Aquáticos": "Disney 9-Dias Básico com Parque Aquático e Esportes Aquáticos",
        "Disney 9-Dias Park Hopper": "9 Dias - Disney Park Hopper",
        "Disney 9-Dias Park Hopper Plus": "9 Dias - Disney Parques Aquaticos",
        "Disney 10-Dias Básico": "10 Dias - Disney World Basico",
        "Disney 10-Dias Básico com Parque Aquático e Esportes Aquáticos": "Disney 10-Dias Básico com Parque Aquático e Esportes Aquáticos",
        "Disney 10-Dias Park Hopper": "10 Dias - Disney Park Hopper",
        "Disney 10-Dias Park Hopper Plus": "10 Dias - Disney Parques Aquaticos",
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

    # Lista para armazenar os dados
    dados = []
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
            while mes_desejado != mes_atual.text:

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
                    logging.info("Não foi possível encontrar o botão de navegação ou clicar nele. - Disney Tio Orlando")
                    break

            time.sleep(3)

            seletor_dia = f".react-datepicker__day--0{dia}"

            try:
                # Aguardar até que o elemento correspondente ao dia desejado esteja clicável na página
                # elemento_dia = WebDriverWait(driver, 5).until(
                #     EC.element_to_be_clickable((By.CSS_SELECTOR, seletor_dia))
                # )

                elemento_dias = driver.find_elements(By.CSS_SELECTOR,seletor_dia)

                if int(dia) > 20:
                    elemento_dia = elemento_dias[-1]
                else:
                    elemento_dia = elemento_dias[0]
                #driver.execute_script("arguments[0].scrollIntoView();", elemento_dia)
                # Clicar no elemento correspondente ao dia desejado
                elemento_dia.click()

            except TimeoutException:
                logging.info(f"Não foi possível clicar no dia {dia} - Disney Tio Orlando.")
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

    driver.get('https://www.tioorlando.com.br/disney-4-park-magic')

    time.sleep(5)

    await coleta(datas)
    for i in range(1, 11):
        driver.get('https://www.tioorlando.com.br/ingressos-disney-orlando')

        # Aguardar o carregamento do elemento
        elemento = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f'//*[@id="page-content"]/div[2]/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[{i}]/button'))
        )

        # Clicar no botão
        elemento.click()
        await coleta(datas)

    # Fechar o navegador após processar todos os dados
    driver.quit()
    # Salvar os dados em um arquivo JSON


    df = pd.DataFrame(dados)

    nome_arquivo = f'disney_tio_{data_atual}.json'

    salvar_dados(df, nome_arquivo, 'orlando/tio', hora_global)
    logging.info('Coleta Finalizada Disney Tio Orlando')
    return

