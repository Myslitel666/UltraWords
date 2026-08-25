-- Наука/Химия/Металлы
INSERT OR IGNORE INTO UltraWords (value, typeId, partOfSpeechId, isDeclinable, link, comment, DateTimeSaving)
SELECT
    value,
    (SELECT id FROM Types WHERE value = 'Наука') AS typeId,
    (SELECT id FROM PartsOfSpeech WHERE value = 'Существительное') AS partOfSpeechId,
    1 AS isDeclinable,
    'https://yaruse.ru/posts/show/id/1253' AS link,
    'Химия/Металлы' as comment,
    datetime('now', 'localtime') AS DateTimeSaving
FROM (
    SELECT 'Алюминий' AS value UNION ALL
    SELECT 'Барий' UNION ALL
    SELECT 'Берилий' UNION ALL
    SELECT 'Ванадий' UNION ALL
    SELECT 'Висмут' UNION ALL
    SELECT 'Вольфрам' UNION ALL
    SELECT 'Галий' UNION ALL
    SELECT 'Гафний' UNION ALL
    SELECT 'Германий' UNION ALL
    SELECT 'Железо' UNION ALL
    SELECT 'Золото' UNION ALL
    SELECT 'Индий' UNION ALL
    SELECT 'Иридий' UNION ALL
    SELECT 'Кадмий' UNION ALL
    SELECT 'Калий' UNION ALL
    SELECT 'Кальций' UNION ALL
    SELECT 'Кобальт' UNION ALL
    SELECT 'Литий' UNION ALL
    SELECT 'Магний' UNION ALL
    SELECT 'Марганец' UNION ALL
    SELECT 'Медь' UNION ALL
    SELECT 'Молибден' UNION ALL
    SELECT 'Натрий' UNION ALL
    SELECT 'Никель' UNION ALL
    SELECT 'Ниобий' UNION ALL
    SELECT 'Олово' UNION ALL
    SELECT 'Осмий' UNION ALL
    SELECT 'Палладий' UNION ALL
    SELECT 'Платина' UNION ALL
    SELECT 'Рений' UNION ALL
    SELECT 'Родий' UNION ALL
    SELECT 'Ртуть' UNION ALL
    SELECT 'Рубидий' UNION ALL
    SELECT 'Рутений' UNION ALL
    SELECT 'Свинец' UNION ALL
    SELECT 'Серебро' UNION ALL
    SELECT 'Стронций' UNION ALL
    SELECT 'Сурьма' UNION ALL
    SELECT 'Таллий' UNION ALL
    SELECT 'Тантал' UNION ALL
    SELECT 'Титан' UNION ALL
    SELECT 'Уран' UNION ALL
    SELECT 'Хром' UNION ALL
    SELECT 'Цинк' UNION ALL
    SELECT 'Цирконий'
);