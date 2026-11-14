"""Interface de démonstration pour l'API de tarification assurance auto.

Lancement : streamlit run ui/app.py
"""
import requests
import streamlit as st

API_URL = "https://car-insurance-pricing-project.onrender.com"

st.set_page_config(page_title="Simulateur de prime auto", page_icon="🚗", layout="centered")
st.title("🚗 Simulateur de prime d'assurance auto")
st.caption(
    "Interface de démonstration qui appelle l'API déployée "
    f"([{API_URL}]({API_URL}/docs)) — fréquence × sévérité = prime pure."
)

with st.form("contrat"):
    st.subheader("Contrat")
    col1, col2 = st.columns(2)
    with col1:
        id_client = st.text_input("ID client", "A00000001")
        id_vehicule = st.text_input("ID véhicule", "V01")
        id_contrat = st.text_input("ID contrat", "A00000001-V01")
        type_contrat = st.selectbox("Type de contrat", ["Maxi", "Median1", "Median2", "Mini"])
        duree_contrat = st.number_input("Durée du contrat (mois)", value=29, step=1)
        bonus = st.number_input("Bonus", value=0.5, step=0.01, format="%.2f")
    with col2:
        anciennete_info = st.number_input("Ancienneté info (ans)", value=9, step=1)
        freq_paiement = st.text_input("Fréquence de paiement", "Biannual")
        paiement = st.selectbox("Paiement en retard ?", ["No", "Yes"])
        utilisation = st.text_input("Utilisation", "Retired")
        code_postal = st.text_input("Code postal", "36233")

    st.subheader("Conducteurs")
    col1, col2 = st.columns(2)
    with col1:
        sex_conducteur1 = st.selectbox("Sexe conducteur 1", ["M", "F"])
        age_conducteur1 = st.number_input("Âge conducteur 1", value=85, step=1)
        anciennete_permis1 = st.number_input("Ancienneté permis 1 (ans)", value=62, step=1)
    with col2:
        conducteur2 = st.selectbox("Second conducteur ?", ["No", "Yes"])
        sex_conducteur2_choix = st.selectbox("Sexe conducteur 2", ["(aucun)", "M", "F"])
        age_conducteur2 = st.number_input("Âge conducteur 2", value=0, step=1)
        anciennete_permis2 = st.number_input("Ancienneté permis 2 (ans)", value=0, step=1)

    st.subheader("Véhicule")
    col1, col2 = st.columns(2)
    with col1:
        marque_vehicule = st.text_input("Marque", "PEUGEOT")
        modele_vehicule = st.text_input("Modèle", "306")
        essence_vehicule = st.selectbox("Carburant", ["Gasoline", "Diesel", "Hybrid"])
        type_vehicule = st.text_input("Type de véhicule", "Tourism")
        anciennete_inconnue = st.checkbox("Ancienneté du véhicule inconnue")
        anciennete_vehicule_val = st.number_input(
            "Ancienneté véhicule (ans)", value=10, step=1, disabled=anciennete_inconnue
        )
    with col2:
        cylindre_vehicule = st.number_input("Cylindrée", value=1587, step=1)
        din_vehicule = st.number_input("Puissance DIN", value=98, step=1)
        vitesse_vehicule = st.number_input("Vitesse max", value=182, step=1)
        prix_vehicule = st.number_input("Prix du véhicule (€)", value=20700, step=100)
        poids_vehicule = st.number_input("Poids (kg)", value=1210, step=10)
        debut_vente_vehicule = st.number_input("Début de vente (ans)", value=10, step=1)
        fin_vente_vehicule = st.number_input("Fin de vente (ans)", value=9, step=1)

    submitted = st.form_submit_button("Calculer la prime")

st.caption("⚠️ Le service gratuit peut mettre jusqu'à une minute à répondre s'il était inactif (mise en veille).")

if submitted:
    contrat = {
        "id_client": id_client, "id_vehicule": id_vehicule, "id_contrat": id_contrat,
        "bonus": bonus, "type_contrat": type_contrat, "duree_contrat": int(duree_contrat),
        "anciennete_info": int(anciennete_info), "freq_paiement": freq_paiement, "paiement": paiement,
        "utilisation": utilisation, "code_postal": code_postal, "conducteur2": conducteur2,
        "age_conducteur1": int(age_conducteur1), "age_conducteur2": int(age_conducteur2),
        "sex_conducteur1": sex_conducteur1,
        "sex_conducteur2": None if sex_conducteur2_choix == "(aucun)" else sex_conducteur2_choix,
        "anciennete_permis1": int(anciennete_permis1), "anciennete_permis2": int(anciennete_permis2),
        "anciennete_vehicule": None if anciennete_inconnue else anciennete_vehicule_val,
        "cylindre_vehicule": int(cylindre_vehicule), "din_vehicule": int(din_vehicule),
        "essence_vehicule": essence_vehicule, "marque_vehicule": marque_vehicule,
        "modele_vehicule": modele_vehicule, "debut_vente_vehicule": int(debut_vente_vehicule),
        "fin_vente_vehicule": int(fin_vente_vehicule), "vitesse_vehicule": int(vitesse_vehicule),
        "type_vehicule": type_vehicule, "prix_vehicule": prix_vehicule, "poids_vehicule": poids_vehicule,
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
