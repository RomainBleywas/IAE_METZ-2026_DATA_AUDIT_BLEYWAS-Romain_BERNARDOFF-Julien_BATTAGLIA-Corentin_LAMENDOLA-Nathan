#!/usr/bin/env python3
"""Version DEBUG pour diagnostiquer les points des événements"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

st.set_page_config(page_title="DEBUG - Points Événements", layout="wide")

st.title("🐛 DEBUG - Points des Événements")

# Générer les données
@st.cache_data
def generate_mock_data(days=1825):
    dates = [datetime.now() - timedelta(days=x) for x in reversed(range(days))]
    np.random.seed(42)
    prices = 100 + np.cumsum(np.random.normal(0.5, 2, days))
    return pd.DataFrame({
        'Date': dates,
        'Close': prices
    }).set_index('Date')

# Événements
political_events = {
    "2021-03-15": {"titre": "CHIPS Act", "impact": "Positif"},
    "2024-01-25": {"titre": "Audience Trump", "impact": "Positif"},
    "2024-11-05": {"titre": "Élections", "impact": "Neutre"},
    "2025-01-20": {"titre": "Inauguration", "impact": "Positif"},
    "2025-02-04": {"titre": "Régulations IA", "impact": "Positif"},
    "2026-02-08": {"titre": "Accord bipartisan", "impact": "Positif"},
}

days = st.slider("Jours:", 30, 1825, 365)
nvidia_data = generate_mock_data(days)

st.write(f"**Plage de données:**")
st.write(f"  - Début: {nvidia_data.index.min().date()}")
st.write(f"  - Fin: {nvidia_data.index.max().date()}")
st.write(f"  - Nombre de jours: {len(nvidia_data)}")

# Diagnostic des événements
st.subheader("🔍 Diagnostic des Événements")

data_start = nvidia_data.index.min()
data_end = nvidia_data.index.max()

colors_map = {
    "Positif": "green",
    "Négatif": "red",
    "Mixed": "orange",
    "Neutre": "gray"
}

event_dates = []
event_prices = []
event_titles = []
event_colors = []

st.write("Vérification de chaque événement:")

for date_str, event_data in political_events.items():
    date = pd.to_datetime(date_str)
    st.write(f"\n📅 {date_str} - {event_data['titre']}")
    st.write(f"   Date Python: {date}")
    st.write(f"   Dans la plage? {data_start <= date <= data_end}")
    
    if data_start <= date <= data_end:
        st.write(f"   ✅ OUI, dans la plage!")
        
        # Chercher l'index
        date_idx = nvidia_data.index.searchsorted(date)
        st.write(f"   Index trouvé: {date_idx}")
        st.write(f"   Nombre total d'indices: {len(nvidia_data)}")
        
        if date_idx < len(nvidia_data):
            price = float(nvidia_data['Close'].iloc[date_idx])
            st.write(f"   ✅ Prix trouvé: ${price:.2f}")
            
            event_dates.append(date.strftime('%Y-%m-%d'))
            event_prices.append(price)
            event_titles.append(event_data["titre"])
            event_colors.append(colors_map.get(event_data.get("impact", "Neutre"), "blue"))
        else:
            st.write(f"   ❌ Index {date_idx} hors limites!")
    else:
        st.write(f"   ❌ NON, hors de la plage")

st.markdown("---")
st.subheader("📊 Créer le Graphique")

st.write(f"Nombre de points à afficher: {len(event_dates)}")

fig = go.Figure()

# Courbe principale
dates_str = [d.strftime('%Y-%m-%d') for d in nvidia_data.index]
prices = nvidia_data['Close'].values.astype(float)

fig.add_trace(go.Scatter(
    x=dates_str,
    y=prices,
    mode='lines',
    name='Prix NVDA',
    line=dict(color='#76B900', width=2)
))

st.write(f"Courbe ajoutée avec {len(prices)} points")

# Ajouter les points des événements
if event_dates:
    st.write(f"Ajout des {len(event_dates)} points d'événements...")
    
    fig.add_trace(go.Scatter(
        x=event_dates,
        y=event_prices,
        mode='markers',
        name='Événements',
        marker=dict(
            size=15,
            color=event_colors,
            line=dict(width=3, color='white'),
            symbol='diamond'
        ),
        text=event_titles,
        hovertemplate='<b>%{text}</b><br>Prix: $%{y:.2f}<extra></extra>'
    ))
    
    st.success(f"✅ {len(event_dates)} points ajoutés!")
else:
    st.error("❌ Aucun point à afficher!")

fig.update_layout(
    title="Test Graphique avec Points",
    height=600,
    template='plotly_white'
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
if event_dates:
    st.success("✅ Les points DEVRAIENT être visibles")
else:
    st.error("❌ Aucun point - Vérifiez les dates des événements")
