#!/usr/bin/env python3
"""Script de test pour diagnostiquer les problèmes avec yfinance"""

import sys
from datetime import datetime, timedelta

print("🧪 Test de téléchargement Yahoo Finance\n")
print("="*60)

# Test 1: Importer yfinance
print("\n1️⃣ Test d'import...")
try:
    import yfinance as yf
    print("   ✅ yfinance importé avec succès")
except ImportError as e:
    print(f"   ❌ Erreur d'import: {e}")
    sys.exit(1)

# Test 2: Importer pandas
print("\n2️⃣ Test d'import pandas...")
try:
    import pandas as pd
    print("   ✅ pandas importé avec succès")
except ImportError as e:
    print(f"   ❌ Erreur d'import: {e}")
    sys.exit(1)

# Test 3: Télécharger une petite quantité de données
print("\n3️⃣ Test de téléchargement (derniers 30 jours)...")
try:
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    print(f"   Date de début: {start_date.date()}")
    print(f"   Date de fin: {end_date.date()}")
    print("   Téléchargement en cours...")
    
    nvidia_data = yf.download("NVDA", start=start_date, end=end_date, progress=False)
    
    if nvidia_data.empty:
        print("   ⚠️ Aucune donnée reçue")
    else:
        print(f"   ✅ {len(nvidia_data)} lignes de données reçues")
        print(f"\n   Derniers prix:")
        print(f"      Dernier: ${float(nvidia_data['Close'].iloc[-1]):.2f}")
        print(f"      Min: ${float(nvidia_data['Close'].min()):.2f}")
        print(f"      Max: ${float(nvidia_data['Close'].max()):.2f}")
        print(f"\n   Aperçu des données:")
        print(nvidia_data.tail(5))
        
except Exception as e:
    print(f"   ❌ Erreur lors du téléchargement:")
    print(f"      {type(e).__name__}: {e}")
    print("\n   💡 Solutions possibles:")
    print("      - Vérifiez votre connexion Internet")
    print("      - Yahoo Finance peut être bloqué temporairement")
    print("      - Essayez: pip install --upgrade yfinance")
    sys.exit(1)

print("\n" + "="*60)
print("\n✅ Tous les tests sont passés!")
print("\nVous pouvez maintenant lancer Streamlit:")
print("   streamlit run streamlit_app.py")
