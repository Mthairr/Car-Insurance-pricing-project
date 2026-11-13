import pickle

import pandas as pd
import pytest

from tarification.config import MODELE_FREQ_PATH, MODELE_MONTANT_PATH, TEST_PATH
from tarification.schema import EXEMPLE_CONTRAT


@pytest.fixture
def contrat():
    return dict(EXEMPLE_CONTRAT)


@pytest.fixture(scope="session")
def modele_frequence():
    with open(MODELE_FREQ_PATH, "rb") as f:
        return pickle.load(f)


@pytest.fixture(scope="session")
def modele_montant():
    with open(MODELE_MONTANT_PATH, "rb") as f:
        return pickle.load(f)


@pytest.fixture(scope="session")
def echantillon_test():
    df = pd.read_csv(TEST_PATH, nrows=200, dtype={"code_postal": str}).drop(columns="index")
    df["id_client"] = "A" + df.index.astype(str)
    df["id_vehicule"] = "V01"
    df["id_contrat"] = df["id_client"] + "-V01"
    return df
