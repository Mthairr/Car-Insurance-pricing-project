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
| Variables | 15 (voir `api/features.py`) | 2 : `maxi`, `anciennete_vehicule` |
| Sortie | probabilité entre 0 et 1 | montant en euros |
| Prétraitement | **inclus dans le pickle** (imputation, encodage) | **partiellement inclus** : l'imputation de `anciennete_vehicule` est dans le pickle, mais la variable `maxi` doit être calculée à part |

Ce tableau explique pourquoi `api/features.py` traite les deux modèles différemment (voir §4).

---

## 3. Les 5 étapes du TD, et où on en est

### Étape 1 — Récupération des modèles et mise en commun
**Statut : fait.**
- Les deux modèles entraînés sont dans `models/`
- Les notebooks de développement (`developement/*.ipynb`) et le script d'inférence batch historique (`inference_test/`) sont conservés pour la traçabilité
- Tout est centralisé sur le dépôt GitHub de l'équipe

### Étape 2 — Traitement des données (passage à l'unité)
**Statut : fait pour la préparation des features, tests à écrire.**

Le piège principal de cette étape : les notebooks traitent un **DataFrame entier** (des milliers de lignes d'un coup), alors qu'une API reçoit **une requête = un contrat**, l'un après l'autre. Le code doit donc être adapté pour marcher sur une seule observation.

C'est le rôle de [`api/features.py`](features.py) :

```python
preparer_frequence(contrat: dict) -> pd.DataFrame
preparer_montant(contrat: dict) -> pd.DataFrame
```

- `preparer_frequence` sélectionne, dans le dict du contrat, les 15 colonnes brutes attendues par `proba_model.pkl` (le prétraitement — imputation des valeurs manquantes, encodage des catégories — est déjà à l'intérieur du pickle, donc pas besoin de le refaire ici).
- `preparer_montant` calcule la colonne `maxi = (type_contrat == "Maxi")`, qui n'existe pas dans les données brutes et n'est **pas** incluse dans le pickle du modèle sévérité (elle est calculée séparément à l'entraînement, voir `developement/price_prediction.ipynb`, cellule `8419970d`).

Ces deux fonctions ont été testées manuellement avec l'exemple de contrat JSON du TD, y compris les cas limites autorisés (`anciennete_vehicule: null`, `sex_conducteur2: null`, contrat non-"Maxi") : tout fonctionne sans erreur.

**Reste à faire** : des tests automatiques (`pytest`) pour ces deux fonctions, afin de garantir qu'un futur changement de code ne casse rien silencieusement.

### Étape 3 — Utilisation des modèles
**Statut : fait.**
- Les deux modèles sont bien sauvegardés en `pickle` (format demandé)
- Testés avec un dictionnaire JSON unique sur chacun des deux modèles (voir §2 ci-dessus)

**Point technique important à connaître** : pour charger `proba_model.pkl`, Python a besoin que le module `preparation` (celui d'`inference_test/preparation.py`, qui définit `manquants_structurels` et `construire_preprocesseur`) soit importable — ce module est référencé à l'intérieur du pickle. Il faut donc que `inference_test/` soit dans le `sys.path` au moment du chargement (voir le code de test dans l'historique, ou directement dans `api/main.py` une fois écrit).

### Étape 4 — Développement de l'API
**Statut : à faire.**

Prochaine étape concrète. Prévu :
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

### Étape 5 — Intégration et déploiement (Docker + CI/CD)
**Statut : à faire.**
- `Dockerfile` : empaqueter l'API + ses dépendances dans une image autonome
- CI (GitHub Actions) : installation des dépendances, exécution des tests, vérification de la qualité du code, à chaque push
- Déploiement : hébergement sur **Render** (solution choisie par l'équipe)

---

## 4. Comment relancer les tests manuels dès maintenant

Depuis la racine du projet, avec l'environnement virtuel activé :

```bash
python -c "
import sys, pickle, json
sys.path.insert(0, 'inference_test')   # nécessaire pour charger proba_model.pkl
sys.path.insert(0, 'api')
from features import preparer_frequence, preparer_montant

contrat = {
    'bonus': 0.5, 'type_contrat': 'Maxi', 'conducteur2': 'No',
    'age_conducteur1': 85, 'age_conducteur2': 0,
    'anciennete_permis1': 62, 'anciennete_permis2': 0,
    'anciennete_vehicule': 10, 'cylindre_vehicule': 1587, 'din_vehicule': 98,
    'debut_vente_vehicule': 10, 'fin_vente_vehicule': 9, 'vitesse_vehicule': 182,
    'prix_vehicule': 20700, 'poids_vehicule': 1210,
}

with open('models/proba_model.pkl', 'rb') as f:
    modele_freq = pickle.load(f)
with open('models/montant_model.pkl', 'rb') as f:
    modele_montant = pickle.load(f)

frequency = float(modele_freq.predict_proba(preparer_frequence(contrat))[0, 1])
amount = float(modele_montant.predict(preparer_montant(contrat))[0])
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
