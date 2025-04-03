import requests
from datetime import datetime
from .config import TZ

def get_daily_fact():
    try:
        today = f"{datetime.now(TZ).month}/{datetime.now(TZ).day}"
        res = requests.get(f"http://numbersapi.com/{today}/date", timeout=5)
        if res.status_code != 200:
            return None
        english_fact = res.text

        try:
            translation_res = requests.get(
                "https://api.mymemory.translated.net/get",
                params={"q": english_fact, "langpair": "en|fr"},
                timeout=5
            )
            if translation_res.status_code == 200:
                return translation_res.json()["responseData"]["translatedText"]
        except Exception as e:
            print(f"⚠️ Erreur traduction : {e}")

        return english_fact

    except Exception as e:
        print(f"⚠️ Erreur récupération fact of the day : {e}")
        return None
