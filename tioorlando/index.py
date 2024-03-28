import datetime
import locale
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from datetime import timedelta
from webdriver_manager.chrome import ChromeDriverManager

# Configurar opções do WebDriver
options = webdriver.ChromeOptions()

# Inicializar o driver remoto
#driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', options=options)
driver = webdriver.Chrome(ChromeDriverManager().install())
# Inicializar o tempo de espera
wait = WebDriverWait(driver, 10)

# Definir o local para português do Brasil
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

# Abrir o site
driver.get('https://www.tioorlando.com.br/ingressos-walt-disney-world-orlando')

# Aguardar o carregamento do elemento
elemento = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="page-content"]/div[2]/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[1]/button'))
)

# Clicar no botão
elemento.click()


mes_desejado = "maio 2024"  # Altere para o mês que desejar

# Aguardar a presença do elemento do mês atual
mes_atual = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "react-datepicker__current-month"))
)

# Verificar se o mês atual é diferente do desejado
while mes_desejado not in mes_atual.text:
    # Se não for, clicar no botão de navegação "next"
    botao_next = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "react-datepicker__navigation--next"))
    )
    botao_next.click()
    # Aguardar a atualização do mês atual
    mes_atual = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "react-datepicker__current-month"))
    )

time.sleep(3)

# # Localizar o botão de data pelo XPath usando a classe
# botao_data = WebDriverWait(driver, 20).until(
#     EC.presence_of_element_located((By.CLASS_NAME,"react-datepicker__day react-datepicker__day--021"))
# )


# botao_data.click()

# # Localizar todos os elementos MuiBox-root mui-7ulwng
# elementos_mui_box = WebDriverWait(driver, 10).until(
#     EC.presence_of_all_elements_located((By.CLASS_NAME,"MuiBox-root.mui-7ulwng")))

time.sleep(3)
elementos = driver.find_elements_by_class_name("MuiBox-root.mui-1ek1v2f")

# Iterar sobre os elementos
for elemento in elementos:
    # Encontrar o span dentro do elemento
    span = elemento.find_element_by_tag_name("span")
    # Verificar se o texto do span é "17"
    if span.text == "17":
        # Clicar no elemento
        elemento.click()
        # Saia do loop após clicar no elemento
        #break
    
    
time.sleep(3)

# Iterar sobre os elementos MuiBox-root mui-7ulwng
for elemento_mui_box in elementos_mui_box:
    # Pegar o título dentro do elemento MuiBox
    titulo = elemento_mui_box.find_element_by_class_name("MuiTypography-root.MuiTypography-body2")
    # Imprimir o texto do título
    print("Título:", titulo.text)
    
    # Pegar o preço dentro do elemento MuiBox
    preco = elemento_mui_box.find_element_by_class_name("MuiBox-root.mui-1ahotr9") # Ou "MuiBox-root.mui-sw026l", dependendo do banner
    # Imprimir o texto do preço
    print("Preço:", preco.text)
    
    # preco2 = elemento_mui_box.find_element_by_class_name("MuiBox-root.mui-sw026l")
    # print("Preço:", preco2.text)


#driver.quit()