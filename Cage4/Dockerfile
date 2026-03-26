FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# copy your repo (without heavy submodule content)
COPY . .

# fetch submodule (this populates cage-challenge-4/)
RUN git clone https://github.com/cage-challenge/cage-challenge-4.git

# install dependencies FROM the submodule
RUN pip install --no-cache-dir -r cage-challenge-4/Requirements.txt

# install your local package (if needed)
RUN pip install -e ./cage-challenge-4

#ENV PYTHONPATH=/app/cage-challenge-4

CMD ["python", "Testing/train_agent.py"]