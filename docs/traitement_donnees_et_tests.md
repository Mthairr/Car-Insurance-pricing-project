# Traitement des données unitaire et stratégie de tests

## 1. Du traitement par lot au traitement d'un contrat

Dans les notebooks, les traitements s'appliquent à un DataFrame de 50 000 lignes. Dans l'API, ils s'appliquent à un seul contrat reçu en JSON. Points identifiés et traitement retenu :

| Point | Problème en unitaire | Traitement retenu |
|---|---|---|
| Valeurs manquantes numériques | Une médiane calculée sur la requête n'a pas de sens (une seule ligne). Une ancienne version de `variables_montant` faisait `fillna(df["anciennete_vehicule"].median())` sur le lot reçu. | `SimpleImputer` dans les pipelines : la médiane est apprise sur le train et stockée dans le pickle. |
| Manquants structurels du conducteur 2 | Aucun, la règle s'applique ligne à ligne. | `manquants_structurels` dans le pipeline de fréquence. |
| Modalités inconnues | Une modalité jamais vue ne doit pas faire planter l'encodage. | Validation en amont (schéma Pydantic) et `handle_unknown="infrequent_if_exist"` dans le `OneHotEncoder`. |
| Variables dérivées (`maxi`) | Le calcul devait être fait à la main avant `predict`. | `variables_montant` intégrée au pipeline de montant (`FunctionTransformer`). |
| Types | Le JSON n'a pas de types pandas : `null`, entiers et décimaux mélangés, code postal en texte. | `preparer_contrat` : validation par le schéma `Contrat`, puis DataFrame d'une ligne avec les champs décimaux en `float64` (`null` devient `NaN`). |
| Ordre et sélection des colonnes | sklearn vérifie les noms de colonnes vus au `fit`. | Chaque modèle sélectionne ses colonnes (`VARIABLES_FREQ`, `COLONNES_MONTANT`). Les champs supplémentaires du JSON sont ignorés. |

## 2. Schéma d'entrée (`schema.py`)

- Tous les champs du contrat du TD sont obligatoires. Seuls `sex_conducteur2` et `anciennete_vehicule` peuvent valoir `null`.
- Mode strict : `"29"` n'est pas accepté pour un entier, ni `36233` pour le code postal. Un entier est accepté pour un décimal (`"bonus": 1`).
- Les variables catégorielles sont restreintes aux modalités observées dans les données (`Literal`), et les numériques sont positives.
- Toute entrée invalide lève une `ValidationError`, que l'API traduira en erreur 422.

## 3. Stratégie de tests

Pyramide adaptée au cours (tests unitaires, d'intégration, fonctionnels) :

| Niveau | Ce qui est testé | Fichier |
|---|---|---|
| Unitaire | Fonctions de traitement isolées : `manquants_structurels`, `variables_montant`, `preparer_contrat` | `tests/test_preparation.py` |
| Unitaire, cas limites | Schéma : champ manquant, mauvais type, modalité inconnue, valeur négative, `null` autorisé ou non, corps vide, champ supplémentaire | `tests/test_schema.py` |
| Non-régression | Le traitement d'un contrat seul donne exactement le même résultat que le traitement par lot (200 contrats de test.csv, passage par JSON) | `tests/test_preparation.py` |
| Modèles (étape 3) | Prédiction depuis un dict : déterminisme, valeurs positives, cohérence prime = fréquence x montant | à venir |
| API (étape 4) | Contrat d'API : codes HTTP, format des réponses, 422 et jamais 500, `/openapi.json` et `/docs` | à venir |

Lancement : `uv run pytest`. Les tests seront exécutés automatiquement par la CI à chaque push (étape 5).
