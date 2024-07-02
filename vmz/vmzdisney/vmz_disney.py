from classes.junta_dados_classe import JuntarJsons
from imports import *
from salvardados import *
from helpers.atualizar_calibragem import atualizar_calibragem

from webdriver_setup import get_webdriver

async def coletar_precos_vmz(hora_global,array_datas,data_atual) -> None:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    # Defina sua lógica para baixar os arquivos e esperar por eles
    baixar_blob_se_existir('disney_vmz_basicos_parcial.json', 'orlando/vmz')
    baixar_blob_se_existir('disney_vmz_dias_parcial.json', 'orlando/vmz')

    # Carregue os dados do JSON baixado
    disney_basicos = carregar_dados_json('disney_vmz_basicos_parcial.json')
    disney_dias = carregar_dados_json('disney_vmz_dias_parcial.json')


    # Combine os dados de disney_basicos e disney_dias
    dados_combinados = disney_basicos[-1]["Dados"] + disney_dias[-1]["Dados"]


    df = pd.DataFrame(dados_combinados)

    df_sorted = df.sort_values(by=['Data_viagem', 'Parque'], ignore_index=True)
    # # Crie o DataFrame a partir dos dados formatados
    # df = pd.DataFrame(dados_formatados)

    nome_arquivo = f'disney_vmz_{data_atual}.json'

    salvar_dados(df_sorted, nome_arquivo, 'orlando/vmz', hora_global)


    logging.info("Coleta finalizada. Vmz Disney.")
    atualizar_calibragem(65)
    return


async def coletar_precos_vmz_disneybasicos(array_datas,hora_global,data_atual):
    logging.info("Iniciando coleta de preços Vmz Disney Basicos.")
    driver = get_webdriver()


    sites = [
    ("https://www.vmzviagens.com.br/ingressos/orlando/disney-world-ingresso/disney-ingresso-magic-kingdom-1dia?", '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/span[1]', '1 Dia - Disney Basico Magic Kingdom'),
    ("https://www.vmzviagens.com.br/ingressos/orlando/disney-world-ingresso/epcot?",  '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/span[1]', '1 Dia - Disney Basico Epcot'),
    ("https://www.vmzviagens.com.br/ingressos/orlando/disney-world-ingresso/disney-ingresso-hollywood-studios-1dia?", '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/span[1]', '1 Dia - Disney Basico Hollywood Studios'),
    ("https://www.vmzviagens.com.br/ingressos/orlando/disney-world-ingresso/disney-ingresso-animal-kingdom-1dia?", '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/span[1]', '1 Dia - Disney Basico Animal Kingdom'),
    ("https://www.vmzviagens.com.br/ingressos/orlando/promocao-disney-world-4-park-magic/4-park-magic?", '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[3]/div[2]/span[1]', '4 Dias - Disney Promocional'),
    ("https://www.vmzviagens.com.br/ingressos/orlando/promocao-disney-world-4-park-magic/4-park-magic-com-parque-aquatico-e-esportes?",'//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/span[1]',"4 Dias - Disney Promocional com Aquatico e Esportes")
    # Adicione outros sites, XPaths e nomes de parques conforme necessario
]

    # Definindo as datas
    datas = [datetime.now().date() + timedelta(days=d) for d in array_datas]

    # Lista para armazenar os dados
    dados = []

    # Percorrer cada site e coletar preços
    for site_url, xpath_selector, parque_nome in sites:
        for data in datas:
            logging.info(f"Coletando preços para {parque_nome} na data: {data} Vmz Basicos.")
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

    logging.info("Coleta de preços finalizada Vmz Basicos.")
    driver.quit()
    # Criando um DataFrame
    df = pd.DataFrame(dados)
    salvar_dados(df, 'disney_vmz_basicos_parcial.json','orlando/vmz',hora_global)


    atualizar_calibragem(40)
    return

async def coletar_precos_vmz_disneydias(dias_para_processar,array_datas,hora_global,data_atual):
    waiter = 2
    logging.info("Iniciando coleta de preços Vmz Disney Dias.")
    driver = get_webdriver()
    #driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    nome_pacotes = {
        2: "2 Dias - Disney World Basico",
        3: "3 Dias - Disney World Basico",
        4: "4 Dias - Disney World Basico",
        5: "5 Dias - Disney World Basico",
        6: "6 Dias - Disney World Basico",
        7: "7 Dias - Disney World Basico",
        8: "8 Dias - Disney World Basico",
        9: "9 Dias - Disney World Basico",
        10: "10 Dias - Disney World Basico",
    }
    def fechar_popups(driver):
        try:
            botao_fechar_selector = '//*[@id="rd-close_button-lxyz9zz9"]'
            botao_fechar = WebDriverWait(driver, waiter + 5).until(
                EC.visibility_of_element_located((By.XPATH, botao_fechar_selector))
            )
            botao_fechar.click()
            botao_cookies = WebDriverWait(driver, waiter + 3).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[3]/div/div/div[2]/button'))
            )
            botao_cookies.click()

            logging.info("Pop-up fechado. Vmz Disney Dias.")
        except Exception as e:
            logging.warning(f"Popup não encontrada - {e} Vmz Disney Dias.")

    def scroll_to_element(driver):
        element = driver.find_element(By.XPATH,'//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[3]/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]')
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(3)
        fechar_popups(driver)

    def mudar_mes_ano(driver, mes, ano):
        try:
            # Espera até que o seletor do ano esteja clicável
            year_select = WebDriverWait(driver, waiter + 20).until(EC.element_to_be_clickable((By.ID, "year-control")))

            # Lê o ano atual selecionado
            ano_atual = year_select.get_attribute("value")

            # Verifica se o ano atual é o mesmo que o ano desejado
            if ano_atual != ano:
                year_select.click()

                # Seleciona o ano desejado
                driver.find_element(By.CSS_SELECTOR, f'option[value="{ano}"]').click()

            # Espera até que o seletor do mês esteja clicável
            month_select = WebDriverWait(driver, waiter).until(EC.element_to_be_clickable((By.ID, "month-control")))

            # Lê o mês atual selecionado
            mes_atual = month_select.get_attribute("value")

            # Verifica se o mês atual é o mesmo que o mês desejado
            if mes_atual != mes:
                # Seleciona o mês desejado
                month_select.click()
                driver.find_element(By.CSS_SELECTOR, f'option[value="{mes}"]').click()

            logging.info(f"Mudança para mês {mes} e ano {ano} realizada com sucesso. - Vmz Disney Dias.")
        except Exception as e:
            logging.error(f"Erro ao mudar mês e ano - Vmz Disney Dias: {e}")


    def encontrar_preco_data(driver, data):
        try:
            wait = WebDriverWait(driver, 30)  # Espera de até 30 segundos
            # Aguarda até que o calendário seja clicável ou visível
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'fc-content')))
            elementos_fc_content = driver.find_elements(By.CLASS_NAME, 'fc-content')
            for elemento in elementos_fc_content:
                fc_date = elemento.find_element(By.CLASS_NAME, 'fc-date').text
                if fc_date == str(data.day):
                    calendar_event_price = elemento.find_element(By.CLASS_NAME, 'calendar-event-price')
                    price_text = calendar_event_price.text.strip()
                    preco_avista = float(price_text.replace('R$', '').replace('.', '').replace(',', '.').strip())
                    preco_parcelado = round(preco_avista * 1.087,2)

                    return preco_avista, preco_parcelado
        except Exception as e:
            logging.error(f"Erro ao encontrar preço para data {data}: {e} - Vmz Disney Dias.")
            return None

    def processar_dias(driver, dias,array_datas):
        base_url = "https://www.vmzviagens.com.br/ingressos/orlando/walt-disney-orlando/ticket-disney-basico"
        datas = [datetime.now() + timedelta(days=d) for d in array_datas]
        dados = []

        for dia in dias:
            logging.info(f"Coletando preços para {dia} dias - Vmz Disney Dias.")
            nome_pacote = nome_pacotes.get(dia, f"{dia} Dias - Desconhecido")
            url_com_dias = f"{base_url}?mes=2024-01&dias={dia}"
            driver.get(url_com_dias)
            time.sleep(5)

            scroll_to_element(driver)

            for data in datas:
                mes = data.month - 1
                ano = data.year
                mudar_mes_ano(driver, mes, ano)
                time.sleep(7)  # Espera para a mudança de mês e ano acontecer
                preco_avista,preco_parcelado = encontrar_preco_data(driver, data)
                if preco_avista:

                    dados.append({
                        'Data_viagem': data.strftime("%Y-%m-%d"),
                        'Parque': nome_pacote,
                        'Preco_Parcelado': preco_parcelado,
                        'Preco_Avista': preco_avista
                    })
                else:
                    logging.warning(f"Preço não encontrado para {nome_pacote} em {data} - Vmz Disney Dias.")

        return dados  # Return the 'dados' list

    dias_para_processar = [2,3,4,5,6,7,8,9,10]
    resultados = processar_dias(driver, dias_para_processar,array_datas)



    df = pd.DataFrame(resultados)
    salvar_dados(df,'disney_vmz_dias_parcial.json','orlando/vmz',hora_global)
    driver.quit()
    logging.info("Coleta de preços finalizada Vmz Disney Dias.")
    await coletar_precos_vmz(hora_global,array_datas,data_atual)
    atualizar_calibragem(60)

    time.sleep(10)


    try:
            empresas = ['voupra', 'vmz', 'decolar','ml','tio','fastPass']
            parques = ['disney', 'universal', 'seaworld']

            juntar_json = JuntarJsons(data_atual, empresas, parques, 'orlando')

            await juntar_json.executar()

    except Exception as e:
            logging.error(f"Erro durante a junção dos arquivos: {e}")

    return


if __name__ == "__main__":
    df_final = asyncio.run(coletar_precos_vmz())
