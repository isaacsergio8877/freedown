# Use uma imagem base do Python
FROM python:3.11-slim

# Instala o ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação para o diretório de trabalho
COPY . .

# Expõe a porta que a aplicação vai usar
EXPOSE 5000

# Define o comando para iniciar a aplicação
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
