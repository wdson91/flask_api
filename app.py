
import threading


from imports import *
import pyautogui
from pynput.keyboard import Key, Controller

from classes.junta_dados_classe import JuntarJsons
from decolar.hopper.decolar_disney_hopper import receive_disney_decolar_hopper
from qualidade.qualidade import coleta_precos


from start.run_hopper import executar_hopper
from start.run_halloween import executar_halloween
from start.run_outros import  coleta_outros_parques

from decolar.halloween.decolar_halloween import decolar_halloween





app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
days_to_add =[5, 10
              , 20, 47, 65, 126]
calibrating = False
global hora_global
global data_atual

sao_paulo_tz = pytz.timezone('America/Sao_Paulo')
data_atual = datetime.now(sao_paulo_tz).strftime("%Y-%m-%d")
hora_global = datetime.now(sao_paulo_tz).strftime("%H:%M")
horarios = []


@app.route('/', methods=['GET'])
def hello():
    return  hora_global

##ROTAS HALLOWEEN - TEMPORARIA
@app.route('/halloween', methods=['GET'])
async def coleta_halloween():
    
    global data_atual
    global hora_global
    data_atual = datetime.now(sao_paulo_tz).strftime("%Y-%m-%d")
    hora_global = datetime.now(sao_paulo_tz).strftime("%H:%M")
    
    array_datas = [5, 10, 20, 47, 65, 126]
    time.sleep(3)
    await executar_halloween(hora_global, array_datas, data_atual)

    return jsonify({"message": "Dados salvos com sucesso!"})


@app.route('/meses_halloween', methods=['GET'])
def meses_halloween():
    meses = ['setembro', 'outubro', 'novembro']
    
    return jsonify(meses)

@app.route('/dias_halloween', methods=['GET'])
def dias_halloween():
    urls = [1,3,5,9,18,23]
    
    return urls

@app.route('/urls_halloween', methods=['GET'])
def get_urls_halloween():
    
    urls = [{'dias':'2024-09-05',
           'urls':'https://www.decolar.com/atracoes-turisticas/d-UN_ORL/ingressos+para+universal+orlando+resort-orlando?clickedPrice=2069&priceDate=1711367621828&clickedCurrency=BRL&distribution=1&modalityId=ORL_24_HHN_LATIN_DATE&fixedDate=2024-09-05'},
            {'dias':'2024-09-18',
             'urls':'https://www.decolar.com/atracoes-turisticas/d-UN_ORL/ingressos+para+universal+orlando+resort-orlando?clickedPrice=2069&priceDate=1711367621828&clickedCurrency=BRL&distribution=1&modalityId=ORL_24_HHN_LATIN_DATE&fixedDate=2024-09-18'},
            {'dias':'2024-10-09',
             'urls':'https://www.decolar.com/atracoes-turisticas/d-UN_ORL/ingressos+para+universal+orlando+resort-orlando?clickedPrice=2069&priceDate=1711367621828&clickedCurrency=BRL&distribution=1&modalityId=ORL_24_HHN_LATIN_DATE&fixedDate=2024-10-09'},
            {'dias':'2024-10-23',
             'urls':'https://www.decolar.com/atracoes-turisticas/d-UN_ORL/ingressos+para+universal+orlando+resort-orlando?clickedPrice=2069&priceDate=1711367621828&clickedCurrency=BRL&distribution=1&modalityId=ORL_24_HHN_LATIN_DATE&fixedDate=2024-10-23'},
            {'dias':'2024-11-01',
             'urls':'https://www.decolar.com/atracoes-turisticas/d-UN_ORL/ingressos+para+universal+orlando+resort-orlando?clickedPrice=2069&priceDate=1711367621828&clickedCurrency=BRL&distribution=1&modalityId=ORL_24_HHN_LATIN_DATE&fixedDate=2024-11-01'},
            {'dias':'2024-11-03',
             'urls':'https://www.decolar.com/atracoes-turisticas/d-UN_ORL/ingressos+para+universal+orlando+resort-orlando?clickedPrice=2069&priceDate=1711367621828&clickedCurrency=BRL&distribution=1&modalityId=ORL_24_HHN_LATIN_DATE&fixedDate=2024-11-03'}]
    
    #urls=['https://www.decolar.com/atracoes-turisticas/d-UN_ORL/ingressos+para+universal+orlando+resort-orlando?clickedPrice=2069&priceDate=1711367621828&clickedCurrency=BRL&distribution=1&modalityId=ORL_24_HHN_LATIN_DATE&fixedDate=2024-09-05','https://www.decolar.com/atracoes-turisticas/d-UN_ORL/ingressos+para+universal+orlando+resort-orlando?clickedPrice=2069&priceDate=1711367621828&clickedCurrency=BRL&distribution=1&modalityId=ORL_24_HHN_LATIN_DATE&fixedDate=2024-09-18','https://www.decolar.com/atracoes-turisticas/d-UN_ORL/ingressos+para+universal+orlando+resort-orlando?clickedPrice=2069&priceDate=1711367621828&clickedCurrency=BRL&distribution=1&modalityId=ORL_24_HHN_LATIN_DATE&fixedDate=2024-10-09','https://www.decolar.com/atracoes-turisticas/d-UN_ORL/ingressos+para+universal+orlando+resort-orlando?clickedPrice=2069&priceDate=1711367621828&clickedCurrency=BRL&distribution=1&modalityId=ORL_24_HHN_LATIN_DATE&fixedDate=2024-10-09','https://www.decolar.com/atracoes-turisticas/d-UN_ORL/ingressos+para+universal+orlando+resort-orlando?clickedPrice=2069&priceDate=1711367621828&clickedCurrency=BRL&distribution=1&modalityId=ORL_24_HHN_LATIN_DATE&fixedDate=2024-10-23','https://www.decolar.com/atracoes-turisticas/d-UN_ORL/ingressos+para+universal+orlando+resort-orlando?clickedPrice=2069&priceDate=1711367621828&clickedCurrency=BRL&distribution=1&modalityId=ORL_24_HHN_LATIN_DATE&fixedDate=2024-11-01','https://www.decolar.com/atracoes-turisticas/d-UN_ORL/ingressos+para+universal+orlando+resort-orlando?clickedPrice=2069&priceDate=1711367621828&clickedCurrency=BRL&distribution=1&modalityId=ORL_24_HHN_LATIN_DATE&fixedDate=2024-11-03']
    return jsonify(urls)

@app.route('/receive_json_decolar_halloween', methods=['POST'])
def receive_json_decolar_halloween():
    global data_atual
    data = request.json
    decolar_halloween(data,data_atual)
    
    return jsonify({"message": "Dados salvos com sucesso!"})

#ROTAS PARA PARIS
@app.route('/meses_paris', methods=['GET'])
def meses_paris_api():
    urls = meses_paris(days_to_add)
    
    return jsonify(urls)

@app.route('/dias_paris', methods=['GET'])
def dias_paris_api():
    urls = dias_paris(days_to_add)
    
    return urls

@app.route('/paris', methods=['GET'])
async def coleta_paris():
    global data_atual
    global hora_global
    data_atual = datetime.now(sao_paulo_tz).strftime("%Y-%m-%d")
    hora_global = datetime.now(sao_paulo_tz).strftime("%H:%M")
    
    array_datas = [5, 10, 20, 47, 65, 126]
    
    time.sleep(5)
    #pyautogui.hotkey('ctrl', '2')
    await executar_paris(hora_global, array_datas, data_atual)
    
    return jsonify({"message": "Dados salvos com sucesso!"})

@app.route('/urls_paris', methods=['GET'])
def get_urls_paris():
    urls = ['https://www.decolar.com/atracoes-turisticas/d-GL_PAR_2453/entrada+da+disneyland+paris-paris?clickedPrice=649&priceDate=1711975109134&clickedCurrency=BRL&currency=BRL','https://www.decolar.com/atracoes-turisticas/d-PAM_PAR_53515/disneyland+paris+acesso+a+2+parques+em+2+dias+2024-paris?clickedPrice=1475&priceDate=1712252562173&clickedCurrency=BRL&currency=BRL']
    
    return jsonify(urls)



# Função para gerar as URLs com as datas desejadas
def generate_urls(url):
    base_url =  url
    base_date = datetime.now()
    

    urls_with_dates = []

    for days in days_to_add:
        new_date = base_date + timedelta(days=days)
        formatted_date = new_date.strftime("%Y-%m-%d")
        new_url = base_url.format(date=formatted_date)

        # Criar um dicionário com a data e a URL
        url_data = {'dias': formatted_date, 'url': new_url}
        
        urls_with_dates.append(url_data)

    return urls_with_dates
# Rota GET para retornar as URLs com as datas desejadas
@app.route('/urls_disney', methods=['GET'])
def get_urls_disney():
    urls = generate_urls("https://www.decolar.com/atracoes-turisticas/d-DY_ORL/ingressos+para+walt+disney+world+resort-orlando?clickedPrice=702&priceDate=1710530966837&clickedCurrency=BRL&distribution=1&modalityId=ANNUAL-2D-2024&fixedDate={date}")
    
    return jsonify(urls)


@app.route('/receive_json_decolar_paris', methods=['POST'])
def receive_json_paris_disney():
    global data_atual
    data = request.json
    decolar_paris(data,data_atual)
    return jsonify({"message": "Dados salvos com sucesso!"})


#ROTAS PARA DECOLAR
@app.route('/urls_universal_basico', methods=['GET'])
def get_urls_universal():
    
    urls = generate_urls("https://www.decolar.com/atracoes-turisticas/d-UN_ORL/ingressos+para+universal+orlando+resort-orlando?clickedPrice=2069&priceDate=1711367621828&clickedCurrency=BRL&distribution=1&modalityId=ORL_2P2DAY-date&fixedDate={date}")
    return jsonify(urls)



@app.route('/urls_universal_aqua', methods=['GET'])
def get_urls_universal_aqua():
    
    urls1 = generate_urls("https://www.decolar.com/atracoes-turisticas/d-DY_ORL/ingressos+para+walt+disney+world+resort-orlando?clickedPrice=701&priceDate=1711572471771&clickedCurrency=BRL&distribution=1&fixedDate={date}&modalityId=4PARKMAGIC-2024&additionalId=DISNEY-4D-WP-SO-water-parks-sports")
    return jsonify(urls1)

@app.route('/urls_universal_14dias', methods=['GET'])
def get_urls_universal2():
    
    urls2 = generate_urls("https://www.decolar.com/atracoes-turisticas/d-UN_ORL/ingressos+para+universal+orlando+resort-orlando?distribution=1&date&fixedDate={date}&modalityId=ORL_3-PE-2024M-date")
    return jsonify(urls2)

@app.route('/receive_json_universal', methods=['POST'])
async def receive_json_universal():
    #data_atual = datetime.now(sao_paulo_tz).strftime("%Y-%m-%d")
    global hora_global
    global data_atual
    data = data_atual
    hora = hora_global
    data_list = request.json
    
    await receive_universal_decolar(data_list,hora_global,data)

    return jsonify({"message": "Dados salvos com sucesso!"})

@app.route('/receive_json_disney', methods=['POST'])
async def receive_json_disney():
    
    
    global hora_global
    global data_atual
    data = data_atual
    hora = hora_global
    data_list = request.json
    await receive_disney_decolar(data_list,hora,data)

    return jsonify({"message": "Dados salvos com sucesso!"})

@app.route('/receive_json_hopper', methods=['POST'])
async def receive_json_hopper():
    
    
    global hora_global
    global data_atual
    data = data_atual
    hora = hora_global
    data_list = request.json
    await receive_disney_decolar_hopper(data_list,hora,data)

    return jsonify({"message": "Dados salvos com sucesso!"})


@app.route('/receive_json_seaworld', methods=['POST'])
async def receive_json_seaworld():
    global hora_global
    global data_atual
    
    data_list = request.json

    data = data_atual
    hora = hora_global
    
    await seaworld_decolar(data_list,hora,data)
    return jsonify({"message": "Dados salvos com sucesso!"})


@app.route('/hopper', methods=['GET'])
async def hopper():
    
    global hora_global
    global data_atual
    
    days_to_add = [5, 10, 20, 47, 65, 126]

    data_atual = datetime.now(sao_paulo_tz).strftime("%Y-%m-%d")
    hora_global = datetime.now(sao_paulo_tz).strftime("%H:%M")
    
    await executar_hopper(hora_global, days_to_add, data_atual)
    return  hora_global

#ROTAS PARA CALIFORNIA

@app.route('/california', methods=['GET'])
async def coleta_california():
    global data_atual
    global hora_global
    data_atual = datetime.now(sao_paulo_tz).strftime("%Y-%m-%d")
    hora_global = datetime.now(sao_paulo_tz).strftime("%H:%M")
    
    array_datas = [5,10, 20, 47, 65, 126]
    
    time.sleep(5)
    #pyautogui.hotkey('ctrl', '2')
    await executar_california(hora_global, array_datas, data_atual)
    
    return jsonify({"message": "Dados salvos com sucesso!"})


@app.route('/receive_json_decolar_california', methods=['POST'])
def receive_json_decolar_california():
    global data_atual
    data = request.json
    
    decolar_california(data,data_atual)
    return jsonify({"message": "Dados salvos com sucesso!"})

##ROTAS DISCOVERY COVE
@app.route('/receive_json_decolar_discovery_cove', methods=['POST'])
def receive_json_decolar_discovery_cove():
    global data_atual
    data = request.json
    decolar_discovery_cove(data,data_atual)
    return jsonify({"message": "Dados salvos com sucesso!"})


@app.route('/outros_parques', methods=['GET'])
async def outros_parques():
    global data_atual
    global hora_global

    # Recebendo o parâmetro da requisição
    parque = request.args.get('parque')
    
    if not parque:
        return jsonify({"error": "O parque deve ser especificado."}), 400

    if parque == 'halloween':
        empresas = ['voupra', 'decolar', 'ml', 'vmz']
        parques = ['halloween']
        pasta = 'halloween'
        
    elif parque == 'dados':
        
        empresas = ['voupra', 'vmz', 'decolar','ml']
        parques = ['lego', 'nasa', 'discovery_cove','furafila']
        pasta = 'outros'

    elif parque ==  'paris':
        
        empresas = ['voupra', 'decolar', 'ml','gyg','civitatis']
        parques = ['paris']
        pasta = 'paris'
        
    elif parque == 'california':
        
        empresas = ['voupra', 'decolar', 'ml', 'vmz','rca']
        parques = ['california']
        pasta = 'california'
        
    else:
        return jsonify({"error": "Parque inválido."}), 400
    
    juntar_jsons = JuntarJsons(data_atual, empresas, parques, pasta)
        
    await juntar_jsons.executar()
    
    return {"message": "Dados salvos com sucesso!"}, 200



##ROTAS NASA

@app.route('/receive_json_decolar_nasa', methods=['POST'])
def receive_json_decolar_nasa():
    global data_atual
    data = request.json
    decolar_nasa(data,data_atual)
    
    return jsonify({"message": "Dados salvos com sucesso!"})





##ROTAS LEGOLAND

@app.route('/receive_json_decolar_lego', methods=['POST'])
def receive_json_decolar_lego():
    global data_atual
    data = request.json
    decolar_lego(data,data_atual)
    
    return jsonify({"message": "Dados salvos com sucesso!"})





## ROTAS FURA FILA
@app.route('/coleta_outros', methods=['GET'])
async def furafila():
    global data_atual
    global hora_global
    
    data_atual = datetime.now(sao_paulo_tz).strftime("%Y-%m-%d")
    hora_global = datetime.now(sao_paulo_tz).strftime("%H:%M")
    
    array_datas = [5,10, 20, 47, 65, 126]
    
    time.sleep(5)
    
    #await coleta_furafila(hora_global, array_datas, data_atual)
    await coleta_outros_parques(hora_global, array_datas, data_atual)

    return jsonify({"message": "Dados salvos com sucesso!"})


## ROTAS CALIBRAGEM
 
@app.route('/calibrar', methods=['GET'])
async def calibrar():

    global calibragem
    global hora_global
    global tipo_calibragem
    global calibrating
    global horarios
    global data_atual
    
    # Se a calibragem já estiver em andamento, retorne uma mensagem de erro
    if calibrating:
        return jsonify({"error": "Calibragem já em andamento"}), 400

    tipo = request.args.get('tipo', 'automatica')  # Obter o parâmetro tipo da URL, padrão é 'manual'

    calibrating = True
    calibragem = 1
    tipo_calibragem = tipo
    hora_global = datetime.now(sao_paulo_tz).strftime("%H:%M")
    
    data_atual = datetime.now(sao_paulo_tz).strftime("%Y-%m-%d")
    
    time.sleep(5)
    if tipo == 'manual':
        pyautogui.hotkey('ctrl', '1')
    
    
    # Criar o nome do arquivo usando a data atual
    nome_arquivo = f"horarios/horarios_{data_atual}.txt"
    # Abrir o arquivo em modo de adição (append) ou criá-lo se não existir
    with open(nome_arquivo, "a") as arquivo:
        # Adicionar o horário ao arquivo
        arquivo.write(hora_global + "\n")
    
    time.sleep(3)
    await executar_ambos(hora_global, days_to_add, data_atual)

    return jsonify({"message": "Calibragem iniciada com sucesso!"})

@app.route('/calibrar_teste', methods=['GET'])
async def calibrar_teste():

    global calibragem
    global hora_global
    global tipo_calibragem
    global calibrating
    global horarios
    global data_atual
    
    # Se a calibragem já estiver em andamento, retorne uma mensagem de erro
    if calibrating:
        return jsonify({"error": "Calibragem já em andamento"}), 400

    tipo = request.args.get('tipo', 'automatica')  # Obter o parâmetro tipo da URL, padrão é 'manual'

    calibrating = True
    calibragem = 1
    tipo_calibragem = tipo
    hora_global = datetime.now(sao_paulo_tz).strftime("%H:%M")
    data_atual = datetime.now(sao_paulo_tz).strftime("%Y-%m-%d")
    
    time.sleep(5)
    if tipo == 'manual':
        pyautogui.hotkey('ctrl', '1')
    
    
    # Criar o nome do arquivo usando a data atual
    nome_arquivo = f"horarios_{data_atual}.txt"
    # Abrir o arquivo em modo de adição (append) ou criá-lo se não existir
    with open(nome_arquivo, "a") as arquivo:
        # Adicionar o horário ao arquivo
        arquivo.write(hora_global + "\n")
    
    time.sleep(3)
    await executar_ambos_teste(hora_global, days_to_add, data_atual)

    return jsonify({"message": "Calibragem iniciada com sucesso!"})


@app.route('/status_calibragem', methods=['GET'])
async def status_calibragem():
    
    global calibragem
    global hora_global
    global tipo_calibragem
    global calibrating
    
    data_atual = datetime.now(sao_paulo_tz).strftime("%Y-%m-%d")
    nome_arquivo = f"horarios/horarios_{data_atual}.txt"
    
    # Verificar se o arquivo existe antes de tentar ler
    if os.path.exists(nome_arquivo):
        with open(nome_arquivo, 'r') as file:
            horarios = file.read().splitlines()
    else:
        horarios = []

    return jsonify({"Porcentagem": calibragem,
                    "Hora_inicio": hora_global,
                    "Tipo": tipo_calibragem,
                    "Data": data_atual,
                    "Horarios": horarios,
                    "Calibrating": calibrating})


@app.route('/calibragem', methods=['POST'])
def set_calibragem():
    global calibragem


    novo_valor = request.json.get('novo_valor')
    if novo_valor is not None:
        calibragem = novo_valor
        return jsonify({'message': 'Calibragem atualizada com sucesso', 'novo_valor': calibragem})
    else:
        return jsonify({'error': 'Falta o parâmetro "novo_valor" no corpo da solicitação'}), 400

@app.route('/abortar_calibragem', methods=['GET'])
def abortar_calibragem():
    global calibrating
    
    # Se a calibragem não estiver em andamento, retorne uma mensagem de erro
    if not calibrating:
        return jsonify({"error": "Não há calibragem em andamento para ser abortada"}), 400
    
    # Define a variável de controle como False para abortar a calibragem
    calibrating = False
    
    # Reinicia a aplicação
    os.execl(sys.executable, sys.executable, *sys.argv)

@app.route('/finalizar_calibragem', methods=['POST'])
def finalizar_calibragem_api():
    global calibrating
    calibrating = False
    # hora_global = None
    # tipo_calibragem = None
    return jsonify({"message": "Calibragem finalizada com sucesso!"})

@app.route('/date', methods=['GET'])
def get_date():
    urls = generate_urls()
    
    return jsonify(urls[1])

app.route('/hora', methods=['POST'])
def atualizar_hora():
    global horarios
    
    horario = request.json.get('horario')
    
    if horario == '07:00':
        horarios = []
    
    horarios.append(horario)

## ROTAS PARA QUALIDADE
@app.route('/qualidade', methods=['GET'])
def coleta():
    
    global calibrating
     # Se a calibragem já estiver em andamento, retorne uma mensagem de erro
    if calibrating:
        return jsonify({"error": "Calibragem já em andamento"}), 400
    
    calibrating = True
    coleta_precos()
    return jsonify({"message": "Dados salvos com sucesso!"})

# @app.route('/nota', methods=['GET'])
# def nota():
    
#     dia = datetime.now().strftime('%d-%m-%Y')
#     # Abre o arquivo JSON e lê os dados
#     with open(f'leads_{dia}.json', 'r', encoding='utf-8') as f:
#         dados = json.load(f)
    
#     # Retorna os dados como resposta JSON
#     return jsonify(dados)

# @app.route('/qualidadeteste', methods=['GET'])
# def coletateste():
    
#     global calibrating
#      # Se a calibragem já estiver em andamento, retorne uma mensagem de erro
#     if calibrating:
#         return jsonify({"error": "Calibragem já em andamento"}), 400
    
#     calibrating = True
#     coleta_precos_teste()
#     return jsonify({"message": "Dados salvos com sucesso!"})


@app.route('/hopper', methods=['GET'])
async def hopper_2():
    
    global hora_global
    global data_atual

    hour = datetime.now(sao_paulo_tz).strftime("%H:%M")
    array_datas = [5,10, 20, 47, 65, 126]
    thread = threading.Thread(target=coletar_precos_vmz_hopperbasicos ,args=(hour, array_datas, data_atual))
    #thread = threading.Thread(target=coletar_precos_vmz_hopperdisneydias, args=(hour, array_datas, data_atual))
    
    thread.start()
    thread.join()
    return  hora_global





if __name__ == '__main__':
    
    app.run(threaded=True,debug=True, host='0.0.0.0',port=5000)
