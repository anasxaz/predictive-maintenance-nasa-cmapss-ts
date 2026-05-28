"""
Dictionnaire de traductions FR / EN pour le dashboard.
Chaque clé correspond à un texte, avec sa version française et anglaise.
"""

import streamlit as st

TRANSLATIONS = {
    # ===== COMMUN / SÉLECTEUR LANGUE =====
    "lang_label": {"fr": "🌍 Langue", "en": "🌍 Language"},

    # ===== PAGE ACCUEIL =====
    "app_title": {
        "fr": "🛩️ Maintenance Prédictive des Moteurs d'Avion",
        "en": "🛩️ Predictive Maintenance for Aircraft Engines"
    },
    "app_subtitle": {
        "fr": "### Système intelligent de prédiction de durée de vie restante (RUL)",
        "en": "### Intelligent Remaining Useful Life (RUL) prediction system"
    },
    "app_welcome": {
        "fr": """Bienvenue sur le dashboard de **maintenance prédictive** basé sur le dataset 
**NASA CMAPSS** (Commercial Modular Aero-Propulsion System Simulation).

Ce système combine deux objectifs Time Series :
- 🎯 **Prévision (Forecasting)** : prédire la durée de vie restante d'un moteur
- 🚨 **Détection d'anomalie** : identifier le début de la dégradation, sans étiquette""",
        "en": """Welcome to the **predictive maintenance** dashboard based on the 
**NASA CMAPSS** dataset (Commercial Modular Aero-Propulsion System Simulation).

This system combines two Time Series objectives:
- 🎯 **Forecasting**: predict the remaining useful life of an engine
- 🚨 **Anomaly detection**: identify the onset of degradation, without labels"""
    },
    "app_kpi_title": {"fr": "### 📊 Le projet en chiffres", "en": "### 📊 The project in numbers"},
    "kpi_engines": {"fr": "Moteurs analysés", "en": "Engines analyzed"},
    "kpi_sensors": {"fr": "Capteurs informatifs", "en": "Informative sensors"},
    "kpi_objectives": {"fr": "Objectifs TS", "en": "TS objectives"},
    "app_compare_title": {"fr": "### 🏆 Comparaison des modèles", "en": "### 🏆 Model comparison"},
    "app_compare_caption": {
        "fr": "💡 Plus le score est bas, meilleur est le modèle. Le LSTM est le meilleur sur toutes les métriques.",
        "en": "💡 Lower score is better. The LSTM is the best on all metrics."
    },
    "app_method_title": {"fr": "### 🔬 Méthodologie", "en": "### 🔬 Methodology"},
    "app_method_body": {
        "fr": """Approche **benchmark first** : progression de modèles de complexité croissante.

1. **EDA** + sélection des capteurs informatifs
2. **Feature engineering** (statistiques glissantes)
3. **Baselines** (référence du plancher)
4. **XGBoost** (ML état de l'art)
5. **LSTM** (DL sur séquences)
6. **Autoencoder** (anomalie non supervisée)""",
        "en": """**Benchmark first** approach: progression of models with increasing complexity.

1. **EDA** + informative sensor selection
2. **Feature engineering** (rolling statistics)
3. **Baselines** (floor reference)
4. **XGBoost** (state-of-the-art ML)
5. **LSTM** (sequence-based DL)
6. **Autoencoder** (unsupervised anomaly detection)"""
    },
    "app_dataset_title": {"fr": "### 📂 Dataset NASA CMAPSS", "en": "### 📂 NASA CMAPSS Dataset"},
    "app_dataset_body": {
        "fr": """**Commercial Modular Aero-Propulsion System Simulation**

- 100 moteurs simulés en *run-to-failure*
- 21 capteurs + 3 réglages opérationnels
- 20 631 observations d'entraînement
- Vérité-terrain RUL dérivée mécaniquement""",
        "en": """**Commercial Modular Aero-Propulsion System Simulation**

- 100 engines simulated *run-to-failure*
- 21 sensors + 3 operational settings
- 20,631 training observations
- Ground-truth RUL mechanically derived"""
    },
    "app_explore_title": {"fr": "### 🚀 Explorer le dashboard", "en": "### 🚀 Explore the dashboard"},
    "app_explore_info": {
        "fr": "👈 Utilisez le menu latéral pour naviguer entre les pages : **Prédiction**, **Comparaison**, **Anomalies**",
        "en": "👈 Use the sidebar to navigate between pages: **Prediction**, **Comparison**, **Anomalies**"
    },

    # ===== PAGE PRÉDICTION =====
    "pred_title": {"fr": "🔧 Prédiction interactive du RUL", "en": "🔧 Interactive RUL Prediction"},
    "pred_subtitle": {
        "fr": "Sélectionnez un moteur de test pour voir la prédiction de **durée de vie restante** en temps réel.",
        "en": "Select a test engine to see the **remaining useful life** prediction in real time."
    },
    "pred_select": {"fr": "🎯 Choisissez un moteur de test", "en": "🎯 Choose a test engine"},
    "pred_info": {
        "fr": "**Moteur n°{n}** — Affichage de la prédiction LSTM, du résultat XGBoost et du statut de maintenance.",
        "en": "**Engine #{n}** — LSTM prediction, XGBoost result and maintenance status."
    },
    "pred_rul_lstm": {"fr": "🤖 RUL prédit (LSTM)", "en": "🤖 Predicted RUL (LSTM)"},
    "pred_rul_real": {"fr": "✅ RUL réel", "en": "✅ Actual RUL"},
    "pred_rul_xgb": {"fr": "📊 RUL XGBoost", "en": "📊 XGBoost RUL"},
    "pred_error": {"fr": "{e:+.1f} d'erreur", "en": "{e:+.1f} error"},
    "pred_cycles": {"fr": "cycles", "en": "cycles"},
    "pred_maint_title": {"fr": "### 🚦 Recommandation de maintenance", "en": "### 🚦 Maintenance recommendation"},
    "pred_legend": {"fr": "ℹ️ Légende des seuils", "en": "ℹ️ Threshold legend"},
    "pred_chart_title": {"fr": "### 📈 Comparaison visuelle des prédictions", "en": "### 📈 Visual comparison of predictions"},
    "pred_sensors_title": {"fr": "### 📊 Évolution récente des capteurs (30 derniers cycles)", "en": "### 📊 Recent sensor evolution (last 30 cycles)"},
    "pred_sensors_caption": {
        "fr": "Ces signaux sont ceux utilisés par le LSTM pour faire sa prédiction.",
        "en": "These are the signals used by the LSTM to make its prediction."
    },

    # Statuts de maintenance
    "status_healthy": {"fr": "🟢 SAIN", "en": "🟢 HEALTHY"},
    "status_healthy_msg": {"fr": "Aucune action requise", "en": "No action required"},
    "status_watch": {"fr": "🟡 SURVEILLANCE", "en": "🟡 MONITORING"},
    "status_watch_msg": {"fr": "Planifier une inspection", "en": "Schedule an inspection"},
    "status_urgent": {"fr": "🔴 MAINTENANCE URGENTE", "en": "🔴 URGENT MAINTENANCE"},
    "status_urgent_msg": {"fr": "Intervention immédiate", "en": "Immediate intervention"},

    # ===== PAGE COMPARAISON =====
    "comp_title": {"fr": "📊 Comparaison des modèles", "en": "📊 Model comparison"},
    "comp_subtitle": {
        "fr": "Analyse comparative des 4 modèles construits selon l'approche **benchmark first**.",
        "en": "Comparative analysis of the 4 models built using the **benchmark first** approach."
    },
    "comp_table_title": {"fr": "### 🏆 Tableau récapitulatif", "en": "### 🏆 Summary table"},
    "comp_table_caption": {
        "fr": "💡 Les valeurs surlignées en vert sont les meilleures de chaque colonne (plus bas = meilleur).",
        "en": "💡 Green-highlighted values are the best in each column (lower = better)."
    },
    "comp_progress_title": {"fr": "### 📉 Progression des RMSE", "en": "### 📉 RMSE progression"},
    "comp_quality_title": {"fr": "### 🎯 Qualité des prédictions LSTM", "en": "### 🎯 LSTM prediction quality"},
    "comp_dist_title": {"fr": "### 📉 Distribution des erreurs", "en": "### 📉 Error distribution"},
    "comp_concl_title": {"fr": "### 💡 Conclusions", "en": "### 💡 Conclusions"},

    # ===== PAGE ANOMALIES =====
    "anom_title": {"fr": "🚨 Détection d'anomalies — Autoencoder", "en": "🚨 Anomaly Detection — Autoencoder"},
    "anom_subtitle": {
        "fr": """Détection **non supervisée** de la dégradation. L'autoencoder a été entraîné 
**uniquement sur des moteurs sains** : quand il échoue à reconstruire les capteurs, il détecte un comportement anormal.""",
        "en": """**Unsupervised** degradation detection. The autoencoder was trained 
**only on healthy engines**: when it fails to reconstruct the sensors, it detects abnormal behavior."""
    },
    "anom_how": {"fr": "ℹ️ Comment ça marche ?", "en": "ℹ️ How does it work?"},
    "anom_select": {"fr": "🎯 Choisissez un moteur", "en": "🎯 Choose an engine"},
    "anom_chart_title": {"fr": "### 📈 Score d'anomalie du moteur sélectionné", "en": "### 📈 Anomaly score of selected engine"},
    "anom_score_max": {"fr": "Score d'anomalie maximal", "en": "Maximum anomaly score"},
    "anom_score_mean": {"fr": "Score d'anomalie moyen", "en": "Average anomaly score"},
    "anom_multi_title": {"fr": "### 🔬 Comparaison de plusieurs moteurs", "en": "### 🔬 Multiple engine comparison"},
    "anom_multi_select": {"fr": "Choisissez des moteurs à comparer", "en": "Choose engines to compare"},
    "anom_interp_title": {"fr": "### 💡 Interprétation", "en": "### 💡 Interpretation"},
}


def init_language():
    """Initialise la langue dans la session (par défaut : anglais)."""
    if "lang" not in st.session_state:
        st.session_state.lang = "en"


def language_selector():
    """Affiche le sélecteur de langue dans la sidebar."""
    init_language()
    choix = st.sidebar.radio(
        TRANSLATIONS["lang_label"][st.session_state.lang],
        options=["en", "fr"],
        format_func=lambda x: "🇬🇧 English" if x == "en" else "🇫🇷 Français",
        index=0 if st.session_state.lang == "en" else 1,
        key="lang_radio",
    )
    st.session_state.lang = choix


def t(key, **kwargs):
    """
    Renvoie la traduction d'une clé dans la langue active.
    Accepte des paramètres de formatage : t('pred_info', n=42)
    """
    init_language()
    lang = st.session_state.lang
    texte = TRANSLATIONS.get(key, {}).get(lang, key)
    if kwargs:
        texte = texte.format(**kwargs)
    return texte