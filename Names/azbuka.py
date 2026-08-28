import requests
import re

URL = 'https://azbyka.ru/shemy/imena-biblejskie.shtml'
OUTPUT_FILE = 'bible_names.txt'

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
        
        # 🔥 Убираем всё, что в скобках (включая сами скобки)
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
        
        # Убираем номера в скобках (если вдруг остались)
        name = re.sub(r'\s*\(\d+\)\s*', '', name).strip()
        
        if name in ['См.', 'См', 'см', '—', '–', '-', '']:
            continue
        
        names.append(name)
    
    # Убираем дубликаты
    seen = set()
    unique_names = []
    for name in names:
        if name not in seen:
            seen.add(name)
            unique_names.append(name)
    
    return unique_names

def main():
    print(f"🌐 Загружаю: {URL}")
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(URL, timeout=30, headers=headers)
        response.raise_for_status()
        html = response.text
    except Exception as e:
        print(f"❌ Ошибка загрузки: {e}")
        return
    
    names = extract_names_from_table(html)
    
    if not names:
        print("⏭️ Имён не найдено")
        return
    
    print(f"\n📝 Найдено имён: {len(names)}\n")
    
    for name in names:
        print(f"   {name}")
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for name in names:
            f.write(name + '\n')
    
    print(f"\n✅ Файл сохранён: {OUTPUT_FILE}")

if __name__ == '__main__':
    main()