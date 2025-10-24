# Imagen base
FROM python:3.11-slim

# Crear directorio
WORKDIR /app

# Copiar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar proyecto
COPY . .

# Variables de entorno (se inyectan luego en EC2 o docker-compose)
ENV PYTHONUNBUFFERED=1

# Ejecutar Gunicorn (producción)
CMD ["gunicorn", "starkadvisorbackend.wsgi:application", "--bind", "0.0.0.0:8000"]
