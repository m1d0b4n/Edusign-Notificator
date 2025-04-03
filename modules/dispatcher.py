import json
import requests
from datetime import datetime, timedelta
from .config import WEBHOOKS_FILE, SUPPRESSION_DELAY, TZ
from .message_builder import construire_message

messages_a_supprimer = []

def charger_webhooks():
    with open(WEBHOOKS_FILE, "r", encoding="utf-8") as f:
        webhooks = json.load(f)
    for nom in webhooks:
        url = webhooks[nom]
        if "?" in url:
            if "wait=true" not in url:
                webhooks[nom] += "&wait=true"
        else:
            webhooks[nom] += "?wait=true"
    return webhooks

def envoyer_messages(webhooks, test_mode=False):
    for nom, url in webhooks.items():
        try:
            message = construire_message(test_mode=test_mode)
            response = requests.post(url, json=message)
            response.raise_for_status()

            if response.status_code == 200 and response.content:
                message_id = response.json()["id"]
                messages_a_supprimer.append({
                    "url": url.split('?')[0],
                    "message_id": message_id,
                    "delete_at": datetime.now(TZ) + timedelta(minutes=SUPPRESSION_DELAY)
                })
                print(f"✅ Message envoyé à {nom} ({message_id})")
            else:
                print(f"⚠️ Message envoyé à {nom}, mais pas de message_id retourné (code {response.status_code})")

        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur avec {nom} : {e}")
            if 'response' in locals():
                print(f"↪️ Réponse brute : {response.text}")

def supprimer_messages():
    now = datetime.now(TZ)
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
