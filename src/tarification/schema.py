"""Schéma d'entrée d'un contrat, conforme au contrat d'API du TD."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

EXEMPLE_CONTRAT = {
    "id_client": "A00000001",
    "id_vehicule": "V01",
    "id_contrat": "A00000001-V01",
    "bonus": 0.5,
    "type_contrat": "Maxi",
    "duree_contrat": 29,
    "anciennete_info": 9,
    "freq_paiement": "Biannual",
    "paiement": "No",
    "utilisation": "Retired",
    "code_postal": "36233",
    "conducteur2": "No",
    "age_conducteur1": 85,
    "age_conducteur2": 0,
    "sex_conducteur1": "M",
    "sex_conducteur2": None,
    "anciennete_permis1": 62,
    "anciennete_permis2": 0,
    "anciennete_vehicule": 10,
    "cylindre_vehicule": 1587,
    "din_vehicule": 98,
    "essence_vehicule": "Gasoline",
    "marque_vehicule": "PEUGEOT",
    "modele_vehicule": "306",
    "debut_vente_vehicule": 10,
    "fin_vente_vehicule": 9,
    "vitesse_vehicule": 182,
    "type_vehicule": "Tourism",
    "prix_vehicule": 20700,
    "poids_vehicule": 1210,
}


class Contrat(BaseModel):
    """Un contrat d'assurance automobile : colonnes du jeu de données hors variables cibles."""

    model_config = ConfigDict(strict=True, extra="ignore", json_schema_extra={"examples": [EXEMPLE_CONTRAT]})

    id_client: str
    id_vehicule: str
    id_contrat: str
    bonus: float = Field(gt=0)
    type_contrat: Literal["Mini", "Median1", "Median2", "Maxi"]
    duree_contrat: int = Field(ge=0)
    anciennete_info: int = Field(ge=0)
    freq_paiement: Literal["Monthly", "Quarterly", "Biannual", "Yearly"]
    paiement: Literal["Yes", "No"]
    utilisation: Literal["WorkPrivate", "Retired", "Professional", "AllTrips"]
    code_postal: str
    conducteur2: Literal["Yes", "No"]
    age_conducteur1: int = Field(ge=0)
    age_conducteur2: int = Field(ge=0)
    sex_conducteur1: Literal["M", "F"]
    sex_conducteur2: Literal["M", "F"] | None
    anciennete_permis1: int = Field(ge=0)
    anciennete_permis2: int = Field(ge=0)
    anciennete_vehicule: float | None = Field(ge=0)
    cylindre_vehicule: int = Field(ge=0)
    din_vehicule: int = Field(ge=0)
    essence_vehicule: Literal["Diesel", "Gasoline", "Hybrid"]
    marque_vehicule: str
    modele_vehicule: str
    debut_vente_vehicule: int = Field(ge=0)
    fin_vente_vehicule: int = Field(ge=0)
    vitesse_vehicule: int = Field(ge=0)
    type_vehicule: Literal["Tourism", "Commercial"]
    prix_vehicule: int = Field(ge=0)
    poids_vehicule: int = Field(ge=0)
