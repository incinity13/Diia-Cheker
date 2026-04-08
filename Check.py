import requests
import os
import time

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
APP_ID = "1483089069"
# Ссылка без страны, чтобы было надежнее
URL = f"https://itunes.apple.com/lookup?id={APP_ID}"

file_path = "version.txt"

print("--- ЗАПУСК ПРОВЕРКИ ---")

# 1. Читаем старую версию
if os.path.exists(file_path):
    with open(file_path, "r") as f:
        last_version = f.read().strip()
else:
    last_version = "0"

try:
    # 2. Запрос с "маскировкой" под браузер
    headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)'}
    response = requests.get(URL, headers=headers, timeout=15).json()
    
    # ПРОВЕРКА: Есть ли вообще результаты?
    if response.get('resultCount', 0) > 0:
        current_version = str(response['results'][0]['version']).strip()
        print(f"Версия в магазине: {current_version}")
        
        # 3. СРАВНЕНИЕ (или тест через файл version.txt со словом TEST)
        if current_version != last_version or last_version == "TEST":
            print("ОТПРАВЛЯЮ 10 СМС...")
            for i in range(1, 11):
                text = f"🚨 ВЛАД, ОБНОВА! 🚨\nВерсия: {current_version}\n(Сигнал {i}/10)"
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                             json={"chat_id": CHAT_ID, "text": text})
                time.sleep(6) # 1 минута тряски на 10 сообщений
            
            # Сохраняем, если это не тест
            if last_version != "TEST":
                with open(file_path, "w") as f:
                    f.write(current_version)
        else:
            print("Версии совпадают.")
    else:
        print("Ошибка: App Store вернул пустой список. Попробуем в следующий раз.")

except Exception as e:
    print(f"Критическая ошибка: {e}")
