import json
import requests
import time
from datetime import datetime, timedelta
import pytz

WEBHOOKS_FILE = "webhooks.json"
MESSAGE_TTS = {"content": "Pensez à signer sur Edusign !", "tts": True}
MESSAGE_EMOJI = {"content": "🤖 ⚠️ 📝"}

tz = pytz.timezone("Europe/Paris")
messages_a_supprimer = []

def charger_webhooks():
    with open(WEBHOOKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def est_heure_d_envoi(now):
    return now.weekday() < 5 and (now.hour, now.minute) in [(9, 35), (14, 5)]

def envoyer_messages(webhooks):
    for nom, url in webhooks.items():
        for payload in [MESSAGE_TTS, MESSAGE_EMOJI]:
            try:
                response = requests.post(url, data=payload)
                response.raise_for_status()
                message_id = response.json()["id"]
                # Planifier la suppression dans 1h
                messages_a_supprimer.append({
                    "url": url,
                    "message_id": message_id,
                    "delete_at": datetime.now(tz) + timedelta(minutes=1)
                })
                print(f"✅ Message envoyé à {nom} ({message_id})")
            except requests.exceptions.RequestException as e:
                print(f"❌ Erreur avec {nom} : {e}")

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
            print(f"⚠️ Erreur suppression : {e}")
    # Retirer les messages supprimés de la liste
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
