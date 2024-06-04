from imports import *


async def coleta_tio_sea(hora,array_datas,data_atual):# Inicializar o driver do Selenium
    driver = webdriver.Chrome()
    driver.maximize_window()
    # Lista de datas para a coleta de dados
    array_datas = [10, 20, 47, 65, 126]
    datas = [datetime.now().date() + timedelta(days=d) for d in array_datas]

    # Função para fechar elemento bloqueador, se existir
    def fechar_elemento_bloqueador(driver):
        try:
            botao_fechar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="jivo_close_button"]/jdiv'))
            )
            botao_fechar.click()
        except TimeoutException:
            print("Elemento bloqueador não encontrado ou não clicável.")

    # Mapeamento dos nomes dos parques
    mapeamento_parques = {
        "SeaWorld Orlando 1-Dia": "1 Dia 1 Parque - SeaWorld Orlando",
        "Busch Gardens Tampa 1-Dia": "1 Dia 1 Parque - Busch Gardens",
        "2-Dias + 1-Dia GRÁTIS!* de parque à sua escolha (SeaWorld Orlando, Busch Gardens Tampa Bay, Aquatica Orlando ou Adventure Island Tampa*)": "3 Dias 3 Parques - SeaWorld Orlando",
        "2-Dias + 1-Dia GRÁTIS!* de parque à sua escolha (SeaWorld Orlando, Busch Gardens Tampa Bay, Aquatica Orlando ou Adventure Island Tampa*) + Plano de Refeição": "3 Dias 3 Parques com Refeições - SeaWorld Orlando",
        "14-Dias de parques à sua escolha (SeaWorld Orlando, Busch Gardens Tampa Bay, Aquatica Orlando ou Adventure Island Tampa*) com estacionamento GRÁTIS!*": "14 Dias 3 Parques - SeaWorld Orlando",
        
    }

    # Mapeamento dos meses em português
    nomes_meses_pt_BR = {
        1: "janeiro",
        2: "fevereiro",
        3: "março",
        4: "abril",
        5: "maio",
        6: "junho",
        7: "julho",
        8: "agosto",
        9: "setembro",
        10: "outubro",
        11: "novembro",
        12: "dezembro"
    }

    # Lista para armazenar os dados
    dados = []

    for i in range(1, 4):
        driver.get('https://www.tioorlando.com.br/ingressos-seaworld-parks')

        # Aguardar o carregamento do elemento
        elemento = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, f'//*[@id="page-content"]/div[2]/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[{i}]/button'))
        )

        # Clicar no botão
        elemento.click()

        # Aguardar a presença do elemento do mês atual
        mes_atual = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, "react-datepicker__current-month"))
        )
        
        for data in datas:
            mes = nomes_meses_pt_BR[data.month]
            ano = data.year
            
            dia = data.day
            if dia < 10:
                dia = f"0{dia}"
            mes_desejado = f'{mes} {ano}'
            
            # Verificar se o mês atual é diferente do desejado
            while mes_desejado not in mes_atual.text:
                try:
                    # Se não for, clicar no botão de navegação "next"
                    botao_next = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "react-datepicker__navigation--next"))
                    )
                    try:
                        # Tenta clicar no botão de navegação
                        botao_next.click()
                    except ElementClickInterceptedException:
                        # Se o clique for interceptado, usa JavaScript para clicar
                        driver.execute_script("arguments[0].click();", botao_next)
                    
                    # Aguardar a atualização do mês atual
                    mes_atual = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "react-datepicker__current-month"))
                    )
                except TimeoutException:
                    print("Não foi possível encontrar o botão de navegação ou clicar nele.")
                    break

            time.sleep(5)

            seletor_dia = f".react-datepicker__day--0{dia}"
            try:
                # Aguardar até que o elemento correspondente ao dia desejado esteja clicável na página
                elemento_dia = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, seletor_dia))
                )

                # Clicar no elemento correspondente ao dia desejado
                elemento_dia.click()
                
            except TimeoutException:
                print(f"Não foi possível clicar no dia {dia}.")
                continue

            time.sleep(7)
            
            # Encontrar todos os elementos com a classe 'MuiBox-root mui-7ulwng'
            elementos = driver.find_elements(By.CLASS_NAME, 'MuiBox-root.mui-7ulwng')

            # Iterar sobre os elementos
            for elemento in elementos:
                
                # Encontrar o título dentro do elemento atual
                titulo = elemento.find_element(By.CLASS_NAME, 'MuiTypography-root.MuiTypography-body2.mui-1sgqvsm').text
                # Encontrar o preço dentro do elemento atual
                preco_a_vista = elemento.find_element(By.CLASS_NAME, 'MuiBox-root.mui-1ahotr9').text
                preco_a_vista = float(preco_a_vista.replace("R$", "").replace(".", "").replace(",", ".").strip())
                preco = elemento.find_elements(By.CLASS_NAME, 'MuiBox-root.mui-sw026l')
                # Dividir a string pelo espaço em branco
                partes = preco[2].text.split()
                # Remover o valor desejado
                preco_parcelado = float(partes[-1].replace('R$', '').replace(',', '.'))
                # Calcula o preço parcelado

                parque = titulo.split(' - ', 1)[0]
                
                # Mapear o nome do parque para o nome completo
                parque = mapeamento_parques.get(parque, titulo)
                
                dados.append({
                    'Data_viagem': data.strftime('%Y-%m-%d'),
                    'Parque': parque,
                    "Preco_Avista": preco_a_vista,
                    "Preco_Parcelado": preco_parcelado * 12
                })
    # Fechar o navegador após processar todos os dados
    driver.quit()
    # Salvar os dados em um arquivo JSON
    
    
    df = pd.DataFrame(dados)
    
    nome_arquivo = f'seaworld_tio_{data_atual}.json'
    
    salvar_dados(df, nome_arquivo, 'orlando/tio', hora)
    
    
    
if __name__ == '__main__':
    
    
    
    coleta_tio_sea()
    print("Coleta de dados finalizada com sucesso.")