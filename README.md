# 📝 EduSign Notificator (version locale)

Petit script Python qui envoie automatiquement des rappels sur des canaux Discord via des **webhooks**, à 9h35 et 14h05 du lundi au vendredi.  
Les messages sont automatiquement supprimés après **35 minutes** pour garder les salons propres.

---

## 🚀 Fonctionnalités

- ⏰ Envoi automatique à 9h35 et 14h05 (heure de Paris)
- 📅 Jours ouvrés uniquement (lundi → vendredi)
- 🔊 Message TTS + emoji
- 🧹 Suppression automatique des messages après 35 minutes
- 💻 Fonctionne **en local ou sur un serveur** (Linux, Raspberry Pi, VPS...)

---

## 📦 Prérequis

- Python 3.7 ou plus
- Un ou plusieurs **webhooks Discord**
- Une machine qui peut exécuter un script en continu (ordi perso, serveur, Raspberry Pi...)

---

## 🧰 Structure du projet

```txt
Edusign-Notificator/
├── main.py                   # Script principal avec boucle continue
├── webhooks.json             # Liste des webhooks Discord
├── requirements.txt          # Dépendances Python
└── README.md                 
```

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

### 3. Remplis le fichier `webhooks.json`

Suis ce guide officiel pour créer un webhook :  
[📄 Discord – Guide Webhooks](https://support.discord.com/hc/fr/articles/228383668-Utiliser-les-Webhooks)

Une fois ton webhook créé, copie l’URL et ajoute-la dans le fichier `_webhooks.json` :

```json
{
  "general": "https://discord.com/api/webhooks/xxxx/...",
  "annonces": "https://discord.com/api/webhooks/yyyy/..."
}
```

⚠️ Pense à renommer le fichier, enlève juste le `_` .

### 4. Lance le script

```bash
python main.py
```

Tu verras une ligne `[HH:MM] Tick` chaque minute, et des logs quand un message est envoyé ou supprimé.

---

## 🧪 Tester rapidement

Tu peux modifier temporairement l’heure d’envoi dans `main.py` :

```python
HEURES_AUTORISEES = [(15, 46)]  # Pour tester à 15h46 par exemple
```

---

## 📌 Astuce : Lancer automatiquement au démarrage

Si tu veux que le script tourne en continu après redémarrage :

- Sur Linux : ajoute-le à `rc.local`, `systemd`, ou un `tmux`/`screen`
- Sur Windows : tâche planifiée

---

## 📁 requirements.txt

```txt
requests
pytz
```

---

## 🛡️ Licence

Ce projet est open-source.  
Tu peux l’utiliser et l’adapter librement, tant que tu crédites l’auteur original [m1d0b4n](https://github.com/m1d0b4n)

---

## 🙏 Merci

Ce projet a été conçu pour automatiser de façon simple et efficace les notifications de signatures de présence EduSign des apprenants sur les serveurs Discord de l'établissement Livecampus ✊

🏗️🚧 Des améliorations sont à venir...
