
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Inicializar o navegador (nesse exemplo, estamos usando o Chrome)
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Abrir uma página da web
driver.get("https://www.decolar.com/atracoes-turisticas/d-PAM_LAX_46269/ingressos+para+os+parques+tematicos+da+disney+california-los+angeles?clickedPrice=1720&priceDate=1711547379358&clickedCurrency=BRL&currency=BRL")

# Imprimir o título da página
print("Título da página:", driver.title)

time.sleep(50)
# Fechar o navegador
driver.quit()
