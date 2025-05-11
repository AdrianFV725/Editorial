FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero para aprovechar la caché de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Crear directorio para imágenes de perfil
RUN mkdir -p static/img/profiles

# Configurar variables de entorno
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Exponer puerto
EXPOSE 8080

# Crear un script de inicio que inicialice la base de datos y luego inicie la aplicación
RUN echo '#!/bin/bash \n\
    python init_db.py && \
    gunicorn --bind 0.0.0.0:$PORT app:app \
    ' > /app/docker-entrypoint.sh

RUN chmod +x /app/docker-entrypoint.sh

# Comando para iniciar la aplicación
CMD ["/app/docker-entrypoint.sh"] 