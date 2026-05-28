# 🛩️ Predictive Maintenance — NASA CMAPSS

A predictive maintenance system for aircraft engines that forecasts the **Remaining Useful Life (RUL)** and detects degradation **anomalies** in turbofan engines.

**Time Series Project — ENSIAS, 2026**

---

## 🎯 Objectives

This project covers two Time Series objectives in a single end-to-end system:

- **Forecasting** — predict the Remaining Useful Life (RUL) of each engine from sensor data.
- **Anomaly Detection** — identify the onset of degradation in an **unsupervised** way (no failure labels needed).

---

## 📊 Results (FD001)

| Model | RMSE | MAE |
|---|---|---|
| Baseline (mean) | 41.94 | 34.83 |
| Linear Regression (1 sensor) | 23.38 | 19.05 |
| XGBoost (42 features) | 17.84 | 12.62 |
| **LSTM (sequences)** | **~13–15** | **~10–11** |

> The LSTM is the best model on every metric (RMSE, MAE, and NASA Score), confirming that the sequential dimension captures information the tabular XGBoost cannot.

---

## 🛠️ Tech Stack

- **Machine Learning:** XGBoost, scikit-learn
- **Deep Learning:** PyTorch (LSTM, Autoencoder)
- **Dashboard:** Streamlit + Plotly (bilingual EN/FR)
- **Interpretability:** SHAP
- **Data:** NASA CMAPSS (FD001 main, FD002 robustness validation)

---

## 📂 Project Structure

```text
Projet_Time_Series/
├── data/                 # NASA CMAPSS dataset (.txt files)
├── models/               # Trained models + saved artifacts
│   ├── xgb_model.json
│   ├── lstm_model.pt
│   ├── autoencoder.pt
│   ├── scaler.pkl
│   ├── config.json
│   └── ...
├── dashboard/            # Streamlit web app
│   ├── app.py            # Home page (entry point)
│   └── pages/
│       ├── 2_Prediction.py
│       ├── 3_Comparaison.py
│       └── 4_Anomalies.py
├── predict.py            # Model-loading & prediction module
├── translations.py       # EN/FR translation dictionary
├── notebook.ipynb        # Full analysis (EDA → ML → DL → anomaly)
├── requirements.txt      # Python dependencies
└── README.md
```

---

## 📈 Methodology

**Benchmark-first** approach: a progression of models of increasing complexity, each required to quantitatively beat the previous one.

1. **EDA** + informative sensor selection (14 of 21 kept)
2. **Feature engineering** — rolling statistics (mean, std) to denoise sensors
3. **Baselines** — naive mean and single-sensor regression (floor reference)
4. **XGBoost** — state-of-the-art tabular ML
5. **LSTM** — sequence-based deep learning (30-cycle windows)
6. **Autoencoder** — unsupervised anomaly detection
7. **Advanced extras** — NASA Score metric, FD002 robustness test, SHAP interpretability

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/predictive-maintenance-nasa-cmapss-ts.git
cd predictive-maintenance-nasa-cmapss-ts
```

### 2. (Recommended) Create a virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

> ⚠️ Use **Python 3.11** for best compatibility (Python 3.13 may cause issues with some libraries).

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the dashboard

```bash
streamlit run dashboard/app.py
```

The app opens automatically at `http://localhost:8501`.

---

## 👥 For My Teammate (How to Use This Project)

This section explains exactly what to do depending on what you want.

### ▶️ Just run the dashboard (no coding needed)

The trained models are already saved in `models/`, so you **don't need to retrain anything**.

```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
```

Then explore the 4 pages from the sidebar:
- **Home** — project overview & KPIs
- **Prediction** — pick an engine, see its predicted RUL + maintenance status
- **Comparison** — compare all models (RMSE, scatter plots, error distribution)
- **Anomalies** — anomaly score evolution per engine

You can switch between **English / French** using the language selector in the sidebar.

### 📓 Just read the analysis (no execution needed)

Open `notebook.ipynb` directly in VS Code or Jupyter. **All cell outputs are already saved** (graphs, metrics, tables), so you can read the full analysis from EDA to anomaly detection without running anything.

### 🔁 Re-run the notebook from scratch (optional)

If you want to regenerate everything yourself:

1. Make sure the dataset `.txt` files are in `data/`.
2. Open `notebook.ipynb`.
3. Click **Restart** then **Run All**.

> Note: training the LSTM takes ~1–2 minutes on CPU. RMSE values may vary slightly between runs due to random initialization (this is normal).

### 🧩 Understand the code architecture

- `predict.py` — loads the trained models and exposes prediction functions used by the dashboard. Start here to understand how the dashboard talks to the models.
- `translations.py` — all UI texts in EN/FR. To add/edit a label, edit this file only.
- `dashboard/app.py` + `dashboard/pages/` — the 4 Streamlit pages. Each page imports `predict.py` and `translations.py`.

---

## 📚 Dataset

[NASA CMAPSS](https://www.nasa.gov/intelligent-systems-division/) — Commercial Modular Aero-Propulsion System Simulation (Turbofan Engine Degradation Simulation Data Set).

- 100 engines simulated run-to-failure (FD001)
- 21 sensors + 3 operational settings per cycle
- Ground-truth RUL derived from the actual failure cycle

---

*Built as part of the Time Series module at ENSIAS, 2026.*
