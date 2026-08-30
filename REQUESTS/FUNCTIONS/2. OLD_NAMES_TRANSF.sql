SELECT CASE WHEN SUBSTR(:word, -1) NOT IN ('а', 'я', 'ь', 'ё', 'е', 'у') -- Оканчивается на согласную
  AND :word NOT LIKE '% %'
  AND :word not in ('Христов','Павлов','Иегуев')
  --AND SUBSTR(:word, -2) <> 'ов'
THEN 
  CASE WHEN :case = 1 -- Именительный падеж
  THEN 
    CASE WHEN :q = 1 -- единственное число
      THEN :word 
      ELSE :word || 'ы' -- множественное
    END
  WHEN :case = 2 -- Родительный падеж
  THEN 
    CASE WHEN :q = 1 -- единственное число
      THEN :word || 'а' 
      ELSE :word || 'ых' -- множественное
    END
  WHEN :case = 3 -- Дательный падеж
  THEN
    CASE WHEN :q = 1 -- единственное число
      THEN :word || 'у' 
      ELSE :word || 'ым' -- множественное
    END
  WHEN :case = 4 -- Винительный падеж
  THEN 
    CASE WHEN :q = 1 -- единственное число
      THEN :word
      ELSE :word || 'ы' -- множественное
    END
  WHEN :case = 5 -- Творительный падеж
  THEN 
    CASE WHEN :q = 1 -- единственное число
      THEN :word || 'ым'
      ELSE :word || 'ыми' -- множественное
    END
  WHEN :case = 6 -- Предложный падеж
  THEN 
    CASE WHEN :q = 1 -- единственное число
      THEN :word || 'е'
      ELSE :word || 'ых' -- множественное
    END
  ELSE -- Ни один из падежей
    :word
  END
ELSE -- Исключения
  CASE WHEN :q = 1 THEN -- Единственное число
    CASE WHEN :word = 'Христов'
    THEN 
      CASE WHEN :case = 1 -- Именительный
        THEN :word
      WHEN :case = 2 -- Родительный
        THEN 'Христова'
      WHEN :case = 3 -- Дательный падеж
        THEN 'Христову'
      WHEN :case = 4 -- Винительный падеж
        THEN 'Христов'
      WHEN :case = 5 -- Творительный падеж
        THEN 'Христовым'
      WHEN :case = 6 -- Предложный падеж
        THEN 'Христе'
      ELSE -- Иной падеж
        :word
      END
    WHEN :word = 'Павлов'
    THEN 
      CASE WHEN :case = 1 -- Именительный
        THEN :word
      WHEN :case = 2 -- Родительный
        THEN 'Павлова'
      WHEN :case = 3 -- Дательный падеж
        THEN 'Павлову'
      WHEN :case = 4 -- Винительный падеж
        THEN 'Павлов'
      WHEN :case = 5 -- Творительный падеж
        THEN 'Павловым'
      WHEN :case = 6 -- Предложный падеж
        THEN 'Павлове'
      ELSE -- Иной падеж
        :word
      END
    WHEN :word = 'Иегуев' -- Иегу
    THEN 
      CASE WHEN :case = 1 -- Именительный
        THEN :word
      WHEN :case = 2 -- Родительный
        THEN :word || 'а'
      WHEN :case = 3 -- Дательный падеж
        THEN :word || 'у'
      WHEN :case = 4 -- Винительный падеж
        THEN :word 
      WHEN :case = 5 -- Творительный падеж
        THEN :word || 'ым'
      WHEN :case = 6 -- Предложный падеж
        THEN :word || 'е'
      ELSE -- Иной падеж
        :word
      END
    ELSE -- Иное исключение
      :word
    END
  ELSE -- Множественное число
    CASE WHEN :word = 'Христов'
    THEN 
      CASE WHEN :case = 1 -- Именительный
        THEN 'Христовы'
      WHEN :case = 2 -- Родительный
        THEN 'Христовых'
      WHEN :case = 3 -- Дательный падеж
        THEN 'Христовым'
      WHEN :case = 4 -- Винительный падеж
        THEN 'Христовы'
      WHEN :case = 5 -- Творительный падеж
        THEN 'Христовыми'
      WHEN :case = 6 -- Предложный падеж
        THEN 'Христовом'
      ELSE -- Иной падеж
        'Христос'
      END
    WHEN :word = 'Павлов'
    THEN 
      CASE WHEN :case = 1 -- Именительный
        THEN 'Павловы'
      WHEN :case = 2 -- Родительный
        THEN 'Павловых'
      WHEN :case = 3 -- Дательный падеж
        THEN 'Павловым'
      WHEN :case = 4 -- Винительный падеж
        THEN 'Павловы'
      WHEN :case = 5 -- Творительный падеж
        THEN 'Павловыми'
      WHEN :case = 6 -- Предложный падеж
        THEN 'Павловых'
      ELSE -- Иной падеж
        :word
      END
    WHEN :word = 'Иегуев'
    THEN 
      CASE WHEN :case = 1 -- Именительный
        THEN :word || 'ы'
      WHEN :case = 2 -- Родительный
        THEN :word || 'ых'
      WHEN :case = 3 -- Дательный падеж
        THEN :word || 'ым'
      WHEN :case = 4 -- Винительный падеж
        THEN :word || 'ы'
      WHEN :case = 5 -- Творительный падеж
        THEN :word || 'ыми'
      WHEN :case = 6 -- Предложный падеж
        THEN :word || 'ых'
      ELSE -- Иной падеж
        :word
      END
    ELSE -- Если ни одно из исключений
      :word
    END
  END
END
