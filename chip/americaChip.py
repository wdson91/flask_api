from helpers.atualizar_calibragem import finalizar_chip
from imports import *

from salvardados import salvar_dados
from webdriver_setup import get_webdriver




def limparCarrinho(driver):

    itens = driver.find_elements(By.CLASS_NAME, 'woocommerce-cart-form__cart-item')

    if len(itens) > 1:
      driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div[2]/div[2]/div[1]/form/div/table/tbody/tr[1]/td[1]/a').click()
      time.sleep(5)
    return

def formulario(driver):
    time.sleep(2)

    email_element = driver.find_element(By.XPATH, '//*[@id="billing_email"]')
    email_element.clear()  # Limpar campo antes de enviar novos dados
    email_element.send_keys('teste@tese.com')

    first_name_element = driver.find_element(By.XPATH, '//*[@id="billing_first_name"]')
    first_name_element.clear()
    first_name_element.send_keys('teste')

    last_name_element = driver.find_element(By.XPATH, '//*[@id="billing_last_name"]')
    last_name_element.clear()
    last_name_element.send_keys('teste')

    postcode_element = driver.find_element(By.XPATH, '//*[@id="billing_postcode"]')
    postcode_element.clear()
    postcode_element.send_keys('42707-850')

    shipping_number_element = driver.find_element(By.XPATH, '//*[@id="shipping_number"]')
    shipping_number_element.clear()
    shipping_number_element.send_keys('25')

    phone_element = driver.find_element(By.XPATH, '//*[@id="billing_phone"]')
    phone_element.clear()
    phone_element.send_keys('1212121-2121')

    cpf_element = driver.find_element(By.XPATH, '//*[@id="shipping_CPF"]')
    cpf_element.clear()
    cpf_element.send_keys('030.111.111-11')

    # Rolar a tela até o elemento desejado
    tela = driver.find_element(By.XPATH, '/html/body/div[1]/footer/div[1]')
    driver.execute_script("arguments[0].scrollIntoView();", tela)
    time.sleep(3)

    # Clicar no botão de ordem (place order)
    driver.find_element(By.XPATH, '//*[@id="place_order-next"]').click()


    return


def coletarPrecos(driver):



    driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div/form/div/div[1]/div[2]/div[2]/ul/li[2]/label').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div/form/div/div[1]/div[2]/div[2]/ul/li[2]/div/div[1]/section/div/div/section[4]/span/span[1]/span').click()
    time.sleep(3)
    input = driver.find_element(By.XPATH, '/html/body/span/span/span[1]/input')
    input.send_keys('6x')
    input.send_keys(Keys.ENTER)
    time.sleep(3)

    precoParcelado = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div/form/div/div[1]/div[2]/div[2]/ul/li[2]/div/div[2]/span[2]/strong/span').text

    time.sleep(5)


    inputAvista = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div/form/div/div[1]/div[2]/div[2]/ul/li[3]/label').click()
    time.sleep(2)
    precoPix = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div/form/div/div[1]/div[2]/div[2]/ul/li[3]/div/div[2]/span[2]/strong/span').text


    time.sleep(5)

    return precoParcelado,precoPix

def coletarPrecosChip(driver):
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[2]/div/form/div/div[1]/div[3]/div[2]/ul/li[3]/label'))).click()
    time.sleep(2)
    precoPix = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/div[2]/div/form/div/div[1]/div[3]/div[2]/ul/li[3]/div/div[2]/span[2]/strong/span'))).text
    precoPix = precoPix.replace('R$','').replace('.','').replace(',','.')

    time.sleep(5)

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="payment"]/ul/li[2]/label'))).click()
    time.sleep(1)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,  '/html/body/div[1]/main/div[2]/div/form/div/div[1]/div[3]/div[2]/ul/li[2]/div/div[1]/section/div/div/section[4]/span/span[1]/span'))).click()
    time.sleep(3)
    input = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,  '/html/body/span/span/span[1]/input')))
    input.send_keys('6x')
    input.send_keys(Keys.ENTER)
    time.sleep(3)

    precoParcelado = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="converted-amount"]/strong/span'))).text
    precoParcelado = precoParcelado.replace('R$','').replace('.','').replace(',','.')
    time.sleep(3)



    return precoParcelado,precoPix


def escolerDiaeData(driver,data,local):

    if local == 'eua':
        elemento = driver.find_elements(By.CLASS_NAME, "calendario")[0]
        xpath_button = "/html/body/div[1]/main/main/section[13]/ul/li[1]/div/div[1]/form/div/div/div/div/button"
    elif local == 'europa':
      elemento = driver.find_elements(By.CLASS_NAME, "calendario")[1]
      xpath_button = "/html/body/div[1]/main/main/section[13]/ul/li[2]/div/div[1]/form/div/div/div/div/button"
    else:
      elemento = driver.find_elements(By.CLASS_NAME, "calendario")[0]
      xpath_button = "/html/body/div[1]/main/main/section[1]/div[3]/ul/li[1]/div[2]/form/div/div[1]/button"
    driver.execute_script("arguments[0].setAttribute('value', arguments[1])", elemento, data)
    time.sleep(3)

    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath_button))).click()

    limparCarrinho(driver)

    time.sleep(3)

    continuar = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/main/div[2]/div/div[2]/div[2]/div/div[1]/div/a")))
    driver.execute_script("arguments[0].scrollIntoView()", continuar)

    continuar.click()

    return





async def esim_eua_europa(hora_global,data_atual):# -> list:
    # Inicializar o navegador (neste exemplo, estamos usando o Chrome)
    #driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    await asyncio.sleep(1)
    dados = []
    driver = get_webdriver()
    # Maximizar a janela do navegador
    driver.maximize_window()
    driver.delete_all_cookies()

    locais = [('eua','//*[@id="numero-de-dias"]')
                    ,('europa','//*[@id="escolha-o-numero-de-dias"]')]
    data = datetime.now().date().strftime('%d-%m-%Y')
    #select_element = driver.find_element(By.XPATH, '//*[@id="numero-de-dias"]')
    for local,xpath in locais:
      for option_value in ['5 dias', '10 dias', '14 dias']:
              driver.get("https://americachip.com/esim/#product-form-75163")
              select_element= WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath )))

              option = select_element.find_element(By.XPATH, f".//option[text()='{option_value}']")
              option.click()

              time.sleep(3)

              escolerDiaeData(driver,data,local)

              time.sleep(3)

              formulario(driver)

              time.sleep(3)

              precoParcelado,precoPix = coletarPrecos(driver)

              time.sleep(3)

              dados.append({
                  'Chip': 'eSIM ILI EUA' if local == 'eua' else 'eSIM ILI Europa',
                  'data_ativacao': data,
                  'dias': option_value,
                  'preco_parcelado': float(precoParcelado.replace('R$','').replace('.','').replace(',','.')),
                  'preco_a_vista': float(precoPix.replace('R$','').replace('.','').replace(',','.'))
              })
              # Fechar o navegador

    driver.quit()


    df = pd.DataFrame(dados)
    nome_arquivo = f'esim_america_{data_atual}.json'
    salvar_dados(df, nome_arquivo, 'chip/america', hora_global)
    time.sleep(5)
    finalizar_chip()
    return



async def chip_eua_europa(hora_global,data_atual):

  #driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    # Maximizar a janela do navegador

  driver = get_webdriver()
  driver.maximize_window()
  driver.delete_all_cookies()
  locais = [('https://americachip.com/plano-estados-unidos/','eua','//*[@id="numero-de-dias"]')
                    ,('https://americachip.com/plano-europa/','europa','//*[@id="escolha-o-numero-de-dias"]')]
  dados = []
  data = datetime.now().date().strftime('%d-%m-%Y')

  for url,local,xpath in locais:
      for option_value in ['5 dias', '10 dias', '14 dias']:

                driver.get(url)
                select_element= WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath )))

                option = select_element.find_element(By.XPATH, f".//option[text()='{option_value}']")
                option.click()

                time.sleep(3)

                escolerDiaeData(driver,data,'chip')

                time.sleep(3)

                formulario(driver)

                time.sleep(3)
                driver.find_element(By.XPATH, '//*[@id="main"]/div[2]/div/form/div/div[1]/div[2]/div[2]/button').click()

                time.sleep(3)

                precoParcelado,precoPix = coletarPrecosChip(driver)

                time.sleep(3)

                dados.append({
                    'Chip': 'CHIP ILI EUA' if local == 'eua' else 'CHIP ILI Europa',
                    'data_ativacao': data,
                    'dias': option_value,
                    'preco_parcelado': float(precoParcelado),
                    'preco_a_vista': float(precoPix)
                })
                # Fechar o navegador

  driver.quit()
  #json_data = json.dumps(dados)

  df = pd.DataFrame(dados)
  nome_arquivo = f'chip_america_{data_atual}.json'
  salvar_dados(df, nome_arquivo, 'chip/america', hora_global)
  time.sleep(5)
  finalizar_chip()

  return




# if __name__ == '__main__':
#     asyncio.run(coleta_dados())
# async def coleta_dados(hora_global,data_atual):
#     # Executa as funções assíncronas simultaneamente
#     await chip_eua_europa(hora_global,data_atual)
#     await esim_eua_europa(hora_global,data_atual)
#     # Combina os DataFrames



if __name__ == '__main__':
    asyncio.run(coleta_dados())
