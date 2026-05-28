"""Page Anomalies — bilingue"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from predict import load_all, score_anomalie
from translations import t, language_selector

st.set_page_config(page_title="Anomalies", page_icon="🚨", layout="wide")
language_selector()

@st.cache_resource
def get_artefacts():
    return load_all(models_dir="models")

artefacts = get_artefacts()

st.title(t("anom_title"))
st.markdown(t("anom_subtitle"))
st.markdown("---")

with st.expander(t("anom_how")):
    if st.session_state.lang == "fr":
        st.markdown("""
        1. **Entraînement** : l'autoencoder apprend à reconstruire des capteurs **sains**.
        2. **Détection** : reconstruction réussie → normal ; échec → **anomalie**.
        3. **Score** = erreur de reconstruction. Plus elle est haute, plus c'est anormal.
        
        👉 Aucune étiquette de panne n'est nécessaire.
        """)
    else:
        st.markdown("""
        1. **Training**: the autoencoder learns to reconstruct **healthy** sensors.
        2. **Detection**: successful reconstruction → normal; failure → **anomaly**.
        3. **Score** = reconstruction error. The higher it is, the more abnormal.
        
        👉 No failure labels are needed.
        """)

col_sel, col_info = st.columns([1, 2])
with col_sel:
    moteur_num = st.selectbox(t("anom_select"), options=list(range(1, 101)), index=0)
    moteur_idx = moteur_num - 1
with col_info:
    st.info(t("pred_info", n=moteur_num))

st.markdown("---")
st.markdown(t("anom_chart_title"))

cycles, scores = score_anomalie(artefacts, moteur_idx, lissage=5)
score_label = "Score d'anomalie" if st.session_state.lang == "fr" else "Anomaly score"
xlab = "Cycle (séquence des 30 derniers)" if st.session_state.lang == "fr" else "Cycle (last 30 sequence)"

fig = go.Figure()
fig.add_trace(go.Scatter(x=cycles, y=scores, mode="lines+markers",
    line=dict(color="#c0392b", width=2), fill="tozeroy",
    fillcolor="rgba(192, 57, 43, 0.2)", name=score_label))
fig.update_layout(height=400, xaxis_title=xlab, yaxis_title=score_label, template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

col_a, col_b = st.columns(2)
with col_a:
    st.metric(t("anom_score_max"), f"{scores.max():.4f}")
with col_b:
    st.metric(t("anom_score_mean"), f"{scores.mean():.4f}")

st.markdown("---")
st.markdown(t("anom_multi_title"))

moteurs_choisis = st.multiselect(t("anom_multi_select"),
    options=list(range(1, 101)), default=[1, 2, 50, 100])

if moteurs_choisis:
    couleurs = ["#c0392b", "#e67e22", "#27ae60", "#2980b9", "#8e44ad", "#16a085"]
    moteur_label = "Moteur" if st.session_state.lang == "fr" else "Engine"
    xlab2 = "% de la séquence" if st.session_state.lang == "fr" else "% of sequence"
    fig_m = go.Figure()
    for i, m_num in enumerate(moteurs_choisis):
        cy, sc = score_anomalie(artefacts, m_num - 1, lissage=5)
        pct = cy / cy.max() * 100
        fig_m.add_trace(go.Scatter(x=pct, y=sc, mode="lines",
            line=dict(width=2, color=couleurs[i % len(couleurs)]),
            name=f"{moteur_label} {m_num}"))
    fig_m.update_layout(height=500, xaxis_title=xlab2, yaxis_title=score_label, template="plotly_dark")
    st.plotly_chart(fig_m, use_container_width=True)

st.markdown("---")
st.markdown(t("anom_interp_title"))
if st.session_state.lang == "fr":
    st.markdown("""
- L'autoencoder détecte la dégradation **sans aucune supervision**.
- Le score est **stable** quand le moteur va bien, puis **croît** vers la panne.
- Cette approche complète le forecasting : une **alerte précoce** indépendante.
""")
else:
    st.markdown("""
- The autoencoder detects degradation **without any supervision**.
- The score is **stable** when the engine is healthy, then **rises** toward failure.
- This complements forecasting: an independent **early warning**.
""")