class WordTransformer:
    # Словарь падежей
    CASES = {
        'им': 'Именительный',
        'род': 'Родительный',
        'дат': 'Дательный',
        'вин': 'Винительный',
        'твор': 'Творительный',
        'пр': 'Предложный'
    }

    def __init__(self, ultra_words):
        """
        Инициализация трансформера
        
        Args:
            ultra_words: объект класса UltraWords (содержит данные о словах)
        """
        self.ultra_words = ultra_words

    def get_word_info(self, word: str) -> Optional[Dict]:
        for w in self.ultra_words:
            if w['value'] == word:
                return {
                    'id': w['id'],
                    'value': w['value'],
                    'type_id': w['type_id'],
                    'part_of_speech_id': w.get('part_of_speech_id', 1),
                    'is_declinable': w.get('is_declinable', 1),
                    'comment': w.get('comment', ''),
                    'pos_name': self.POS_NAMES.get(w.get('type_id', 1), 'Неизвестно')
                }
        return None