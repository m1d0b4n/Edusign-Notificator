import json
import requests
import time
from datetime import datetime, timedelta
import pytz
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

WEBHOOKS_FILE = "webhooks.json"
MESSAGE = {"content": "🤖 ⚠️ 📝 @APPRENANTS pensez à signer sur Edusign !"}

tz = pytz.timezone("Europe/Paris")
messages_a_supprimer = []

def charger_webhooks():
    with open(WEBHOOKS_FILE, "r", encoding="utf-8") as f:
        webhooks = json.load(f)

    # Ajouter ?wait=true si absent
    for nom in webhooks:
        url = webhooks[nom]
        if "?" in url:
            if "wait=true" not in url:
                webhooks[nom] += "&wait=true"
        else:
            webhooks[nom] += "?wait=true"
    return webhooks

def est_heure_d_envoi(now):
    return now.weekday() < 5 and (now.hour, now.minute) in [(9, 32), (14, 2)]

def envoyer_messages(webhooks):
    for nom, url in webhooks.items():
        try:
            response = requests.post(url, json=MESSAGE)
            response.raise_for_status()

            if response.status_code == 200 and response.content:
                message_id = response.json()["id"]
                messages_a_supprimer.append({
                    "url": url.split('?')[0],  # Pour les suppressions, enlever le ?wait=true
                    "message_id": message_id,
                    "delete_at": datetime.now(tz) + timedelta(minutes=30)
                })
                print(f"✅ Message envoyé à {nom} ({message_id})")
            else:
                print(f"⚠️ Message envoyé à {nom}, mais pas de message_id retourné (code {response.status_code})")

        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur avec {nom} : {e}")
            if 'response' in locals():
                print(f"↪️ Réponse brute : {response.text}")

def supprimer_messages():
    now = datetime.now(tz)
    to_delete = [msg for msg in messages_a_supprimer if msg["delete_at"] <= now]
    for msg in to_delete:
        delete_url = f'{msg["url"]}/messages/{msg["message_id"]}'
        try:
            response = requests.delete(delete_url)
            response.raise_for_status()
            print(f"🗑️ Supprimé : {msg['message_id']}")
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Erreur suppression message {msg['message_id']} : {e}")
    for msg in to_delete:
        messages_a_supprimer.remove(msg)

def main():
    webhooks = charger_webhooks()
    last_minute = None
    while True:
        now = datetime.now(tz)
        if now.minute != last_minute:
            last_minute = now.minute
            print(f"[{now.strftime('%H:%M')}] Tick")
            if est_heure_d_envoi(now):
                envoyer_messages(webhooks)
            supprimer_messages()
        time.sleep(1)

if __name__ == "__main__":
    main()
