import asyncio
import locale
from flask import Flask, jsonify, request
import pandas as pd
import sys
import time
import requests
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import logging
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys

from webdriver_setup import get_webdriver




def limparCarrinho(driver):

    itens = driver.find_elements(By.CLASS_NAME, 'woocommerce-cart-form__cart-item')

    if len(itens) > 1:
      driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div[2]/div[2]/div[1]/form/div/table/tbody/tr[1]/td[1]/a').click()
      time.sleep(5)
    return

def formulario(driver):
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="billing_email"]').send_keys('teste@tese.com')
    driver.find_element(By.XPATH, '//*[@id="billing_first_name"]').send_keys('teste')
    driver.find_element(By.XPATH, '//*[@id="billing_last_name"]').send_keys('teste')
    driver.find_element(By.XPATH, '//*[@id="billing_postcode"]').send_keys('42707-850')
    driver.find_element(By.XPATH, '//*[@id="shipping_number"]').send_keys('25')
    driver.find_element(By.XPATH, '//*[@id="billing_phone"]').send_keys('1212121-2121')
    driver.find_element(By.XPATH, '//*[@id="shipping_CPF"]').send_keys('030.111.111-11')


    tela = driver.find_element(By.XPATH, '/html/body/div[1]/footer/div[1]')
    driver.execute_script("arguments[0].scrollIntoView();", tela)
    time.sleep(3)
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
    driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div/form/div/div[1]/div[3]/div[2]/ul/li[3]/label').click()
    time.sleep(2)
    precoPix = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div/form/div/div[1]/div[3]/div[2]/ul/li[3]/div/div[2]/span[2]/strong/span').text
    precoPix = precoPix.replace('R$','').replace('.','').replace(',','.')

    time.sleep(5)

    driver.find_element(By.XPATH, '//*[@id="payment"]/ul/li[2]/label').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div/form/div/div[1]/div[3]/div[2]/ul/li[2]/div/div[1]/section/div/div/section[4]/span/span[1]/span').click()
    time.sleep(3)
    input = driver.find_element(By.XPATH, '/html/body/span/span/span[1]/input')
    input.send_keys('6x')
    input.send_keys(Keys.ENTER)
    time.sleep(3)

    precoParcelado = driver.find_element(By.XPATH, '//*[@id="converted-amount"]/strong/span').text
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

    driver.find_element(By.XPATH, xpath_button).click()

    limparCarrinho(driver)

    time.sleep(3)

    continuar = driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div[2]/div[2]/div/div[1]/div/a")
    driver.execute_script("arguments[0].scrollIntoView()", continuar)

    continuar.click()

    return




dados = []
async def esim_eua_europa():# -> list:
    # Inicializar o navegador (neste exemplo, estamos usando o Chrome)
    #driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    await asyncio.sleep(1)
    driver = get_webdriver()
    # Maximizar a janela do navegador
    driver.maximize_window()
    locais = [('eua','//*[@id="numero-de-dias"]')
                    ,('europa','//*[@id="escolha-o-numero-de-dias"]')]
    data = "01/07/2024"
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
                  'dias': option_value,
                  'preco_parcelado': precoParcelado,
                  'preco_a_vista': precoPix
              })
              # Fechar o navegador

    driver.quit()

    return dados



async def chip_eua_europa():

  #driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    # Maximizar a janela do navegador
  await asyncio.sleep(1)
  driver = get_webdriver()
  driver.maximize_window()
  locais = [('https://americachip.com/plano-estados-unidos/','eua','//*[@id="numero-de-dias"]')
                    ,('https://americachip.com/plano-europa/','europa','//*[@id="escolha-o-numero-de-dias"]')]

  data = "01/07/2024"

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
                    'Chip': 'Chip ILI EUA' if local == 'eua' else 'Chip ILI Europa',
                    'dias': option_value,
                    'preco_parcelado': precoParcelado,
                    'preco_a_vista': precoPix
                })
                # Fechar o navegador

  driver.quit()

  return dados


# async def coleta_dados():
#     #df1 = await esim_eua_europa()
#     df2 = await chip_eua_europa()

#     #print(df1)
#     print(df2)

#     return

# if __name__ == '__main__':
#     asyncio.run(coleta_dados())
async def coleta_dados():
    # Executa as funções assíncronas simultaneamente
    await chip_eua_europa()
    await esim_eua_europa()
    # Combina os DataFrames
    #df = pd.merge(df1, df2, on='Country')

    print(dados)

if __name__ == '__main__':
    asyncio.run(coleta_dados())
