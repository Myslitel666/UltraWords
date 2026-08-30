class WordTransformer:
    # Словарь падежей
    CASES = {
        1: 'Именительный',
        2: 'Родительный',
        3: 'Дательный',
        4: 'Винительный',
        5: 'Творительный',
        6: 'Предложный'
    }

    # Словарь частей речи
    PartsOfSpeech = {
        1: 'Существительное',
        2: 'Прилагательное',
        3: 'Глагол'
    }

    def __init__(self, ultra_words):
        self.ultra_words = ultra_words

    def transf(self, word_obj, case_id: int, multiplicity: int = 1) -> str:
        word = word_obj['Value']
        pos_id = word_obj.get('PartOfSpeechId', 1)
        type_id = word_obj.get('TypeId', 1)
        
        # Если TypeId = 1 и PartOfSpeechId = 1 (Существительное)
        if type_id == 1 and pos_id == 1:
            if case_id == 1: return word
            elif case_id == 2: return word + 'а' if multiplicity == 1 else word + 'ов'
            elif case_id == 3: return word + 'у' if multiplicity == 1 else word + 'ам'
            elif case_id == 4: return word + 'а' if multiplicity == 1 else word + 'ов'
            elif case_id == 5: return word + 'ом' if multiplicity == 1 else word + 'ами'
            elif case_id == 6: return word + 'е' if multiplicity == 1 else word + 'ах'
        
        # Если TypeId = 1 и PartOfSpeechId = 2 (Прилагательное)
        elif type_id == 1 and pos_id == 2:
            if case_id == 1: return word
            elif case_id == 2: return word + 'ого'
            elif case_id == 3: return word + 'ому'
            elif case_id == 4: return word + 'ый'
            elif case_id == 5: return word + 'ым'
            elif case_id == 6: return word + 'ом'
        
        # Если TypeId = 1 и PartOfSpeechId = 3 (Глагол)
        elif type_id == 1 and pos_id == 3:
            return word
        
        # По умолчанию
        return word