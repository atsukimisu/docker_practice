FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

RUN apt-get -o Acquire::Check-Valid-Until=false -o Acquire::Check-Date=false update && \
     apt-get -o Acquire::Check-Valid-Until=false -o Acquire::Check-Date=false install -y --no-install-recommends \
     gcc g++ python3-magic libopencv-dev libopencv-core-dev python3-opencv && \
     rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN pip install fastapi uvicorn sqlalchemy async-exit-stack async-generator

COPY ./app/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "4"]