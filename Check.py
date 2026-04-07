import requests
import os
import time  # Важно! Чтобы не было ошибки Exit Code 1

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
APP_ID = "1483089069"
URL = f"https://itunes.apple.com/lookup?id={APP_ID}&country=ua"

file_path = "version.txt"

# Читаем старую версию
if os.path.exists(file_path):
    with open(file_path, "r") as f:
        last_version = f.read().strip()
else:
    last_version = "0"

try:
    response = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15).json()
    if response.get('resultCount', 0) > 0:
        current_version = response['results'][0]['version']
        
        if str(current_version) != str(last_version):
            # ВЕРСИЯ ОБНОВИЛАСЬ — ВКЛЮЧАЕМ РЕЖИМ БУДИЛЬНИКА
            for i in range(50):
                text = f"🚨 ВЛАД, ВСТАВАЙ!!! ДІЯ ОБНОВИЛАСЬ! 🚨\nВерсия: {current_version}\n(Сигнал {i+1}/50)"
                
                # Отправка сообщения
                requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", 
                             json={"chat_id": CHAT_ID, "text": text})
                
                # Пауза 2 секунды, чтобы телефон успел провибрировать
                time.sleep(2) 
            
            # Записываем новую версию только когда закончили спамить
            with open(file_path, "w") as f:
                f.write(str(current_version))
        else:
            print(f"Версия не изменилась: {current_version}")
except Exception as e:
    print(f"Ошибка в работе скрипта: {e}")
    exit(1) # Это поможет увидеть ошибку в логах Гитхаба
