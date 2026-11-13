"""Schémas Pydantic : forme exacte du contrat d'entrée et des réponses de l'API.

Les champs reprennent les colonnes de data/train.csv (hors index et cibles
nombre_sinistres / montant_sinistre), conformément au contrat d'API du TD.
"""

from pydantic import BaseModel, Field


class Contrat(BaseModel):
    id_client: str
    id_vehicule: str
    id_contrat: str
    bonus: float
    type_contrat: str
    duree_contrat: int
    anciennete_info: int
    freq_paiement: str
    paiement: str
    utilisation: str
    code_postal: str
    conducteur2: str
    age_conducteur1: int
    age_conducteur2: int
    sex_conducteur1: str
    sex_conducteur2: str | None = None
    anciennete_permis1: int
    anciennete_permis2: int
    anciennete_vehicule: float | None = None
    cylindre_vehicule: int
    din_vehicule: int
    essence_vehicule: str
    marque_vehicule: str
    modele_vehicule: str
    debut_vente_vehicule: int
    fin_vente_vehicule: int
    vitesse_vehicule: int
    type_vehicule: str
    prix_vehicule: float
    poids_vehicule: float

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id_client": "A00000001", "id_vehicule": "V01", "id_contrat": "A00000001-V01",
                    "bonus": 0.5, "type_contrat": "Maxi", "duree_contrat": 29,
                    "anciennete_info": 9, "freq_paiement": "Biannual", "paiement": "No",
                    "utilisation": "Retired", "code_postal": "36233", "conducteur2": "No",
                    "age_conducteur1": 85, "age_conducteur2": 0,
                    "sex_conducteur1": "M", "sex_conducteur2": None,
                    "anciennete_permis1": 62, "anciennete_permis2": 0,
                    "anciennete_vehicule": 10, "cylindre_vehicule": 1587, "din_vehicule": 98,
                    "essence_vehicule": "Gasoline", "marque_vehicule": "PEUGEOT",
                    "modele_vehicule": "306", "debut_vente_vehicule": 10,
                    "fin_vente_vehicule": 9, "vitesse_vehicule": 182,
                    "type_vehicule": "Tourism", "prix_vehicule": 20700, "poids_vehicule": 1210,
                }
            ]
        }
    }


class HealthResponse(BaseModel):
    status: str = Field(..., examples=["ok"])


class FrequencyResponse(BaseModel):
    frequency: float = Field(..., ge=0, examples=[0.12])


class AmountResponse(BaseModel):
    amount: float = Field(..., ge=0, examples=[1500.0])


class PredictResponse(BaseModel):
    frequency: float = Field(..., ge=0, examples=[0.12])
    amount: float = Field(..., ge=0, examples=[1500.0])
    premium: float = Field(..., ge=0, examples=[180.0])
