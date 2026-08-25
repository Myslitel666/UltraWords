import re
import requests
import time
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from db import get_connection

BASE_URL = 'https://gufo.me/dict/surnames_ru'

# ✅ ПРАВИЛЬНЫЙ СПИСОК СТРАНИЦ (по буквам)
PAGES = [
    '/А', '/Б', '/В', '/Г', '/Д', '/Е', '/Ё', '/Ж', '/З', '/И',
    '/Й', '/К', '/Л', '/М', '/Н', '/О', '/П', '/Р', '/С', '/Т',
    '/У', '/Ф', '/Х', '/Ц', '/Ч', '/Ш', '/Щ', '/Э', '/Ю', '/Я'
]

def extract_surnames_from_page(html):
    surnames = []
    pattern = re.compile(r'<a\s+href="[^"]*">([А-ЯЁ]+)</a>', re.IGNORECASE)
    matches = pattern.findall(html)
    for match in matches:
        surname = match.strip()
        if len(surname) > 1:
            surnames.append(surname)
    return surnames

def insert_surname(cursor, surname, link):
    TYPE_ID = 3   # Фамилии
    POS_ID = 1    # Существительное
    
    surname = surname[0].upper() + surname[1:].lower()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('''
        INSERT OR IGNORE INTO UltraWords 
        (value, typeId, partOfSpeechId, isDeclinable, link, comment, DateTimeSaving) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (surname, TYPE_ID, POS_ID, 1, link, 'Русские', now))
    
    return cursor.rowcount > 0

def main():
    conn = get_connection()
    cursor = conn.cursor()
    
    total_inserted = 0
    
    for page in PAGES:
        url = BASE_URL + page
        print(f"\n🌐 Загружаю: {url}")
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, timeout=30, headers=headers)
            response.raise_for_status()
            html = response.text
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
            continue
        
        surnames = extract_surnames_from_page(html)
        
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
        
        time.sleep(0.5)
    
    conn.close()
    print(f"\n🎯 ВСЕГО ДОБАВЛЕНО: {total_inserted}")

if __name__ == '__main__':
    main()