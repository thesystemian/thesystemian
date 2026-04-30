# 🌸 pmail — Client Mail CLI Souverain

**Premier pilier de [The P Universe](https://github.com/thesystemian).**

Un client mail terminal léger, rapide et respectueux de la vie privée.  
Conçu pour fonctionner nativement sur **macOS** (Apple Silicon) et interagir avec les services Google (Gmail) via une interface CLI pure.

> "La souveraineté numérique, c'est contrôler ses outils, ligne de commande par ligne de commande."

## ✨ Fonctionnalités

- 📬 **Lecture Propre** : Extraction automatique du texte brut (adieu le code HTML/CSS polluant).
- 🚀 **Rapidité** : Lancement instantané via alias (`pmail`).
- 🔒 **Sécurité** : Authentification par code 16 lettres (App Password). Aucun mot de passe principal stocké.
- 🍎 **Native Apple** : Optimisé pour macOS (Zsh, Keychain ready). Conçu pour compléter l'écosystème Apple en mode power-user.
- 🛠️ **Zéro Dépendance** : Utilise uniquement les bibliothèques standards de Python 3.

## 🚀 Installation

### 1. Cloner le dépôt
```bash
git clone https://github.com/thesystemian/pmail-cli.git
cd pmail-cli
chmod +x primmail.py
echo 'alias pmail="$PWD/primmail.py"' >> ~/.zshrc
source ~/.zshrc
pmail

#### 3️⃣ Création de la Licence (MIT)

```bash
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2026 thesystemian

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
