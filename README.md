# 🛩️ Predictive Maintenance for Aircraft Engines

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.x-ee4c2c.svg)](https://pytorch.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live%20Demo-ff4b4b.svg)](https://predictive-maintenance-nasa.streamlit.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

End-to-end predictive maintenance system for aircraft turbofan engines, combining **RUL forecasting** and **unsupervised anomaly detection** on the NASA CMAPSS dataset.

> 🚀 **Live demo:** [predictive-maintenance-nasa.streamlit.app](https://predictive-maintenance-nasa.streamlit.app)

---

## 🎯 Overview

Two Time Series objectives in a single end-to-end system:

- **🎯 Forecasting** — predict the **Remaining Useful Life (RUL)** of each engine from sensor sequences
- **🚨 Anomaly Detection** — identify the onset of degradation in an **unsupervised** way (no failure labels needed)

The system is shipped as an interactive **bilingual (EN/FR) Streamlit dashboard** with 4 pages: project overview, per-engine prediction, model comparison, and anomaly detection.

---

## 📊 Results (FD001)

| Model | RMSE | MAE | NASA Score |
|---|---|---|---|
| Baseline (mean) | 41.94 | 34.83 | 33,354 |
| Linear Regression (1 sensor) | 23.38 | 19.05 | 1,516 |
| XGBoost (42 features) | 17.84 | 12.62 | 987 |
| **LSTM (sequences)** | **13.31** | **9.71** | **324** |

**The LSTM wins on every metric**, confirming that the sequential dimension captures degradation patterns that tabular models miss. **−68% RMSE vs. baseline.**

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| **Machine Learning** | XGBoost, scikit-learn |
| **Deep Learning** | PyTorch (LSTM, Autoencoder) |
| **Dashboard** | Streamlit + Plotly (bilingual EN/FR) |
| **Interpretability** | SHAP |
| **Data** | NASA CMAPSS (FD001 main, FD002 robustness validation) |

---

## 📈 Methodology

**Benchmark-first** approach: a progression of models of increasing complexity, each required to quantitatively beat the previous one.

1. **EDA** + informative sensor selection (14 of 21 kept)
2. **Feature engineering** — rolling statistics (mean, std) to denoise sensors → 42 features
3. **Baselines** — naive mean and single-sensor regression (floor reference)
4. **XGBoost** — state-of-the-art tabular ML
5. **LSTM** — sequence-based deep learning (30-cycle sliding windows)
6. **Autoencoder** — unsupervised anomaly detection
7. **Advanced extras** — NASA Score metric, FD002 robustness validation, SHAP interpretability

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/anasxaz/predictive-maintenance-nasa-cmapss-ts.git
cd predictive-maintenance-nasa-cmapss-ts
```

### 2. Create a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

> ⚠️ **Python 3.11 recommended** for best compatibility (Python 3.13+ may cause issues with some libraries).

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the dashboard

```bash
streamlit run dashboard/app.py
```

The app opens at `http://localhost:8501`. Switch between **English / French** using the language selector in the sidebar.

---

## 📂 Project Structure

```text
predictive-maintenance-nasa-cmapss-ts/
├── data/                 # NASA CMAPSS dataset (.txt files)
├── models/               # Trained models + saved artifacts
│   ├── xgb_model.json
│   ├── lstm_model.pt
│   ├── autoencoder.pt
│   ├── scaler.pkl
│   └── config.json
├── dashboard/            # Streamlit web app
│   ├── app.py            # Home page (entry point)
│   └── pages/
│       ├── 2_🔧_Prediction.py
│       ├── 3_📊_Comparaison.py
│       └── 4_🚨_Anomalies.py
├── predict.py            # Model-loading & prediction module
├── translations.py       # EN/FR translation dictionary
├── notebook.ipynb        # Full analysis (EDA → ML → DL → anomaly)
├── requirements.txt
└── README.md
```

---

## 📓 Reading the Analysis

The full analysis lives in `notebook.ipynb`. **All cell outputs are saved** (graphs, metrics, tables), so you can read the entire pipeline from EDA to anomaly detection **without re-running anything**.

If you want to regenerate everything from scratch:

1. Make sure the dataset `.txt` files are in `data/`.
2. Open `notebook.ipynb` and click **Restart** → **Run All**.

> LSTM training takes ~1–2 minutes on CPU. RMSE values may vary slightly between runs due to random initialization.

---

## 📚 Dataset

[**NASA CMAPSS**](https://www.nasa.gov/intelligent-systems-division/) — Commercial Modular Aero-Propulsion System Simulation (Turbofan Engine Degradation Simulation Data Set).

- 100 engines simulated run-to-failure (FD001)
- 21 sensors + 3 operational settings per cycle
- Ground-truth RUL derived from the actual failure cycle
- FD002 used for robustness validation (6 operating conditions)

---

## 👥 Authors

- **Anas Benamara** — [@anasxaz](https://github.com/anasxaz)
- **Ali Benhima**

Built as part of the **Time Series** module — *Pr. Brahim Ait Skourt*  
**ENSIAS** — École Nationale Supérieure d'Informatique et d'Analyse des Systèmes, 2026.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
