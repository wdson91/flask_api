from helpers.atualizar_calibragem import finalizar_calibragem
from imports import *


def coleta_precos(): 
    login = 'supervisao.fila@voupra.com'
    senha =  'Vp!7070st'
    valor_conversores = 0    
        
    data = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    dia = datetime.now().strftime('%d-%m-%Y')
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ativa o modo headless

    # Inicializa o serviço do Chrome
    service = Service(ChromeDriverManager().install())

    # Inicializa o driver do Chrome com as opções e o serviço
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 20)
    dados = {}   

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
    
    time.sleep(15)


    driver.get('https://grupoysa.sz.chat/monitoring')

    time.sleep(1)

    botao_filtro = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/section/div/div/div[3]/div/button')))
    botao_filtro.click()

    filtro_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#selectSearchCampaigns')))
    time.sleep(1)
    
    filtro_texto = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="selectSearchCampaigns"]/input')))
    time.sleep(3)
    
    filtro_input.click()
    
    filtro_texto.send_keys('conver')

    time.sleep(2)

    filtro_input.send_keys(Keys.ENTER)

    time.sleep(2)

    botao_pesquisar = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/section/div/div/div[3]/form/button[1]')))
    botao_pesquisar.click()

    time.sleep(2)

    conversores = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/section/div/div/div[2]/div/div[1]/div/div[2]/div[1]')))
    valor_conversores= int(conversores.text)

    filtro_texto = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="selectSearchCampaigns"]/input')))
    #time.sleep(3)

    botao_delete = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="selectSearchCampaigns"]/div[1]/i')))
    botao_delete.click()

    time.sleep(2)

    filtro_input.click()
    
    filtro_texto.send_keys('prime')
    
    time.sleep(1)
    
    filtro_input.send_keys(Keys.ENTER)
    
    time.sleep(2)

    botao_pesquisar = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/section/div/div/div[3]/form/button[1]')))
    
    botao_pesquisar.click()

    time.sleep(2)

    primeiroContato = driver.find_element(By.XPATH, '/html/body/div[3]/section/div/div/div[2]/div/div[1]/div/div[2]/div[1]')
    valor_pimeiroContato = int(primeiroContato.text)

    qualiddade_do_lead = (valor_conversores / valor_pimeiroContato) * 10

    #qualidade_do_lead_formatado = round(qualiddade_do_lead, 2)

    # Imprime o valor formatado
    
    if qualiddade_do_lead>10:
        qualiddade_do_lead = 10
    
    
    dados = {
        "qualidade": qualiddade_do_lead,
        "conversores": valor_conversores,
        "primeiro_contato": valor_pimeiroContato,
        "data": data
    }
    
    driver.quit()
    
   
    
    nome_arquivo = f'leads_{dia}.json'
    
    json.dumps(dados, indent=4)
    
    salvar_dados_lead(dados, nome_arquivo, 'leads', data)
    
    finalizar_calibragem()
    return

if __name__ == '__main__':
    coleta_precos()



