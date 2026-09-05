import re
import requests
from datetime import datetime

# Настройки
BASE_URL = 'https://codenlp.ru/slovar/spisok-prilagatelnyih-russkogo-yazyika.html'
OUTPUT_FILE = 'insert_adjectives.sql'
BATCH_SIZE = 500  # Количество слов в одном INSERT

# Параметры для UltraWords
TYPE_ID = 7  # Общий тип (как для слов)
PART_OF_SPEECH_ID = 2  # Прилагательное
LINK = 'https://codenlp.ru/slovar/spisok-prilagatelnyih-russkogo-yazyika.html'

def fetch_page(url):
    """Загружает HTML-страницу."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    response = requests.get(url, timeout=30, headers=headers)
    response.raise_for_status()
    response.encoding = 'utf-8'
    return response.text

def extract_adjectives(html):
    """Извлекает прилагательные из HTML."""
    adjectives = []
    
    # Ищем все слова в тексте между <p>...</p>
    # Паттерн: слова на русском, разделённые <br /> или переводом строки
    # Проще: ищем все русские слова в тексте, но чтобы не хватать лишнее, ищем в определённом контексте
    
    # Вариант 1: Ищем по паттерну после тега <p> и до </p>
    # Но там много мусора, лучше искать по списку из файла, но мы парсим страницу
    
    # Ищем все русские слова (буквы от А до Я, включая Ё)
    # Слова должны быть отделены переносом строки или <br />
    pattern = re.compile(r'<br\s*/?>\s*([А-ЯЁа-яё\-]+)', re.IGNORECASE)
    matches = pattern.findall(html)
    
    for match in matches:
        word = match.strip()
        # Проверяем, что слово не слишком короткое и не содержит цифр
        if len(word) > 1 and word.isalpha():
            # Приводим к нижнему регистру (они и так в нижнем)
            adjectives.append(word.lower())
    
    # Вариант 2: Если через <br /> не нашли, пробуем искать просто в тексте
    if not adjectives:
        # Ищем текст внутри абзацев
        p_pattern = re.compile(r'<p>(.*?)</p>', re.DOTALL)
        p_matches = p_pattern.findall(html)
        for p_text in p_matches:
            # Ищем русские слова в абзаце
            words = re.findall(r'([А-ЯЁа-яё\-]{2,})', p_text)
            for w in words:
                if len(w) > 1 and w.isalpha():
                    adjectives.append(w.lower())
    
    return adjectives

def remove_duplicates(adjectives):
    """Удаляет дубликаты, сохраняя порядок."""
    seen = set()
    result = []
    for word in adjectives:
        if word not in seen:
            seen.add(word)
            result.append(word)
    return result

def capitalize_words(adjectives):
    """Преобразует слова в формат с большой буквы (первая буква заглавная, остальные строчные)."""
    return [word.capitalize() for word in adjectives]

def generate_insert_sql(adjectives, batch_size=500):
    """Генерирует SQL INSERT запросы."""
    if not adjectives:
        return ""
    
    sql_parts = []
    total = len(adjectives)
    
    for i in range(0, total, batch_size):
        batch = adjectives[i:i+batch_size]
        
        sql = f"""-- Прилагательные (часть {i//batch_size + 1}/{ (total + batch_size - 1)//batch_size })
INSERT OR IGNORE INTO UltraWords (value, typeId, partOfSpeechId, isDeclinable, link, DateTimeSaving, Popularity, IsModern, Comment, TypeId)
SELECT
    value,
    TypeId,
    {PART_OF_SPEECH_ID} AS partOfSpeechId,
    1 AS isDeclinable,
    '{LINK}' AS link,
    datetime('now', 'localtime') AS DateTimeSaving,
    popularity,
    isModern,
    Comment
FROM (
"""
        
        union_parts = []
        for word in batch:
            union_parts.append(f"    SELECT '{word}' AS value, 1 as popularity, 1 as isModern, NULL as Comment, 7 as TypeId")
        
        sql += " UNION ALL\n".join(union_parts)
        sql += "\n);\n"
        
        sql_parts.append(sql)
    
    return "\n".join(sql_parts)

def main():
    print("🔍 Загрузка страницы...")
    html = fetch_page(BASE_URL)
    
    print("📝 Извлечение прилагательных...")
    adjectives = extract_adjectives(html)
    
    print(f"   Найдено слов: {len(adjectives)}")
    
    print("🔄 Удаление дубликатов...")
    adjectives = remove_duplicates(adjectives)
    
    print(f"   Уникальных слов: {len(adjectives)}")

    print("🔠 Преобразование в формат с большой буквы...")
    adjectives = capitalize_words(adjectives)
    
    print("📄 Генерация SQL...")
    sql = generate_insert_sql(adjectives, BATCH_SIZE)
    
    print(f"💾 Сохранение в {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("-- Прилагательные из списка на codenlp.ru\n")
        f.write(f"-- Источник: {BASE_URL}\n")
        f.write(f"-- Всего слов: {len(adjectives)}\n")
        f.write(f"-- Дата генерации: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(sql)
    
    print(f"✅ Готово! Файл {OUTPUT_FILE} создан.")
    print(f"   Всего прилагательных: {len(adjectives)}")

if __name__ == '__main__':
    main()