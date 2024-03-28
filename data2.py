from datetime import datetime, timedelta

def dias_d_mais2(lista_dias):
    # Data atual
    data_atual = datetime.now().date()
    
    # Lista para armazenar os resultados como dicionários
    datas_formatadas = []

    # Mapeamento dos nomes dos meses
    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

    # Iterar sobre os dias da lista
    for dias in lista_dias:
        # Adicionar dias à data atual
        nova_data = data_atual + timedelta(days=dias)
        # Obter o dia e o mês
        dia_numero = nova_data.day
        mes_extenso = meses[nova_data.month - 1]  # -1 pois o índice começa em 0

        # Criando um dicionário com dia e mês
    
        datas_formatadas.append(dia_numero)

    return datas_formatadas

# Lista de dias a serem adicionados





