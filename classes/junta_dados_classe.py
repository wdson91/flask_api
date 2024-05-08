from imports import *

from helpers.excluir_json import apagar_arquivos_json_na_pasta_atual

from salvardados import baixar_blob_se_existir, carregar_dados_json, salvar_dados_margem
from helpers.atualizar_calibragem import atualizar_calibragem, finalizar_calibragem, mudar_horarios

class JuntarJsons:
    def __init__(self, data_atual, empresas, parques, cidade=None):
        self.data_atual = data_atual
        self.empresas = empresas
        self.parques = parques
        self.cidade = cidade
        self.hora_global = datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%H:%M")

    async def executar(self):
        dados_modificados = {}
        nova_hora_formatada = self.hora_global
        
        for empresa in self.empresas:
            for parque in self.parques:
                pasta_empresa = self.cidade + '/' + empresa if self.cidade else empresa
                
                arquivo = f'{parque}_{empresa}_{self.data_atual}.json'
                baixar_blob_se_existir(arquivo, pasta_empresa)
                
                dados = carregar_dados_json( arquivo)
                if empresa not in dados_modificados:
                    dados_modificados[empresa] = {}
                dados_modificados[empresa][parque] = dados

        nome_arquivo = f'dados_{self.data_atual}.json'
        
        self.salvar_dados_json(dados_modificados, nome_arquivo)
        self.salvar_dataframe_json(nome_arquivo, nova_hora_formatada)
        
        finalizar_calibragem()
        apagar_arquivos_json_na_pasta_atual()

        return
        # Se necessário, descomente a linha abaixo para chamar a função `atualizar_calibragem`
        # atualizar_calibragem(100)

    def salvar_dados_json(self, dados, nome_arquivo):
        with open(nome_arquivo, 'w') as f:
            json.dump(dados, f)

    def salvar_dataframe_json(self, nome_arquivo, nova_hora_formatada):
        df = pd.read_json(nome_arquivo)
        df = pd.DataFrame(df)
        
        salvar_dados_margem(df, nome_arquivo, f'{self.cidade}/dados', nova_hora_formatada)

if __name__ == "__main__":
    data_atual = datetime.now(pytz.timezone('America/Sao_Paulo')).strftime("%Y-%m-%d")
    empresas = ['voupra', 'vmz', 'decolar', 'ml']
    parques = ['disney', 'universal', 'seaworld']
    cidade = 'orlando'
    
    juntar_json = JuntarJsons(data_atual, empresas, parques, cidade)
    asyncio.run(juntar_json.executar())

    # Se você quiser rodar sem especificar uma cidade, basta chamar a classe sem esse parâmetro:
    # juntar_json_sem_cidade = JuntarJsons(data_atual, empresas, parques)
    # asyncio.run(juntar_json_sem_cidade.executar())
