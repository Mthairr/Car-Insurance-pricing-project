"""Paramètres centraux du projet : chemins, variables et hyperparamètres des deux modèles."""

from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
DATA_DIR = RACINE / "data"
MODELE_DIR = RACINE / "models"

TRAIN_PATH = DATA_DIR / "train.csv"
TEST_PATH = DATA_DIR / "test.csv"
MODELE_FREQ_PATH = MODELE_DIR / "proba_model.pkl"
MODELE_MONTANT_PATH = MODELE_DIR / "montant_model.pkl"

CIBLE_NOMBRE = "nombre_sinistres"
CIBLE_MONTANT = "montant_sinistre"

NUM_FREQ = [
    "bonus",
    "anciennete_vehicule",
    "din_vehicule",
    "anciennete_permis1",
    "age_conducteur1",
    "cylindre_vehicule",
    "age_conducteur2",
    "anciennete_permis2",
    "prix_vehicule",
    "poids_vehicule",
    "vitesse_vehicule",
    "debut_vente_vehicule",
    "fin_vente_vehicule",
]
CAT_FREQ = ["type_contrat", "conducteur2"]
VARIABLES_FREQ = NUM_FREQ + CAT_FREQ

COLONNES_MONTANT = ["type_contrat", "anciennete_vehicule"]
VARIABLES_MONTANT = ["maxi", "anciennete_vehicule"]

RANDOM_STATE = 42
PART_TEST_FREQ = 0.10
PART_DEV_FREQ = 0.20

PARAMS_RF = {
    "n_estimators": 300,
    "min_samples_leaf": 200,
    "max_features": "sqrt",
    "n_jobs": -1,
    "random_state": RANDOM_STATE,
}

PARAMS_XGB = {
    "n_estimators": 100,
    "learning_rate": 0.03,
    "max_depth": 3,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "random_state": RANDOM_STATE,
}
