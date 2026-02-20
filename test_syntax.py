import ast
import sys

try:
    with open('streamlit_app.py', 'r', encoding='utf-8') as f:
        code = f.read()
    ast.parse(code)
    print("✅ Syntaxe correcte!")
    sys.exit(0)
except SyntaxError as e:
    print(f"❌ Erreur de syntaxe: {e}")
    sys.exit(1)
