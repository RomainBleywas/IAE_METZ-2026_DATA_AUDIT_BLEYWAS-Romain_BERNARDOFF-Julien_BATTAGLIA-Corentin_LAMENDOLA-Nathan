#!/usr/bin/env python3
"""Version DEBUG de streamlit_app.py pour diagnostiquer le problème"""

import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go

st.set_page_config(page_title="DEBUG - Analyse Nvidia", layout="wide")

st.title("🐛 VERSION DEBUG - Analyseur Nvidia")
st.write("Cette version affiche les étapes pour identifier le problème")

# ===== ÉTAPE 1: PARAMÈTRES =====
st.subheader("Étape 1️⃣: Configuration")
st.write(f"Date actuelle: {datetime.now()}")

# ===== ÉTAPE 2: TÉLÉCHARGER LES DONNÉES =====
st.subheader("Étape 2️⃣: Téléchargement des données")

days = st.slider("Jours:", 30, 365, 90)
st.write(f"Nombre de jours sélectionnés: {days}")

try:
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    st.write(f"Plage: {start_date.date()} à {end_date.date()}")
    
    with st.spinner("⏳ Téléchargement..."):
        nvidia_data = yf.download("NVDA", start=start_date, end=end_date, progress=False)
    
    st.success("✅ Données téléchargées!")
    st.write(f"Nombre de lignes: {len(nvidia_data)}")
    st.write(f"Colonnes: {list(nvidia_data.columns)}")
    
    if nvidia_data.empty:
        st.error("❌ Les données sont vides!")
        st.stop()
    
    st.write("Aperçu des données:")
    st.dataframe(nvidia_data.head())
    
except Exception as e:
    st.error(f"❌ Erreur au téléchargement: {e}")
    import traceback
    st.error(traceback.format_exc())
    st.stop()

# ===== ÉTAPE 3: PRÉPARER LES DONNÉES =====
st.subheader("Étape 3️⃣: Préparation des données")

try:
    dates_str = [d.strftime('%Y-%m-%d') for d in nvidia_data.index]
    prices_float = nvidia_data['Close'].astype(float).values
    
    st.write(f"Nombre de dates: {len(dates_str)}")
    st.write(f"Nombre de prix: {len(prices_float)}")
    st.write(f"Type dates: {type(dates_str[0])}")
    st.write(f"Type prix: {type(prices_float[0])}")
    st.write(f"Prix min: {prices_float.min():.2f}")
    st.write(f"Prix max: {prices_float.max():.2f}")
    
    st.success("✅ Données préparées!")
    
except Exception as e:
    st.error(f"❌ Erreur de préparation: {e}")
    import traceback
    st.error(traceback.format_exc())
    st.stop()

# ===== ÉTAPE 4: CRÉER LE GRAPHIQUE =====
st.subheader("Étape 4️⃣: Création du graphique")

try:
    fig = go.Figure()
    
    st.write("Ajout de la courbe...")
    fig.add_trace(go.Scatter(
        x=dates_str,
        y=prices_float,
        mode='lines',
        name='NVDA',
        line=dict(color='#76B900', width=2)
    ))
    
    st.write("Mise à jour du layout...")
    fig.update_layout(
        title="Cours Nvidia",
        xaxis_title="Date",
        yaxis_title="Prix ($)",
        height=500,
        template='plotly_white'
    )
    
    st.success("✅ Graphique créé!")
    
except Exception as e:
    st.error(f"❌ Erreur de création: {e}")
    import traceback
    st.error(traceback.format_exc())
    st.stop()

# ===== ÉTAPE 5: AFFICHER LE GRAPHIQUE =====
st.subheader("Étape 5️⃣: Affichage du graphique")

st.write("MOMENT CRITIQUE: Affichage du graphique...")

try:
    st.plotly_chart(fig, use_container_width=True)
    st.success("✅ GRAPHIQUE AFFICHÉ AVEC SUCCÈS!")
except Exception as e:
    st.error(f"❌ Erreur d'affichage: {e}")
    import traceback
    st.error(traceback.format_exc())

st.markdown("---")
st.info("Si vous voyez le graphique ci-dessus ✅, tout fonctionne!")
