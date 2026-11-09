FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código del servicio
COPY . .

# Puerto expuesto (8097)
EXPOSE 8097

# Arrancar con uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8097", "--proxy-headers"]
