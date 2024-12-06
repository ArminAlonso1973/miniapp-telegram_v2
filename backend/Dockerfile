FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

# Actualiza pip antes de instalar las dependencias
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt



COPY . .

# Configurar la variable de entorno para Quart
ENV QUART_APP=app:app

COPY . .

EXPOSE 5001

CMD ["python", "-m", "quart", "run", "--host=0.0.0.0", "--port=5001"]
