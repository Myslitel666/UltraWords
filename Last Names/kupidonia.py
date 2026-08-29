import re
import requests
import sys
import os
import time
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from db import get_connection, create_tables, capitalize_first

# === Ссылки на страницы ===
# На сайте kupidonia.ru список фамилий разбит по буквам.
# Вот URL для всех букв:
URLS = [
    'https://kupidonia.ru/spisok/spisok-russkih-familij/bukva/А',
    'https://kupidonia.ru/spisok/spisok-russkih-familij/bukva/Б',
    'https://kupidonia.ru/spisok/spisok-russkih-familij/bukva/В',
    'https://kupidonia.ru/spisok/spisok-russkih-familij/bukva/Г',
    'https://kupidonia.ru/spisok/spisok-russkih-familij/bukva/Д',
    'https://kupidonia.ru/spisok/spisok-russkih-familij/bukva/Е',
    'https://kupidonia.ru/spisok/spisok-russkih-familij/bukva/Ж',
    'https://kupidonia.ru/spisok/spisok-russkih-familij/bukva/З',
    'https://kupidonia.ru/spisok/spisok-russkih-familij/bukva/И',
    'https://kupidonia.ru/spisok/spisok-russkih-familij/bukva/К',
    'https://kupidonia.ru/spisok/spisok-russkih-familij/bukva/Л',
    'https://kupidonia.ru/spisok/spisok-russkih-familij/bukva/М',
    'https://kupidonia.ru/spisok/spisok-russkih-familij/bukva/Н',
    'https://kupidonia.ru/spisok/spisok-russkih-familij/bukva/О',
    'https://kupidonia.ru/spisok/spisok-russkih-familij/bukva/П',
    'https://kupidonia.ru/spisok/spisok-russkih-familij/bukva/Р',
    'https://kupidonia.ru/spisok/spisok-russkih-familij/bukva/С',
    'https://kupidonia.ru/spisok/spisok-russkih-familij/bukva/Т',
    'https://kupidonia.ru/spisok/spisok-russkih-familij/bukva/У',
    'https://kupidonia.ru/spisok/spisok-russkih-familij/bukva/Ф',
    'https://kupidonia.ru/spisok/spisok-russkih-familij/bukva/Х',
    'https://kupidonia.ru/spisok/spisok-russkih-familij/bukva/Ц',
    'https://kupidonia.ru/spisok/spisok-russkih-familij/bukva/Ч',
    'https://kupidonia.ru/spisok/spisok-russkih-familij/bukva/Ш',
    'https://kupidonia.ru/spisok/spisok-russkih-familij/bukva/Щ',
    'https://kupidonia.ru/spisok/spisok-russkih-familij/bukva/Ю',
    'https://kupidonia.ru/spisok/spisok-russkih-familij/bukva/Я',
]

def extract_surnames_from_html(html):
    """Извлекает фамилии из HTML по классу position_title."""
    surnames = []
    
    # Ищем все элементы с классом position_title
    pattern = re.compile(
        r'<div[^>]*class="[^"]*position_title[^"]*"[^>]*>\s*(.*?)\s*</div>',
        re.IGNORECASE | re.DOTALL
    )
    
    matches = pattern.findall(html)
    
    for match in matches:
        surname = match.strip()
        if len(surname) < 2:
            continue
        # Пропускаем мусор
        if surname in ('', ' ', ' '):
            continue
        surnames.append(surname)
    
    return surnames

def get_type_id(cursor, type_name):
    """Возвращает id типа, создаёт если нет."""
    type_name = capitalize_first(type_name)
    cursor.execute('INSERT OR IGNORE INTO Types (value) VALUES (?)', (type_name,))
    cursor.execute('SELECT id FROM Types WHERE value = ?', (type_name,))
    return cursor.fetchone()[0]

def get_pos_id(cursor, pos_name):
    """Возвращает id части речи, создаёт если нет."""
    pos_name = capitalize_first(pos_name)
    cursor.execute('INSERT OR IGNORE INTO PartsOfSpeech (value) VALUES (?)', (pos_name,))
    cursor.execute('SELECT id FROM PartsOfSpeech WHERE value = ?', (pos_name,))
    return cursor.fetchone()[0]

def insert_surname(cursor, surname, link):
    """Вставляет фамилию в базу."""
    surname = capitalize_first(surname)
    
    # Тип "Фамилии"
    type_id = get_type_id(cursor, 'Фамилии')
    
    # Часть речи "Собственное"
    pos_id = get_pos_id(cursor, 'Существительное')
    
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('''
        INSERT OR IGNORE INTO UltraWords 
        (value, typeId, partOfSpeechId, isDeclinable, link, DateTimeSaving) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (surname, type_id, pos_id, 1, link, now))
    
    return cursor.rowcount > 0

def main():
    create_tables()
    conn = get_connection()
    cursor = conn.cursor()
    
    total_inserted = 0
    
    for url in URLS:
        print(f"\n🌐 Загружаю: {url}")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, timeout=30, headers=headers)
            response.raise_for_status()
            html = response.text
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
            continue
        
        surnames = extract_surnames_from_html(html)
        
        if not surnames:
            print("   ⏭️ Ничего не найдено")
            continue
        
        inserted = 0
        for surname in surnames:
            if insert_surname(cursor, surname, url):
                inserted += 1
                print(f"   ✅ {surname}")
        
        conn.commit()
        total_inserted += inserted
        print(f"   📝 Добавлено: {inserted}")
        
        time.sleep(1)
    
    conn.close()
    print(f"\n🎯 ВСЕГО ДОБАВЛЕНО: {total_inserted}")

if __name__ == '__main__':
    main()