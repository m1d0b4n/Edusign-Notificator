import sys
import time
from datetime import datetime
from modules.config import HEURES_AUTORISEES, TZ
from modules.dispatcher import (
    charger_webhooks,
    envoyer_messages,
    supprimer_messages,
)
from modules.ascii_art import afficher_ascii

def est_heure_d_envoi(now):
    return now.weekday() < 5 and (now.hour, now.minute) in HEURES_AUTORISEES

def main():
    
    afficher_ascii()

    print("🔄 Chargement des webhooks...")

    webhooks = charger_webhooks()
    test_mode = "--test" in sys.argv

    if test_mode:
        print("🧪 Envoi immédiat (mode test)")
        envoyer_messages(webhooks, test_mode=True)

    last_minute = None
    while True:
        now = datetime.now(TZ)
        if now.minute != last_minute:
            last_minute = now.minute
            print(f"[{now.strftime('%H:%M')}] Tick")
            if est_heure_d_envoi(now) and not test_mode:
                envoyer_messages(webhooks)
            supprimer_messages()
        else:
            supprimer_messages()
        time.sleep(1)

if __name__ == "__main__":
    main()
