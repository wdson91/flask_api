import json
import locale
from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import pandas as pd
import pytz
import asyncio
import os
import sys
import time
import requests
import pandas as pd
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
import logging
from selenium.webdriver.chrome.service import Service as ChromeService
import schedule
from flask_cors import CORS
from bs4 import BeautifulSoup
import json
from threading import Thread
from decolar.salvardadosdecolar import salvar_dados_decolar
from salvardados import salvar_dados
from salvardados import *
from urllib.parse import urlparse, parse_qs
import chromedriver_autoinstaller
import asyncio  # Importa o módulo asyncio para suporte a tarefas assíncronas
import schedule  # Importa o módulo schedule para agendar tarefas
from datetime import datetime  # Importa a classe datetime do módulo datetime
import pytz  # Importa o módulo pytz para lidar com fusos horários
from selenium.common.exceptions import NoSuchElementException
import re


from voupra.orlando.voupradisney.voupradisney import coletar_precos_voupra_disney
from voupra.orlando.vouprasea.vouprasea import coletar_precos_voupra_sea
from voupra.orlando.vouprauniversal.vouprauniversal import coletar_precos_voupra_universal

from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse, parse_qs


from vmz.vmzdisney.vmz_disney import coletar_precos_vmz
from vmz.vmzsea.vmzsea import coletar_precos_vmz_seaworld
from vmz.vmzuniversal.vmzuniversal import coletar_precos_vmz_universal


from ml.orlando.ml_universal.ml_universal import coletar_precos_ml_universal
from ml.orlando.mldisney.ml_disney import coletar_precos_ml_disney
from ml.orlando.mlsea.mlsea import coletar_precos_ml_seaworld

from decolar.discovery_cove.decolar_cove import decolar_discovery_cove
from decolar.legoland.decolar_lego import decolar_lego
from decolar.nasa.decolar_nasa import decolar_nasa

from decolar.california.decolar_california import decolar_california
from decolar.paris.decolar_paris import decolar_paris
from decolar.paris.dias_paris import dias_paris
from decolar.paris.meses_paris import meses_paris

from start.run import executar_ambos
from start.run_california import executar_california
from start.run_cove import coleta_cove
from start.run_furafila import coleta_furafila
from start.run_lego import coleta_lego
from start.run_nasa import coleta_nasa
from start.run_paris import executar_paris


from decolar.orlando.decolar_disney import  receive_disney_decolar
from decolar.orlando.sea_decolar import seaworld_decolar
from decolar.orlando.universal_decolar import receive_universal_decolar


import os
from helpers.excluir_json import apagar_arquivos_json_na_pasta_atual
sao_paulo_tz = pytz.timezone('America/Sao_Paulo')



def get_directories():
    """
    Retorna uma tupla com os caminhos para o diretório atual, pai e avô do arquivo.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    grandparent_dir = os.path.dirname(parent_dir)

    return current_dir, parent_dir, grandparent_dir


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


calibragem = 0
tipo_calibragem = 'automatica'
horarios = []

