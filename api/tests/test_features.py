"""Tests unitaires de la préparation des features (api/features.py)."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "api") not in sys.path:
    sys.path.insert(0, str(ROOT / "api"))

from features import COLONNES_FREQUENCE, preparer_frequence, preparer_montant

CONTRAT_BASE = {
    "bonus": 0.5, "type_contrat": "Maxi", "conducteur2": "No",
    "age_conducteur1": 85, "age_conducteur2": 0,
    "anciennete_permis1": 62, "anciennete_permis2": 0,
    "anciennete_vehicule": 10, "cylindre_vehicule": 1587, "din_vehicule": 98,
    "debut_vente_vehicule": 10, "fin_vente_vehicule": 9, "vitesse_vehicule": 182,
    "prix_vehicule": 20700, "poids_vehicule": 1210,
}


def test_preparer_frequence_colonnes():
    X = preparer_frequence(CONTRAT_BASE)
    assert list(X.columns) == COLONNES_FREQUENCE
    assert len(X) == 1


def test_preparer_frequence_valeurs():
    X = preparer_frequence(CONTRAT_BASE)
    assert X.loc[0, "bonus"] == 0.5
    assert X.loc[0, "type_contrat"] == "Maxi"


def test_preparer_montant_maxi_vrai():
    contrat = {**CONTRAT_BASE, "type_contrat": "Maxi"}
    X = preparer_montant(contrat)
    assert X.loc[0, "maxi"] == 1
    assert X.loc[0, "anciennete_vehicule"] == 10


def test_preparer_montant_maxi_faux():
    contrat = {**CONTRAT_BASE, "type_contrat": "Mini"}
    X = preparer_montant(contrat)
    assert X.loc[0, "maxi"] == 0


def test_preparer_montant_anciennete_nulle():
    contrat = {**CONTRAT_BASE, "anciennete_vehicule": None}
    X = preparer_montant(contrat)
    assert X.loc[0, "anciennete_vehicule"] is None or X["anciennete_vehicule"].isna().iloc[0]


def test_preparer_frequence_champ_absent_devient_none():
    """Un champ non fourni (ex: contrat partiel) ne doit pas faire planter la construction de la ligne."""
    X = preparer_frequence({"bonus": 0.5})
    assert X.loc[0, "type_contrat"] is None
