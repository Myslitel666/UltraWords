SELECT CASE WHEN SUBSTR(:word, -1) NOT IN ('а', 'я', 'ь', 'ё', 'у') -- Оканчивается на согласную
  AND :word NOT LIKE '% %'
  AND :word not in ('Христос','Павел')
  AND SUBSTR(:word, -2) <> 'ов'
THEN 
  CASE WHEN :case = 1 -- Именительный падеж
  THEN 
    CASE WHEN SUBSTR(:word, -1) <> 'й' -- не на икраткое 
      THEN :word || 'ов'
    ELSE -- на икраткое
      SUBSTR(:word, 1, LENGTH(:word) - 1) || 'ев'
    END
  WHEN :case = 2 -- Родительный падеж
  THEN 
    CASE WHEN SUBSTR(:word, -1) <> 'й' -- не на икраткое 
      THEN :word || 'ова'
    ELSE -- на икраткое
      SUBSTR(:word, 1, LENGTH(:word) - 1) || 'ева'
    END
  WHEN :case = 3 -- Дательный падеж
  THEN 
    CASE WHEN SUBSTR(:word, -1) <> 'й' -- не на икраткое 
      THEN :word || 'ову'
    ELSE -- на икраткое
      SUBSTR(:word, 1, LENGTH(:word) - 1) || 'еву'
    END
  WHEN :case = 4 -- Винительный падеж
  THEN 
    CASE WHEN SUBSTR(:word, -1) <> 'й' -- не на икраткое 
      THEN :word || 'ов'
    ELSE -- на икраткое
      SUBSTR(:word, 1, LENGTH(:word) - 1) || 'ев'
    END
  WHEN :case = 5 -- Творительный падеж
  THEN 
    CASE WHEN SUBSTR(:word, -1) <> 'й' -- не на икраткое 
      THEN :word || 'овым'
    ELSE -- на икраткое
      SUBSTR(:word, 1, LENGTH(:word) - 1) || 'еву'
    END
  WHEN :case = 6 -- Предложный падеж
  THEN 
    CASE WHEN SUBSTR(:word, -1) <> 'й' -- не на икраткое 
      THEN :word || 'ове'
    ELSE -- на икраткое
      SUBSTR(:word, 1, LENGTH(:word) - 1) || 'еве'
    END
  ELSE
    :word
  END
ELSE -- Исключения
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
  WHEN SUBSTR(:word, -1) = 'у'
  THEN 
    CASE WHEN :case = 1 -- Именительный
      THEN 'Иегуев'
    WHEN :case = 2 -- Родительный
      THEN 'Иегуева'
    WHEN :case = 3 -- Дательный падеж
      THEN 'Иегуеву'
    WHEN :case = 4 -- Винительный падеж
      THEN 'Иегуев'
    WHEN :case = 5 -- Творительный падеж
      THEN 'Иегуевым'
    WHEN :case = 6 -- Предложный падеж
      THEN 'Иегуеве'
    ELSE -- Иной падеж
      'Иегуев'
    END
  ELSE -- Если ни одно из исключений
    :word
  END
END
