FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código del servicio
COPY . .

# Puerto expuesto (8096)
EXPOSE 8096

# Arrancar con uvicorn respetando cabeceras del proxy inverso
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8096", "--proxy-headers"]
