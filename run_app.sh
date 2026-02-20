#!/bin/bash

# 🚀 Guide complet pour lancer l'application Streamlit
# Exécutez ce script pour démarrer l'application avec tous les checks

echo "================================"
echo "🚀 Démarrage de l'application"
echo "================================"
echo ""

# Check 1: Python installé?
echo "✓ Vérification de Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé"
    exit 1
fi
python3 --version
echo ""

# Check 2: Dépendances installées?
echo "✓ Vérification des dépendances..."
python3 -c "import streamlit; import pandas; import yfinance; import plotly" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Certaines dépendances manquent"
    echo "📦 Installation des dépendances en cours..."
    pip install -r requirements.txt
fi
echo ""

# Check 3: Syntaxe du code
echo "✓ Vérification de la syntaxe..."
python3 -m py_compile streamlit_app.py 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ Syntaxe OK"
else
    echo "❌ Erreur de syntaxe dans streamlit_app.py"
    exit 1
fi
echo ""

# Lancer l'app
echo "================================"
echo "🎬 Lancement de Streamlit"
echo "================================"
echo ""
echo "📍 L'app s'ouvrira sur: http://localhost:8501"
echo "🔄 Pour recharger: Ctrl+R (ou F5)"
echo "⛔ Pour arrêter: Ctrl+C"
echo ""
echo "💡 Conseil: Importez votre fichier Excel dès le démarrage!"
echo ""

streamlit run streamlit_app.py
