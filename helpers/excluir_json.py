import os

def apagar_arquivos_json_na_pasta_atual():
    # Obter o diretório atual
    pasta_atual = os.getcwd()

    # Listar todos os arquivos na pasta atual
    arquivos_na_pasta_atual = os.listdir(pasta_atual)

    # Iterar sobre os arquivos na pasta atual
    for arquivo in arquivos_na_pasta_atual:
        # Verificar se o arquivo é um JSON
        if arquivo.endswith('.json'):
            # Construir o caminho completo do arquivo
            caminho_completo = os.path.join(pasta_atual, arquivo)
            # Tentar apagar o arquivo
            try:
                os.remove(caminho_completo)
                print(f"Arquivo {caminho_completo} apagado com sucesso.")
            except OSError as e:
                print(f"Erro ao apagar o arquivo {caminho_completo}: {e}")

