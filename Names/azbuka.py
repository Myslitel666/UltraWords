import re
import requests
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from db import get_connection

URL = 'https://azbyka.ru/shemy/imena-biblejskie.shtml'

def extract_names_from_table(html):
    names = []
    
    for line in html.split('<tr>'):
        if '<td>' not in line:
            continue
        
        td_start = line.find('<td>')
        if td_start == -1:
            continue
        
        td_end = line.find('</td>', td_start)
        if td_end == -1:
            continue
        
        content = line[td_start + 4:td_end]
        
        # Удаляем все HTML-теги
        while '<' in content and '>' in content:
            start = content.find('<')
            end = content.find('>', start)
            if start != -1 and end != -1:
                content = content[:start] + content[end + 1:]
            else:
                break
        
        name = content.strip()
        
        if not name or len(name) < 2:
            continue
        
        # Убираем всё, что в скобках
        name = re.sub(r'\s*\([^)]*\)\s*', '', name).strip()
        
        # Убираем всё после запятой
        if ',' in name:
            name = name.split(',')[0].strip()
        
        # Убираем всё после тире
        if '—' in name or '–' in name or '-' in name:
            for sep in [' — ', ' —', '— ', '—', ' – ', ' –', '– ', '–', ' - ', ' -', '- ', '-']:
                if sep in name:
                    name = name.split(sep)[0].strip()
                    break
        
        # Убираем номера в скобках
        name = re.sub(r'\s*\(\d+\)\s*', '', name).strip()
        
        if name in ['См.', 'См', 'см', '—', '–', '-', '']:
            continue
        
        names.append(name)
    
    # Убираем дубликаты, сохраняя порядок
    seen = set()
    unique_names = []
    for name in names:
        if name not in seen:
            seen.add(name)
            unique_names.append(name)
    
    return unique_names

def insert_names(cursor, names, link):
    """Вставляет имена в UltraWords."""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    inserted = 0
    
    # Получаем ID типа и части речи
    cursor.execute("SELECT id FROM Types WHERE value = 'Имена'")
    type_row = cursor.fetchone()
    if not type_row:
        print("   ❌ Тип 'Имена' не найден в таблице Types!")
        return 0
    type_id = type_row[0]
    
    cursor.execute("SELECT id FROM PartsOfSpeech WHERE value = 'Существительное'")
    pos_row = cursor.fetchone()
    if not pos_row:
        print("   ❌ Часть речи 'Собственное' не найдена в таблице PartsOfSpeech!")
        return 0
    pos_id = pos_row[0]
    
    for name in names:
        cursor.execute('''
            INSERT OR IGNORE INTO UltraWords 
            (value, typeId, partOfSpeechId, isDeclinable, link, comment, DateTimeSaving) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, type_id, pos_id, 1, link, 'Библия', now))
        if cursor.rowcount > 0:
            inserted += 1
    
    return inserted

def main():
    conn = get_connection()
    cursor = conn.cursor()
    
    print(f"🌐 Загружаю: {URL}")
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(URL, timeout=30, headers=headers)
        response.raise_for_status()
        html = response.text
    except Exception as e:
        print(f"❌ Ошибка загрузки: {e}")
        conn.close()
        return
    
    names = extract_names_from_table(html)
    
    if not names:
        print("⏭️ Имён не найдено")
        conn.close()
        return
    
    print(f"\n📝 Найдено имён: {len(names)}")
    
    # Вставляем в базу
    inserted = insert_names(cursor, names, URL)
    conn.commit()
    conn.close()
    
    print(f"   ➡️ Вставлено: {inserted} (новых)")
    print(f"\n✅ Готово!")

if __name__ == '__main__':
    main()