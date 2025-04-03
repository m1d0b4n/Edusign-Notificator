import json
import random
from datetime import datetime
from .config import MENTION_ROLE_ID, SUPPRESSION_DELAY, TZ
from .utils import get_daily_fact

def construire_message(test_mode=False):
    now = datetime.now(TZ)

    message_texte = "📢 Pensez à signer sur EduSign !"
    try:
        with open("messages.json", "r", encoding="utf-8") as f:
            descriptions = json.load(f)
            message_texte = random.choice(descriptions)
    except Exception as e:
        print(f"⚠️ Erreur chargement messages.json : {e}")

    contenu = "**[👉 Accéder à EduSign](https://edusign.app/student/)**\n"
    contenu += f"{message_texte}\n\n"
    contenu += "---"

    if now.hour < 12 or test_mode:
        citation = get_daily_fact()
        if citation:
            contenu += f"\n🧠 **Le saviez-vous ?**\n{citation}"
        else:
            print("⚠️ Aucune citation récupérée.")

    contenu += f"\n\n⌛ Ce message sera supprimé dans {SUPPRESSION_DELAY} minute(s)."

    message = {"content": contenu}

    if MENTION_ROLE_ID:
        message["content"] = f"<@&{MENTION_ROLE_ID}>\n{message['content']}"

    return message
