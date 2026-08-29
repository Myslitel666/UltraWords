from mawo_pymorphy3 import create_analyzer

# Создаем анализатор
analyzer = create_analyzer()

# Анализируем слово
word = "мамы"
parse_result = analyzer.parse(word)[0]  # Берем первый вариант разбора

# Получаем начальную форму
normal_form = parse_result.normal_form
print(f"Начальная форма: {normal_form}")  # Выведет: красивый

# Получаем часть речи (POS-тег)
pos_tag = parse_result.tag.POS
print(f"Часть речи (POS-тег): {pos_tag}")  # Выведет: ADJF (имя прилагательное)