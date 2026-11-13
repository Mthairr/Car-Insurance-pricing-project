# Industrialisation du modèle de pricing — guide complet

Ce document explique **ce qu'est l'industrialisation**, **pourquoi chaque étape est nécessaire**, et **où en est le projet**, pour que n'importe qui dans l'équipe puisse reprendre le travail sans contexte préalable.

Référence : `TD 2 – Industrialisation IA` (voir `data/td_data_science.pdf` pour le premier TD de modélisation ; le TD d'industrialisation définit le contrat d'API suivi ici).

---

## 1. Pourquoi industrialiser ?

Un notebook Jupyter sert à **prouver qu'un modèle fonctionne** : on a toutes les données en mémoire, on lance les cellules dans l'ordre, on regarde les résultats à l'œil. Une entreprise ne peut pas exploiter ça directement — il faut transformer ce travail de recherche en **service appelable automatiquement, par n'importe quel programme, de façon fiable et répétable.**

Industrialiser, c'est faire cette chaîne complète :

```
Notebook (exploration)
      │
      ▼
Code de préparation des données, isolé et réutilisable
      │
      ▼
Modèle entraîné une fois, sauvegardé (pickle)
      │
      ▼
Traitement "à l'unité" (1 contrat à la fois, pas un DataFrame entier)
      │
      ▼
API (reçoit du JSON, valide, prédit, répond)
      │
      ▼
Tests automatiques (garantissent que rien ne casse)
      │
      ▼
Docker (empaquette le code + son environnement)
      │
      ▼
CI/CD (teste et déploie automatiquement à chaque changement)
```

Chaque étape répond à la même question : **"et si quelqu'un d'autre que nous utilise ce modèle, sans nous à côté ?"**

---

## 2. Les deux modèles à industrialiser

Le projet combine deux modèles pour calculer une **prime pure** :

```
prime pure = P(sinistre)  ×  E[montant du sinistre | sinistre]
             (modèle fréquence)   (modèle sévérité)
```

| | Modèle fréquence | Modèle sévérité |
|---|---|---|
| Fichier | `models/proba_model.pkl` | `models/montant_model.pkl` |
| Algorithme | Random Forest (300 arbres) | XGBoost |
| Variables | 15 (voir `src/tarification/config.py`) | 2 : `maxi`, `anciennete_vehicule` |
| Sortie | probabilité entre 0 et 1 | montant en euros |
| Prétraitement | **inclus dans le pickle** (imputation, encodage) | **inclus dans le pickle** : calcul de `maxi` (`variables_montant`) puis imputation |

Les deux modèles prennent donc les colonnes brutes d'un contrat, sans transformation préalable. Le modèle de fréquence doit recevoir exactement ses 15 colonnes (`VARIABLES_FREQ`).

---

## 3. Les 5 étapes du TD, et où on en est

### Étape 1 — Récupération des modèles et mise en commun
**Statut : fait.**
- Le code de production est regroupé dans le package `src/tarification/`, installé avec `uv sync` (plus besoin de `sys.path`)
- Les deux modèles sont régénérés par `uv run python -m tarification.entrainement`, avec les hyperparamètres retenus dans les notebooks
- Les notebooks de développement (`developement/*.ipynb`) et le script d'inférence par lot (`inference_test/`) sont conservés pour la traçabilité

### Étape 2 — Traitement des données (passage à l'unité)
<<<<<<< HEAD
**Statut : fait.**
=======
**Statut : fait, tests inclus (voir `api/tests/test_features.py`).**
>>>>>>> b8d6e9e13f32f2c98c2841283e60e66d9e2fc692

Le piège principal de cette étape : les notebooks traitent un **DataFrame entier**, alors qu'une API reçoit **une requête = un contrat**. Détail des points traités : [`docs/traitement_donnees_et_tests.md`](../docs/traitement_donnees_et_tests.md).

<<<<<<< HEAD
- `src/tarification/schema.py` : schéma Pydantic `Contrat`, conforme au contrat d'API du TD (champs obligatoires, types stricts, modalités autorisées, `null` accepté sur `sex_conducteur2` et `anciennete_vehicule`).
- `src/tarification/preparation.py` : `preparer_contrat(donnees)` valide le contrat puis le convertit en DataFrame d'une ligne, utilisable tel quel par les deux pickles.
- Tests automatiques : `tests/test_schema.py` et `tests/test_preparation.py`, dont un test qui vérifie que le traitement d'un contrat seul (passé par JSON) donne exactement le même résultat que le traitement par lot.
=======
C'est le rôle de [`api/features.py`](features.py) :

```python
preparer_frequence(contrat: dict) -> pd.DataFrame
preparer_montant(contrat: dict) -> pd.DataFrame
```

- `preparer_frequence` sélectionne, dans le dict du contrat, les 15 colonnes brutes attendues par `proba_model.pkl` (le prétraitement — imputation des valeurs manquantes, encodage des catégories — est déjà à l'intérieur du pickle, donc pas besoin de le refaire ici).
- `preparer_montant` calcule la colonne `maxi = (type_contrat == "Maxi")`, qui n'existe pas dans les données brutes et n'est **pas** incluse dans le pickle du modèle sévérité (elle est calculée séparément à l'entraînement, voir `developement/price_prediction.ipynb`, cellule `8419970d`).

Ces deux fonctions sont couvertes par des tests automatiques (`api/tests/test_features.py`), y compris les cas limites autorisés (`anciennete_vehicule: null`, `sex_conducteur2: null`, contrat non-"Maxi").
>>>>>>> b8d6e9e13f32f2c98c2841283e60e66d9e2fc692

### Étape 3 — Utilisation des modèles
**Statut : à faire.**
- Les deux modèles sont sauvegardés en `pickle` (format demandé)
- Reste : fonctions de prédiction à partir d'un dict et tests associés (déterminisme, valeurs positives, prime = fréquence x montant)

### Étape 4 — Développement de l'API
**Statut : fait.**

- Framework **FastAPI** (validation automatique des entrées via Pydantic → erreurs 422 natives, documentation Swagger/OpenAPI générée automatiquement)
- 4 routes, respectant le contrat exact du TD :

| Route | Méthode | Réponse |
|---|---|---|
| `/health` | GET | `{"status": "ok"}` |
| `/predict_frequency` | POST | `{"frequency": 0.12}` |
| `/predict_amount` | POST | `{"amount": 1500.0}` |
| `/predict` | POST | `{"frequency": 0.12, "amount": 1500.0, "premium": 180.0}` |

Règles à respecter (imposées par le TD) :
- `premium = frequency × amount`
- une même entrée → toujours la même prédiction (déterminisme)
- entrée invalide (champ manquant, mauvais type, corps vide) → erreur **4xx** (jamais 500)
- documentation disponible sur `/openapi.json` et `/docs`

**Fichiers** : [`api/schemas.py`](schemas.py) (modèle Pydantic `Contrat` + réponses), [`api/main.py`](main.py) (chargement des modèles au démarrage + 4 routes).

**Lancer l'API en local** (depuis la racine du projet) :
```bash
pip install -r api/requirements.txt
uvicorn api.main:app --reload --app-dir .
```
Puis ouvrir http://127.0.0.1:8000/docs pour tester interactivement.

**Lancer les tests** (16 tests : features unitaires + 10 tests de bout en bout sur l'API, y compris corps vide / champ manquant / mauvais type / déterminisme) :
```bash
pytest api/tests -v
```

### Étape 5 — Intégration et déploiement (Docker + CI/CD)
**Statut : à faire.**
- `Dockerfile` : empaqueter l'API + ses dépendances dans une image autonome
- CI (GitHub Actions) : installation des dépendances, exécution des tests, vérification de la qualité du code, à chaque push
- Déploiement : hébergement sur **Render** (solution choisie par l'équipe)

---

## 4. Comment tester une prédiction sur un contrat

Depuis la racine du projet :

```bash
uv run python -c "
import json, pickle
from tarification.config import MODELE_FREQ_PATH, MODELE_MONTANT_PATH, VARIABLES_FREQ
from tarification.preparation import preparer_contrat
from tarification.schema import EXEMPLE_CONTRAT

with open(MODELE_FREQ_PATH, 'rb') as f:
    modele_freq = pickle.load(f)
with open(MODELE_MONTANT_PATH, 'rb') as f:
    modele_montant = pickle.load(f)

contrat = preparer_contrat(EXEMPLE_CONTRAT)
frequency = float(modele_freq.predict_proba(contrat[VARIABLES_FREQ])[0, 1])
amount = float(modele_montant.predict(contrat)[0])
print(json.dumps({'frequency': frequency, 'amount': amount, 'premium': frequency * amount}, indent=2))
"
```

---

## 5. Glossaire rapide

- **Pickle** : format de sauvegarde Python qui permet de recharger un objet (ici, un modèle entraîné) exactement tel qu'il était, sans le ré-entraîner.
- **API** : un programme qui écoute des requêtes réseau (ex: `POST /predict`) et y répond en JSON — une façade entre le modèle et le reste du monde.
- **Pydantic / FastAPI** : bibliothèque Python qui décrit la forme attendue des données (types, champs obligatoires) et rejette automatiquement ce qui ne correspond pas.
- **CI (intégration continue)** : exécution automatique des tests et des vérifications qualité à chaque changement de code poussé sur GitHub.
- **CD (déploiement continu)** : mise en ligne automatique de l'application une fois les tests passés.
- **Docker** : outil qui empaquette le code et toutes ses dépendances dans une "image" qui tourne de façon identique sur n'importe quelle machine.
