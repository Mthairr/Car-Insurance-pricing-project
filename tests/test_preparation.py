import json

import numpy as np
import pandas as pd
import pytest
from pydantic import ValidationError

from tarification.config import VARIABLES_FREQ
from tarification.preparation import manquants_structurels, preparer_contrat, variables_montant
from tarification.schema import Contrat


def test_manquants_structurels_sans_conducteur2():
    X = pd.DataFrame(
        {"conducteur2": ["No", "Yes"], "age_conducteur2": [np.nan, 40], "anciennete_permis2": [np.nan, 20]}
    )
    resultat = manquants_structurels(X)
    assert resultat.loc[0, "age_conducteur2"] == 0
    assert resultat.loc[0, "anciennete_permis2"] == 0
    assert resultat.loc[1, "age_conducteur2"] == 40


def test_manquants_structurels_ne_modifie_pas_l_entree():
    X = pd.DataFrame({"conducteur2": ["No"], "age_conducteur2": [np.nan], "anciennete_permis2": [np.nan]})
    manquants_structurels(X)
    assert X["age_conducteur2"].isna().all()


def test_variables_montant():
    df = pd.DataFrame({"type_contrat": ["Maxi", "Mini"], "anciennete_vehicule": [3.0, np.nan]})
    resultat = variables_montant(df)
    assert resultat.columns.tolist() == ["maxi", "anciennete_vehicule"]
    assert resultat["maxi"].tolist() == [1, 0]
    assert np.isnan(resultat.loc[1, "anciennete_vehicule"])


def test_preparer_contrat_une_ligne(contrat):
    df = preparer_contrat(contrat)
    assert df.shape == (1, len(Contrat.model_fields))
    assert set(VARIABLES_FREQ) <= set(df.columns)


def test_preparer_contrat_accepte_un_objet_contrat(contrat):
    pd.testing.assert_frame_equal(
        preparer_contrat(Contrat.model_validate(contrat)), preparer_contrat(contrat)
    )


def test_preparer_contrat_null_devient_nan(contrat):
    contrat["anciennete_vehicule"] = None
    df = preparer_contrat(contrat)
    assert df["anciennete_vehicule"].dtype == "float64"
    assert df["anciennete_vehicule"].isna().all()


def test_preparer_contrat_types_numeriques(contrat):
    df = preparer_contrat(contrat)
    assert df["bonus"].dtype == "float64"
    assert df["anciennete_vehicule"].dtype == "float64"
    assert pd.api.types.is_integer_dtype(df["age_conducteur1"])


def test_preparer_contrat_invalide(contrat):
    contrat["type_contrat"] = "Gold"
    with pytest.raises(ValidationError):
        preparer_contrat(contrat)


def test_traitement_unitaire_identique_au_traitement_par_lot(
    echantillon_test, modele_frequence, modele_montant
):
    prep_freq = modele_frequence.named_steps["prep"]
    prep_montant = modele_montant[:-1]
    lot_freq = prep_freq.transform(echantillon_test[VARIABLES_FREQ])
    lot_montant = prep_montant.transform(echantillon_test)
    contrats_json = json.loads(echantillon_test.to_json(orient="records"))
    for i, contrat_json in enumerate(contrats_json):
        df = preparer_contrat(contrat_json)
        np.testing.assert_allclose(prep_freq.transform(df[VARIABLES_FREQ]), lot_freq[[i]])
        np.testing.assert_allclose(prep_montant.transform(df), lot_montant[[i]])


def test_traitement_unitaire_anciennete_nulle_imputee_par_la_mediane_du_train(contrat, modele_montant):
    contrat["anciennete_vehicule"] = None
    imputeur = modele_montant.named_steps["prep"].named_transformers_["num"]
    mediane_train = imputeur.statistics_[1]
    resultat = modele_montant[:-1].transform(preparer_contrat(contrat))
    assert resultat[0, 1] == mediane_train
