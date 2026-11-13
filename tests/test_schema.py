import pytest
from pydantic import ValidationError

from tarification.schema import Contrat


def test_exemple_du_td_valide(contrat):
    assert Contrat.model_validate(contrat).type_contrat == "Maxi"


@pytest.mark.parametrize("champ", ["sex_conducteur2", "anciennete_vehicule"])
def test_champs_nullables(contrat, champ):
    contrat[champ] = None
    assert getattr(Contrat.model_validate(contrat), champ) is None


@pytest.mark.parametrize(
    "champ", ["bonus", "type_contrat", "id_client", "sex_conducteur2", "anciennete_vehicule"]
)
def test_champ_manquant_refuse(contrat, champ):
    del contrat[champ]
    with pytest.raises(ValidationError):
        Contrat.model_validate(contrat)


@pytest.mark.parametrize(
    ("champ", "valeur"),
    [
        ("duree_contrat", "29"),
        ("duree_contrat", 29.5),
        ("duree_contrat", True),
        ("bonus", "0.5"),
        ("code_postal", 36233),
        ("type_contrat", "Gold"),
        ("conducteur2", "Oui"),
        ("age_conducteur1", -1),
        ("bonus", 0),
        ("age_conducteur1", None),
    ],
)
def test_valeur_invalide_refusee(contrat, champ, valeur):
    contrat[champ] = valeur
    with pytest.raises(ValidationError):
        Contrat.model_validate(contrat)


def test_entier_accepte_pour_un_decimal(contrat):
    contrat["bonus"] = 1
    assert Contrat.model_validate(contrat).bonus == 1.0


def test_champ_supplementaire_ignore(contrat):
    contrat["index"] = 3
    assert "index" not in Contrat.model_validate(contrat).model_dump()


def test_corps_vide_refuse():
    with pytest.raises(ValidationError):
        Contrat.model_validate({})
