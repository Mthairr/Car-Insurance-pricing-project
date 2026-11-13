"""Préparation d'une observation unique (un contrat, au format dict/JSON) pour les deux modèles.

Les deux pickles (models/proba_model.pkl, models/montant_model.pkl) sont des
sklearn.Pipeline qui embarquent déjà leur propre prétraitement (imputation,
encodage). Ces fonctions se contentent donc de sélectionner / dériver les bonnes
colonnes brutes, dans le bon format, à partir du contrat reçu par l'API.
"""
import pandas as pd

COLONNES_FREQUENCE_NUM = [
    "bonus", "anciennete_vehicule", "din_vehicule", "anciennete_permis1",
    "age_conducteur1", "cylindre_vehicule", "age_conducteur2", "anciennete_permis2",
    "prix_vehicule", "poids_vehicule", "vitesse_vehicule",
    "debut_vente_vehicule", "fin_vente_vehicule",
]
COLONNES_FREQUENCE_CAT = ["type_contrat", "conducteur2"]
COLONNES_FREQUENCE = COLONNES_FREQUENCE_NUM + COLONNES_FREQUENCE_CAT


def preparer_frequence(contrat: dict) -> pd.DataFrame:
    """Ligne attendue par proba_model.pkl (15 colonnes brutes, prétraitement inclus dans le pickle)."""
    ligne = {col: contrat.get(col) for col in COLONNES_FREQUENCE}
    return pd.DataFrame([ligne])


def preparer_montant(contrat: dict) -> pd.DataFrame:
    """Ligne attendue par montant_model.pkl : maxi dérivée de type_contrat (hors pickle, cf. price_prediction.ipynb)."""
    ligne = {
        "maxi": int(contrat.get("type_contrat") == "Maxi"),
        "anciennete_vehicule": contrat.get("anciennete_vehicule"),
    }
    return pd.DataFrame([ligne])
