import re
import requests
import time
from urllib.parse import quote
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from db import get_connection

BASE_URL = 'https://gufo.me'
LETTERS = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'э', 'ю', 'я']

def extract_surnames_from_page(html):
    surnames = []
    pattern = re.compile(r'<a\s+href="/dict/surnames_ru/[^"]*">([А-ЯЁ\-]+)</a>', re.IGNORECASE)
    matches = pattern.findall(html)
    for match in matches:
        surname = match.strip()
        if len(surname) > 1:
            surname = surname[0].upper() + surname[1:].lower()
            surnames.append(surname)
    return surnames

def insert_surnames(cursor, surnames, link):
    """Вставляет фамилии в UltraWords."""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    inserted = 0
    
    # Получаем ID типа и части речи
    cursor.execute("SELECT id FROM Types WHERE value = 'Фамилии'")
    type_row = cursor.fetchone()
    if not type_row:
        print("   ❌ Тип 'Фамилии' не найден в таблице Types!")
        return 0
    type_id = type_row[0]
    
    cursor.execute("SELECT id FROM PartsOfSpeech WHERE value = 'Собственное'")
    pos_row = cursor.fetchone()
    if not pos_row:
        print("   ❌ Часть речи 'Собственное' не найдена в таблице PartsOfSpeech!")
        return 0
    pos_id = pos_row[0]
    
    for surname in surnames:
        cursor.execute('''
            INSERT OR IGNORE INTO UltraWords 
            (value, typeId, partOfSpeechId, isDeclinable, link, comment, DateTimeSaving) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (surname, type_id, pos_id, 1, link, 'Русские', now))
        if cursor.rowcount > 0:
            inserted += 1
    
    return inserted

def process_all_letters(cursor):
    """Собирает все фамилии со всех букв и вставляет в базу."""
    total_inserted = 0
    total_found = 0
    
    for letter in LETTERS:
        print(f"\n📖 Обработка буквы '{letter}'...")
        encoded = quote(letter)
        letter_found = 0
        letter_inserted = 0
        
        # Перебираем страницы 1–16
        for page_num in range(1, 17):
            if page_num == 1:
                url = f'{BASE_URL}/dict/surnames_ru?letter={encoded}'
            else:
                url = f'{BASE_URL}/dict/surnames_ru?page={page_num}&letter={encoded}'
            
            print(f"      Загрузка страницы {page_num}...")
            
            try:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                response = requests.get(url, timeout=30, headers=headers)
                response.raise_for_status()
                html = response.text
            except Exception as e:
                print(f"         ❌ Ошибка: {e}")
                break
            
            surnames = extract_surnames_from_page(html)
            
            # Если на странице нет фамилий — заканчиваем для этой буквы
            if not surnames:
                print(f"         ⏭️ Фамилий не найдено (страница {page_num})")
                break
            
            letter_found += len(surnames)
            
            # Вставляем в базу
            inserted = insert_surnames(cursor, surnames, url)
            letter_inserted += inserted
            total_inserted += inserted
            
            print(f"         Найдено: {len(surnames)}, вставлено: {inserted} (всего на букву: {letter_found})")
            
            # Коммитим после каждой страницы
            cursor.connection.commit()
            
            time.sleep(0.3)
        
        total_found += letter_found
        print(f"   ✅ Буква '{letter}': найдено {letter_found}, вставлено {letter_inserted} (новых)")
    
    return total_found, total_inserted

def main():
    conn = get_connection()
    cursor = conn.cursor()
    
    print("🔍 Сбор и вставка фамилий из словаря...\n")
    start_time = time.time()
    
    # Собираем и вставляем фамилии
    total_found, total_inserted = process_all_letters(cursor)
    
    # Финальный коммит
    conn.commit()
    
    elapsed = time.time() - start_time
    print(f"\n🎯 ВСЕГО:")
    print(f"   Найдено фамилий: {total_found}")
    print(f"   Вставлено в базу: {total_inserted} (новых)")
    print(f"   Время выполнения: {elapsed:.2f} секунд")
    
    conn.close()

if __name__ == '__main__':
    main()