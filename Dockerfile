# Use uma imagem base adequada
FROM python:3.8

EXPOSE 5000

RUN apt update -y

# Crie um ambiente virtual
RUN python3 -m venv venv

# Ative o ambiente virtual
RUN . venv/bin/activate

# Defina o diretório de trabalho
WORKDIR /app

# Copie o requirements.txt para o contêiner
COPY requirements.txt .

# Instale as dependências no ambiente virtual
RUN pip install -r requirements.txt

# Copie o restante do código-fonte
COPY . .

# Defina o comando de inicialização da aplicação
CMD ["python", "app.py"]
