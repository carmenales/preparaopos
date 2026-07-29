FROM python:3.11-slim

WORKDIR /workspace

# Solo copiamos requirements en el build para aprovechar la cache de capas
# de Docker; el código real (services/embeddings) se monta como volumen
# en docker-compose.yml, igual que se hace con el PHP de studyassistant.
COPY services/embeddings/requirements.txt services/embeddings/requirements.txt
RUN pip install --no-cache-dir -r services/embeddings/requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "/workspace/services/embeddings"]
