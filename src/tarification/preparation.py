"""Traitements des données communs à l'entraînement et à l'inférence."""

from typing import get_args

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder

from tarification.config import VARIABLES_MONTANT
from tarification.schema import Contrat


def colonnes_decimales():
    """Champs du contrat de type float, éventuellement nuls."""
    return [
        nom
        for nom, champ in Contrat.model_fields.items()
        if champ.annotation is float or float in get_args(champ.annotation)
    ]


def preparer_contrat(donnees):
    """Valide un contrat (dict issu du JSON) et le convertit en DataFrame d'une ligne."""
    contrat = donnees if isinstance(donnees, Contrat) else Contrat.model_validate(donnees)
    df = pd.DataFrame([contrat.model_dump()])
    return df.astype(dict.fromkeys(colonnes_decimales(), "float64"))


def manquants_structurels(X):
    """Sans second conducteur : âge et permis à 0, pas une médiane."""
    X = X.copy()
    sans_c2 = X["conducteur2"] == "No"
    X.loc[sans_c2, ["age_conducteur2", "anciennete_permis2"]] = 0
    return X


def construire_preprocesseur(num, cat):
    """Préprocesseur du modèle de fréquence : imputation, encodage one-hot."""
    colonnes = ColumnTransformer(
        [
            ("num", SimpleImputer(strategy="median", add_indicator=True), num),
            (
                "cat",
                Pipeline(
                    [
                        ("imputation", SimpleImputer(strategy="constant", fill_value="Inconnu")),
                        (
                            "encodage",
                            OneHotEncoder(
                                handle_unknown="infrequent_if_exist",
                                min_frequency=30,
                                drop="if_binary",
                                sparse_output=False,
                            ),
                        ),
                    ]
                ),
                cat,
            ),
        ]
    )
    return Pipeline(
        [
            ("structurels", FunctionTransformer(manquants_structurels, feature_names_out="one-to-one")),
            ("colonnes", colonnes),
        ]
    )


def variables_montant(df):
    """Variables du modèle de montant, identiques à l'entraînement et à l'inférence."""
    return pd.DataFrame(
        {
            "maxi": (df["type_contrat"] == "Maxi").astype(int),
            "anciennete_vehicule": df["anciennete_vehicule"],
        },
        index=df.index,
    )


def construire_preprocesseur_montant():
    """Préprocesseur du modèle de montant : médiane apprise sur le train."""
    return ColumnTransformer([("num", SimpleImputer(strategy="median"), VARIABLES_MONTANT)])
