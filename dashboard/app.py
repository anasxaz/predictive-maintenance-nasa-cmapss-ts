"""
Dashboard Predictive Maintenance — Page d'accueil (bilingue)
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
from predict import load_all
from translations import t, language_selector

st.set_page_config(
    page_title="Predictive Maintenance — NASA CMAPSS",
    page_icon="🛩️",
    layout="wide",
)

# Sélecteur de langue (sidebar)
language_selector()

@st.cache_resource
def get_artefacts():
    return load_all(models_dir="models")

artefacts = get_artefacts()

# ===== CONTENU =====
st.title(t("app_title"))
st.markdown(t("app_subtitle"))
st.markdown("---")
st.markdown(t("app_welcome"))
st.markdown("---")

# KPIs
st.markdown(t("app_kpi_title"))
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label=t("kpi_engines"), value="100")
with col2:
    rmse_lstm = artefacts["resultats"]["LSTM"]["RMSE"]
    st.metric(label="RMSE (LSTM)", value=f"{rmse_lstm:.2f}",
              delta=f"-{41.94 - rmse_lstm:.1f} vs baseline", delta_color="inverse")
with col3:
    st.metric(label=t("kpi_sensors"), value="14 / 21")
with col4:
    st.metric(label=t("kpi_objectives"), value="2")

st.markdown("---")

# Tableau comparatif
st.markdown(t("app_compare_title"))
resultats_df = pd.DataFrame(artefacts["resultats"]).T
resultats_df.index.name = "Modèle"
st.dataframe(
    resultats_df.style.highlight_min(axis=0, color="lightgreen"),
    use_container_width=True
)
st.caption(t("app_compare_caption"))
st.markdown("---")

# Méthodologie + Dataset
col_a, col_b = st.columns(2)
with col_a:
    st.markdown(t("app_method_title"))
    st.markdown(t("app_method_body"))
with col_b:
    st.markdown(t("app_dataset_title"))
    st.markdown(t("app_dataset_body"))

st.markdown("---")
st.markdown(t("app_explore_title"))
st.info(t("app_explore_info"))
st.markdown("---")
st.caption("📅 Projet Time Series — ENSIAS, 2026")