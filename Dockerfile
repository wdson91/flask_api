# Use a imagem oficial do Python como base
FROM python:3.8-slim

# Defina o diretório de trabalho
WORKDIR /app

# Copie os arquivos de requisitos para o contêiner
COPY requirements.txt .

# Instale as dependências da aplicação
RUN pip install --no-cache-dir -r requirements.txt

# Copie os arquivos Python para o diretório de trabalho no contêiner
COPY  . .

# Comando para executar os scripts Python
CMD ["python", "app.py"]
