from datetime import datetime, timedelta
import time
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


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Abrir a página desejada
driver.get("https://disneyworld.disney.go.com/pt-br/admission/tickets/theme-parks/")
wait = WebDriverWait(driver, 5)
# Aguardar até que o elemento radio-1 esteja presente na página
# Aguardar até que o elemento radio-1 esteja presente na página
element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/tickets-spa//div/div[2]/uirouter-uiview/tickets-config-page-v2//div[2]/tickets-module[1]/tickets-num-days//iron-selector/div[1]")))

# Clicar no elemento
element.click()

# Fechar o navegador
driver.quit()