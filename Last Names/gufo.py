import re
import requests
import time

BASE_URL = 'https://gufo.me'

def extract_surnames_from_page(html):
    surnames = []
    pattern = re.compile(r'<a\s+href="/dict/surnames_ru/[^"]*">([А-ЯЁ\-]+)</a>', re.IGNORECASE)
    matches = pattern.findall(html)
    for match in matches:
        surname = match.strip()
        if len(surname) > 1:
            surnames.append(surname)
    return surnames

def has_next_page(html):
    return 'rel="next"' in html

def get_next_page_url(html):
    """Извлекает полный URL следующей страницы."""
    pattern = re.compile(r'<a\s+href="([^"]+)"\s+rel="next"')
    match = pattern.search(html)
    if match:
        # Ссылка уже полная, просто добавляем домен
        return BASE_URL + match.group(1)
    return None

def main():
    # Стартуем с первой страницы для буквы "А"
    url = BASE_URL + '/dict/surnames_ru?letter=%D0%B0'
    total_found = 0
    page_num = 1

    while url:
        print(f"\n🌐 Загружаю страницу {page_num}: {url}")
        
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response = requests.get(url, timeout=30, headers=headers)
            response.raise_for_status()
            html = response.text
        except Exception as e:
            print(f"   ❌ Ошибка: {e}")
            break

        surnames = extract_surnames_from_page(html)

        if not surnames:
            print("   ⏭️ Фамилий не найдено")
            break

        for surname in surnames:
            print(f"   {surname}")

        print(f"   📝 Найдено: {len(surnames)}")
        total_found += len(surnames)

        if has_next_page(html):
            url = get_next_page_url(html)
            page_num += 1
            time.sleep(1)  # пауза между запросами
        else:
            print("   🏁 Страницы закончились")
            break

    print(f"\n🎯 ВСЕГО НАЙДЕНО: {total_found}")

if __name__ == '__main__':
    main()