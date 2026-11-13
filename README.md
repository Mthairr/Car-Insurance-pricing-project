# Car Insurance Pricing Project

Tarification automobile par Machine Learning (CY Tech, ING3 Fintech).
Prime pure = fréquence (Random Forest, probabilité d'au moins un sinistre) x montant (XGBoost, coût moyen d'un sinistre).

## Structure

```
data/                 train.csv, test.csv
models/               proba_model.pkl, montant_model.pkl (pickle), produits par le script d'entraînement
developement/         notebooks de développement (exploration, fréquence, montant)
inference_test/       prédiction par lot sur test.csv (soumission Kaggle)
api/                  API (étape 4) et documentation de l'industrialisation
src/tarification/     package Python
  config.py           chemins, variables, hyperparamètres
  schema.py           schéma Pydantic d'un contrat (entrée de l'API)
  preparation.py      traitements des données communs entraînement / inférence, contrat JSON -> DataFrame
  entrainement.py     entraînement reproductible des deux modèles
tests/                tests pytest
docs/                 documentation (traitement des données, stratégie de tests)
```

## Installation

Le projet utilise [uv](https://docs.astral.sh/uv/) pour gérer l'environnement et les versions des dépendances (`uv.lock`).

```bash
uv sync                      # dépendances + outils de dev, installe le package tarification
uv sync --group notebooks    # en plus, pour relancer les notebooks
```

## Utilisation

```bash
uv run python -m tarification.entrainement             # ré-entraîne et enregistre les deux modèles dans models/
uv run python inference_test/inference.py              # probabilités de sinistre sur test.csv
uv run pytest                                          # tests
uv run ruff check . && uv run ruff format --check .    # qualité de code
```

## Modèles

| Modèle | Algorithme | Variables |
|---|---|---|
| Fréquence | Random Forest (300 arbres, min_samples_leaf=200) | 13 numériques + type_contrat, conducteur2 |
| Montant | XGBoost (100 arbres, profondeur 3, subsample et colsample_bytree 0,8) | maxi (type_contrat == Maxi), anciennete_vehicule |

Les deux pickles sont des pipelines sklearn complets : ils prennent les colonnes brutes d'un contrat, sans transformation préalable, et embarquent tout leur prétraitement. Le modèle de fréquence doit recevoir exactement ses 15 colonnes (`VARIABLES_FREQ`).
