# Usar una imagen base de Python reciente
FROM python:3.11-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de requisitos
COPY requirements.txt .

# Instalar dependencias
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código al contenedor
COPY . .

# Configurar la variable de entorno para Quart
ENV QUART_APP=app:app PYTHONPATH=/app

# Exponer el puerto utilizado por el backend
EXPOSE 5001

# Comando por defecto para ejecutar el servidor
CMD ["python", "-m", "quart", "run", "--host=0.0.0.0", "--port=5001"]
