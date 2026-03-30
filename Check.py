import requests
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

print(f"--- ПРОВЕРКА СВЯЗИ ---")
print(f"Твой ID из настроек: {CHAT_ID}")

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
data = {"chat_id": CHAT_ID, "text": "🔔 Проверка связи! Если ты это видишь — всё работает."}

try:
    response = requests.post(url, json=data)
    print(f"Код ответа: {response.status_code}")
    print(f"Текст ответа: {response.text}")
    
    if response.status_code == 200:
        print("✅ ТЕЛЕГРАМ ПРИНЯЛ СООБЩЕНИЕ!")
    else:
        print("❌ ОШИБКА ОТПРАВКИ!")
except Exception as e:
    print(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
