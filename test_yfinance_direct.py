#!/usr/bin/env python3
"""Test DIRECT de yfinance - pas de Streamlit"""

import sys
print("🧪 Test direct de yfinance (sans Streamlit)")
print("=" * 60)

# Test 1: Import
print("\n1️⃣ Import yfinance...")
try:
    import yfinance as yf
    print("   ✅ yfinance importé")
except ImportError as e:
    print(f"   ❌ Erreur: {e}")
    sys.exit(1)

# Test 2: Version
print(f"   Version: {yf.__version__}")

# Test 3: Téléchargement simple
print("\n2️⃣ Téléchargement simple de 5 jours...")
try:
    print("   Requête en cours (cela peut prendre 10-30 secondes)...")
    data = yf.download("NVDA", period="5d", progress=False)
    
    if data.empty:
        print("   ⚠️ Données vides reçues")
    else:
        print(f"   ✅ {len(data)} lignes reçues")
        print("\n   Aperçu:")
        print(data)
        
except Exception as e:
    print(f"   ❌ Erreur: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("Si vous voyez '✅' et les données ci-dessus, yfinance fonctionne.")
print("Si vous ne voyez rien, Yahoo Finance ne répond pas.")
