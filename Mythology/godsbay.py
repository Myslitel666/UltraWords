import re
import requests
import sys
import os
import time
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from db import get_connection, create_tables, capitalize_first

BASE_URL = 'https://godsbay.ru/'
PAGES = [
    'all.html', 'all_b.html', 'all_v.html', 'all_g.html', 'all_d.html',
    'all_e.html', 'all_j.html', 'all_z.html', 'all_i.html', 'all1.html',
    'all_l.html', 'all_m.html', 'all_n.html', 'all_o.html', 'all_p.html',
    'all_r.html', 'all_s.html', 'all_t.html', 'all2.html', 'all_f.html',
    'all_h.html', 'all_zt.html', 'all_ch.html', 'all_sh.html', 'all_ye.html',
    'all_yu.html', 'all_ya.html'
]

def extract_entries_from_html(html):
    """Извлекает слова из HTML-таблицы."""
    entries = []
    
    pattern = re.compile(
        r'<a\s+href="[^"]*"\s*[^>]*>([^<]+)</a>\s*</td>',
        re.IGNORECASE | re.DOTALL
    )
    
    matches = pattern.findall(html)
    
    for word in matches:
        word = word.strip()
        if len(word) < 2:
            continue
        # Пропускаем мусорные строки
        if word in ('Алфавитный указатель', 'Мифология и История', 'Боги, демиурги, герои'):
            continue
        if re.search(r'[<>{}\[\]!]', word):
            continue
        entries.append(word)
    
    return entries

def get_mythology_type_id(cursor):
    """Возвращает id типа 'Мифология'. Если его нет — создаёт."""
    cursor.execute('INSERT OR IGNORE INTO Types (value) VALUES (?)', ('Мифология',))
    cursor.execute('SELECT id FROM Types WHERE value = ?', ('Мифология',))
    return cursor.fetchone()[0]

def get_pos_id(cursor, pos_name):
    pos_name = capitalize_first(pos_name)
    cursor.execute('INSERT OR IGNORE INTO PartsOfSpeech (value) VALUES (?)', (pos_name,))
    cursor.execute('SELECT id FROM PartsOfSpeech WHERE value = ?', (pos_name,))
    return cursor.fetchone()[0]

def insert_word(cursor, word, link):
    word = capitalize_first(word)
    type_id = get_mythology_type_id(cursor)
    pos_id = get_pos_id(cursor, 'Собственное')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cursor.execute('''
        INSERT OR IGNORE INTO UltraWords 
        (value, typeId, partOfSpeechId, isDeclinable, link, DateTimeSaving) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (word, type_id, pos_id, 1, link, now))
    
    return cursor.rowcount > 0

def main():
    create_tables()
    conn = get_connection()
    cursor = conn.cursor()
    
    # Убеждаемся, что тип 'Мифология' существует
    get_mythology_type_id(cursor)
    conn.commit()
    
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
        
        words = extract_entries_from_html(html)
        if not words:
            print("   ⏭️ Ничего не найдено")
            continue
        
        inserted = 0
        for word in words:
            if insert_word(cursor, word, url):
                inserted += 1
                print(f"   ✅ {word}")
        
        conn.commit()
        total_inserted += inserted
        print(f"   📝 Добавлено: {inserted}")
        time.sleep(0.5)
    
    conn.close()
    print(f"\n🎯 ВСЕГО ДОБАВЛЕНО: {total_inserted}")

if __name__ == '__main__':
    main()