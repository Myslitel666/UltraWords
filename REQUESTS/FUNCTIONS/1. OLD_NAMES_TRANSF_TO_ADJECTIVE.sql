SELECT CASE WHEN SUBSTR(:word, -1) NOT IN ('а', 'я', 'ь', 'ё', 'у') -- Оканчивается на согласную
  AND :word NOT LIKE '% %'
  AND :word not in ('Христос','Павел')
  AND SUBSTR(:word, -2) <> 'ов'
THEN 
  CASE WHEN :case = 1 -- Именительный падеж
  THEN 
    CASE WHEN SUBSTR(:word, -1) <> 'й' -- не на икраткое 
    THEN CASE WHEN :q = 1 -- единственное число
        THEN :word || 'ов' 
        ELSE :word || 'овы' -- множественное
      END
    ELSE -- на икраткое
      CASE WHEN :q = 1 -- единственное число
        THEN SUBSTR(:word, 1, LENGTH(:word) - 1) || 'ев' 
        ELSE SUBSTR(:word, 1, LENGTH(:word) - 1) || 'евы' -- множественное
      END
    END
  WHEN :case = 2 -- Родительный падеж
  THEN 
    CASE WHEN SUBSTR(:word, -1) <> 'й' -- не на икраткое 
      THEN CASE WHEN :q = 1 -- единственное число
        THEN :word || 'ова' 
        ELSE :word || 'овых' -- множественное
      END
    ELSE -- на икраткое
      CASE WHEN :q = 1 -- единственное число
        THEN SUBSTR(:word, 1, LENGTH(:word) - 1) || 'ева'
        ELSE SUBSTR(:word, 1, LENGTH(:word) - 1) || 'евых' -- множественное
      END
    END
  WHEN :case = 3 -- Дательный падеж
  THEN
    CASE WHEN SUBSTR(:word, -1) <> 'й' -- не на икраткое 
      THEN CASE WHEN :q = 1 -- единственное число
        THEN :word || 'ову' 
        ELSE :word || 'овым' -- множественное
      END
    ELSE -- на икраткое
      CASE WHEN :q = 1 -- единственное число
        THEN SUBSTR(:word, 1, LENGTH(:word) - 1) || 'еву'
        ELSE SUBSTR(:word, 1, LENGTH(:word) - 1) || 'евым' -- множественное
      END
    END
  WHEN :case = 4 -- Винительный падеж
  THEN 
    CASE WHEN SUBSTR(:word, -1) <> 'й' -- не на икраткое 
      THEN CASE WHEN :q = 1 -- единственное число
        THEN :word || 'ов'
        ELSE :word || 'овы' -- множественное
      END
    ELSE -- на икраткое
      CASE WHEN :q = 1 -- единственное число
        THEN SUBSTR(:word, 1, LENGTH(:word) - 1) || 'ев'
        ELSE SUBSTR(:word, 1, LENGTH(:word) - 1) || 'евы' -- множественное
      END
    END
  WHEN :case = 5 -- Творительный падеж
  THEN 
    CASE WHEN SUBSTR(:word, -1) <> 'й' -- не на икраткое 
      THEN CASE WHEN :q = 1 -- единственное число
        THEN :word || 'овым'
        ELSE :word || 'овыми' -- множественное
      END
    ELSE -- на икраткое
      CASE WHEN :q = 1 -- единственное число
        THEN SUBSTR(:word, 1, LENGTH(:word) - 1) || 'евовым'
        ELSE SUBSTR(:word, 1, LENGTH(:word) - 1) || 'евовыми' -- множественное
      END
    END
  WHEN :case = 6 -- Предложный падеж
  THEN 
    CASE WHEN SUBSTR(:word, -1) <> 'й' -- не на икраткое 
      THEN CASE WHEN :q = 1 -- единственное число
        THEN :word || 'ове'
        ELSE :word || 'овых' -- множественное
      END
    ELSE -- на икраткое
      CASE WHEN :q = 1 -- единственное число
        THEN SUBSTR(:word, 1, LENGTH(:word) - 1) || 'еве'
        ELSE SUBSTR(:word, 1, LENGTH(:word) - 1) || 'евых' -- множественное
      END
    END
  ELSE -- Ни один из падежей
    :word
  END
ELSE -- Исключения
  CASE WHEN :q = 1 THEN -- Единственное число
    CASE WHEN :word = 'Христос'
    THEN 
      CASE WHEN :case = 1 -- Именительный
        THEN 'Христов'
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
      'Христос'
      END
    WHEN :word = 'Павел'
    THEN 
      CASE WHEN :case = 1 -- Именительный
        THEN 'Павлов'
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
        'Павлов'
      END
    WHEN SUBSTR(:word, -1) = 'у' -- Иегу
    THEN 
      CASE WHEN :case = 1 -- Именительный
        THEN :word || 'ев'
      WHEN :case = 2 -- Родительный
        THEN :word || 'ева'
      WHEN :case = 3 -- Дательный падеж
        THEN :word || 'еву'
      WHEN :case = 4 -- Винительный падеж
        THEN :word || 'ев' 
      WHEN :case = 5 -- Творительный падеж
        THEN :word || 'евым'
      WHEN :case = 6 -- Предложный падеж
        THEN :word || 'еве'
      ELSE -- Иной падеж
        :word || 'ев'
      END
    ELSE
      :word
    END
  ELSE -- Множественное число
    CASE WHEN :word = 'Христос'
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
    WHEN :word = 'Павел'
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
        'Павлов'
      END
    WHEN SUBSTR(:word, -1) = 'у'
    THEN 
      CASE WHEN :case = 1 -- Именительный
        THEN :word || 'евы'
      WHEN :case = 2 -- Родительный
        THEN :word || 'евых'
      WHEN :case = 3 -- Дательный падеж
        THEN :word || 'евым'
      WHEN :case = 4 -- Винительный падеж
        THEN :word || 'евы'
      WHEN :case = 5 -- Творительный падеж
        THEN :word || 'евыми'
      WHEN :case = 6 -- Предложный падеж
        THEN :word || 'евых'
      ELSE -- Иной падеж
        :word || 'ев'
      END
    ELSE -- Если ни одно из исключений
      :word
    END
  END
END
