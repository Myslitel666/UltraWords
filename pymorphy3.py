from pymystem3 import Mystem
import sqlite3

# Подключаемся к базе
conn = sqlite3.connect('UltraWords.db')
cursor = conn.cursor()

# Создаем анализатор Mystem
m = Mystem()

# Словарь для преобразования POS-тегов Mystem в человекочитаемый вид
POS_MAP = {
    'A': 'Прилагательное',
    'ADV': 'Наречие',
    'ADVPRO': 'Наречие-местоимение',
    'ANUM': 'Прилагательное-числительное',
    'APRO': 'Прилагательное-местоимение',
    'COM': 'Часть композита',
    'CONJ': 'Союз',
    'INTJ': 'Междометие',
    'NUM': 'Числительное',
    'PART': 'Частица',
    'PR': 'Предлог',
    'S': 'Существительное',
    'SPRO': 'Местоимение',
    'V': 'Глагол',
    'UNKN': 'Неизвестно',
}

# Список тегов, которые считаем мусором и не выводим
SKIP_TAGS = {'UNKN'}

# Читаем строки из таблицы Words
cursor.execute('SELECT Id, Value, Link FROM Words ORDER BY Value LIMIT 5000')
rows = cursor.fetchall()

# Для отслеживания уникальных нормальных форм
seen_lemmas = {}
result = []

print("Value\t\t\tНормальная форма\t\tЧасть речи\t\tLink")
print("-" * 120)

for row_id, value, link in rows:
    try:
        # Анализируем слово через Mystem
        result_mystem = m.analyze(value)[0]
        
        # Проверяем, есть ли анализ
        if 'analysis' not in result_mystem or not result_mystem['analysis']:
            continue
        
        analysis = result_mystem['analysis'][0]
        
        # Получаем лемму (начальную форму)
        normal_form = analysis.get('lex', value)
        
        # Получаем часть речи
        gr = analysis.get('gr', '')
        if gr:
            # Берём первую часть до запятой — это POS-тег
            pos_tag = gr.split(',')[0]
        else:
            pos_tag = 'UNKN'
        
        # Пропускаем мусорные теги
        if pos_tag in SKIP_TAGS:
            continue
        
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