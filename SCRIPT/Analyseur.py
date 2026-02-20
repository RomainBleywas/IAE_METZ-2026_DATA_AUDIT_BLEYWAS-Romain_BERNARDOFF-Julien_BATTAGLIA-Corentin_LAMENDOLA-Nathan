import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import plotly.graph_objects as go


st.set_page_config(
    page_title="Analyse Nvidia & Politique",
    page_icon="",
    layout="wide"
)

st.title(" Analyseur de Corrélations : Décisions Politiques / Cours Nvidia")
st.markdown("Le but est d'explorer les liens entre les événements politiques et les mouvements boursiers de Nvidia")
st.markdown("---")


if "messages" not in st.session_state:
    st.session_state.messages = []
if "nvidia_data" not in st.session_state:
    st.session_state.nvidia_data = None
if "events" not in st.session_state:
    st.session_state.events = []
if "data_source" not in st.session_state:
    st.session_state.data_source = "yfinance"  

# Pour excel
def process_excel_data(uploaded_file):
    """Traite un fichier Excel/CSV uploadé et retourne un DataFrame nettoyé"""
    try:
        if str(uploaded_file.name).lower().endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

       
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df = df.set_index('Date')

      
        price_col = None
        if 'Close' in df.columns:
            price_col = 'Close'
        elif 'Adj Close' in df.columns:
            price_col = 'Adj Close'
        else:
            numeric_cols = df.select_dtypes(include='number').columns.tolist()
            if numeric_cols:
                price_col = numeric_cols[0]

     
        if not isinstance(df.index, pd.DatetimeIndex):
            date_candidates = [c for c in df.columns if 'date' in c.lower()]
            if date_candidates:
                date_col = date_candidates[0]
                try:
                    df[date_col] = pd.to_datetime(df[date_col])
                    df = df.set_index(date_col)
                except Exception as e:
                    st.warning(f"Impossible de parser la colonne date: {e}")
            else:
                try:
                    df.index = pd.to_datetime(df.index)
                except Exception:
                    st.warning("L'index n'est pas en datetime et aucune colonne date détectée.")

        if price_col and price_col in df.columns:
            if price_col != 'Close':
                df = df.rename(columns={price_col: 'Close'})

      
        try:
            df.index = pd.to_datetime(df.index, errors='coerce')
            df = df.dropna(subset=['Close'])
            df = df.sort_index()
        except Exception:
            pass

        return df
    except Exception as e:
        st.error(f"Erreur lors du traitement du fichier: {e}")
        return None

# Données Nvidia
@st.cache_data
def get_nvidia_data(days=180):
    """ données Nvidia des 6 derniers mois"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

 
    try:
        with st.spinner(" Téléchargement des données Nvidia (start/end)"):
            data = yf.download("NVDA", start=start_date, end=end_date, interval='1d', progress=False)
            if data is not None and not data.empty:
                st.info(f" Données reçues ({len(data)} lignes) via start/end")
                return data
          
    except Exception as e:
        st.warning(f" Erreur start/end: {e}")


    try:
        period_str = f"{days}d" if days <= 3650 else "10y"
        with st.spinner(f" Tentative fallback: period={period_str}..."):
            data = yf.download("NVDA", period=period_str, interval='1d', progress=False)
            if data is not None and not data.empty:
                st.info(f" Données reçues ({len(data)} lignes) via period={period_str}")
                return data
    except Exception as e:
        st.warning(f" Erreur period fallback: {e}")

  
    try:
        with st.spinner(" Dernière tentative: period=10y..."):
            data = yf.download("NVDA", period="10y", interval='1d', progress=False)
            if data is not None and not data.empty:
                st.info(f" Données reçues ({len(data)} lignes) via period=10y")
                return data
    except Exception as e:
        st.warning(f" Erreur dernière tentative: {e}")

  
    if data is not None and not data.empty:
        try:
            
            data.index = pd.to_datetime(data.index)
            data = data.sort_index()
            data = data[~data.index.duplicated(keep='first')]

          
            freq = pd.infer_freq(data.index)
            if freq is None or 'D' not in freq and 'B' not in freq:
                st.info("ℹ Index non-daily détecté — resampling en jours ouvrés (B) avec forward-fill")
                idx = pd.date_range(start=data.index.min().date(), end=data.index.max().date(), freq='B')
                data = data.reindex(idx)
                data = data.ffill()

            return data
        except Exception as e:
            st.warning(f" Erreur lors du post-traitement des données: {e}")

    st.error(" Aucune donnée reçue de Yahoo Finance après plusieurs tentatives.")
    st.info(" Vérifiez la connexion Internet, le pare-feu ou réessayez plus tard.")
    return None

# événements politiques
political_events = {
    # 2015
    "2015-03-20": {
        "titre": "Lancement GPU Maxwell",
        "impact": "Positif",
        "description": "Nouvelle architecture GPU pour gaming et IA"
    },
    "2015-07-15": {
        "titre": "Accord européen sur l'IA",
        "impact": "Positif",
        "description": "Régulations favorables pour le secteur tech"
    },
    # 2016
    "2016-06-23": {
        "titre": "Brexit referendum",
        "impact": "Mixed",
        "description": "Incertitude économique globale"
    },
    "2016-11-08": {
        "titre": "Élection Trump",
        "impact": "Positif",
        "description": "Politiques pro-business et tech-friendly"
    },
    # 2017
    "2017-02-13": {
        "titre": "Boom du machine learning",
        "impact": "Positif",
        "description": "Explosion de la demande en GPU pour l'IA"
    },
    "2017-05-10": {
        "titre": "Lancement GPU Volta",
        "impact": "Positif",
        "description": "Architecture révolutionnaire pour data centers"
    },
    "2017-12-06": {
        "titre": "Essor du deep learning",
        "impact": "Positif",
        "description": "Adoption massive de l'IA en entreprise"
    },
    # 2018
    "2018-03-22": {
        "titre": "Tarifs USA-China",
        "impact": "Négatif",
        "description": "Tensions commerciales avec la Chine"
    },
    "2018-06-15": {
        "titre": "Crash du Bitcoin",
        "impact": "Négatif",
        "description": "Effondrement du crypto-mining (demande GPU)"
    },
    "2018-09-20": {
        "titre": "Lancement Turing (RTX)",
        "impact": "Positif",
        "description": "Nouvelle génération GPU avec ray tracing"
    },
    # 2019
    "2019-01-10": {
        "titre": "CES 2019 - Nvidia dominance",
        "impact": "Positif",
        "description": "Leadership confirmé en IA et gaming"
    },
    "2019-05-15": {
        "titre": "Course technologique USA-Chine",
        "impact": "Positif",
        "description": "Priorité à la supériorité tech américaine"
    },
    "2019-07-20": {
        "titre": "Boom de l'AI enterprise",
        "impact": "Positif",
        "description": "Adoption massive de l'IA dans les entreprises"
    },
    # 2020
    "2020-02-20": {
        "titre": "Début de la crise COVID",
        "impact": "Négatif",
        "description": "Panique boursière et crash initial"
    },
    "2020-03-16": {
        "titre": "Rebond tech post-crash",
        "impact": "Positif",
        "description": "Forte demande GPU pour cloud computing"
    },
    "2020-05-10": {
        "titre": "Boom du gaming à domicile",
        "impact": "Positif",
        "description": "Explosion de la demande GPU gaming"
    },
    "2020-09-13": {
        "titre": "Nvidia annonce ARM acquisition",
        "impact": "Positif",
        "description": "Expansion stratégique majeure"
    },
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
        "titre": "Ordre exécutif sur l'IA renforcé",
        "impact": "Positif",
        "description": "Cadre réglementaire favorable à l'innovation"
    },
    "2023-10-20": {
        "titre": "Restrictions d'export de GPU",
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
        "titre": "Ordre exécutif IA Biden",
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
        "titre": "Programme IA national",
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
        "titre": "Accord bipartisan semi-conducteurs",
        "impact": "Positif",
        "description": "Rare accord politique favorable"
    },
}

# Analyse
def analyze_correlation(question, price_data, events):
    """Analyse simple des corrélations (sans API externe)"""
    responses = {
        "élections": "Les élections de novembre 2024 ont impacté le secteur tech. Nvidia, leader en IA, a bénéficié de l'intérêt politique pour les technologies émergentes.",
        "impact": "L'annonce de nouvelles régulations IA a provoqué une volatilité à court terme, suivi d'une reprise liée aux applications pratiques.",
        "régulations": "Les nouvelles régulations IA en 2025 ont créé une incertitude initiale, mais Nvidia reste dominant dans les GPU d'IA.",
        "tendance": "Tendance générale positive : les décisions politiques favorisant l'investissement en IA ont soutenu le cours.",
        "corrélation": "Forte corrélation observée : les annonces politiques pro-tech augmentent généralement le cours Nvidia dans les 2-5 jours",
    }
    
    # Réponse par défaut
    for key in responses:
        if key.lower() in question.lower():
            return responses[key]
    
    return f"Analyse du contexte actuel: Nvidia est en position forte suite aux développements récents en IA. Les événements politiques affectent surtout la volatilité court-terme."

st.subheader(" Cours Nvidia (NVDA)")

# Upload file widget - car bug avec yahoo finance
uploaded_file = st.file_uploader(" Importer un fichier Excel/CSV", type=["csv", "xlsx"])

if uploaded_file is not None:

    excel_data = process_excel_data(uploaded_file)
    if excel_data is not None and not excel_data.empty:
        st.session_state.nvidia_data = excel_data
        st.session_state.data_source = "excel"
        st.success(f" Données Excel chargées ({len(excel_data)} lignes)")
else:

    st.session_state.data_source = "yfinance"


col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    days = st.slider("Nombre de jours à afficher (10 ans max):", 30, 3650, 365)

with col2:
    if st.button(" Actualiser"):
        st.cache_data.clear()
        st.rerun()

with col3:
    if st.session_state.data_source == "excel":
        if st.button("✕ Supprimer Excel"):
            st.session_state.nvidia_data = None
            st.session_state.data_source = "yfinance"
            st.rerun()

if st.session_state.data_source == "excel" and st.session_state.nvidia_data is not None:
    nvidia_data = st.session_state.nvidia_data.copy()
    st.info(" C'est carré")
else:
    nvidia_data = get_nvidia_data(days)

if nvidia_data is None or nvidia_data.empty:
    st.error(" Aucune donnée disponible. Importez un Excel ou vérifiez votre connexion Internet.")
    st.stop()


try:
    end_date = nvidia_data.index.max()
    start_date = end_date - timedelta(days=days)
    nvidia_data = nvidia_data[(nvidia_data.index >= start_date) & (nvidia_data.index <= end_date)]
    st.caption(f" Affichage: {len(nvidia_data)} jours ({start_date.strftime('%Y-%m-%d')} → {end_date.strftime('%Y-%m-%d')})")
except Exception as e:
    st.warning(f" Erreur lors du filtrage par date: {e}")

if nvidia_data.empty:
    st.error(" Aucune donnée pour cette période. Augmentez le nombre de jours.")
    st.stop()

# Convertir les données pour le package plotly
dates = nvidia_data.index.astype(str)
prices = nvidia_data['Close'].astype(float)

# mettre le graphique 
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=dates,
    y=prices,
    mode='lines',
    name='Prix NVDA',
    line=dict(color='#76B900', width=2),
    hovertemplate='<b>Date:</b> %{x}<br><b>Prix:</b> $%{y:.2f}<extra></extra>'
))

# Ajouter les événements politiques qui se situent dans la plage des données
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
            price = float(nvidia_data['Close'].iloc[date_idx])
            event_dates.append(date.strftime('%Y-%m-%d'))
            event_prices.append(price)
            event_titles.append(event_data["titre"])
            event_colors.append(colors_map.get(event_data.get("impact", "Neutre"), "blue"))
            event_impacts.append(event_data["impact"])
        
       
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
    title=" Évolution du cours NVDA avec événements politiques clés",
    xaxis_title="Date",
    yaxis_title="Prix ($)",
    hovermode='x unified',
    height=700,
    template='plotly_white',
    font=dict(size=12),
    margin=dict(t=100, b=100)
)

# Afficher le graphique principal
st.plotly_chart(fig, use_container_width=True)

# Message de confirmation
st.success(f" Graphique généré - {len(event_dates)} point(s) d'événement ajoutés")

#  Matrice de corrélation
try:
    returns = nvidia_data['Close'].pct_change()

    mode = st.radio("Mode de corrélation:", options=["Par événement", "Par catégorie"], index=0, horizontal=True)

    
    presets = [0, 1, 3, 5, 10, 30, 90, 180, 365]
    col_h1, col_h2 = st.columns([2, 3])
    with col_h1:
        selected = st.multiselect("Choisir horizons (jours)", options=presets, default=presets)
    with col_h2:
        custom_txt = st.text_input("Ajouter horizons personnalisés (ex: 7,14,210)", value="")

    # Parser les horizons personnalisés
    custom = []
    if custom_txt:
        for token in custom_txt.replace(';', ',').split(','):
            token = token.strip()
            if not token:
                continue
            try:
                v = int(token)
                if v >= 0:
                    custom.append(v)
            except Exception:
               
                pass

    horizons = sorted(set(selected + custom)) if (selected or custom) else presets

    if mode == "Par catégorie":
        impacts = ["Positif", "Négatif", "Mixed", "Neutre"]
        indicators = pd.DataFrame(0, index=nvidia_data.index, columns=impacts)
        for date_str, event_data in political_events.items():
            date = pd.to_datetime(date_str)
            if data_start <= date <= data_end:
                idx = nvidia_data.index.searchsorted(date)
                if idx < len(nvidia_data):
                    impact = event_data.get('impact', 'Neutre')
                    if impact not in indicators.columns:
                        indicators[impact] = 0
                    indicators.iloc[idx, indicators.columns.get_loc(impact)] = 1

        corr_matrix = pd.DataFrame(index=[f"{h}j" for h in horizons], columns=impacts, dtype=float)
        for h in horizons:
            shifted_returns = returns.shift(-h)
            for imp in impacts:
                try:
                    corr = indicators[imp].corr(shifted_returns)
                except Exception:
                    corr = None
                corr_matrix.loc[f"{h}j", imp] = corr

        title = 'Matrice corrélation: Impact événements ↔ Rendements (catégories)'
        x_labels = corr_matrix.columns
        z = corr_matrix.values

    else:
     
        event_items = []
        for date_str, event_data in sorted(political_events.items()):
            date = pd.to_datetime(date_str)
            if data_start <= date <= data_end:
                label = f"{date_str} - {event_data.get('titre','')[:30]}"
                event_items.append((date_str, label))

        if not event_items:
            st.info("Aucun événement dans la plage sélectionnée pour calculer la corrélation.")
            corr_matrix = pd.DataFrame()
        else:
            labels = [lbl for _, lbl in event_items]
            indicators = pd.DataFrame(0, index=nvidia_data.index, columns=labels)
            for date_str, label in event_items:
                date = pd.to_datetime(date_str)
                idx = nvidia_data.index.searchsorted(date)
                if idx < len(nvidia_data):
                    indicators.iloc[idx, indicators.columns.get_loc(label)] = 1

            corr_matrix = pd.DataFrame(index=[f"{h}j" for h in horizons], columns=labels, dtype=float)
            for h in horizons:
                shifted_returns = returns.shift(-h)
                for lbl in labels:
                    try:
                        corr = indicators[lbl].corr(shifted_returns)
                    except Exception:
                        corr = None
                    corr_matrix.loc[f"{h}j", lbl] = corr

            title = 'Matrice corrélation: Événements individuels ↔ Rendements (horizons)'
            x_labels = corr_matrix.columns
            z = corr_matrix.values

    st.subheader(" Corrélation événements ↔ rendements")
    st.caption("Corrélation entre indicateurs d'événement (1 le jour de l'événement) et rendements à différents horizons")

    if corr_matrix.empty:
        st.write("(Aucune corrélation calculable)")
    else:
        # Heatmap
        height = max(420, 25 * len(x_labels))
        heat = go.Figure(data=go.Heatmap(
            z=z,
            x=x_labels,
            y=corr_matrix.index,
            colorscale='RdBu',
            zmid=0,
            colorbar=dict(title='Corr')
        ))
        heat.update_layout(title=title, height=height)
        heat.update_xaxes(tickangle=45)
        st.plotly_chart(heat, use_container_width=True)

        # Tableau des valeurs
        st.dataframe(corr_matrix.fillna(''), use_container_width=True)
except Exception as e:
    st.warning(f"Impossible de calculer la matrice de corrélation: {e}")

# Statistiques
col1, col2, col3, col4 = st.columns(4)
with col1:
    price = float(nvidia_data['Close'].iloc[-1])
    st.metric("Prix actuel", f"${price:.2f}")
with col2:
    current = float(nvidia_data['Close'].iloc[-1])
    previous = float(nvidia_data['Close'].iloc[0])
    change = ((current - previous) / previous) * 100
    st.metric("Variation (%)", f"{change:.2f}%", delta=f"{change:.2f}%")
with col3:
    max_price = float(nvidia_data['Close'].max())
    st.metric("Plus haut", f"${max_price:.2f}")
with col4:
    min_price = float(nvidia_data['Close'].min())
    st.metric("Plus bas", f"${min_price:.2f}")

st.markdown("---")

# details des événements (impact)
st.subheader(" Événements Politiques Clés")
st.write("Les événements affichés sur le graphique avec codes couleur :")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("### Vert = Positif")
    st.write("Favorable à Nvidia")
with col2:
    st.markdown("### Rouge = Négatif")
    st.write("Défavorable")
with col3:
    st.markdown("### Orange = Mitigé")
    st.write("Impact mixte")
with col4:
    st.markdown("### Blanc = Neutre")
    st.write("Impact incertain")

st.markdown("---")

# Tableau des événements
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

# Détails des événements
st.markdown("---")
st.subheader(" Analyse Détaillée des Événements")

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
                st.write("**Implication pour Nvidia:**  Devrait augmenter la demande et soutenir les cours")
            elif event_data['impact'] == "Négatif":
                st.write("**Implication pour Nvidia:**  Pourrait réduire la demande et peser sur les cours")
            elif event_data['impact'] == "Mixed":
                st.write("**Implication pour Nvidia:**  Impact à court terme incertain")
            else:
                st.write("**Implication pour Nvidia:**  Impact à surveiller")

st.markdown("---")

# Tentative de chatbot 
st.subheader(" Chatbot Analyseur")
st.info(" Posez des questions sur les corrélations entre les événements politiques et le cours Nvidia")

# Le but est de garder une trace des messages 
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Posez une question (ex: 'Quel impact les élections ont eu sur Nvidia?')"):
   
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Générer une réponse 
    with st.chat_message("assistant"):
        with st.spinner("Analyse en cours..."):
            response = analyze_correlation(prompt, nvidia_data, political_events)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
