# syntax=docker/dockerfile:1
FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# port interne // streamlit : 8501 by default
EXPOSE 80

# Lancement de Streamlit
CMD ["streamlit", "run", "app.py", \
     "--server.port=80", \
     "--server.address=0.0.0.0"]
