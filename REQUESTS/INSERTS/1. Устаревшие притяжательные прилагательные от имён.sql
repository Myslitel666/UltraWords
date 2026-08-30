-- Обычные слова из файла АВП
INSERT OR IGNORE INTO UltraWords (value, typeId, partOfSpeechId, isDeclinable, link, comment, DateTimeSaving, Popularity, IsModern)
SELECT
    value,
    (SELECT Id FROM Types WHERE Value = 'Имена') AS typeId,
    (SELECT Id FROM PartsOfSpeech WHERE Value = 'Прилагательное') AS partOfSpeechId,
    1 AS isDeclinable,
    'https://azbyka.ru/shemy/imena-biblejskie.shtml' AS link,
    'Библия' AS comment,
    datetime('now', 'localtime') AS DateTimeSaving,
    0 AS Popularity,
    0 AS IsModern
FROM (
    -- ============ СУЩЕСТВИТЕЛЬНЫЕ ============
    SELECT 
      OLD_NAMES_TRANSF_TO_ADJECTIVE(uw.value, c.id, 1) as value, 
      c.value
    FROM UltraWords uw
    JOIN Cases c
      on c.id = 1
    WHERE uw.comment = 'Библия'
      AND SUBSTR(uw.value, -1) not in ('а','я','ь', 'ё')
      AND uw.value NOT LIKE '% %'
      AND SUBSTR(uw.value, -2) <> 'ов'
    ORDER BY uw.value, c.id
);