"""Interface de démonstration pour l'API de tarification assurance auto.

N'affiche que les 15 champs qui influencent réellement la prédiction
(cf. api/features.py). Les autres champs, exigés par le contrat de l'API
mais ignorés par les modèles, sont envoyés avec des valeurs neutres fixes,
invisibles ici.

Lancement : streamlit run ui/app.py
"""
import requests
import streamlit as st

API_URL = "https://car-insurance-pricing-project.onrender.com"

# Valeurs neutres pour les champs exigés par le contrat de l'API mais que
# les modèles n'utilisent jamais (voir api/features.py : COLONNES_FREQUENCE
# et la dérivation de "maxi" ne portent que sur les champs du formulaire).
CHAMPS_IGNORES_PAR_LES_MODELES = {
    "id_client": "DEMO", "id_vehicule": "DEMO", "id_contrat": "DEMO",
    "duree_contrat": 12, "anciennete_info": 1,
    "freq_paiement": "Annual", "paiement": "No", "utilisation": "Private",
    "code_postal": "00000", "sex_conducteur1": "M", "sex_conducteur2": None,
    "essence_vehicule": "Gasoline", "marque_vehicule": "INCONNU",
    "modele_vehicule": "INCONNU", "type_vehicule": "Tourism",
}

st.set_page_config(page_title="Simulateur de prime auto", page_icon="🚗", layout="centered")
st.title("🚗 Simulateur de prime d'assurance auto")
st.caption(
    "Appelle l'API déployée "
    f"([{API_URL}]({API_URL}/docs)) — fréquence × sévérité = prime pure. "
    "Seuls les champs qui influencent réellement la prédiction sont affichés ici."
)

with st.form("contrat"):
    st.subheader("Contrat")
    col1, col2 = st.columns(2)
    with col1:
        type_contrat = st.selectbox("Type de contrat", ["Maxi", "Median1", "Median2", "Mini"])
    with col2:
        bonus = st.number_input("Bonus", value=0.5, step=0.01, format="%.2f")

    st.subheader("Conducteurs")
    col1, col2 = st.columns(2)
    with col1:
        age_conducteur1 = st.number_input("Âge conducteur 1", value=85, step=1)
        anciennete_permis1 = st.number_input("Ancienneté permis 1 (ans)", value=62, step=1)
    with col2:
        conducteur2 = st.selectbox("Second conducteur ?", ["No", "Yes"])
        age_conducteur2 = st.number_input("Âge conducteur 2", value=0, step=1)
        anciennete_permis2 = st.number_input("Ancienneté permis 2 (ans)", value=0, step=1)

    st.subheader("Véhicule")
    col1, col2 = st.columns(2)
    with col1:
        anciennete_inconnue = st.checkbox("Ancienneté du véhicule inconnue")
        anciennete_vehicule_val = st.number_input(
            "Ancienneté véhicule (ans)", value=10, step=1, disabled=anciennete_inconnue
        )
        cylindre_vehicule = st.number_input("Cylindrée", value=1587, step=1)
        din_vehicule = st.number_input("Puissance DIN", value=98, step=1)
    with col2:
        vitesse_vehicule = st.number_input("Vitesse max", value=182, step=1)
        prix_vehicule = st.number_input("Prix du véhicule (€)", value=20700, step=100)
        poids_vehicule = st.number_input("Poids (kg)", value=1210, step=10)
    debut_vente_vehicule = st.number_input("Début de vente (ans)", value=10, step=1)
    fin_vente_vehicule = st.number_input("Fin de vente (ans)", value=9, step=1)

    submitted = st.form_submit_button("Calculer la prime")

st.caption("⚠️ Le service gratuit peut mettre jusqu'à une minute à répondre s'il était inactif (mise en veille).")

if submitted:
    contrat = {
        **CHAMPS_IGNORES_PAR_LES_MODELES,
        "type_contrat": type_contrat,
        "bonus": bonus,
        "conducteur2": conducteur2,
        "age_conducteur1": int(age_conducteur1),
        "age_conducteur2": int(age_conducteur2),
        "anciennete_permis1": int(anciennete_permis1),
        "anciennete_permis2": int(anciennete_permis2),
        "anciennete_vehicule": None if anciennete_inconnue else anciennete_vehicule_val,
        "cylindre_vehicule": int(cylindre_vehicule),
        "din_vehicule": int(din_vehicule),
        "debut_vente_vehicule": int(debut_vente_vehicule),
        "fin_vente_vehicule": int(fin_vente_vehicule),
        "vitesse_vehicule": int(vitesse_vehicule),
        "prix_vehicule": prix_vehicule,
        "poids_vehicule": poids_vehicule,
    }

    try:
        with st.spinner("Appel de l'API (peut prendre jusqu'à une minute si le service dormait)..."):
            reponse = requests.post(f"{API_URL}/predict", json=contrat, timeout=90)
    except requests.exceptions.RequestException as exc:
        st.error(f"Impossible de contacter l'API : {exc}")
    else:
        if reponse.status_code == 200:
            resultat = reponse.json()
            c1, c2, c3 = st.columns(3)
            c1.metric("Probabilité de sinistre", f"{resultat['frequency'] * 100:.2f} %")
            c2.metric("Montant attendu", f"{resultat['amount']:.0f} €")
            c3.metric("Prime pure", f"{resultat['premium']:.2f} €")
        else:
            st.error(f"Erreur {reponse.status_code} : {reponse.text}")
