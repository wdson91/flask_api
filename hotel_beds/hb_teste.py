import json
import re
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
# Função para converter strings de preços para floats
def convert_price(price_str):
    # Remove caracteres não numéricos exceto ponto ou vírgula
    clean_price = re.sub(r'[^\d,]', '', price_str)
    # Substitui vírgula por ponto para conversão correta
    clean_price = clean_price.replace(',', '.')
    return float(clean_price)

def format_date(date_str):
    # Converte a data para o formato datetime
    date_obj = datetime.strptime(date_str, "%a, %d %b")
    # Formata a data para "dd/mm"
    return date_obj.strftime("%d/%m")

# Configuración del controlador de Chrome
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
login='CVOUPRA01'
password='01Voupr@2024'

# Abrir la página de Google
driver.get("https://app.hotelbeds.com/auth/login")
wait = WebDriverWait(driver, 20)
dados = []
time.sleep(2)

cookies_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll"]')))   
cookies_button.click()

# Esperar unos segundos para que la página cargue completamente
time.sleep(2)

login_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="username"]')))
login_input.send_keys(login)

time.sleep(2)
password_input = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
password_input.send_keys(password)

time.sleep(2)
actions = ActionChains(driver)
actions.send_keys(Keys.ENTER)
actions.perform()

time.sleep(5)

# Generar fechas para os meses a partir de julho deste ano
mes_atual = datetime.now().month
ano_atual = datetime.now().year
#datas_meses = [datetime(ano_atual, mes, 1) for mes in range(mes_atual, 13)]
datas_meses = [datetime(2024, mes, 12) for mes in range(6,7)]+[datetime(2024, mes, 1) for mes in range(7, 13)] + [datetime(2025, mes, 1) for mes in range(1, 5)]
#datas_meses = [datetime(ano, mes, dia) for ano in range(2024, 2026) for mes in range(6 if ano == 2024 else 1, 5 if ano == 2025 else 13) for dia in range(12 if ano == 2024 and mes == 6 else 1, 32 if mes in [1, 3, 5, 7, 8, 10, 12] else 31 if mes != 2 else 30)]

# Iterar sobre as datas dos meses
for data_mes in datas_meses:
    #if data_mes >= datetime(ano_atual, 7, 1):
        primeiro_dia_mes = data_mes.strftime("%d-%m-%Y")
        ultimo_dia_mes = (data_mes + timedelta(days=31)).replace(day=1) - timedelta(days=1)
        ultimo_dia_mes = ultimo_dia_mes.strftime("%d-%m-%Y")
        
        # URL base
        url_base = f'https://app.hotelbeds.com/factsheet/experience/E-U10-UNILATIN?id=55221&countriesControl=US&countryTab=Estados%20Unidos&destination=MCO&destinationTab=Orlando%20Area%20-%20FL&check_in={primeiro_dia_mes}&check_out={ultimo_dia_mes}&destinationCode=MCO'    
        # Abrir a URL
        driver.get(url_base)
        
        # Verificar disponibilidade
        verify_button = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/clientb2b-front-root/clientb2b-front-main-feature-layout/section/div/div/clientb2b-front-factsheet-feature-factsheet/clientb2b-front-factsheet/div/clientb2b-front-factsheet-sticky-dates/div/div/div[2]/button/div/div[1]/div')))
        verify_button.click()
        time.sleep(3)  # Esperar a verificação
        
        # Se houver um modal, manipule-o
        try:
            modal_element = wait.until(EC.presence_of_element_located((By.ID, "cdk-overlay-0")))
            decrement_adults_button = modal_element.find_element(By.CSS_SELECTOR, ".hb-form-prefix button")
            decrement_adults_button.click()
            
            button = modal_element.find_elements(By.CSS_SELECTOR, ".hb-form-suffix button")

            button[1].click()
            
            # time.sleep(3)
            # #dropdown_options = modal_element.find_elements((By.CSS_SELECTOR, ".hb-form-field__input-wrapper"))
            # dropdown = modal_element.find_element(By.CSS_SELECTOR, ".hb-select__display-name")
            # dropdown.click()
            # time.sleep(2)
            # dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".hb-select__display-name")))
            # dropdown.click()

            # # Seleciona a opção "6"
            # option_to_select = dropdown.find_element(By.XPATH, "//span[contains(text(), '4')]")
            # option_to_select.click()

            # # Verifica se a seleção foi feita corretamente
            # selected_value = dropdown.find_element(By.CSS_SELECTOR, ".hb-select__display-name span").text
            # print("Selecionado:", selected_value)

            # # Iterar sobre las opciones del menú desplegable y seleccionar la opción "5"
            # for option in dropdown_options:
            #     if option.text.strip() == "5":
            #         option.click()
            #         break
                
        except TimeoutException:
            pass  # Se não houver modal, continue
        time.sleep(5)  # Aguarde um momento
        # Consultar disponibilidade
        consultar_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".check-availability__footer button")))
        consultar_button.click()
        
        time.sleep(3)  # Esperar pelos resultados
        
        # Iterar sobre as datas disponíveis
        calendar_elements = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "check-availability-calendar__content")))
        for element in calendar_elements:
            element.click()
            data_atual = element.find_element(By.CLASS_NAME, "check-availability-calendar__content__date").text
            print(f"Data atual: {data_atual}")
            time.sleep(1)  # Aguardar um momento
            
            offer_cards = modal_element.find_elements(By.CLASS_NAME, "offer-card-experience")
            for card in offer_cards:
                label = card.find_element(By.CLASS_NAME, "hb-radio__label")
                if " 3 Parques 3 Dias - Entrada Parque a Parque com data + Promo 2 dias gratis " in label.text:
                    parque = label.text
                    input_wrapper = card.find_element(By.CLASS_NAME, "hb-radio__input-wrapper")
                    input_wrapper.click()
                    time.sleep(1)  # Aguardar um momento
                    
                    # Buscar o resumo de disponibilidade
                    summary = driver.find_element(By.TAG_NAME, "clientb2b-front-check-availability-summary")
                    
                    # Buscar o preço dos adultos
                    adult_price = summary.find_element(By.CLASS_NAME, "check-availability-summary__adults__item-right").find_element(By.TAG_NAME, "p").text
                    
                    # Buscar o preço das crianças
                    children_price = summary.find_element(By.CLASS_NAME, "check-availability-summary__childrens__item-right").find_element(By.TAG_NAME, "p").text
                    
                    dados.append({
                    "data": data_atual,
                    "parque": parque,
                    "adulto": adult_price,
                    "crianca": children_price
                })
                
# Cerrar el navegador
driver.quit()
time.sleep(2)

df = pd.DataFrame(dados)
df['adulto'] = df['adulto'].apply(convert_price)
df['crianca'] = df['crianca'].apply(convert_price)
df_melted = df.melt(id_vars=['data', 'parque'], value_vars=['adulto', 'crianca'], 
                    var_name='tipo', value_name='preco')

# Criar a tabela pivotada onde as datas são colunas
df_pivot = df_melted.pivot_table(index=['data', 'tipo'], columns='parque', values='preco')
df_pivot.reset_index(inplace=True)

# Salvar o DataFrame pivotado em um arquivo CSV
df_pivot.to_csv('precos_parques.csv', index=False)

print("Dados salvos em 'precos_parques.csv'")