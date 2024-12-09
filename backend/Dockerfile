FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

# Instalar dependencias
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . .

# Configurar QUART_APP
ENV QUART_APP=app:app


EXPOSE 5001

CMD ["python", "-m", "quart", "run", "--host=0.0.0.0", "--port=5001"]
