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




def limparCarrinho(driver):



    itens = driver.find_elements(By.CLASS_NAME, 'woocommerce-cart-form__cart-item')
    print('itens',len(itens))
    if len(itens) > 1:
      driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div[2]/div[2]/div[1]/form/div/table/tbody/tr[1]/td[1]/a').click()
    time.sleep(5)
    return

def formulario(driver):

    driver.find_element(By.XPATH, '//*[@id="billing_email"]').send_keys('teste@tese.com')
    driver.find_element(By.XPATH, '//*[@id="billing_first_name"]').send_keys('teste')
    driver.find_element(By.XPATH, '//*[@id="billing_last_name"]').send_keys('teste')
    driver.find_element(By.XPATH, '//*[@id="billing_postcode"]').send_keys('26053-210')
    driver.find_element(By.XPATH, '//*[@id="shipping_number"]').send_keys('25')
    driver.find_element(By.XPATH, '//*[@id="billing_phone"]').send_keys('1212121-2121')
    driver.find_element(By.XPATH, '//*[@id="shipping_CPF"]').send_keys('030.111.111-11')


    tela = driver.find_element(By.XPATH, '/html/body/div[1]/footer/div[1]')
    driver.execute_script("arguments[0].scrollIntoView();", tela)
    time.sleep(2)
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
    print('preco em 6x',precoParcelado.replace('R$', '').replace('.', '').replace(',', '.'))
    time.sleep(5)


    inputAvista = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div/form/div/div[1]/div[2]/div[2]/ul/li[3]/label').click()
    time.sleep(2)
    precoPix = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div/form/div/div[1]/div[2]/div[2]/ul/li[3]/div/div[2]/span[2]/strong/span').text

    print('preco a vista',precoPix.replace('R$', '').replace('.', '').replace(',', '.'))
    time.sleep(5)

    return precoParcelado,precoPix



def escolerDiaeData(driver,data):

    elemento = driver.find_elements(By.CLASS_NAME, "calendario")[0]


    driver.execute_script("arguments[0].setAttribute('value', arguments[1])", elemento, data)
    time.sleep(3)

    driver.find_element(By.XPATH, "/html/body/div[1]/main/main/section[13]/ul/li[1]/div/div[1]/form/div/div/div/div/button").click()

    limparCarrinho(driver)

    time.sleep(3)

    driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/div/div[2]/div[2]/div/div[1]/div/a").click()

    return








dados = []
def coletar_1e2_dias():# -> list:
    # Inicializar o navegador (neste exemplo, estamos usando o Chrome)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    # Maximizar a janela do navegador
    driver.maximize_window()

    data = "01/07/2024"
    #select_element = driver.find_element(By.XPATH, '//*[@id="numero-de-dias"]')
    for option_value in ['5 dias', '10 dias', '14 dias']:
            driver.get("https://americachip.com/esim/#product-form-75163")
            select_element= WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="numero-de-dias"]')))

            option = select_element.find_element(By.XPATH, f".//option[text()='{option_value}']")
            option.click()

            time.sleep(3)

            escolerDiaeData(driver,data)

            time.sleep(3)

            formulario(driver)

            time.sleep(3)

            precoParcelado,precoPix = coletarPrecos(driver)

            time.sleep(3)

            dados.append({
                'Chip': 'eSIM ILI EUA',
                'dias': option_value,
                'preco_parcelado': precoParcelado,
                'preco_a_vista': precoPix
            })
            # Fechar o navegador

    driver.quit()


    print(dados)

    return


if __name__ == "__main__":
   coletar_1e2_dias()
