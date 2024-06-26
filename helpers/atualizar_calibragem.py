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

def mudar_horarios(hour):
    response = requests.post('http://localhost:5000/hora', json={'horario': hour})

    if response.status_code == 200:
        print("Horários atualizados com sucesso.")
    else:
        print("Erro ao atualizar os horários.")

def finalizar_halloween():
    response = requests.get('http://localhost:5000/finalizar_halloween')

    if response.status_code == 200:
        print("Halloween finalizado com sucesso.")
    else:
        print("Erro ao finalizar o Halloween.")


def finalizar_chip():
    response = requests.get('http://localhost:5000/finalizar_chip')

    if response.status_code == 200:
        print("Chip finalizado com sucesso.")
    else:
        print("Erro ao finalizar o Chip.")
