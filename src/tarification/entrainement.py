"""Entraînement reproductible des modèles de fréquence et de montant.

Lancement : uv run python -m tarification.entrainement
"""

import pickle

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    mean_absolute_error,
    mean_squared_error,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from xgboost import XGBRegressor

from tarification.config import (
    CAT_FREQ,
    CIBLE_MONTANT,
    CIBLE_NOMBRE,
    COLONNES_MONTANT,
    MODELE_DIR,
    MODELE_FREQ_PATH,
    MODELE_MONTANT_PATH,
    NUM_FREQ,
    PARAMS_RF,
    PARAMS_XGB,
    PART_DEV_FREQ,
    PART_TEST_FREQ,
    RANDOM_STATE,
    TRAIN_PATH,
    VARIABLES_FREQ,
)
from tarification.preparation import (
    construire_preprocesseur,
    construire_preprocesseur_montant,
    variables_montant,
)


def charger_donnees(chemin=TRAIN_PATH):
    """Charge le jeu d'entraînement."""
    return pd.read_csv(chemin, sep=",")


def decouper_frequence(df):
    """Découpage train / dev / test stratifié, identique au notebook de développement."""
    X = df[VARIABLES_FREQ]
    y = (df[CIBLE_NOMBRE] > 0).astype(int)
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y, test_size=PART_TEST_FREQ, stratify=y, random_state=RANDOM_STATE
    )
    X_train, X_dev, y_train, y_dev = train_test_split(
        X_temp, y_temp, test_size=PART_DEV_FREQ, stratify=y_temp, random_state=RANDOM_STATE
    )
    return pd.concat([X_train, X_dev]), pd.concat([y_train, y_dev]), X_test, y_test


def construire_modele_frequence():
    """Pipeline complet du modèle de fréquence."""
    return Pipeline(
        [
            ("prep", construire_preprocesseur(NUM_FREQ, CAT_FREQ)),
            ("modele", RandomForestClassifier(**PARAMS_RF)),
        ]
    )


def construire_modele_montant():
    """Pipeline complet du modèle de montant, qui prend en entrée les colonnes brutes."""
    return Pipeline(
        [
            ("variables", FunctionTransformer(variables_montant)),
            ("prep", construire_preprocesseur_montant()),
            ("reg", XGBRegressor(**PARAMS_XGB)),
        ]
    )


def evaluer_frequence(modele, X, y):
    """Métriques du modèle de fréquence."""
    p = modele.predict_proba(X)[:, 1]
    return {
        "ROC_AUC": roc_auc_score(y, p),
        "PR_AUC": average_precision_score(y, p),
        "Brier": brier_score_loss(y, p),
        "proba_moy": p.mean(),
    }


def evaluer_montant(modele, X, y):
    """Métriques du modèle de montant."""
    p = modele.predict(X)
    return {
        "RMSE": mean_squared_error(y, p) ** 0.5,
        "MAE": mean_absolute_error(y, p),
        "ratio_total": p.sum() / y.sum(),
    }


def entrainer_frequence(df):
    """Entraîne le modèle de fréquence sur train + dev et l'évalue sur le test isolé."""
    X_final, y_final, X_test, y_test = decouper_frequence(df)
    modele = construire_modele_frequence().fit(X_final, y_final)
    return modele, evaluer_frequence(modele, X_test, y_test)


def entrainer_montant(df):
    """Entraîne le modèle de montant sur tous les sinistres du train."""
    sinistres = df[(df[CIBLE_NOMBRE] > 0) & (df[CIBLE_MONTANT] > 0)]
    y = sinistres[CIBLE_MONTANT]
    X = sinistres[COLONNES_MONTANT]
    modele = construire_modele_montant().fit(X, y)
    return modele, evaluer_montant(modele, X, y)


def sauvegarder_modele(modele, chemin):
    """Sérialise un modèle au format pickle."""
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with open(chemin, "wb") as f:
        pickle.dump(modele, f)


def main():
    df = charger_donnees()
    modele_freq, metriques_freq = entrainer_frequence(df)
    modele_montant, metriques_montant = entrainer_montant(df)
    sauvegarder_modele(modele_freq, MODELE_FREQ_PATH)
    sauvegarder_modele(modele_montant, MODELE_MONTANT_PATH)
    print(f"Fréquence (test isolé) : {metriques_freq}")
    print(f"Montant (train) : {metriques_montant}")
    print(f"Modèles enregistrés dans {MODELE_DIR}")


if __name__ == "__main__":
    main()
