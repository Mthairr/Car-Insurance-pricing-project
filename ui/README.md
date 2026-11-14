# Interface de démonstration (Streamlit)

Petit formulaire web qui appelle l'API déjà déployée sur Render
(https://car-insurance-pricing-project.onrender.com) et affiche le résultat
(probabilité de sinistre, montant attendu, prime pure). Ce n'est **pas**
l'API elle-même (voir [`../api/README.md`](../api/README.md)) — c'est une
démonstration visuelle en plus, utile pour une présentation.

## Lancer en local

```bash
pip install -r ui/requirements.txt
streamlit run ui/app.py
```

Puis ouvrir http://localhost:8501.

## Remarque

Le champ `API_URL` en haut de [`app.py`](app.py) pointe vers l'API en
production. Pour tester contre une API lancée en local à la place
(`uvicorn api.main:app`), changer cette valeur en `http://localhost:8000`.

Le plan gratuit de Render met le service en veille après 15 minutes
d'inactivité : le premier appel après une veille peut prendre jusqu'à une
minute (c'est normal, l'interface l'indique).
