# 📝 EduSign Notificator (version locale)

Script Python qui envoie automatiquement des rappels de signature sur EduSign via **webhooks Discord**, à 9h35 et 14h05 du lundi au vendredi.  
Les messages sont automatiquement **supprimés après un délai configurable**.

> 💡 Nouvelle version modulaire avec structure claire, citation du jour, et test à la volée.

---

## 🚀 Fonctionnalités

- ⏰ Envoi automatique à 9h35 et 14h05 (heure de Paris, jours ouvrés uniquement)
- 🤖 Message dynamique pioché aléatoirement dans une liste
- 🧠 Ajout d’un fait historique traduit en français chaque matin
- 🧹 Suppression automatique des messages après `x` minutes (configurable)
- 🧪 Envoi manuel immédiat avec `--test`
- 🧼 Code modulaire pour une meilleure maintenabilité

---

## 📁 Structure du projet

```
Edusign-Notificator/
├── main.py                  # Point d’entrée du script
├── webhooks.json            # Liste des webhooks Discord
├── messages.json            # Messages aléatoires à afficher
├── requirements.txt
├── README.md
└── modules/
    ├── config.py            # Constantes de configuration
    ├── utils.py             # Fonction pour récupérer la citation du jour
    ├── message_builder.py   # Construction du message
    └── dispatcher.py        # Envoi + suppression automatique
```

---

## 📦 Prérequis

- Python 3.7+
- Un ou plusieurs **webhooks Discord** :  
  [📄 Guide officiel Discord – Webhooks](https://support.discord.com/hc/fr/articles/228383668-Utiliser-les-Webhooks)
- Une machine capable d’exécuter un script en continu (PC, VPS, Raspberry Pi…)

---

## 🔧 Installation et lancement

### 1. Clone le dépôt

```bash
git clone https://github.com/ton-pseudo/Edusign-Notificator.git
cd Edusign-Notificator
```

### 2. Installe les dépendances

```bash
pip install -r requirements.txt
```

### 3. Configure les webhooks

```json
// webhooks.json
{
  "canal-m1": "https://discord.com/api/webhooks/...",
  "canal-m2": "https://discord.com/api/webhooks/..."
}
```

### 4. Configure les messages

```json
// messages.json
[
  "📸 Dites « signé ! » ✍️",
  "💼 Vous êtes presque pro ? Alors signez comme des pros !",
  "📝 Une signature aujourd'hui, un avenir assuré demain.",
  "⚠️ Pas de signature, pas d’attestation !"
]
```

### 5. Lance le script

```bash
python main.py
```

Tu verras un `[HH:MM] Tick` chaque minute et des logs clairs en console.

---

## 🧪 Lancer un test immédiatement

```bash
python main.py --test
```

👉 Cela envoie un message immédiatement et le supprime automatiquement après le délai défini.

---

## ⚙️ Personnaliser les horaires ou paramètres

Modifie `modules/config.py` :

```python
HEURES_AUTORISEES = [(9, 35), (14, 5)]  # Horaire Paris
SUPPRESSION_DELAY = 30  # En minutes
MENTION_ROLE_ID = ""  # Rôle Discord à ping : ex. "123456789012345678"
```

---

## 📌 Exécution automatique au démarrage

- **Linux** : via `systemd`, `tmux`, `rc.local`, etc.
- **Windows** : via le Planificateur de tâches (`taskschd.msc`)

---

## 📁 requirements.txt

```txt
requests
pytz
```

---

## 🛡️ Licence

Projet open-source. Tu peux l’utiliser et le modifier librement, tant que tu crédites l’auteur original [@m1d0b4n](https://github.com/m1d0b4n).

---

## 🙏 Merci

Ce projet a été conçu pour automatiser de façon simple et efficace les rappels de signature EduSign sur les serveurs Discord de l’établissement **Livecampus** 🎓

> 🧠 Avec une touche de culture générale chaque matin 💛
