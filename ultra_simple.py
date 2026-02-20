#!/usr/bin/env python3
"""Version ULTRA SIMPLE pour tester plotly dans Streamlit"""

import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Test Plotly Ultra Simple", layout="wide")

st.title("🧪 Test Ultra Simple de Plotly")

st.write("Étape 1: Créer un graphique basique")

# Graphique basique sans données yfinance
x_data = ['Jan', 'Fév', 'Mar', 'Avr', 'Mai']
y_data = [100, 150, 120, 180, 200]

fig = go.Figure()
fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines', name='Test'))
fig.update_layout(title="Graphique de Test Simple", height=400)

st.write("Étape 2: Afficher le graphique")

st.plotly_chart(fig, use_container_width=True)

st.success("✅ Si vous voyez un graphique ci-dessus, Plotly fonctionne!")
st.info("Si vous ne voyez rien, il y a un problème avec Plotly ou Streamlit.")

st.write("---")
st.write("Maintenant on va essayer avec yfinance...")

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

try:
    st.write("Téléchargement des données...")
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    nvidia = yf.download("NVDA", start=start_date, end=end_date, progress=False)
    
    st.write(f"✅ {len(nvidia)} données téléchargées")
    
    # Créer le graphique avec les vraies données
    fig2 = go.Figure()
    
    dates_str = [d.strftime('%Y-%m-%d') for d in nvidia.index]
    prices = nvidia['Close'].values.astype(float)
    
    fig2.add_trace(go.Scatter(
        x=dates_str,
        y=prices,
        mode='lines',
        name='NVDA',
        line=dict(color='green', width=2)
    ))
    
    fig2.update_layout(
        title="Cours Nvidia (30 jours)",
        xaxis_title="Date",
        yaxis_title="Prix ($)",
        height=500
    )
    
    st.write("Affichage du graphique Nvidia...")
    st.plotly_chart(fig2, use_container_width=True)
    st.success("✅ Graphique Nvidia affiché!")
    
except Exception as e:
    st.error(f"Erreur: {e}")
    import traceback
    st.error(traceback.format_exc())
