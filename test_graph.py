#!/usr/bin/env python3
"""Version simplifiée sans cache pour tester le graphique"""

import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go

st.set_page_config(page_title="Test Graphique Nvidia", layout="wide")

st.title("🧪 Test du Graphique Nvidia")
st.write("Cette version simplifiée teste le téléchargement et l'affichage du graphique")

# Section 1: Informations de debug
st.subheader("📊 Étape 1: Téléchargement des données")

try:
    with st.spinner("⏳ Téléchargement en cours..."):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)
        
        st.write(f"Date début: {start_date.date()}")
        st.write(f"Date fin: {end_date.date()}")
        
        nvidia_data = yf.download("NVDA", start=start_date, end=end_date, progress=False)
        
    st.success("✅ Données téléchargées avec succès!")
    st.write(f"Nombre de lignes: {len(nvidia_data)}")
    st.write(f"Colonnes: {list(nvidia_data.columns)}")
    st.write("Aperçu des données:")
    st.dataframe(nvidia_data.head())
    
except Exception as e:
    st.error(f"❌ Erreur lors du téléchargement: {e}")
    st.stop()

# Section 2: Création du graphique
st.subheader("📈 Étape 2: Création du graphique")

try:
    # Convertir les données pour plotly
    dates = nvidia_data.index.astype(str)  # Convertir les dates en string
    prices = nvidia_data['Close'].astype(float)  # Convertir les prix en float
    
    st.write("Données converties:")
    st.write(f"  - Type dates: {type(dates[0])}")
    st.write(f"  - Type prix: {type(prices.iloc[0])}")
    
    fig = go.Figure()
    
    # Ajouter la courbe
    fig.add_trace(go.Scatter(
        x=dates,
        y=prices,
        mode='lines',
        name='Prix NVDA',
        line=dict(color='#76B900', width=2)
    ))
    
    # Mettre à jour la disposition
    fig.update_layout(
        title="Cours Nvidia (90 jours)",
        xaxis_title="Date",
        yaxis_title="Prix ($)",
        height=500,
        template='plotly_white'
    )
    
    st.write("✅ Graphique créé avec succès!")
    st.write("Les données du graphique:")
    st.write(f"  - Nombre de points: {len(nvidia_data)}")
    st.write(f"  - Prix min: ${float(nvidia_data['Close'].min()):.2f}")
    st.write(f"  - Prix max: ${float(nvidia_data['Close'].max()):.2f}")
    st.write(f"  - Prix actuel: ${float(nvidia_data['Close'].iloc[-1]):.2f}")
    
except Exception as e:
    st.error(f"❌ Erreur lors de la création du graphique: {e}")
    import traceback
    st.error(traceback.format_exc())
    st.stop()

# Section 3: Affichage
st.subheader("📊 Étape 3: Affichage du graphique")

try:
    st.plotly_chart(fig, use_container_width=True)
    st.success("✅ Graphique affiché avec succès!")
except Exception as e:
    st.error(f"❌ Erreur lors de l'affichage: {e}")

st.markdown("---")
st.info("Si vous voyez ce message until ici sans erreur ET le graphique ci-dessus, tout fonctionne! 🎉")
