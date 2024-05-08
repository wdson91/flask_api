import time
from helpers.atualizar_calibragem import finalizar_calibragem
from imports import *



def coleta_precos_teste(): 
    
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 20)
    login = 'supervisao.fila@voupra.com'
    senha =  'Vp!7070st'
   
    driver.get('https://grupoysa.sz.chat/static/signin')
    time.sleep(4)
    email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-cy='form-email']")))
    email_input.send_keys(login)

    time.sleep(2)

    password_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-cy='form-password']")))
    password_input.send_keys(senha)

    time.sleep(2)

    actions = ActionChains(driver) 

    actions.send_keys(Keys.ENTER)
    actions.perform()
        
    time.sleep(15)

    driver.get('https://grupoysa.sz.chat/monitoring')
    
    time.sleep(1)
    
    botao_filtro = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/section/div/div/div[3]/div/button')))
    botao_filtro.click()
     
    
    while True:
        
        url_atual = driver.current_url
          
        valor_conversores = 0    
            
        data = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        dia = datetime.now().strftime('%d-%m-%Y')

        dados = {} 
          
    
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
        valor_conversores = int(conversores.text)

        filtro_texto = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="selectSearchCampaigns"]/input')))
        
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

        time.sleep(2)
        
        # botao_delete = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="selectSearchCampaigns"]/div[1]/i')))
        # botao_delete.click()
        
        qualiddade_do_lead = (valor_conversores / valor_pimeiroContato) * 10

        if qualiddade_do_lead > 10:
            qualiddade_do_lead = 10
        
        dados = {
            "qualidade": qualiddade_do_lead,
            "conversores": valor_conversores,
            "primeiro_contato": valor_pimeiroContato,
            "data": data
        }

        nome_arquivo = f'leads_{dia}.json'
        salvar_dados_lead(dados, nome_arquivo, 'leads', data)
        
        driver.refresh()
        
        time.sleep(2)
        
        botao_filtro = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/section/div/div/div[3]/div/button')))
        botao_filtro.click()
        
        time.sleep(1)
        
        botao_delete = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="selectSearchCampaigns"]/div[1]/i')))
        botao_delete.click()
        #driver.quit()
        #finalizar_calibragem()
        
        # Intervalo de espera antes da próxima coleta
        time.sleep(30)  # 1 minuto


if __name__ == '__main__':
    coleta_precos_teste()
