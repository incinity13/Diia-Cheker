import requests
import os

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
APP_ID = "1483089069"
URL = f"https://itunes.apple.com/lookup?id={APP_ID}&country=ua"

file_path = "version.txt"

# 1. Читаем старую версию
if os.path.exists(file_path):
    with open(file_path, "r") as f:
        last_version = f.read().strip()
else:
    last_version = "0"

try:
    # 2. Запрос в App Store
    response = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15).json()
    if response.get('resultCount', 0) > 0:
        current_version = str(response['results'][0]['version']).strip()
        
        # 3. Сравнение и отправка 1 сообщения
        if current_version != last_version:
            text = f"🚨 ДІЯ ОБНОВИЛАСЬ! 🚨\nНовая версия: {current_version}"
            
            # Отправка
            requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                         json={"chat_id": CHAT_ID, "text": text})
            
            # Сохранение версии
            with open(file_path, "w") as f:
                f.write(current_version)
except Exception as e:
    print(f"Ошибка: {e}")
