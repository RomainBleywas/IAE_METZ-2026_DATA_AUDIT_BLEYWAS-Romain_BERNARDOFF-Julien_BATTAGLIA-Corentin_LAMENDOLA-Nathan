# 📊 Installation et lancement - Guide complet

## Option 1️⃣ : Script Python (Recommandé)

Exécutez simplement :
```bash
python3 setup_and_run.py
```

Ce script :
- ✅ Installera automatiquement toutes les dépendances
- ✅ Lancera Streamlit
- ✅ Ouvrira l'app dans votre navigateur

---

## Option 2️⃣ : Installation manuelle + lancement

### Étape 1 : Installer les dépendances individuellement

```bash
python3 -m pip install yfinance
python3 -m pip install plotly
python3 -m pip install streamlit
python3 -m pip install pandas
```

### Étape 2 : Lancer Streamlit

```bash
python3 -m streamlit run streamlit_app.py
```

---

## Option 3️⃣ : Utiliser requirements.txt

```bash
python3 -m pip install -r requirements.txt
python3 -m streamlit run streamlit_app.py
```

---

## 📱 Accès à l'application

Une fois lancée, ouvrez :
```
http://localhost:8501
```

---

## 🛠️ Dépannage

### Si yfinance ne fonctionne pas :

```bash
python3 -m pip install --upgrade yfinance
```

### Si vous avez des erreurs de proxy :

```bash
python3 -m pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org yfinance
```

### Vérifier que les packages sont installés :

```bash
python3 -c "import yfinance; import plotly; import streamlit; print('✅ Tous les packages sont OK')"
```

---

## 🎯 Structure des fichiers

```
/workspaces/IAE_METZ-2026_DATA_AUDIT/
├── streamlit_app.py          ← Application principale
├── chatbot.ipynb              ← Notebook Jupyter
├── requirements.txt           ← Liste des dépendances
├── setup_and_run.py          ← Script d'installation auto
├── install_and_run.sh        ← Script bash
└── INSTALL.md                ← Ce fichier
```

---

## 💡 Contenu de l'application

- **📈 Graphique Nvidia** : Cours NVDA avec événements politiques
- **🏛️ Événements politiques** : Timeline des décisions clés
- **🤖 Chatbot analyseur** : Posez des questions sur les corrélations
- **📊 Statistiques** : Prix actuel, variations, min/max

Amusez-vous à explorer ! 🚀
