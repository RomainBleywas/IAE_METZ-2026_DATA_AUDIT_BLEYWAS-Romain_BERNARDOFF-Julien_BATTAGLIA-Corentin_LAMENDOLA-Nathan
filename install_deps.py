#!/usr/bin/env python3
"""Script d'installation des dépendances"""

import subprocess
import sys

print("📦 Installation de plotly et autres dépendances...\n")

packages = [
    'plotly',
    'yfinance',
    'streamlit',
    'pandas'
]

for package in packages:
    print(f"  Instalation de {package}...", end=" ", flush=True)
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-q", package],
            check=True,
            capture_output=True
        )
        print("✅")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur: {e}")

print("\n✅ Installation terminée!")
print("\n🚀 Pour lancer l'app, exécutez:")
print("   streamlit run streamlit_app.py")
print("\nOu:")
print("   python3 setup_and_run.py")
