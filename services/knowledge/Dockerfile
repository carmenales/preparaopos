# services/knowledge/Dockerfile
#
# Imagen ligera: este servicio NO necesita sentence-transformers/torch
# (eso vive en services/embeddings, contenedor separado). Solo FastAPI +
# httpx para hablar con embeddings y con Ollama.
#
# Principio de mínimo privilegio: usuario no-root, sin paquetes de
# compilación innecesarios en la imagen final.

FROM python:3.11-slim

RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
