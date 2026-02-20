#!/usr/bin/env python3
"""Script d'installation des dépendances et lancement de Streamlit"""

import subprocess
import sys

packages = ['yfinance', 'plotly', 'streamlit', 'pandas']

print("📦 Installation des dépendances...")
for package in packages:
    print(f"  Installing {package}...", end=" ")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", package],
        capture_output=True
    )
    if result.returncode == 0:
        print("✅")
    else:
        print("❌")
        print(result.stderr.decode())

print("\n✅ Installation terminée!")
print("\n🚀 Lancement de l'application...\n")

subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
