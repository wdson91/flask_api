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


def coletar():
    
    waiter = 2
     
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    
    
    def fechar_popups(driver):
        try:
            botao_fechar_selector = '.dinTargetFormCloseButtom'
            botao_fechar = WebDriverWait(driver, waiter + 3).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, botao_fechar_selector))
            )
            botao_fechar.click()
            botao_cookies = WebDriverWait(driver, waiter + 3).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[3]/div/div/div[2]/button'))
            )
            botao_cookies.click()
            
            logging.info("Pop-up fechado.")
        except Exception as e:
            logging.warning(f"Popup não encontrada")
            
            
    
    mes_calendario = driver.find_element(By.XPATH, '//*[@id="custom-month"]')
    mes_calendario_atual = mes_calendario.text
    
    
    