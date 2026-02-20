#!/usr/bin/env python3
"""Script de test pour vérifier yfinance et télécharger les données Nvidia"""

print("🧪 Test de yfinance...\n")

try:
    import yfinance as yf
    print("✅ yfinance importé avec succès")
except ImportError:
    print("❌ yfinance non trouvé. Installation en cours...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance"])
    import yfinance as yf
    print("✅ yfinance installé et importé")

try:
    import pandas as pd
    print("✅ pandas importé avec succès")
except ImportError:
    print("❌ pandas non trouvé.")

print("\n📊 Téléchargement des données Nvidia (derniers 30 jours)...\n")

try:
    # Télécharger les données Nvidia
    nvidia = yf.download("NVDA", period="1mo", progress=False)
    
    print("✅ Données Nvidia téléchargées avec succès!\n")
    print("Dernières données:")
    print(nvidia.tail())
    
    print(f"\n📈 Prix actuel: ${nvidia['Close'].iloc[-1]:.2f}")
    print(f"   Prix max (30 jours): ${nvidia['Close'].max():.2f}")
    print(f"   Prix min (30 jours): ${nvidia['Close'].min():.2f}")
    
except Exception as e:
    print(f"❌ Erreur lors du téléchargement: {e}")
    print("\nVérifiez votre connexion Internet et réessayez.")

print("\n" + "="*50)
print("🎯 Si tout est OK, lancez: streamlit run streamlit_app.py")
