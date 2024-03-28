import pandas as pd
import re




def extrair_preco(texto):
    # Procurar por um padrão numérico precedido por "R$"
    padrao = r'R\$\s*(\d+\.?\d*)'
    correspondencia = re.search(padrao, texto)
    if correspondencia:
        return float(correspondencia.group(1))
    else:
        return None
    
def decolar_paris2(dados):
    
    precos = []
    for dado in dados:
        preco = extrair_preco(dado.get("preco", ""))
        if preco is not None:
            precos.append(preco)
    
    print(precos)    
    return precos


