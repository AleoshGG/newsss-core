# Usamos la imagen oficial de Python en su versión "slim" (basada en Debian)
# Es mucho más rápida de construir que Alpine porque soporta wheels precompilados
# (evita tener que compilar numpy, scikit-learn o asyncpg desde cero).
FROM python:3.12-slim

# Evita que Python escriba archivos .pyc en el disco y asegura que los logs salgan en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Establecemos el directorio de trabajo
WORKDIR /app

# Instalamos dependencias del sistema mínimas que puedan necesitar algunas librerías
# y limpiamos el caché de apt para mantener la imagen ligera.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiamos solo el archivo de requerimientos primero
# Esto aprovecha el caché de capas de Docker: si requirements.txt no cambia,
# Docker no volverá a descargar ni instalar las dependencias.
COPY requirements.txt .

# 1. Instalamos explícitamente PyTorch en su versión CPU-only ANTES de los requirements.
# Por defecto, pip instala PyTorch con soporte para GPU (CUDA), lo cual pesa más de 2.5 GB.
# Como corremos la inferencia en CPU, esto reducirá radicalmente el tamaño de la imagen.
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu

# 2. Instalamos el resto de dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Pre-descargamos el modelo de ML (sentence-transformers) durante el build
# De esta forma, el modelo de 90MB se queda horneado en la imagen de Docker.
# Cuando el contenedor inicie, no tendrá que descargar nada de internet y arrancará al instante.
ENV SENTENCE_TRANSFORMERS_HOME=/app/.cache
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Copiamos el resto del código fuente del proyecto
# (El archivo .dockerignore evitará que se copien venv, .env, .git, etc.)
COPY . .

# Exponemos el puerto en el que corre FastAPI
EXPOSE 8000

# Comando por defecto para iniciar el servidor
# Usamos formato shell para que inyecte la variable PORT dinámica de Railway
CMD uvicorn src.app:app --host 0.0.0.0 --port ${PORT:-8000}
