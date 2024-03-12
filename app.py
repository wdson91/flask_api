from imports import *
from decolar_disney import disney_decolar
from sea import seaworld_decolar
from universal_decolar import universal_decolar


app = Flask(__name__)

# Função para gerar as URLs com as datas desejadas
def generate_urls(url):
    base_url =  url
    base_date = datetime.now()
    days_to_add = [5, 10, 20, 47, 65, 126]

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
    urls = generate_urls("https://www.decolar.com/atracoes-turisticas/d-DY_ORL/ingressos+para+walt+disney+world+resort-orlando?from=2024-03-08&to=2025-03-08&destination=ORL&distribution=1&fixedDate={date}&modalityId=ANNUAL-2D-2024")
    
    return jsonify(urls)

@app.route('/urls_universal', methods=['GET'])
def get_urls_universal():
    
    urls = generate_urls("https://www.decolar.com/atracoes-turisticas/d-UN_ORL/ingressos+para+universal+orlando+resort-orlando?distribution=1&modalityId=ORL_2P1DPTP-date&fixedDate={date}")
    
    return jsonify(urls)

@app.route('/date', methods=['GET'])
def get_date():
    urls = generate_urls()
    
    return jsonify(urls[1])


@app.route('/', methods=['GET'])
def hello():
    return "Hello, World!"


@app.route('/receive_json_universal', methods=['POST'])
async def receive_json_universal():
    sao_paulo_tz = pytz.timezone('America/Sao_Paulo')
    data_hora = datetime.now(sao_paulo_tz).strftime("%H:%M")
    data_list = request.json
    await universal_decolar(data_list,data_hora)

    return jsonify({"message": "Dados salvos com sucesso!"})

@app.route('/receive_json_disney', methods=['POST'])
async def receive_json_disney():
    sao_paulo_tz = pytz.timezone('America/Sao_Paulo')
    data_hora = datetime.now(sao_paulo_tz).strftime("%H:%M")
    data_list = request.json
    await disney_decolar(data_list,data_hora)

    return jsonify({"message": "Dados salvos com sucesso!"})

@app.route('/receive_json_seaworld', methods=['POST'])
async def receive_json_seaworld():
    sao_paulo_tz = pytz.timezone('America/Sao_Paulo')
    data_hora = datetime.now(sao_paulo_tz).strftime("%H:%M")
    data_list = request.json
    await seaworld_decolar(data_list,data_hora)

    return jsonify({"message": "Dados salvos com sucesso!"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0',port=5000)