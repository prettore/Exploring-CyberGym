FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# isso evita ele baixar os requirements dnv ao mudar o app.py
COPY requirements.txt . 

RUN pip install --no-cache-dir -r requirements.txt 
#
COPY . .

EXPOSE 8050

CMD ["python", "app.py"]