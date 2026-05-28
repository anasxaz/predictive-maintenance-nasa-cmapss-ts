# 🛩️ Predictive Maintenance — NASA CMAPSS

Système de maintenance prédictive pour moteurs d'avion, prédisant la durée de vie restante (RUL) et détectant les anomalies de dégradation.

**Projet Time Series — ENSIAS, 2026**

## 🎯 Objectifs

- **Forecasting** : prédire le RUL (Remaining Useful Life) des moteurs
- **Anomaly Detection** : détecter la dégradation de manière non supervisée

## 📊 Résultats (FD001)

| Modèle | RMSE | MAE |
|---|---|---|
| Baseline | 41.94 | 34.83 |
| Régression linéaire | 23.38 | 19.05 |
| XGBoost | 17.84 | 12.62 |
| **LSTM** | **~13-15** | **~10-11** |

## 🛠️ Stack technique

- **ML** : XGBoost, scikit-learn
- **DL** : PyTorch (LSTM, Autoencoder)
- **Dashboard** : Streamlit + Plotly (bilingue FR/EN)
- **Interprétabilité** : SHAP

## 🚀 Lancer le dashboard

```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
```

## 📂 Structure
├── data/              # Dataset NASA CMAPSS
├── models/            # Modèles entraînés
├── dashboard/         # Application Streamlit
│   ├── app.py
│   └── pages/
├── predict.py         # Module de prédiction
├── translations.py    # Traductions FR/EN
└── notebook.ipynb     # Analyse complète

## 📈 Méthodologie

Approche *benchmark first* : progression de modèles de complexité croissante (baseline → ML → DL), chacun devant battre le précédent.

---

*Dataset : [NASA CMAPSS](https://www.nasa.gov/intelligent-systems-division/) — Turbofan Engine Degradation Simulation*  