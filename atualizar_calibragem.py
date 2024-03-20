import requests

def atualizar_calibragem(novo_valor):
    response = requests.post('http://localhost:5000/calibragem', json={'novo_valor': novo_valor})
    if response.status_code == 200:
        print("Calibragem atualizada com sucesso.")
    else:
        print("Erro ao atualizar a calibragem.")

def finalizar_calibragem():
    response = requests.post('http://localhost:5000/finalizar_calibragem')
    
    if response.status_code == 200:
        print("Calibragem finalizada com sucesso.")
    else:
        print("Erro ao finalizar a calibragem.")