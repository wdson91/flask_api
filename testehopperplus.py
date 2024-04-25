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
driver.get("https://www.tioorlando.com.br/ingressos-disney-orlando")
wait = WebDriverWait(driver, 5)
# Aguardar até que o elemento radio-1 esteja presente na página
# Aguardar até que o elemento radio-1 esteja presente na página
element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="page-content"]/div[2]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div[1]/button')))

# Clicar no elemento
element.click()


data = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="page-content"]/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div[1]/div[1]')))
print(data.text)



time.sleep(50)
# Fechar o navegador
driver.quit()