# 🚀 Guide Rapide - Excel comme Source Principale

## Démarrage

```bash
cd /workspaces/IAE_METZ-2026_DATA_AUDIT
streamlit run streamlit_app.py
```

L'app s'ouvrira par défaut sur `http://localhost:8501`

## 📊 Utiliser votre fichier Excel

### Étape 1️⃣ - Importer le fichier
- En haut de la page, cliquez sur **"📁 Importer un fichier Excel/CSV"**
- Sélectionnez votre fichier (ex: `NVDA PRICE.xlsx`)
- ✅ Message: "✅ Données Excel chargées (X lignes)"

### Étape 2️⃣ - Voir le graphique
- Le graphique se génère **automatiquement** avec vos données
- Les événements politiques s'affichent comme des diamants colorés
- Source affichée: **"📊 Source: Fichier Excel importé"**

### Étape 3️⃣ - Explorer les données
- **Tableau des événements**: Voir tous les événements politiques (2021-2026)
- **Analyse détaillée**: Cliquez pour voir l'impact de chaque événement
- **Chatbot**: Posez des questions sur les corrélations

### Étape 4️⃣ - Changer le nombre de jours
- Utilisez le slider **"Nombre de jours à afficher"**
- Les graphiques et événements se mettront à jour automatiquement

## ℹ️ Structure du fichier Excel attendue

**Votre fichier doit avoir au minimum:**

| Date | Close |
|------|-------|
| 2021-01-01 | 500.50 |
| 2021-01-02 | 505.25 |
| ... | ... |

**Colonnes acceptées:**
- **Date:** `Date`, `date`, ou index DatetimeIndex
- **Prix:** `Close`, `Adj Close`, ou première colonne numérique

## 🔄 Utiliser yfinance (fallback)

Si vous n'importez pas de fichier:
1. L'app utilise automatiquement **yfinance** pour télécharger les données
2. Un message indique: "Téléchargement des données Nvidia..."
3. Si la connexion est lente ou s'il y a une erreur, elle essaie 3 fallbacks

## ✕ Supprimer les données Excel

- Cliquez sur le bouton **"✕ Supprimer Excel"** (à droite du slider)
- L'app bascule automatiquement vers yfinance
- Le graphique se régénère avec les données yfinance

## 🎯 Fonctionnalités

### 📈 Graphique interactif
- Ligne verte: Prix de Nvidia
- Diamants colorés: Événements politiques
  - 🟢 **Vert (Positif)**: Favorable à Nvidia
  - 🔴 **Rouge (Négatif)**: Défavorable
  - 🟠 **Orange (Mixed)**: Impact mixte
  - ⚪ **Gris (Neutre)**: Impact incertain
- Survolez le graphique pour voir les détails

### 📊 Statistiques en temps réel
- Prix actuel
- Variation (%)
- Plus haut / Plus bas

### 🤖 Chatbot Analyseur
Posez des questions comme:
- "Quel impact les élections ont eu?"
- "Quelles régulations favorisent Nvidia?"
- "Comment les événements affectent le cours?"

### 🏛️ Événements détaillés
- Liste complète: 20 événements politiques (2021-2026)
- Pour chaque événement: Impact, description, implications

## 🐛 Dépannage

### ❓ "Aucune donnée disponible"
**Solution:**
1. Vérifiez que votre fichier Excel a une colonne "Date" et "Close"
2. Vérifiez que les dates sont au format YYYY-MM-DD
3. Vérifiez que la colonne "Close" contient des nombres
4. Essayez d'actualiser (bouton 🔄)

### ❓ Les événements ne s'affichent pas
**Raison:** Les événements en dehors de la plage de vos données n'apparaissent pas
**Solution:** Utilisez le slider pour ajuster la plage, ou importez plus de données

### ❓ Graphique vide
**Raison:** Prix ou dates non valides
**Solution:** Vérifiez le formatage de votre Excel et réimportez

## 📁 Fichiers clés

- **`streamlit_app.py`**: Application principale (Excel + yfinance)
- **`streamlit_app_mock.py`**: Version démo avec données générées (pour tester l'UI)
- **`requirements.txt`**: Dépendances Python

## 🔧 Installation des dépendances

```bash
pip install -r requirements.txt
```

Ou manuellement:
```bash
pip install streamlit pandas yfinance plotly openpyxl
```

## 💡 Tips

- **Slider à 1825 jours**: Vue complète sur 5 ans
- **Slider à 365 jours**: Vue annuelle
- **Slider à 30 jours**: Vue mensuelle
- **Bouton Actualiser**: Vide le cache Streamlit et recharge

---

**Besoin d'aide?** Consultez [CHANGELOG_EXCEL_PRIORITY.md](CHANGELOG_EXCEL_PRIORITY.md) pour détails techniques.
