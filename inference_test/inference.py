"""
Inférence : probabilité de sinistre sur test.csv avec rf_proba_model.pkl
Lancement :
  - Depuis la racine : python inference_test/inference.py
  - Depuis inference_test : python inference.py
"""
import pickle
import sys
from pathlib import Path

import pandas as pd

# Résolution des dossiers pour compatibilité quel que soit le dossier de lancement
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent

# Requis pour recharger le pipeline contenant construire_preprocesseur
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from preparation import construire_preprocesseur  # noqa: F401

MODELE_PATH = (PROJECT_ROOT / "models" / "rf_proba_model.pkl") if (PROJECT_ROOT / "models" / "rf_proba_model.pkl").exists() else (BASE_DIR / "rf_proba_model.pkl")
TEST_PATH = (PROJECT_ROOT / "data" / "test.csv") if (PROJECT_ROOT / "data" / "test.csv").exists() else (PROJECT_ROOT / "test.csv")
SORTIE_PATH = BASE_DIR / "predictions_proba_test.csv"


def charger_modele(chemin):
    with open(chemin, "rb") as f:
        return pickle.load(f)


def main():
    # 1. Chargement
    modele = charger_modele(MODELE_PATH)
    test = pd.read_csv(TEST_PATH, sep=",")
    print("Test chargé :", test.shape)

    # 2. Vérification des colonnes attendues par le modèle
    colonnes_attendues = list(modele.feature_names_in_)
    manquantes = set(colonnes_attendues) - set(test.columns)
    if manquantes:
        raise ValueError(f"Colonnes manquantes dans {TEST_PATH} : {manquantes}")

    X_test = test[colonnes_attendues]

    # 3. Prédiction
    proba = modele.predict_proba(X_test)

    resultat = pd.DataFrame({
        "index": test["index"] if "index" in test.columns else test.index,
        
        "proba": proba[:, 1],
    })

    # 4. Sauvegarde
    resultat.to_csv(SORTIE_PATH, index=False)
    print(resultat.head())
    print(resultat["proba"].describe().round(4))
    print(f"Prédictions enregistrées dans {SORTIE_PATH}")


if __name__ == "__main__":
    main()