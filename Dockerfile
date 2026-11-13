# Image de l'API de tarification assurance auto.
# Build : docker build -t prime-api .
# Run   : docker run -p 8000:8000 prime-api
FROM python:3.14-slim

WORKDIR /app

# Dépendances d'abord : tant que requirements.txt ne change pas, Docker réutilise
# ce calque en cache et ne réinstalle rien aux builds suivants.
COPY api/requirements.txt ./requirements.txt
# xgboost installé à part, sans ses dépendances : sur Linux, pip embarque par
# défaut nvidia-nccl-cu13 (~200 Mo, communication multi-GPU) alors que
# l'inférence ici tourne sur CPU — numpy/scipy (ses seules vraies dépendances)
# sont de toute façon déjà installés via pandas/scikit-learn.
RUN grep -v '^xgboost' requirements.txt > base-requirements.txt \
    && pip install --no-cache-dir -r base-requirements.txt \
    && pip install --no-cache-dir --no-deps $(grep '^xgboost' requirements.txt)

# Code et artefacts nécessaires à l'exécution (pas les notebooks, pas les données
# d'entraînement : voir .dockerignore).
COPY api/ ./api/
COPY models/ ./models/
COPY inference_test/preparation.py ./inference_test/preparation.py

EXPOSE 8000

# Render (et tout orchestrateur Docker) fournit le port via la variable PORT ;
# en local, sans cette variable, on retombe sur 8000.
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import os,urllib.request; urllib.request.urlopen('http://localhost:' + os.environ.get('PORT', '8000') + '/health')"

CMD ["sh", "-c", "uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
