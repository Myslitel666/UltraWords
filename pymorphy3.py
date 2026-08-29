from mawo_pymorphy3 import create_analyzer
import sqlite3

# Подключаемся к базе
conn = sqlite3.connect('UltraWords.db')
cursor = conn.cursor()

# Создаем анализатор
analyzer = create_analyzer()

# Словарь для преобразования POS-тегов в человекочитаемый вид
POS_MAP = {
    'NOUN': 'Существительное',
    'ADJF': 'Прилагательное',
    'ADJS': 'Прилагательное (краткое)',
    'VERB': 'Глагол',
    'INFN': 'Глагол (инфинитив)',
    'ADVB': 'Наречие',
    'PRTF': 'Причастие',
    'PRTS': 'Причастие (краткое)',
    'GRND': 'Деепричастие',
    'NUMR': 'Числительное',
    'ADJ': 'Прилагательное',
    'NPRO': 'Местоимение',
    'PRED': 'Предикатив',
    'PREP': 'Предлог',
    'CONJ': 'Союз',
    'PRCL': 'Частица',
    'INTJ': 'Междометие',
}

# Список тегов, которые считаем мусором и не выводим
SKIP_TAGS = {'UNKN', 'LATN', 'PNCT', 'NUMB'}

# Читаем первые 1000 строк из таблицы Words, сортируем по Value
cursor.execute('SELECT Id, Value, Link FROM Words Where Link is not null ORDER BY Value LIMIT 5000')
rows = cursor.fetchall()

# Для отслеживания уникальных нормальных форм и их данных
seen_lemmas = {}
result = []

print("Value\t\t\tНормальная форма\t\tЧасть речи\t\tLink")
print("-" * 120)

for row_id, value, link in rows:
    try:
        # Анализируем слово
        parse_result = analyzer.parse(value)[0]
        pos_tag = parse_result.tag.POS
        
        # Пропускаем мусорные теги
        if pos_tag in SKIP_TAGS:
            continue
        
        normal_form = parse_result.normal_form
        
        # Проверяем, не встречалась ли уже эта нормальная форма
        if normal_form in seen_lemmas:
            continue
        
        # Сохраняем в словарь
        seen_lemmas[normal_form] = True
        
        pos_human = POS_MAP.get(pos_tag, pos_tag)
        
        # Выводим слово с большой буквы
        value_capitalized = value.capitalize()
        normal_form_capitalized = normal_form.capitalize()
        
        print(f"{value_capitalized:<20}\t\t{normal_form_capitalized:<20}\t\t{pos_human:<15}\t\t{link}")
        result.append((value_capitalized, normal_form_capitalized, pos_human, link))
        
        # Останавливаемся после 1000 уникальных слов
        if len(result) >= 1000:
            break
            
    except Exception as e:
        # Пропускаем слова с ошибками
        continue

conn.close()
print(f"\nВсего выведено: {len(result)} уникальных слов")