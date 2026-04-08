import requests
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
APP_ID = "1483089069"
URL = f"https://itunes.apple.com/lookup?id={APP_ID}&country=ua"

print("--- ЗАПУСК ПРОВЕРКИ ---")

try:
    # 1. Просто берем версию для инфы
    resp = requests.get(URL, timeout=10).json()
    ver = resp['results'][0]['version']
    print(f"Версия в App Store сейчас: {ver}")

    # 2. ШЛЕМ СМС БЕЗ УСЛОВИЙ (Чисто тест связи)
    text = f"🤖 Бот на связи! Версия Дии: {ver}\nЕсли видишь это — значит не бан!"
    r = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                     json={"chat_id": CHAT_ID, "text": text})
    
    print(f"Ответ Телеграма: {r.status_code} - {r.text}")

except Exception as e:
    print(f"Ошибка: {e}")
