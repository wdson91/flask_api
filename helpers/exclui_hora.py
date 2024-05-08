import os
import json
import pandas as pd
import logging
import asyncio
import time
from datetime import datetime
import pytz

from imports import baixar_blob_se_existir, upload_blob
from salvardados import carregar_dados_json, salvar_dados_json, salvar_dados_margem
from helpers.atualizar_calibragem import atualizar_calibragem, finalizar_calibragem

async def juntarjsons(hour, data_atual):
    # Lista de empresas e parques
    empresas = ['voupra', 'vmz', 'decolar', 'ml']
    parques = ['disney', 'universal', 'seaworld']
    
    # Obtém o horário atual
    nova_hora_formatada = '08:15'
    data_atual = '2024-03-24'

    # Dicionário para armazenar os dados filtrados
    dados_filtrados = {}

    # Baixa os arquivos JSON dos diferentes parques e empresas
    for empresa in empresas:
        for parque in parques:
            # Nome do arquivo
            nome_arquivo = f'{parque}_{empresa}_{data_atual}.json'
            
            # Baixa o arquivo JSON se existir
            baixar_blob_se_existir(nome_arquivo, empresa)

            # Carrega os dados JSON baixados
            dados = carregar_dados_json(nome_arquivo)

            # Filtra os dados para excluir aqueles da hora específica
            dados_filtrados_empresa_parque = [dado for dado in dados if dado.get('Hora_coleta') != nova_hora_formatada]

            # Salva os dados filtrados de volta no arquivo JSON
            with open(nome_arquivo, 'w') as f:
                json.dump(dados_filtrados_empresa_parque, f)
            
            # Salva o arquivo no Blob Storage
            upload_blob(nome_arquivo, nome_arquivo, empresa)

            # Adiciona os dados filtrados ao dicionário
            if empresa not in dados_filtrados:
                dados_filtrados[empresa] = {}
            dados_filtrados[empresa][parque] = dados_filtrados_empresa_parque

    # Nome do arquivo para salvar os dados
    nome_arquivo_agregado = f'dados_{data_atual}.json'
    
    # Salva os dados filtrados no Blob Storage e também localmente como um arquivo JSON
    with open(nome_arquivo_agregado, 'w') as f:
        json.dump(dados_filtrados, f)

    # Salva os dados filtrados agregados no Blob Storage
    upload_blob(nome_arquivo_agregado, nome_arquivo_agregado, 'arquivos-agregados')

    # Remove os arquivos JSON locais
    for arquivo in os.listdir():
        if arquivo.endswith('.json'):
            os.remove(arquivo)
    
    logging.info("Arquivos JSON locais excluídos.")
    
    # Aguarda um momento antes de finalizar a calibragem
    await asyncio.sleep(30)
    finalizar_calibragem()

if __name__ == "__main__":
    # Hora global
    hora_global = datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%H:%M")
    data_atual = datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%Y-%m-%d")
    
    # Executa a função principal
    asyncio.run(juntarjsons(hora_global, data_atual))
