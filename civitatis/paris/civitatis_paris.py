from imports import *
from datetime import datetime, timedelta
import pandas as pd
import asyncio

def somar_15_porcento(valor):
    return valor * 1.15 # acrescenta 15%(taxa do cartão de credito 12x) ao valor 

def nome_para_numero_mes(nome_mes):
        meses = {
            "JANEIRO": "01",
            "FEVEREIRO": "02",
            "MARÇO": "03",
            "ABRIL": "04",
            "MAIO": "05",
            "JUNHO": "06",
            "JULHO": "07",
            "AGOSTO": "08",
            "SETEMBRO": "09",
            "OUTUBRO": "10",
            "NOVEMBRO": "11",
            "DEZEMBRO": "12"
        }
        return meses.get(nome_mes.upper(), None)

    # Função para traduzir o nome do mês
def traduzir_mes(nome_mes):
        meses_traduzidos = {
            "JANUARY": "JANEIRO",
            "FEBRUARY": "FEVEREIRO",
            "MARCH": "MARÇO",
            "APRIL": "ABRIL",
            "MAY": "MAIO",
            "JUNE": "JUNHO",
            "JULY": "JULHO",
            "AUGUST": "AGOSTO",
            "SEPTEMBER": "SETEMBRO",
            "OCTOBER": "OUTUBRO",
            "NOVEMBER": "NOVEMBRO",
            "DECEMBER": "DEZEMBRO"
        }
        return meses_traduzidos.get(nome_mes.upper(), None)

    # Função para calcular o mês desejado com base em uma data
def calcular_mes_desejado(data):
        mes_numero = data.month
        nome_mes = traduzir_mes(data.strftime("%B"))
        return mes_numero, nome_mes


async def coletar_precos_civitatis_paris(hour, array_datas,data_atual):
    
    # Definir as datas desejadas em um intervalo de 10, 20, 47, 65, 126 dias, 5 dias não disponível
    array_datas =  [10,20,47,65,126]
    # Função para converter o nome do mês para o formato de número
    df1 = await coletar_1e2_dias( array_datas)
    df2 = await coletar_3e4_dias( array_datas)
    df3 = await coletar_2_dias( array_datas)
    df_precos_ingressos = pd.DataFrame(df1 + df2 + df3)

    # Exibir o DataFrame mesclado
    df_precos_ingressos = df_precos_ingressos.drop_duplicates()
    df_precos_ingressos = df_precos_ingressos.sort_values(by=['Data_viagem', 'Parque'])
    df_precos_ingressos["Preco_Parcelado"] = df_precos_ingressos["Preco_Parcelado"].apply(somar_15_porcento)
    # Salvar como JSON
    nome_arquivo = f'paris_civitatis_{data_atual}.json'
    # Fechar o navegador

    salvar_dados(df_precos_ingressos, nome_arquivo, 'paris/civitatis', hour)
    
async def coletar_1e2_dias(array_datas):# -> list:
    # Inicializar o navegador (neste exemplo, estamos usando o Chrome)
    driver = webdriver.Chrome()
    # Maximizar a janela do navegador
    driver.maximize_window()
    # Abrir uma página da web
    driver.get("https://www.civitatis.com/br/disneyland-paris/ingresso-disneyland-paris")
    time.sleep(5)
    # Definir os tipos de ingressos
    parques = [
        {"tipo": "1 Dia 2 Parques - Disney Paris", "xpath": "//li[contains(@class, 'select2-results__option') and contains(., 'Ingresso de 2 parques')]"},
        {"tipo": "1 Dia 1 Parque - Disney Paris", "xpath": "//li[contains(@class, 'select2-results__option') and contains(., 'Ingresso de 1 parque')]"}
    ]
    precos_ingressos = []

    # Definir as datas desejadas em um intervalo de 5, 10, 20, 47, 65, 126 dias
    datas_desejadas = [datetime.now() + timedelta(days=d) for d in array_datas]

    for data_desejada in datas_desejadas:
        # Calcular o mês desejado para a data atual
        mes_desejado_numero, mes_desejado_nome = calcular_mes_desejado(data_desejada)

        # Converter o nome do mês para o formato de número
        mes_desejado_numero = nome_para_numero_mes(mes_desejado_nome)

        # Encontrar e imprimir o mês do calendário
        nome_elemnt = driver.find_element(By.XPATH, '//*[@id="activityCalendar"]/div[1]/div/div/div[2]/span[1]')
        driver.execute_script("arguments[0].scrollIntoView(true);", nome_elemnt)
        mes_calendario = nome_elemnt.text

        # Verificar se o mês do calendário é diferente do mês desejado
        while mes_calendario != mes_desejado_nome:
            # Clicar no botão "Próximo mês"
            botao_proximo_mes = driver.find_element(By.XPATH, '//*[@id="activityCalendar"]/div[1]/div/div/div[3]')
            botao_proximo_mes.click()
            time.sleep(2)
            # Atualizar o mês do calendário
            nome_elemnt = driver.find_element(By.XPATH, '//*[@id="activityCalendar"]/div[1]/div/div/div[2]/span[1]')
            mes_calendario = nome_elemnt.text

        # Iterar sobre os tipos de ingressos
        for parque_info in parques:
            parque_tipo: str = parque_info["tipo"]
            parque_xpath = parque_info["xpath"]

            try:
                # Encontrar o elemento do dia e clicar nele
                elemento_dia = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, f"activity-calendar-2024-{mes_desejado_numero}-{data_desejada.day:02d}"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", elemento_dia)
                elemento_dia.click()
                time.sleep(2)

                # Abrir o menu suspenso e selecionar o tipo de ingresso
                elemento_menu = driver.find_element(By.ID, "select2-categoria-container")
                elemento_menu.click()
                elemento_clicavel = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, parque_xpath))
                )
                time.sleep(2)
                elemento_clicavel.click()

                # Encontrar e imprimir o valor para a data atual e o tipo de ingresso
                elemento_valor = driver.find_element(By.XPATH,'//*[@id="tPrecioSpan0"]')
                
                valor = elemento_valor.text
                valor  = float(valor.replace('R$', '').replace('.', '').replace(',', '.'))
                
                #print(f"Valor para {data_desejada.strftime('%Y-%m-%d')} ({parque_tipo}): {valor}")

                precos_ingressos.append({
                    'Data_viagem': data_desejada.strftime('%Y-%m-%d'),
                    'Parque': parque_tipo,
                    "Preco_Avista": valor,
                    "Preco_Parcelado": valor
                })

                # Clicar no elemento para abrir o calendário novamente
                elemento_calendario = driver.find_element(By.XPATH, '//*[@id="foldedDate"]')
                elemento_calendario.click()
                time.sleep(2)
            except:
                precos_ingressos.append({
                    'Data_viagem': data_desejada.strftime('%Y-%m-%d'),
                    'Parque': parque_tipo,
                    "Preco_Avista": '-',
                    "Preco_Parcelado": '-'
                })
                print(f"Elemento do dia não encontrado para {data_desejada.strftime('%Y-%m-%d')} ({parque_tipo})")

    driver.quit()
    return precos_ingressos
# Chamada da função para obter os preços dos ingressos


async def coletar_2_dias(array_datas):# -> list:
    # Inicializar o navegador (neste exemplo, estamos usando o Chrome)
    driver = webdriver.Chrome()
    # Maximizar a janela do navegador
    driver.maximize_window()
    # Abrir uma página da web
    driver.get("https://www.civitatis.com/br/disneyland-paris/ingresso-disneyland-walt-disney-studios/")
    time.sleep(5)
    # Definir os tipos de ingressos
    precos_ingressos = []

    # Definir as datas desejadas em um intervalo de 5, 10, 20, 47, 65, 126 dias
    datas_desejadas = [datetime.now() + timedelta(days=d) for d in array_datas]

    for data_desejada in datas_desejadas:
        # Calcular o mês desejado para a data atual
        mes_desejado_numero, mes_desejado_nome = calcular_mes_desejado(data_desejada)

        # Converter o nome do mês para o formato de número
        mes_desejado_numero = nome_para_numero_mes(mes_desejado_nome)

        # Encontrar e imprimir o mês do calendário
        nome_elemnt = driver.find_element(By.XPATH, '//*[@id="activityCalendar"]/div[1]/div/div/div[2]/span[1]')
        driver.execute_script("arguments[0].scrollIntoView(true);", nome_elemnt)
        mes_calendario = nome_elemnt.text

        # Verificar se o mês do calendário é diferente do mês desejado
        while mes_calendario != mes_desejado_nome:
            # Clicar no botão "Próximo mês"
            botao_proximo_mes = driver.find_element(By.XPATH, '//*[@id="activityCalendar"]/div[1]/div/div/div[3]')
            botao_proximo_mes.click()
            time.sleep(2)
            # Atualizar o mês do calendário
            nome_elemnt = driver.find_element(By.XPATH, '//*[@id="activityCalendar"]/div[1]/div/div/div[2]/span[1]')
            mes_calendario = nome_elemnt.text


        try:
                # Encontrar o elemento do dia e clicar nele
                elemento_dia = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, f"activity-calendar-2024-{mes_desejado_numero}-{data_desejada.day:02d}"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", elemento_dia)
                elemento_dia.click()
                time.sleep(2)

                # Abrir o menu suspenso e selecionar o tipo de ingresso
                elemento_menu = driver.find_element(By.ID, "formActividad-paxes")
                elemento_menu.click()
                

                # Encontrar e imprimir o valor para a data atual e o tipo de ingresso
                elemento_valor = driver.find_element(By.XPATH,'//*[@id="tPrecioSpan0"]')
                
                valor = elemento_valor.text
                valor  = float(valor.replace('R$', '').replace('.', '').replace(',', '.'))
                
                #print(f"Valor para {data_desejada.strftime('%Y-%m-%d')} ({parque_tipo}): {valor}")

                precos_ingressos.append({
                    'Data_viagem': data_desejada.strftime('%Y-%m-%d'),
                    'Parque': '2 Dias 2 Parques - Disney Paris',
                    "Preco_Avista": valor,
                    "Preco_Parcelado": valor
                })

                # Clicar no elemento para abrir o calendário novamente
                elemento_calendario = driver.find_element(By.XPATH, '//*[@id="foldedDate"]')
                elemento_calendario.click()
                time.sleep(2)
        except:
                precos_ingressos.append({
                    'Data_viagem': data_desejada.strftime('%Y-%m-%d'),
                    'Parque': '2 Dias 2 Parques - Disney Paris',
                    "Preco_Avista": '-',
                    "Preco_Parcelado": '-'
                })
                print(f"Elemento do dia não encontrado para {data_desejada.strftime('%Y-%m-%d')} ({'2 Dias 2 Parques - Disney Paris'})")

    # df_precos_ingressos = pd.DataFrame(precos_ingressos)
    # # Exibir o DataFrame mesclado
    # df_precos_ingressos = df_precos_ingressos.drop_duplicates()
    # df_precos_ingressos = df_precos_ingressos.sort_values(by=['Data_viagem', 'Parque'])
    # # Salvar como JSON
    # df_precos_ingressos.to_json('precos_ingressos.json', orient='records')
    # Fechar o navegador
    driver.quit()
    
    return precos_ingressos
# Chamada da função para obter os preços dos ingressos

async def coletar_3e4_dias(array_datas):
    driver = webdriver.Chrome()
    
    # Maximizar a janela do navegador
    driver.maximize_window()
    # Abrir uma página da web
    driver.get("https://www.civitatis.com/br/disneyland-paris/varios-dias-disneyland-walt-disney-studios/")
    time.sleep(5)
    # Definir os tipos de ingressos
    parques = [
        {"tipo": "3 Dias 2 Parques - Disney Paris", "xpath": "//li[contains(@class, 'select2-results__option') and contains(., 'Ingresso de 3 dias')]"},
        {"tipo": "4 Dias 2 Parques - Disney Paris", "xpath": "//li[contains(@class, 'select2-results__option') and contains(., 'Ingresso de 4 dias')]"}
    ]
    precos_ingressos = []

    # Definir as datas desejadas em um intervalo de 5, 10, 20, 47, 65, 126 dias
    datas_desejadas = [datetime.now() + timedelta(days=d) for d in array_datas]

    for data_desejada in datas_desejadas:
        # Calcular o mês desejado para a data atual
        mes_desejado_numero, mes_desejado_nome = calcular_mes_desejado(data_desejada)

        # Converter o nome do mês para o formato de número
        mes_desejado_numero = nome_para_numero_mes(mes_desejado_nome)

        # Encontrar e imprimir o mês do calendário
        nome_elemnt = driver.find_element(By.XPATH, '//*[@id="activityCalendar"]/div[1]/div/div/div[2]/span[1]')
        driver.execute_script("arguments[0].scrollIntoView(true);", nome_elemnt)
        mes_calendario = nome_elemnt.text

        # Verificar se o mês do calendário é diferente do mês desejado
        while mes_calendario != mes_desejado_nome:
            # Clicar no botão "Próximo mês"
            botao_proximo_mes = driver.find_element(By.XPATH, '//*[@id="activityCalendar"]/div[1]/div/div/div[3]')
            botao_proximo_mes.click()
            time.sleep(2)
            # Atualizar o mês do calendário
            nome_elemnt = driver.find_element(By.XPATH, '//*[@id="activityCalendar"]/div[1]/div/div/div[2]/span[1]')
            mes_calendario = nome_elemnt.text

        # Iterar sobre os tipos de ingressos
        for parque_info in parques:
            parque_tipo: str = parque_info["tipo"]
            parque_xpath = parque_info["xpath"]

            try:
                # Encontrar o elemento do dia e clicar nele
                elemento_dia = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, f"activity-calendar-2024-{mes_desejado_numero}-{data_desejada.day:02d}"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", elemento_dia)
                elemento_dia.click()
                time.sleep(2)

                # Abrir o menu suspenso e selecionar o tipo de ingresso
                elemento_menu = driver.find_element(By.ID, "select2-categoria-container")
                elemento_menu.click()
                elemento_clicavel = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, parque_xpath))
                )
                time.sleep(2)
                elemento_clicavel.click()

                # Encontrar e imprimir o valor para a data atual e o tipo de ingresso
                elemento_valor = driver.find_element(By.XPATH,'//*[@id="tPrecioSpan0"]')
                valor = elemento_valor.text
                valor  = float(valor.replace('R$', '').replace('.', '').replace(',', '.'))
                #print(f"Valor para {data_desejada.strftime('%Y-%m-%d')} ({parque_tipo}): {valor}")

                precos_ingressos.append({
                    'Data_viagem': data_desejada.strftime('%Y-%m-%d'),
                    'Parque': parque_tipo,
                    "Preco_Avista": valor,
                    "Preco_Parcelado": valor
                })

                # Clicar no elemento para abrir o calendário novamente
                elemento_calendario = driver.find_element(By.XPATH, '//*[@id="foldedDate"]')
                elemento_calendario.click()
                time.sleep(2)
            except:
                precos_ingressos.append({
                    'Data_viagem': data_desejada.strftime('%Y-%m-%d'),
                    'Parque': parque_tipo,
                    "Preco_Avista": '-',
                    "Preco_Parcelado": '-'
                })
                print(f"Elemento do dia não encontrado para {data_desejada.strftime('%Y-%m-%d')} ({parque_tipo})")
    driver.quit()
    # df_precos_ingressos = pd.DataFrame(precos_ingressos)
    # # Exibir o DataFrame mesclado
    # df_precos_ingressos = df_precos_ingressos.drop_duplicates()
    # df_precos_ingressos = df_precos_ingressos.sort_values(by=['Data_viagem', 'Parque'])
    # # Salvar como JSON
    # df_precos_ingressos.to_json('precos_ingressos.json', orient='records')
    # # Fechar o navegador
    return precos_ingressos
    
# Chamada da função para obter os preços dos ingressos

async def main():
    await coletar_precos_civitatis_paris('40', [ 10, 20, 47, 65, 126],datetime.now().strftime("%Y-%m-%d"))
    
if __name__ == "__main__":
    asyncio.run(main())
