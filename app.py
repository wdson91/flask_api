from atualizar_calibragem import mudar_horarios

from imports import *
import pyautogui
from pynput.keyboard import Key, Controller

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
days_to_add =[5, 10, 20, 47, 65, 126]
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

@app.route('/dados_paris', methods=['GET'])
async def dados_paris():
    
    global data_atual
    global hora_global
    
    
    await juntarjsons_paris(hora_global,data_atual)
    
    return jsonify({"message": "Dados salvos com sucesso!"})

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

@app.route('/receive_json_seaworld', methods=['POST'])
async def receive_json_seaworld():
    global hora_global
    global data_atual
    
    data_list = request.json

    data = data_atual
    hora = hora_global
    
    await seaworld_decolar(data_list,hora,data)
    return jsonify({"message": "Dados salvos com sucesso!"})


#ROTAS PARA CALIFORNIA
# @app.route('/xpath_california', methods=['GET'])
# def get_xpath_california():
    
#     base_xpath = "/html/body/div[2]/div/div[2]/div/div/div/div[4]/tour-modalities/div/ul/li"
#     xpaths = []
#     for i in range(1, num_elements + 1):
#         xpath = f"{base_xpath}[{i}]/tour-modality-cluster/div/div/em/div/div[2]/div[1]/div[3]/section[1]/date-picker/div/div[1]/div/input"
#         xpaths.append(xpath)
    
#     return jsonify(xpaths)

# @app.route('/xpath_calendar', methods=['GET'])
# def get_xpath_calendar():
    
#     xpath_base = '/html/body/div[2]/div/div[2]/div/div/div/div[4]/tour-modalities/div/ul/li'
    
#     xpaths = []
#     for i in range(1, num_elements + 1):
#         xpath = f"{xpath_base}[{i}]/tour-modality-cluster/div/div/em/div/div[2]/div[1]/div[3]/section[1]/date-picker/div/span/span"
#         xpaths.append(xpath)
    
#     return jsonify(xpaths)

# @app.route('/xpath_preco_california', methods=['GET'])
# def get_xpath_preco_california():
    # base_xpath = "/html/body/div[2]/div/div[2]/div/div/div/div[4]/tour-modalities/div/ul/li"
    
    # xpaths = []
    # for i in range(1, num_elements + 1):
    #     xpath = f"{base_xpath}[{i}]/tour-modality-cluster/div/div/em/div/div[2]/div[2]/div/div/div[2]/div/span[2]"
    #     xpaths.append(xpath)
    # return jsonify(xpaths)

@app.route('/california', methods=['GET'])
async def coleta_california():
    global data_atual
    global hora_global
    data_atual = datetime.now(sao_paulo_tz).strftime("%Y-%m-%d")
    hora_global = datetime.now(sao_paulo_tz).strftime("%H:%M")
    
    array_datas = [5, 10, 20, 47, 65, 126]
    
    time.sleep(5)
    #pyautogui.hotkey('ctrl', '2')
    await executar_california(hora_global, array_datas, data_atual)
    
    return jsonify({"message": "Dados salvos com sucesso!"})

@app.route('/dados_california', methods=['GET'])
async def dados_california():
    
    global data_atual
    global hora_global
    
    
    await juntarjsons_california(hora_global,data_atual)
    
    return jsonify({"message": "Dados salvos com sucesso!"})


@app.route('/receive_json_decolar_california', methods=['POST'])
def receive_json_decolar_california():
    global data_atual
    data = request.json
    
    decolar_california(data,data_atual)
    return jsonify({"message": "Dados salvos com sucesso!"})


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
    
    if hora_global == "07:00" or "11:00" or "14:00" or "17:00":
        if hora_global == "07:00":
            horarios = []
        horarios.append(hora_global)
    time.sleep(3)
    await executar_ambos(hora_global, days_to_add,data_atual)

    return jsonify({"message": "Calibragem iniciada com sucesso!"})

@app.route('/status_calibragem', methods=['GET'])
async def status_calibragem():
    
    global calibragem
    global hora_global
    global tipo_calibragem
    global horarios
    global calibrating
    
    data_atual = datetime.now(sao_paulo_tz).strftime("%Y-%m-%d")
    
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




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)
