"""Page Prédiction — bilingue"""
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from predict import load_all, predict_rul, statut_maintenance
from translations import t, language_selector, TRANSLATIONS

st.set_page_config(page_title="Prediction", page_icon="🔧", layout="wide")
language_selector()

@st.cache_resource
def get_artefacts():
    return load_all(models_dir="models")

artefacts = get_artefacts()

st.title(t("pred_title"))
st.markdown(t("pred_subtitle"))
st.markdown("---")

col_sel, col_info = st.columns([1, 2])
with col_sel:
    moteur_num = st.selectbox(t("pred_select"), options=list(range(1, 101)), index=0)
    moteur_idx = moteur_num - 1
with col_info:
    st.info(t("pred_info", n=moteur_num))

st.markdown("---")

pred = predict_rul(artefacts, moteur_idx)
niveau, statut_color = statut_maintenance(pred["lstm"])

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label=t("pred_rul_lstm"), value=f"{pred['lstm']:.0f} {t('pred_cycles')}")
with col2:
    erreur = pred["lstm"] - pred["reel"]
    st.metric(label=t("pred_rul_real"), value=f"{pred['reel']:.0f} {t('pred_cycles')}",
              delta=t("pred_error", e=erreur), delta_color="off")
with col3:
    st.metric(label=t("pred_rul_xgb"), value=f"{pred['xgb']:.0f} {t('pred_cycles')}")

st.markdown("---")
st.markdown(t("pred_maint_title"))

# Texte du statut selon le niveau et la langue
statut_label = t(f"status_{niveau}")
statut_msg = t(f"status_{niveau}_msg")

st.markdown(f"""
<div style="background-color: {statut_color}20; border-left: 6px solid {statut_color};
    padding: 20px; border-radius: 8px; margin: 10px 0;">
    <h2 style="color: {statut_color}; margin: 0;">{statut_label}</h2>
    <p style="font-size: 18px; margin: 10px 0 0 0;">{statut_msg}</p>
</div>
""", unsafe_allow_html=True)

with st.expander(t("pred_legend")):
    if st.session_state.lang == "fr":
        st.markdown("""
        | Statut | Seuil RUL | Action |
        |---|---|---|
        | 🟢 **SAIN** | > 80 cycles | Aucune action requise |
        | 🟡 **SURVEILLANCE** | 30 à 80 cycles | Planifier une inspection |
        | 🔴 **MAINTENANCE URGENTE** | ≤ 30 cycles | Intervention immédiate |
        """)
    else:
        st.markdown("""
        | Status | RUL threshold | Action |
        |---|---|---|
        | 🟢 **HEALTHY** | > 80 cycles | No action required |
        | 🟡 **MONITORING** | 30 to 80 cycles | Schedule an inspection |
        | 🔴 **URGENT MAINTENANCE** | ≤ 30 cycles | Immediate intervention |
        """)

st.markdown("---")
st.markdown(t("pred_chart_title"))

real_label = "RUL réel" if st.session_state.lang == "fr" else "Actual RUL"
fig = go.Figure()
fig.add_trace(go.Bar(
    x=[real_label, "LSTM (DL)", "XGBoost (ML)"],
    y=[pred["reel"], pred["lstm"], pred["xgb"]],
    marker_color=["#22c55e", "#c0392b", "#4a7fb5"],
    text=[f"{pred['reel']:.0f}", f"{pred['lstm']:.0f}", f"{pred['xgb']:.0f}"],
    textposition="outside", textfont=dict(size=16, color="white"),
))
ytitle = "Cycles restants" if st.session_state.lang == "fr" else "Remaining cycles"
fig.update_layout(height=400, yaxis_title=ytitle, showlegend=False, template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown(t("pred_sensors_title"))
st.caption(t("pred_sensors_caption"))

X_seq = artefacts["X_test_seq"][moteur_idx]
capteurs = artefacts["config"]["capteurs_utiles"]
capteurs_a_voir = [c for c in ["sensor4", "sensor11", "sensor15", "sensor9"] if c in capteurs]

fig2 = make_subplots(rows=2, cols=2, subplot_titles=capteurs_a_voir)
cycles_relatifs = np.arange(-29, 1)
for i, capteur in enumerate(capteurs_a_voir):
    col_idx = capteurs.index(capteur)
    fig2.add_trace(go.Scatter(x=cycles_relatifs, y=X_seq[:, col_idx],
        mode="lines", line=dict(color="#4a7fb5", width=2), showlegend=False),
        row=i // 2 + 1, col=i % 2 + 1)
fig2.update_layout(height=500, template="plotly_dark", showlegend=False)
st.plotly_chart(fig2, use_container_width=True)