from selenium.webdriver.remote.webelement import WebElement
from imports import *
from webdriver_setup import get_webdriver


async def coleta_tio_chip(hora_global,data_atual):# Inicializar o driver do Selenium
    logging.info("Iniciando coleta de preços Tio Orlando Chip.")
    #driver = get_webdriver()
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()

    # Lista para armazenar os dados
    dados = []
    dias = [5 ,10,14]
    driver.get('https://www.tioorlando.com.br/chip-de-celular')

    time.sleep(15)

    fisic_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="page-content"]/div[2]/div/div[2]/div/div/div/div[2]/div[3]/div/div[2]/button'))
        ).click()

    time.sleep(10)

    cep_input = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, ':r2:'))
        )
    cep_input.click()
    cep_input.send_keys('01311-200')

    cep_ok = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="page-content"]/div[2]/div/div[2]/div/div[2]/div/form/div/div[2]/button'))
        ).click()

    time.sleep(10)
    frete_normal = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="page-content"]/div[2]/div/div[2]/div/div[2]/div/div/div/table/tbody/tr[1]/td'))
        )

    frete = float(frete_normal.text.replace('R$','').replace(',','.'))

    virtual_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="page-content"]/div[2]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/button'))
        )
    virtual_button.click()

    time.sleep(10)

    data_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="page-content"]/div[2]/div/div[2]/div/div/div/div[2]/div[5]/div/div[1]/button'))
        )
    data_button.click()

    time.sleep(10)
    for dia in dias:

        logging.info(f"Coletando preços para {dia} dias - Tio Chip.")
        # Aguardar o carregamento do elemento

        try:
          inputDias: WebElement = WebDriverWait(driver, 20).until(
              EC.presence_of_element_located((By.XPATH, '//*[@id=":r4:"]'))
          )

          inputDias.click()

          opcao = driver.find_element(By.XPATH, f'//*[@role="option" and text()="{dia}"]')
          opcao.click()

          time.sleep(10)


          preco_a_vista = WebDriverWait(driver, 20).until(
              EC.element_to_be_clickable((By.CSS_SELECTOR, '#page-content > div.MuiContainer-root.MuiContainer-maxWidthLg.mui-2jualf > div > div:nth-child(2) > div > div > div > div.MuiBox-root.mui-0 > div.MuiBox-root.mui-1yjvs5a > div.MuiBox-root.mui-1yl4gnp > div.MuiBox-root.mui-148528'))
          ).text

          preco_parcelado = WebDriverWait(driver, 20).until(
              EC.element_to_be_clickable((By.CSS_SELECTOR, '#page-content > div.MuiContainer-root.MuiContainer-maxWidthLg.mui-2jualf > div > div:nth-child(2) > div > div:nth-child(1) > div > div.MuiBox-root.mui-0 > div.MuiBox-root.mui-1yjvs5a > div.MuiTypography-root.MuiTypography-body1.MuiBox-root.mui-zt93w0'))
          ).text

          preco_a_vista = float(preco_a_vista.replace('R$','').replace(',','.').strip())
          preco_final = float(preco_parcelado[preco_parcelado.find('R$') + 3:].split(' ')[0].replace('.','').replace(',','.'))
          preco_final_formatado = float(f'{preco_final:.2f}')* 12
          # print(preco_a_vista)
          # print(f'{float(preco_final)*12:.2f}')

          dados.append({
                      'Chip': 'eSIM ILI EUA',
                      'Data_Ativacao': datetime.now().date().strftime('%d-%m-%Y'),
                      'Dias':f'{dia} dias',
                      "Preco_Avista":  preco_a_vista,
                      "Preco_Parcelado": preco_final_formatado
                  })
          dados.append({
                      'Chip': 'CHIP ILI EUA',
                      'Data_Ativacao': datetime.now().date().strftime('%d-%m-%Y'),
                      'Dias':f'{dia} dias',
                      "Preco_Avista": preco_a_vista + frete,
                      "Preco_Parcelado": preco_final_formatado + frete
          })
        except Exception as e:
            logging.error(f"Erro ao coletar dados - Tio Orlando Chip: {e}")



    # Fechar o navegador após processar todos os dados
    driver.quit()
    # Salvar os dados em um arquivo JSON

    df = pd.DataFrame(dados)

    nome_arquivo = f'chip_tio_{data_atual}.json'

    salvar_dados(df, nome_arquivo, 'chip/tio', hora_global)
    logging.info("Coleta finalizada Site Tio Orlando - Chip.")
    return

if __name__ == '__main__':
    coleta_tio_chip()
    logging.info("Coleta de dados finalizada com sucesso.")
