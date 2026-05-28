"""
Module de prédiction — Predictive Maintenance NASA CMAPSS
Charge les modèles entraînés et fournit des fonctions de prédiction
pour le dashboard Streamlit.
"""

import json
import pickle
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from xgboost import XGBRegressor


# ============================================================
# 1. Architectures des modèles (mêmes que dans le notebook)
# ============================================================

class LSTMRegressor(nn.Module):
    def __init__(self, n_features, hidden_size=64, num_layers=2, dropout=0.2):
        super().__init__()
        self.lstm = nn.LSTM(
            input_size=n_features,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout
        )
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = out[:, -1, :]
        out = self.dropout(out)
        return self.fc(out).squeeze()


class Autoencoder(nn.Module):
    def __init__(self, n_features):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(n_features, 8), nn.ReLU(),
            nn.Linear(8, 4), nn.ReLU()
        )
        self.decoder = nn.Sequential(
            nn.Linear(4, 8), nn.ReLU(),
            nn.Linear(8, n_features)
        )

    def forward(self, x):
        return self.decoder(self.encoder(x))


# ============================================================
# 2. Chargement des modèles
# ============================================================

def load_all(models_dir="models"):
    """Charge tous les modèles, le scaler, la config et les données."""

    # Config
    with open(f"{models_dir}/config.json") as f:
        config = json.load(f)

    # XGBoost
    xgb = XGBRegressor()
    xgb.load_model(f"{models_dir}/xgb_model.json")

    # LSTM
    lstm_ckpt = torch.load(f"{models_dir}/lstm_model.pt", weights_only=False)
    lstm = LSTMRegressor(
        n_features=lstm_ckpt['n_features'],
        hidden_size=lstm_ckpt['hidden_size'],
        num_layers=lstm_ckpt['num_layers'],
        dropout=lstm_ckpt['dropout'],
    )
    lstm.load_state_dict(lstm_ckpt['state_dict'])
    lstm.eval()

    # Autoencoder
    ae_ckpt = torch.load(f"{models_dir}/autoencoder.pt", weights_only=False)
    ae = Autoencoder(n_features=ae_ckpt['n_features'])
    ae.load_state_dict(ae_ckpt['state_dict'])
    ae.eval()

    # Scaler
    with open(f"{models_dir}/scaler.pkl", "rb") as f:
        scaler = pickle.load(f)

    # Données de test
    test_last = pd.read_csv(f"{models_dir}/test_last.csv")
    X_test_seq = np.load(f"{models_dir}/X_test_seq.npy")
    y_true = np.load(f"{models_dir}/y_true.npy")
    y_pred_xgb = np.load(f"{models_dir}/y_pred_xgb.npy")
    y_pred_lstm = np.load(f"{models_dir}/y_pred_lstm.npy")

    # Résultats
    with open(f"{models_dir}/resultats.json") as f:
        resultats = json.load(f)

    return {
        "config": config,
        "xgb": xgb,
        "lstm": lstm,
        "autoencoder": ae,
        "scaler": scaler,
        "test_last": test_last,
        "X_test_seq": X_test_seq,
        "y_true": y_true,
        "y_pred_xgb": y_pred_xgb,
        "y_pred_lstm": y_pred_lstm,
        "resultats": resultats,
    }


# ============================================================
# 3. Fonctions de prédiction par moteur
# ============================================================

def predict_rul(artefacts, moteur_idx):
    """
    Pour un moteur de test donné (idx 0 à 99), renvoie :
    - prédiction XGBoost
    - prédiction LSTM
    - vrai RUL
    """
    return {
        "xgb": float(artefacts["y_pred_xgb"][moteur_idx]),
        "lstm": float(artefacts["y_pred_lstm"][moteur_idx]),
        "reel": float(artefacts["y_true"][moteur_idx]),
    }


def statut_maintenance(rul):
    """Renvoie le NIVEAU de maintenance (pas le texte — géré par les traductions)."""
    if rul > 80:
        return ("healthy", "#22c55e")
    elif rul > 30:
        return ("watch", "#eab308")
    else:
        return ("urgent", "#ef4444")


def score_anomalie(artefacts, moteur_idx, lissage=10):
    """
    Calcule le score d'anomalie au fil de la vie d'un moteur de test.
    Renvoie (cycles, scores_lisses).
    """
    config = artefacts["config"]
    capteurs = config["capteurs_utiles"]

    # Récupérer toute la séquence de ce moteur (30 derniers cycles disponibles)
    X = artefacts["X_test_seq"][moteur_idx]  # shape (30, 14)

    # Erreur de reconstruction pour chaque cycle de la séquence
    X_t = torch.tensor(X, dtype=torch.float32)
    with torch.no_grad():
        recon = artefacts["autoencoder"](X_t).numpy()
    err = np.mean((recon - X) ** 2, axis=1)

    # Lisser
    err_lisse = pd.Series(err).rolling(window=lissage, min_periods=1).mean().values

    return np.arange(len(err_lisse)), err_lisse