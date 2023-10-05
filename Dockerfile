FROM python:3.9-slim

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie o arquivo requirements.txt e instale as dependências
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copie o restante do código da aplicação para o contêiner
COPY . .

# Expõe a porta em que sua aplicação Flask está escutando (substitua pela porta correta)
EXPOSE 5000

# Comando para executar a aplicação Flask
CMD ["python", "app.py"]
