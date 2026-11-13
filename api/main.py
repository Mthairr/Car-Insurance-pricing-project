"""API de tarification assurance auto.

Lancement local :
  uvicorn api.main:app --reload --app-dir .
ou, depuis le dossier api/ :
  uvicorn main:app --reload
Documentation : /docs (Swagger UI) et /openapi.json
"""
import pickle
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
MODELS_DIR = PROJECT_ROOT / "models"

# inference_test/ doit être sur sys.path : proba_model.pkl référence le module
# "preparation" (manquants_structurels, construire_preprocesseur) qu'il contient.
for chemin in (PROJECT_ROOT / "inference_test", BASE_DIR):
    if str(chemin) not in sys.path:
        sys.path.insert(0, str(chemin))

from features import preparer_frequence, preparer_montant  # noqa: E402
from schemas import (  # noqa: E402
    AmountResponse,
    Contrat,
    FrequencyResponse,
    HealthResponse,
    PredictResponse,
)

modeles = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    with open(MODELS_DIR / "proba_model.pkl", "rb") as f:
        modeles["frequence"] = pickle.load(f)
    with open(MODELS_DIR / "montant_model.pkl", "rb") as f:
        modeles["montant"] = pickle.load(f)
    yield
    modeles.clear()


app = FastAPI(
    title="API de tarification assurance auto",
    description=(
        "Expose les modèles de fréquence (probabilité de sinistre) et de "
        "sévérité (montant attendu) pour calculer la prime pure d'un contrat."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


def _predire_frequence(contrat: dict) -> float:
    X = preparer_frequence(contrat)
    return float(modeles["frequence"].predict_proba(X)[0, 1])


def _predire_montant(contrat: dict) -> float:
    X = preparer_montant(contrat)
    return float(modeles["montant"].predict(X)[0])


@app.get("/health", response_model=HealthResponse)
def health() -> dict:
    return {"status": "ok"}


@app.post("/predict_frequency", response_model=FrequencyResponse)
def predict_frequency(contrat: Contrat) -> dict:
    return {"frequency": _predire_frequence(contrat.model_dump())}


@app.post("/predict_amount", response_model=AmountResponse)
def predict_amount(contrat: Contrat) -> dict:
    return {"amount": _predire_montant(contrat.model_dump())}


@app.post("/predict", response_model=PredictResponse)
def predict(contrat: Contrat) -> dict:
    payload = contrat.model_dump()
    frequency = _predire_frequence(payload)
    amount = _predire_montant(payload)
    return {"frequency": frequency, "amount": amount, "premium": frequency * amount}
