import requests
import os

# Получаем данные из секретов
TOKEN = os.getenv("TELEGRAM_TOKEN")
# Собираем ID в список, убирая пустые значения
raw_ids = [os.getenv("TELEGRAM_CHAT_ID"), os.getenv("FRIEND_CHAT_ID")]
CHAT_IDS = [i for i in raw_ids if i]

APP_ID = "1489715534"
URL = f"https://itunes.apple.com/lookup?id={APP_ID}&country=ua"

# Загружаем старую версию
if os.path.exists("version.txt"):
    with open("version.txt", "r") as f:
        last_version = f.read().strip()
else:
    last_version = ""

try:
    # Запрос к App Store
    response = requests.get(URL, timeout=15).json()
    if response.get('resultCount', 0) > 0:
        current_version = response['results'][0]['version']
        
        # Если версия новая
        if current_version != last_version:
            msg = f"🚀 Обновление Дії!\nНовая версия: {current_version}"
            
            for chat_id in CHAT_IDS:
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                             json={"chat_id": chat_id, "text": msg})
            
            # Сохраняем новую версию
            with open("version.txt", "w") as f:
                f.write(current_version)
            print(f"Обновлено до {current_version}")
        else:
            print(f"Версия не изменилась: {current_version}")
    else:
        print("Приложение не найдено")
except Exception as e:
    print(f"Ошибка: {e}")
    
