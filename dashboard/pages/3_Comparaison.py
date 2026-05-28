"""Page Comparaison — bilingue"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from predict import load_all
from translations import t, language_selector

st.set_page_config(page_title="Comparison", page_icon="📊", layout="wide")
language_selector()

@st.cache_resource
def get_artefacts():
    return load_all(models_dir="models")

artefacts = get_artefacts()

st.title(t("comp_title"))
st.markdown(t("comp_subtitle"))
st.markdown("---")

st.markdown(t("comp_table_title"))
resultats = artefacts["resultats"]
df = pd.DataFrame(resultats).T
df.index.name = "Modèle"
df = df.round(2)
st.dataframe(df.style.highlight_min(axis=0, color="lightgreen").format("{:.2f}"),
             use_container_width=True)
st.caption(t("comp_table_caption"))
st.markdown("---")

st.markdown(t("comp_progress_title"))
modeles = list(resultats.keys())
rmse_values = [resultats[m]["RMSE"] for m in modeles]
couleurs = ["#c0c0c0", "#7fa8d0", "#4a7fb5", "#c0392b"]
fig = go.Figure()
fig.add_trace(go.Bar(x=modeles, y=rmse_values, marker_color=couleurs,
    text=[f"{v:.2f}" for v in rmse_values], textposition="outside",
    textfont=dict(size=16, color="white")))
ytitle = "RMSE (cycles) — plus bas = meilleur" if st.session_state.lang == "fr" else "RMSE (cycles) — lower = better"
fig.update_layout(height=500, yaxis_title=ytitle, template="plotly_dark", showlegend=False)
st.plotly_chart(fig, use_container_width=True)
st.markdown("---")

st.markdown(t("comp_quality_title"))
y_true = artefacts["y_true"]
y_pred_lstm = artefacts["y_pred_lstm"]
y_pred_xgb = artefacts["y_pred_xgb"]
perfect_label = "Prédiction parfaite" if st.session_state.lang == "fr" else "Perfect prediction"
xlab = "RUL réel" if st.session_state.lang == "fr" else "Actual RUL"
ylab = "RUL prédit" if st.session_state.lang == "fr" else "Predicted RUL"
lims = [0, 125]

col1, col2 = st.columns(2)
with col1:
    f = go.Figure()
    f.add_trace(go.Scatter(x=y_true, y=y_pred_lstm, mode="markers",
        marker=dict(size=10, color="#c0392b", line=dict(color="white", width=1)), name="LSTM"))
    f.add_trace(go.Scatter(x=lims, y=lims, mode="lines",
        line=dict(color="white", dash="dash"), name=perfect_label))
    f.update_layout(title=f"LSTM (RMSE = {resultats['LSTM']['RMSE']:.2f})",
        xaxis_title=xlab, yaxis_title=ylab, template="plotly_dark", height=500)
    st.plotly_chart(f, use_container_width=True)
with col2:
    f = go.Figure()
    f.add_trace(go.Scatter(x=y_true, y=y_pred_xgb, mode="markers",
        marker=dict(size=10, color="#4a7fb5", line=dict(color="white", width=1)), name="XGBoost"))
    f.add_trace(go.Scatter(x=lims, y=lims, mode="lines",
        line=dict(color="white", dash="dash"), name=perfect_label))
    f.update_layout(title=f"XGBoost (RMSE = {resultats['XGBoost']['RMSE']:.2f})",
        xaxis_title=xlab, yaxis_title=ylab, template="plotly_dark", height=500)
    st.plotly_chart(f, use_container_width=True)

st.markdown("---")
st.markdown(t("comp_dist_title"))
errors_lstm = y_pred_lstm - y_true
errors_xgb = y_pred_xgb - y_true
zero_label = "Erreur nulle" if st.session_state.lang == "fr" else "Zero error"
xlab2 = "Erreur (cycles)" if st.session_state.lang == "fr" else "Error (cycles)"
ylab2 = "Nombre de moteurs" if st.session_state.lang == "fr" else "Number of engines"
fig_h = go.Figure()
fig_h.add_trace(go.Histogram(x=errors_lstm, name="LSTM", marker_color="#c0392b", opacity=0.7, nbinsx=30))
fig_h.add_trace(go.Histogram(x=errors_xgb, name="XGBoost", marker_color="#4a7fb5", opacity=0.7, nbinsx=30))
fig_h.add_vline(x=0, line_dash="dash", line_color="white", annotation_text=zero_label)
fig_h.update_layout(xaxis_title=xlab2, yaxis_title=ylab2, template="plotly_dark", height=450, barmode="overlay")
st.plotly_chart(fig_h, use_container_width=True)

st.markdown("---")
st.markdown(t("comp_concl_title"))
if st.session_state.lang == "fr":
    st.markdown("""
- **Progression claire** : chaque modèle améliore significativement le précédent.
- **LSTM gagnant** : la dimension séquentielle apporte une information non capturée par XGBoost.
- **Précision en fin de vie** : les prédictions sont plus serrées pour les RUL faibles.
- **NASA Score** : le LSTM minimise aussi la pénalité asymétrique.
""")
else:
    st.markdown("""
- **Clear progression**: each model significantly improves on the previous one.
- **LSTM wins**: the sequential dimension captures information XGBoost cannot.
- **End-of-life accuracy**: predictions are tighter for low RUL values.
- **NASA Score**: the LSTM also minimizes the asymmetric penalty.
""")