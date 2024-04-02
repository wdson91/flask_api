from datetime import datetime, timedelta

def dias_d_mais(lista_dias):
    # Data atual
    data_atual = datetime.now().date()
    
   
    # Mapeamento dos nomes dos meses
    meses = ['Janeiro', 'Fevereiro', 'Março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    datas_formatadas = []   
    # Iterar sobre os dias da lista
    for dias in lista_dias:
        # Adicionar dias à data atual
        nova_data = data_atual + timedelta(days=dias)
        # Obter o dia e o mês
        dia_numero = nova_data.day
        mes_extenso = meses[nova_data.month - 1]  # -1 pois o índice começa em 0

        # Criando um dicionário com dia e mês
    
        datas_formatadas.append(mes_extenso)

    return datas_formatadas 

# Lista de dias a serem adicionados
lista_de_dias = [5, 10, 20, 47, 65, 126]

# Chamada da função e exibição dos resultados
print(dias_d_mais(lista_de_dias))
