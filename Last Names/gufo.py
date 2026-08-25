import re
import requests
import time
from urllib.parse import quote

BASE_URL = 'https://gufo.me'
LETTERS = ['а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'э', 'ю', 'я']
OUTPUT_FILE = 'surnames_all.txt'

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

def process_all_letters():
    """Собирает все фамилии со всех букв."""
    all_surnames = []
    total_surnames = 0
    
    for letter in LETTERS:
        print(f"\n📖 Обработка буквы '{letter}'...")
        encoded = quote(letter)
        letter_surnames = []
        
        # Пробуем страницы с 1 по 16
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
            
            letter_surnames.extend(surnames)
            total_surnames += len(surnames)
            print(f"         Найдено: {len(surnames)} (всего на букву: {len(letter_surnames)})")
            
            time.sleep(0.3)
        
        all_surnames.extend(letter_surnames)
        print(f"   ✅ Буква '{letter}': всего {len(letter_surnames)} фамилий")
    
    return all_surnames

def main():
    print("🔍 Сбор фамилий из словаря...\n")
    start_time = time.time()
    
    # Собираем все фамилии
    all_surnames = process_all_letters()
    
    # Удаляем дубли и сортируем
    print("\n🔄 Сортировка и удаление дублей...")
    unique_sorted = sorted(set(all_surnames))
    
    # Записываем в файл
    print(f"💾 Запись в файл {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        for surname in unique_sorted:
            f.write(surname + '\n')
    
    elapsed = time.time() - start_time
    print(f"\n✅ Готово!")
    print(f"   Найдено фамилий: {len(all_surnames)}")
    print(f"   Уникальных фамилий: {len(unique_sorted)}")
    print(f"   Время выполнения: {elapsed:.2f} секунд")
    print(f"   Файл: {OUTPUT_FILE}")

if __name__ == '__main__':
    main()