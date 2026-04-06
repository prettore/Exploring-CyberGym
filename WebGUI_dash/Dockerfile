FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# copy your repo (without heavy submodule content)
COPY . .

# install dependencies FROM the submodule
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8050

RUN useradd app
USER app

CMD ["python", "app.py"]