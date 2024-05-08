import json
import locale
from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import pandas as pd
import pytz
import asyncio
import os
import sys
import time
import requests
import pandas as pd
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import logging
from selenium.webdriver.chrome.service import Service as ChromeService
import schedule
from flask_cors import CORS
from bs4 import BeautifulSoup
import json
from threading import Thread
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains



    
login = 'supervisao.fila@voupra.com'
senha =  'Vp!7070st'
valor_conversores = 0    
    
    
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 20)

    

driver.get('https://grupoysa.sz.chat/static/signin')

time.sleep(4)
email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-cy='form-email']")))
email_input.send_keys(login)

time.sleep(2)

password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-cy='form-password']")))
password_input.send_keys(senha)

time.sleep(2)

#login_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="q-app"]/div/div/div[1]/div[1]/div[2]/form/button/span[2]')))
actions = ActionChains(driver) 


actions.send_keys(Keys.ENTER)
actions.perform()
time.sleep(10)


driver.get('https://grupoysa.sz.chat/monitoring')



botao_filtro = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/section/div/div/div[3]/div/button')))
botao_filtro.click()



#equipes = ['conver','']

filtro_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#selectSearchCampaigns')))
time.sleep(1)
filtro_texto = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="selectSearchCampaigns"]/input')))
time.sleep(3)
filtro_input.click()
filtro_texto.send_keys('conver')

time.sleep(2)

filtro_input.send_keys(Keys.ENTER)

time.sleep(3)

botao_pesquisar = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/section/div/div/div[3]/form/button[1]')))
botao_pesquisar.click()

time.sleep(5)

conversores = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/section/div/div/div[2]/div/div[1]/div/div[2]/div[1]')))
valor_conversores= int(conversores.text)

filtro_texto = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="selectSearchCampaigns"]/input')))
time.sleep(3)

botao_delete = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="selectSearchCampaigns"]/div[1]/i')))
botao_delete.click()

time.sleep(3)

filtro_input.click()


time.sleep(3)
filtro_texto.send_keys('prime')
time.sleep(3)
filtro_input.send_keys(Keys.ENTER)
time.sleep(3)

botao_pesquisar = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/section/div/div/div[3]/form/button[1]')))
botao_pesquisar.click()

time.sleep(5)

primeiroContato = driver.find_element(By.XPATH, '/html/body/div[3]/section/div/div/div[2]/div/div[1]/div/div[2]/div[1]')
valor_pimeiroContato = int(primeiroContato.text)

qualiddade_do_lead = round((valor_conversores / valor_pimeiroContato) * 10 ,2)

#qualidade_do_lead_formatado = round(qualiddade_do_lead, 2)

# Imprime o valor formatado
print({"Qualidade do Lead": qualiddade_do_lead})
time.sleep(50)







    
login = 'supervisao.fila@voupra.com'
senha =  'Vp!7070st'
valor_conversores = 0    
    
    
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
wait = WebDriverWait(driver, 20)

    

driver.get('https://grupoysa.sz.chat/static/signin')

time.sleep(4)
email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-cy='form-email']")))
email_input.send_keys(login)

time.sleep(2)

password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-cy='form-password']")))
password_input.send_keys(senha)

time.sleep(2)

#login_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="q-app"]/div/div/div[1]/div[1]/div[2]/form/button/span[2]')))
actions = ActionChains(driver) 


actions.send_keys(Keys.ENTER)
actions.perform()
time.sleep(10)


driver.get('https://grupoysa.sz.chat/monitoring')



botao_filtro = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/section/div/div/div[3]/div/button')))
botao_filtro.click()



#equipes = ['conver','']

filtro_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#selectSearchCampaigns')))
time.sleep(1)
filtro_texto = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="selectSearchCampaigns"]/input')))
time.sleep(3)
filtro_input.click()
filtro_texto.send_keys('conver')

time.sleep(2)

filtro_input.send_keys(Keys.ENTER)

time.sleep(3)

botao_pesquisar = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/section/div/div/div[3]/form/button[1]')))
botao_pesquisar.click()

time.sleep(5)

conversores = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/section/div/div/div[2]/div/div[1]/div/div[2]/div[1]')))
valor_conversores= int(conversores.text)

filtro_texto = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="selectSearchCampaigns"]/input')))
time.sleep(3)

botao_delete = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="selectSearchCampaigns"]/div[1]/i')))
botao_delete.click()

time.sleep(3)

filtro_input.click()


time.sleep(3)
filtro_texto.send_keys('prime')
time.sleep(3)
filtro_input.send_keys(Keys.ENTER)
time.sleep(3)

botao_pesquisar = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/section/div/div/div[3]/form/button[1]')))
botao_pesquisar.click()

time.sleep(5)

primeiroContato = driver.find_element(By.XPATH, '/html/body/div[3]/section/div/div/div[2]/div/div[1]/div/div[2]/div[1]')
valor_pimeiroContato = int(primeiroContato.text)

qualiddade_do_lead = round((valor_conversores / valor_pimeiroContato) * 10 ,2)

#qualidade_do_lead_formatado = round(qualiddade_do_lead, 2)

# Imprime o valor formatado
print({"Qualidade do Lead": qualiddade_do_lead})
time.sleep(50)






