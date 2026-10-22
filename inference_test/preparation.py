# preparation.py
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer
from sklearn.impute import SimpleImputer


def manquants_structurels(X):
    """Sans second conducteur : âge et permis à 0, pas une médiane."""
    X = X.copy()
    if "age_conducteur2" in X.columns:
        sans_c2 = X["conducteur2"] == "No"
        X.loc[sans_c2, ["age_conducteur2", "anciennete_permis2"]] = 0
    return X


def construire_preprocesseur(num, cat):
    colonnes = ColumnTransformer([
        ("num", SimpleImputer(strategy="median", add_indicator=True), num),
        ("cat", Pipeline([
            ("imputation", SimpleImputer(strategy="constant", fill_value="Inconnu")),
            ("encodage", OneHotEncoder(handle_unknown="infrequent_if_exist", min_frequency=30,
                                       drop="if_binary", sparse_output=False)),
        ]), cat),
    ])
    return Pipeline([
        ("structurels", FunctionTransformer(manquants_structurels, feature_names_out="one-to-one")),
        ("colonnes", colonnes),
    ])