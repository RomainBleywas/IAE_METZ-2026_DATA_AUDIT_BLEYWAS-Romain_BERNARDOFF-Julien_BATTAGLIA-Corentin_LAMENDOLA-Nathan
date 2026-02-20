#!/usr/bin/env python3
"""Version avec DONNÉES MOCK - pas besoin de yfinance"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

st.set_page_config(page_title="Analyst Nvidia (Mock Data)", layout="wide")

st.title("📊 Analyseur Nvidia - Version Données de Test")
st.markdown("Cette version utilise des données de test pour éviter les problèmes Yahoo Finance")
st.markdown("---")

# Générer des données de test réalistes
@st.cache_data
def generate_mock_nvidia_data(days=1825):
    """Génère 5 ans de données Nvidia réalistes pour les tests"""
    dates = [datetime.now() - timedelta(days=x) for x in reversed(range(days))]
    
    # Simuler une tendance à la hausse avec volatilité
    np.random.seed(42)
    prices = 100 + np.cumsum(np.random.normal(0.5, 2, days))
    
    return pd.DataFrame({
        'Date': dates,
        'Close': prices
    }).set_index('Date')

# Événements politiques importants pour Nvidia et l'IA (5 ans)
political_events = {
    # 2021
    "2021-03-15": {
        "titre": "Biden signe le CHIPS Act",
        "impact": "Positif",
        "description": "Investissement fédéral en semi-conducteurs"
    },
    "2021-06-10": {
        "titre": "Restrictions d'export vers la Chine",
        "impact": "Négatif",
        "description": "Nouvelles restrictions sur les ventes à la Chine"
    },
    # 2022
    "2022-04-20": {
        "titre": "Auditions au Congrès sur l'IA",
        "impact": "Mixed",
        "description": "Débats sur la régulation de l'IA"
    },
    "2022-08-09": {
        "titre": "Inflation Reduction Act signé",
        "impact": "Positif",
        "description": "Subventions pour la fabrication de semi-conducteurs"
    },
    # 2023
    "2023-02-01": {
        "titre": "Sommet du G7 sur l'IA",
        "impact": "Positif",
        "description": "Accord mondial sur les régulations IA"
    },
    "2023-06-15": {
        "titre": "Ordre exécutif sur l'IA d'Obama renforcé",
        "impact": "Positif",
        "description": "Cadre réglementaire favorable à l'innovation"
    },
    "2023-10-20": {
        "titre": "Nouvelles restrictions d'export annoncées",
        "impact": "Négatif",
        "description": "Limitations sur les GPU avancés vers la Chine"
    },
    # 2024
    "2024-01-25": {
        "titre": "Audience Trump sur les régulations tech",
        "impact": "Positif",
        "description": "Politiques tech favorables aux grandes entreprises"
    },
    "2024-04-15": {
        "titre": "Biden signe l'ordre exécutif IA",
        "impact": "Positif",
        "description": "Investissements massifs en infrastructure IA"
    },
    "2024-06-18": {
        "titre": "Débat Biden-Trump",
        "impact": "Mixed",
        "description": "Discussion sur l'IA et l'industrie tech"
    },
    "2024-11-05": {
        "titre": "Élections présidentielles",
        "impact": "Neutre",
        "description": "Résultats électoraux - Impact politique"
    },
    "2024-12-10": {
        "titre": "CHIPS Act II approuvé",
        "impact": "Positif",
        "description": "Subventions supplémentaires pour les puces"
    },
    # 2025
    "2025-01-20": {
        "titre": "Inauguration Trump",
        "impact": "Positif",
        "description": "Nouvelles directions politiques"
    },
    "2025-01-30": {
        "titre": "Investissement fédéral semi-conducteurs",
        "impact": "Positif",
        "description": "Poussée majeure pour la production nationale"
    },
    "2025-02-04": {
        "titre": "Régulations IA favorables",
        "impact": "Positif",
        "description": "Cadre réglementaire favorable à l'innovation"
    },
    "2025-06-15": {
        "titre": "Sommet international IA",
        "impact": "Positif",
        "description": "Accord sur la leadership technologique américaine"
    },
    "2025-09-10": {
        "titre": "Lancement du programme IA national",
        "impact": "Positif",
        "description": "Initiative majeure de soutien à l'IA"
    },
    # 2026
    "2026-01-05": {
        "titre": "Annonce d'investissements en IA",
        "impact": "Positif",
        "description": "Engagement politique pour la leadership en IA"
    },
    "2026-02-08": {
        "titre": "Accord bipartisan sur les semi-conducteurs",
        "impact": "Positif",
        "description": "Rare accord politique favorable"
    },
}

# Section 1: Affichage
st.subheader("📈 Cours Nvidia (DONNÉES DE TEST)")

col1, col2 = st.columns([3, 1])
with col1:
    days = st.slider("Nombre de jours à afficher:", 30, 1825, 365)
with col2:
    if st.button("🔄 Régénérer"):
        st.cache_data.clear()
        st.rerun()

# Générer les données
nvidia_data = generate_mock_nvidia_data(days)

st.success(f"✅ {len(nvidia_data)} jours de données générées")

# Créer le graphique
fig = go.Figure()

dates_str = [d.strftime('%Y-%m-%d') for d in nvidia_data.index]
prices = nvidia_data['Close'].values.astype(float)

fig.add_trace(go.Scatter(
    x=dates_str,
    y=prices,
    mode='lines',
    name='Prix NVDA',
    line=dict(color='#76B900', width=2)
))

# Ajouter les événements
data_start = nvidia_data.index.min()
data_end = nvidia_data.index.max()

colors_map = {
    "Positif": "green",
    "Négatif": "red",
    "Mixed": "orange",
    "Neutre": "gray"
}

# Listes pour les points des événements
event_dates = []
event_prices = []
event_titles = []
event_colors = []
event_impacts = []

for date_str, event_data in political_events.items():
    date = pd.to_datetime(date_str)
    if data_start <= date <= data_end:
        # Trouver le prix le plus proche de cette date
        date_idx = nvidia_data.index.searchsorted(date)
        if date_idx < len(nvidia_data):
            price = nvidia_data['Close'].iloc[date_idx]
            event_dates.append(date.strftime('%Y-%m-%d'))
            event_prices.append(price)
            event_titles.append(event_data["titre"])
            event_colors.append(colors_map.get(event_data.get("impact", "Neutre"), "blue"))
            event_impacts.append(event_data["impact"])
        
        # Ajouter aussi la ligne verticale
        color = colors_map.get(event_data.get("impact", "Neutre"), "blue")
        fig.add_vline(
            x=date.strftime('%Y-%m-%d'),
            line_dash="dash",
            line_color=color,
            line_width=1,
            opacity=0.5
        )

# Ajouter les points des événements sur le graphique
if event_dates:
    fig.add_trace(go.Scatter(
        x=event_dates,
        y=event_prices,
        mode='markers',
        name='Événements politiques',
        marker=dict(
            size=12,
            color=event_colors,
            line=dict(width=2, color='white'),
            symbol='diamond'
        ),
        text=[f"<b>{title}</b><br>({impact})<br>Prix: ${price:.2f}" 
              for title, impact, price in zip(event_titles, event_impacts, event_prices)],
        hovertemplate='%{text}<extra></extra>'
    ))

fig.update_layout(
    title="Cours Nvidia avec Événements Politiques",
    xaxis_title="Date",
    yaxis_title="Prix ($)",
    height=700,
    template='plotly_white',
    hovermode='x unified',
    margin=dict(t=100, b=100)
)

st.plotly_chart(fig, use_container_width=True)

st.success(f"✅ Graphique affiché avec {len(event_dates)} points d'événements marqués sur la courbe")

st.markdown("---")

# Section 2: Événements détaillés
st.subheader("🏛️ Événements Politiques Clés")
st.write("Les événements affichés sur le graphique en couleur :")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("### 🟢 Positif")
    st.write("Favorable à Nvidia")
with col2:
    st.markdown("### 🔴 Négatif")
    st.write("Défavorable")
with col3:
    st.markdown("### 🟠 Mixed")
    st.write("Impact mixte")
with col4:
    st.markdown("### ⚪ Neutre")
    st.write("Impact incertain")

st.markdown("---")

# Tableau détaillé
events_list = []
for date_str, event_data in sorted(political_events.items(), reverse=True):
    events_list.append({
        "Date": date_str,
        "Titre": event_data["titre"],
        "Impact": event_data["impact"],
        "Description": event_data["description"]
    })

events_df = pd.DataFrame(events_list)
st.dataframe(events_df, use_container_width=True, hide_index=True)

# Affichage détaillé
st.markdown("---")
st.subheader("📋 Détails des Événements")

for date_str, event_data in sorted(political_events.items(), reverse=True):
    date = pd.to_datetime(date_str)
    if data_start <= date <= data_end:
        impact_emoji = {
            "Positif": "🟢",
            "Négatif": "🔴",
            "Mixed": "🟠",
            "Neutre": "⚪"
        }.get(event_data.get("impact", "Neutre"), "❓")
        
        with st.expander(f"{impact_emoji} {date_str} - {event_data['titre']}"):
            st.write(f"**Impact:** {event_data['impact']}")
            st.write(f"**Description:** {event_data['description']}")
            
            if event_data['impact'] == "Positif":
                st.write("**Implication pour Nvidia:** ✅ Devrait augmenter la demande et les cours")
            elif event_data['impact'] == "Négatif":
                st.write("**Implication pour Nvidia:** ❌ Pourrait réduire la demande et les cours")
            elif event_data['impact'] == "Mixed":
                st.write("**Implication pour Nvidia:** ⚠️ Impact à court terme incertain")
            else:
                st.write("**Implication pour Nvidia:** ❓ Impact à surveiller")

st.markdown("---")

# Section 3: Chatbot
st.subheader("🤖 Chatbot Analyseur")
st.info("Posez une question sur les corrélations entre événements politiques et le cours Nvidia")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Votre question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    response = "Basé sur les données de test: Nvidia montre une tendance à la hausse avec volatilité autour des événements politiques clés."
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

st.markdown("---")
st.info("💡 Cette version utilise des DONNÉES FICTIVES pour tester l'interface. Utilisez `streamlit_app.py` pour les vraies données Yahoo Finance.")
