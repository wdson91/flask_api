from imports import *
from salvardados import *
from helpers.atualizar_calibragem import atualizar_calibragem
from webdriver_setup import get_webdriver

async def coletar_precos_vmz_california(hora_global, array_datas,data_atual):
    logging.info("Iniciando coleta de preços de VMZ California.")
    
    # Configuração dos sites e URLs
    sites = [
        #("https://www.vmzviagens.com.br/ingressos/orlando/universal-orlando-resort/1-parque-1-dia-data-fixa?", "1 Dia - Disney California"),
        ("https://www.vmzviagens.com.br/ingressos/california/disneyland-california/disneyland-california-2-dias-basicos?", '2 Dias - Disney California'),
        ("https://www.vmzviagens.com.br/ingressos/california/disneyland-california/disneyland-california-3-dias-basicos?", '3 Dias - Disney California'),
        ("https://www.vmzviagens.com.br/ingressos/california/disneyland-california/disneyland-california-4-dias-basicos?", '4 Dias - Disney California'),
        #("https://www.vmzviagens.com.br/ingressos/california/disneyland-california/disneyland-california-4-dias-basicos?", '5 Dias - Disney California')
    ]
    url_14_dias = "https://www.vmzviagens.com.br/ingressos/orlando/universal-orlando-resort/14-dias-flexiveis-uso-em-2024?"
    
    # Configurações do WebDriver
    driver = get_webdriver()
    try:
        datas = [datetime.now().date() + timedelta(days=d) for d in array_datas]
        dados = []

        for data in datas:
            for url_template, parque in sites:
                logging.info(f"Coletando preços do parque {parque}.")
                site_url = f"{url_template}data={data.strftime('%Y-%m-%d')}"
                driver.get(site_url)

                preco_parcelado, preco_avista = extrair_precos(driver)
                
                dados.append({
                    'Data_viagem': data.strftime("%Y-%m-%d"),
                    'Parque': parque,
                    'Preco_Parcelado': preco_parcelado,
                    'Preco_Avista': preco_avista
                })

            # # Coleta de preços para 14 Dias 3 Parques - Universal Orlando
            # driver.get(url_14_dias)
            # preco_parcelado_14_dias, preco_avista_14_dias = extrair_precos(driver)
            # dados.append({
            #     'Data_viagem': data.strftime("%Y-%m-%d"),
            #     'Parque': '14 Dias 3 Parques - Universal Orlando',
            #     'Preco_Parcelado': preco_parcelado_14_dias,
            #     'Preco_Avista': preco_avista_14_dias
            # })

        # Criação do DataFrame e salvamento dos dados
        df = pd.DataFrame(dados)
        nome_arquivo = f'california_vmz_{data_atual}.json'
        salvar_dados(df, nome_arquivo, 'california/vmz', hora_global)
        #atualizar_calibragem(75)
        logging.info("Coleta finalizada Site Vmz- California.")

    finally:
        driver.quit()


def extrair_precos(driver):
    try:
        preco_parcelado_element = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/b')
        preco_avista_element = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/span[1]')
    except NoSuchElementException:
        # try:
        #     preco_parcelado_element = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/b')
        #     preco_avista_element = driver.find_element(By.XPATH, '//*[@id="__layout"]/div/div[1]/section/article[1]/div/div/div[4]/div[1]/div[2]/div[2]/span[1]')
        # except NoSuchElementException:
            preco_final_avista = preco_float = "-"
        # else:
        #     preco_parcelado = preco_parcelado_element.text.replace('R$ ', '').replace(',', '.')
        #     preco_float = float(preco_parcelado) * 10
        #     preco_final_avista = float(preco_avista_element.text.replace('R$ ', '').replace('.','').replace(',', '.'))
    else:
        preco_final_avista = float(preco_avista_element.text.replace('R$ ', '').replace('.','').replace(',', '.'))
        preco_parcelado = preco_parcelado_element.text.replace('R$ ', '').replace(',', '.')
        preco_float = float(preco_parcelado) * 10
    
    return preco_float, preco_final_avista


if __name__ == "__main__":
    asyncio.run(coletar_precos_vmz_california())
