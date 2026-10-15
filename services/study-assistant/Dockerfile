FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código del servicio
COPY . .

# Puerto expuesto (por defecto 8095)
EXPOSE 8095

# Arrancar con uvicorn respetando cabeceras del reverse proxy
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8095", "--proxy-headers"]

