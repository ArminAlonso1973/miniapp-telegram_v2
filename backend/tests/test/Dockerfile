# Usar Python 3.9 slim como base
FROM python:3.11-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de dependencias al contenedor
COPY requirements.txt .

# Instalar dependencias
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código al contenedor
COPY . .

# Configurar el comando para ejecutar los tests
CMD ["pytest", "-v", "--setup-show"]
