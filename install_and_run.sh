#!/bin/bash

echo "📦 Installation des dépendances..."
pip install -r requirements.txt

echo ""
echo "✅ Installation terminée!"
echo ""
echo "🚀 Lancement de l'application Streamlit..."
streamlit run streamlit_app.py
