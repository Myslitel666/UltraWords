import re
import requests
import time
import sys
import os
from datetime import datetime

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

def has_next_page(html):
    return 'rel="next"' in html

def get_next_page_url(html):
    pattern = re.compile(r'<a\s+href="([^"]+)"\s+rel="next"')
    match = pattern.search(html)
    if match:
        return BASE_URL + match.group(1)
    return None

def insert_surnames(cursor, surnames, link):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    inserted = 0
    
    cursor.execute("SELECT id FROM Types WHERE value = 'Фамилии'")
    type_row = cursor.fetchone()
    if not type_row:
        print("   ❌ Тип 'Фамилии' не найден!")
        return 0
    type_id = type_row[0]
    
    cursor.execute("SELECT id FROM PartsOfSpeech WHERE value = 'Собственное'")
    pos_row = cursor.fetchone()
    if not pos_row:
        print("   ❌ Часть речи 'Собственное' не найдена!")
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

def process_letter(letter, cursor):
    url = f'{BASE_URL}/dict/surnames_ru?letter={letter}'
    page_num = 1
    total_inserted = 0
    total_found = 0

    while url:
        print(f"\n   🌐 Загружаю страницу {page_num} для буквы '{letter}': {url}")

        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, timeout=30, headers=headers)
            response.raise_for_status()
            html = response.text
        except Exception as e:
            print(f"      ❌ Ошибка: {e}")
            break

        surnames = extract_surnames_from_page(html)

        if not surnames:
            break

        total_found += len(surnames)
        
        # 👇 ВЫВОДИМ ФАМИЛИИ
        for surname in surnames:
            print(f"      {surname}")
        
        inserted = insert_surnames(cursor, surnames, url)
        total_inserted += inserted
        
        print(f"      📝 Найдено: {len(surnames)}, вставлено: {inserted} (всего на букву: {total_found})")

        if has_next_page(html):
            url = get_next_page_url(html)
            page_num += 1
            time.sleep(0.5)
        else:
            print(f"      🏁 Страницы для буквы '{letter}' закончились")
            break
    
    return total_found, total_inserted

def main():
    conn = get_connection()
    cursor = conn.cursor()
    
    print("🔍 Сбор и вставка фамилий из словаря...\n")
    
    total_all_found = 0
    total_all_inserted = 0
    
    for letter in LETTERS:
        found, inserted = process_letter(letter, cursor)
        print(f"   ✅ Буква '{letter}': найдено {found}, вставлено {inserted} (новых)")
        total_all_found += found
        total_all_inserted += inserted
        conn.commit()
    
    print(f"\n🎯 ВСЕГО: найдено {total_all_found}, вставлено {total_all_inserted} фамилий")
    
    conn.close()

if __name__ == '__main__':
    main()