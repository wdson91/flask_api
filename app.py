from atualizar_calibragem import mudar_horarios
from imports import *
from decolar.decolar_disney import disney_decolar

from decolar.sea import seaworld_decolar
from decolar.universal_decolar import universal_decolar
import pyautogui
from pynput.keyboard import Key, Controller


app = Flask(__name__)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})
days_to_add = [5, 10, 20, 47, 65, 126]
calibrating = False


horarios = []

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
        url_data = {'data': formatted_date, 'url': new_url}
        
        urls_with_dates.append(url_data)

    return urls_with_dates
# Rota GET para retornar as URLs com as datas desejadas
@app.route('/urls_disney', methods=['GET'])
def get_urls_disney():
    urls = generate_urls("https://www.decolar.com/atracoes-turisticas/d-DY_ORL/ingressos+para+walt+disney+world+resort-orlando?clickedPrice=702&priceDate=1710530966837&clickedCurrency=BRL&distribution=1&modalityId=ANNUAL-2D-2024&fixedDate={date}")
    
    return jsonify(urls)


@app.route('/urls_universal_basico', methods=['GET'])
def get_urls_universal():
    
    urls = generate_urls("https://www.decolar.com/atracoes-turisticas/d-UN_ORL/ingressos+para+universal+orlando+resort-orlando?distribution=1&date&fixedDate={date}&modalityId=ORL_2P1DPTP-date")
    return jsonify(urls)

@app.route('/urls_universal_14dias', methods=['GET'])
def get_urls_universal2():
    
    urls2 = generate_urls("https://www.decolar.com/atracoes-turisticas/d-UN_ORL/ingressos+para+universal+orlando+resort-orlando?distribution=1&date&fixedDate={date}&modalityId=ORL_3-PE-2024M-date")
    return jsonify(urls2)
@app.route('/date', methods=['GET'])
def get_date():
    urls = generate_urls()
    
    return jsonify(urls[1])


@app.route('/', methods=['GET'])
def hello():
    return  hora_global


@app.route('/receive_json_universal', methods=['POST'])
async def receive_json_universal():
    sao_paulo_tz = pytz.timezone('America/Sao_Paulo')
    
    data_list = request.json
    
    await universal_decolar(data_list,hora_global)

    return jsonify({"message": "Dados salvos com sucesso!"})

@app.route('/receive_json_disney', methods=['POST'])
async def receive_json_disney():
    sao_paulo_tz = pytz.timezone('America/Sao_Paulo')
    
    data_list = request.json
    await disney_decolar(data_list,hora_global)

    return jsonify({"message": "Dados salvos com sucesso!"})

@app.route('/receive_json_seaworld', methods=['POST'])
async def receive_json_seaworld():
    
    data_list = request.json
    
    await seaworld_decolar(data_list,hora_global)
    return jsonify({"message": "Dados salvos com sucesso!"})

@app.route('/calibrar', methods=['GET'])
async def calibrar():

    global calibragem
    global hora_global
    global tipo_calibragem
    global calibrating
    global horarios

    # Se a calibragem já estiver em andamento, retorne uma mensagem de erro
    if calibrating:
        return jsonify({"error": "Calibragem já em andamento"}), 400

    tipo = request.args.get('tipo', 'automatica')  # Obter o parâmetro tipo da URL, padrão é 'manual'

    calibrating = True
    calibragem = 1
    tipo_calibragem = tipo
    hora_global = datetime.now(sao_paulo_tz).strftime("%H:%M")
    
    time.sleep(2)
    if tipo == 'manual':
        pyautogui.hotkey('ctrl', '1')

    if hora_global == "07:00" or "11:00" or "14:00" or "17:00":
        if hora_global == "07:00":
            horarios = []
        horarios.append(hora_global)

    await executar_ambos(hora_global, days_to_add)

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

@app.route('/abortar_calibracao', methods=['GET'])
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


app.route('/hora', methods=['POST'])
def atualizar_hora():
    global horarios
    
    horario = request.json.get('horario')
    
    if horario == '07:00':
        horarios = []
    
    horarios.append(horario)


if __name__ == '__main__':
    
    app.run(debug=True, host='0.0.0.0',port=5000)