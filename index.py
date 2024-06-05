import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Inicializando o driver do Chrome
driver = webdriver.Chrome()

# Maximizando a janela do navegador
driver.maximize_window()

# Navegando até o site
driver.get("https://www.decolar.com/atracoes-turisticas/d-DY_ORL/ingressos+para+walt+disney+world+resort-orlando?clickedPrice=702&priceDate=1710530966837&clickedCurrency=BRL&distribution=1&modalityId=ANNUAL-2D-2024&fixedDate=2024-06-26")

# Aguardando a página carregar completamente
# wait = WebDriverWait(driver, 10)
# wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(), 'Walt Disney World Resort Orlando')]")))

# Exemplo de como clicar em algum elemento na página (substitua pelo que for necessário)
# driver.find_element_by_xpath("//button[contains(text(), 'Example Button')]").click()
time.sleep(500)
# Fechando o navegador
# driver.quit()
