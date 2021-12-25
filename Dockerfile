FROM python:3.8.10

WORKDIR /prueba_backend

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install httpx
RUN pip install itsdangerous

COPY . .