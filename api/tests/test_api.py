"""Tests de bout en bout de l'API, via le contrat d'API du TD d'industrialisation."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from api.main import app  # noqa: E402

CONTRAT_VALIDE = {
    "id_client": "A00000001", "id_vehicule": "V01", "id_contrat": "A00000001-V01",
    "bonus": 0.5, "type_contrat": "Maxi", "duree_contrat": 29,
    "anciennete_info": 9, "freq_paiement": "Biannual", "paiement": "No",
    "utilisation": "Retired", "code_postal": "36233", "conducteur2": "No",
    "age_conducteur1": 85, "age_conducteur2": 0,
    "sex_conducteur1": "M", "sex_conducteur2": None,
    "anciennete_permis1": 62, "anciennete_permis2": 0,
    "anciennete_vehicule": 10, "cylindre_vehicule": 1587, "din_vehicule": 98,
    "essence_vehicule": "Gasoline", "marque_vehicule": "PEUGEOT",
    "modele_vehicule": "306", "debut_vente_vehicule": 10,
    "fin_vente_vehicule": 9, "vitesse_vehicule": 182,
    "type_vehicule": "Tourism", "prix_vehicule": 20700, "poids_vehicule": 1210,
}


@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_predict_frequency_valide(client):
    r = client.post("/predict_frequency", json=CONTRAT_VALIDE)
    assert r.status_code == 200
    body = r.json()
    assert "frequency" in body
    assert isinstance(body["frequency"], float)
    assert 0 <= body["frequency"] <= 1


def test_predict_amount_valide(client):
    r = client.post("/predict_amount", json=CONTRAT_VALIDE)
    assert r.status_code == 200
    body = r.json()
    assert "amount" in body
    assert isinstance(body["amount"], float)
    assert body["amount"] >= 0


def test_predict_valide_et_coherent(client):
    r = client.post("/predict", json=CONTRAT_VALIDE)
    assert r.status_code == 200
    body = r.json()
    assert body.keys() == {"frequency", "amount", "premium"}
    assert body["premium"] == pytest.approx(body["frequency"] * body["amount"])


def test_predict_deterministe(client):
    """Une même entrée doit toujours renvoyer la même prédiction."""
    r1 = client.post("/predict", json=CONTRAT_VALIDE).json()
    r2 = client.post("/predict", json=CONTRAT_VALIDE).json()
    assert r1 == r2


def test_champs_nullable_acceptes(client):
    contrat = {**CONTRAT_VALIDE, "anciennete_vehicule": None, "sex_conducteur2": None}
    r = client.post("/predict", json=contrat)
    assert r.status_code == 200


def test_champ_manquant_renvoie_4xx(client):
    contrat = dict(CONTRAT_VALIDE)
    del contrat["bonus"]
    r = client.post("/predict", json=contrat)
    assert 400 <= r.status_code < 500


def test_mauvais_type_renvoie_4xx(client):
    contrat = {**CONTRAT_VALIDE, "bonus": "pas un nombre"}
    r = client.post("/predict", json=contrat)
    assert 400 <= r.status_code < 500


def test_corps_vide_renvoie_4xx(client):
    r = client.post("/predict", content=b"")
    assert 400 <= r.status_code < 500


def test_documentation_openapi_accessible(client):
    assert client.get("/openapi.json").status_code == 200
    assert client.get("/docs").status_code == 200
