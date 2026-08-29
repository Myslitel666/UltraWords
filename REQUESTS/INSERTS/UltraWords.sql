-- Запрос с вариативностью по частям речи (сузествительное/прилагательное)
-- Регионы России (краткие названия)
INSERT OR IGNORE INTO UltraWords (value, typeId, partOfSpeechId, isDeclinable, link, comment, DateTimeSaving)
SELECT
    value,
    6 AS typeId,
    partOfSpeechId,
    1 AS isDeclinable,
    'https://www.consultant.ru/document/cons_doc_LAW_108669/88a12659e7cc781c56303430d98ae6c8a683892a/' AS link,
    comment,
    datetime('now', 'localtime') AS DateTimeSaving
FROM (
    -- Республики (существительные, partOfSpeechId = 1)
    SELECT 'Адыгея' AS value, 1 AS partOfSpeechId, 'Российские/Республики' AS comment UNION ALL
    SELECT 'Башкортостан', 1, 'Российские/Республики' UNION ALL
    SELECT 'Бурятия', 1, 'Российские/Республики' UNION ALL
    SELECT 'Алтай', 1, 'Российские/Республики' UNION ALL
    SELECT 'Дагестан', 1, 'Российские/Республики' UNION ALL
    SELECT 'Ингушетия', 1, 'Российские/Республики' UNION ALL
    SELECT 'Кабардино-Балкарская', 2, 'Российские/Республики' UNION ALL
    SELECT 'Калмыкия', 1, 'Российские/Республики' UNION ALL
    SELECT 'Карачаево-Черкесская', 2, 'Российские/Республики' UNION ALL
    SELECT 'Карелия', 1, 'Российские/Республики' UNION ALL
    SELECT 'Коми', 1, 'Российские/Республики' UNION ALL
    SELECT 'Марий Эл', 1, 'Российские/Республики' UNION ALL
    SELECT 'Мордовия', 1, 'Российские/Республики' UNION ALL
    SELECT 'Саха', 1, 'Российские/Республики' UNION ALL
    SELECT 'Якутия', 1, 'Российские/Республики' UNION ALL
    SELECT 'Северная Осетия', 1, 'Российские/Республики' UNION ALL
    SELECT 'Алания', 1, 'Российские/Республики' UNION ALL
    SELECT 'Татарстан', 1, 'Российские/Республики' UNION ALL
    SELECT 'Тыва', 1, 'Российские/Республики' UNION ALL
    SELECT 'Удмуртская', 2, 'Российские/Республики' UNION ALL
    SELECT 'Хакасия', 1, 'Российские/Республики' UNION ALL
    SELECT 'Чеченская', 2, 'Российские/Республики' UNION ALL
    SELECT 'Чувашская', 2, 'Российские/Республики' UNION ALL

    -- Края (прилагательные, partOfSpeechId = 2)
    SELECT 'Алтайский', 2, 'Российские/Края' UNION ALL
    SELECT 'Краснодарский', 2, 'Российские/Края' UNION ALL
    SELECT 'Красноярский', 2, 'Российские/Края' UNION ALL
    SELECT 'Приморский', 2, 'Российские/Края' UNION ALL
    SELECT 'Ставропольский', 2, 'Российские/Края' UNION ALL
    SELECT 'Хабаровский', 2, 'Российские/Края' UNION ALL
    SELECT 'Камчатский', 2, 'Российские/Края' UNION ALL
    SELECT 'Пермский', 2, 'Российские/Края' UNION ALL
    SELECT 'Забайкальский', 2, 'Российские/Края' UNION ALL

    -- Области (прилагательные, partOfSpeechId = 2)
    SELECT 'Амурская', 2, 'Российские/Области' UNION ALL
    SELECT 'Архангельская', 2, 'Российские/Области' UNION ALL
    SELECT 'Астраханская', 2, 'Российские/Области' UNION ALL
    SELECT 'Белгородская', 2, 'Российские/Области' UNION ALL
    SELECT 'Брянская', 2, 'Российские/Области' UNION ALL
    SELECT 'Владимирская', 2, 'Российские/Области' UNION ALL
    SELECT 'Волгоградская', 2, 'Российские/Области' UNION ALL
    SELECT 'Вологодская', 2, 'Российские/Области' UNION ALL
    SELECT 'Воронежская', 2, 'Российские/Области' UNION ALL
    SELECT 'Ивановская', 2, 'Российские/Области' UNION ALL
    SELECT 'Иркутская', 2, 'Российские/Области' UNION ALL
    SELECT 'Калининградская', 2, 'Российские/Области' UNION ALL
    SELECT 'Калужская', 2, 'Российские/Области' UNION ALL
    SELECT 'Кемеровская', 2, 'Российские/Области' UNION ALL
    SELECT 'Кировская', 2, 'Российские/Области' UNION ALL
    SELECT 'Костромская', 2, 'Российские/Области' UNION ALL
    SELECT 'Курганская', 2, 'Российские/Области' UNION ALL
    SELECT 'Курская', 2, 'Российские/Области' UNION ALL
    SELECT 'Ленинградская', 2, 'Российские/Области' UNION ALL
    SELECT 'Липецкая', 2, 'Российские/Области' UNION ALL
    SELECT 'Магаданская', 2, 'Российские/Области' UNION ALL
    SELECT 'Московская', 2, 'Российские/Области' UNION ALL
    SELECT 'Мурманская', 2, 'Российские/Области' UNION ALL
    SELECT 'Нижегородская', 2, 'Российские/Области' UNION ALL
    SELECT 'Новгородская', 2, 'Российские/Области' UNION ALL
    SELECT 'Новосибирская', 2, 'Российские/Области' UNION ALL
    SELECT 'Омская', 2, 'Российские/Области' UNION ALL
    SELECT 'Оренбургская', 2, 'Российские/Области' UNION ALL
    SELECT 'Орловская', 2, 'Российские/Области' UNION ALL
    SELECT 'Пензенская', 2, 'Российские/Области' UNION ALL
    SELECT 'Псковская', 2, 'Российские/Области' UNION ALL
    SELECT 'Ростовская', 2, 'Российские/Области' UNION ALL
    SELECT 'Рязанская', 2, 'Российские/Области' UNION ALL
    SELECT 'Самарская', 2, 'Российские/Области' UNION ALL
    SELECT 'Саратовская', 2, 'Российские/Области' UNION ALL
    SELECT 'Сахалинская', 2, 'Российские/Области' UNION ALL
    SELECT 'Свердловская', 2, 'Российские/Области' UNION ALL
    SELECT 'Смоленская', 2, 'Российские/Области' UNION ALL
    SELECT 'Тамбовская', 2, 'Российские/Области' UNION ALL
    SELECT 'Тверская', 2, 'Российские/Области' UNION ALL
    SELECT 'Томская', 2, 'Российские/Области' UNION ALL
    SELECT 'Тульская', 2, 'Российские/Области' UNION ALL
    SELECT 'Тюменская', 2, 'Российские/Области' UNION ALL
    SELECT 'Ульяновская', 2, 'Российские/Области' UNION ALL
    SELECT 'Челябинская', 2, 'Российские/Области' UNION ALL
    SELECT 'Ярославская', 2, 'Российские/Области' UNION ALL

    -- Города федерального значения (существительные, partOfSpeechId = 1)
    SELECT 'Москва', 1, 'Российские/Города' UNION ALL
    SELECT 'Санкт-Петербург', 1, 'Российские/Города' UNION ALL

    -- Автономные образования (прилагательные, partOfSpeechId = 2)
    SELECT 'Еврейская', 2, 'Российские/Автономные области' UNION ALL
    SELECT 'Ненецкий', 2, 'Российские/Автономные округа' UNION ALL
    SELECT 'Ханты-Мансийский', 2, 'Российские/Автономные округа' UNION ALL
    SELECT 'Чукотский', 2, 'Российские/Автономные округа' UNION ALL
    SELECT 'Ямало-Ненецкий', 2, 'Российские/Автономные округа' UNION ALL

    -- Особые территории (существительное, partOfSpeechId = 1)
    SELECT 'Байконур', 1, 'Российские/Особые территории'
);

-- Запрос с одинаковыми частями речи
INSERT OR IGNORE INTO UltraWords (value, typeId, partOfSpeechId, isDeclinable, link, comment, DateTimeSaving)
SELECT
    value,
    (SELECT id FROM Types WHERE value = 'Наука') AS typeId,
    (SELECT id FROM PartsOfSpeech WHERE value = 'Существительное') AS partOfSpeechId,
    1 AS isDeclinable,
    'https://yaruse.ru/posts/show/id/1253' AS link,
    comment,
    datetime('now', 'localtime') AS DateTimeSaving
FROM (
    SELECT 'Азот' AS value, 'Химия/Неметаллы/Газ' AS comment UNION ALL
    SELECT 'Водород', 'Химия/Неметаллы/Газ' UNION ALL
    SELECT 'Гелий', 'Химия/Неметаллы/Газ' UNION ALL
    SELECT 'Кислород', 'Химия/Неметаллы/Газ' UNION ALL
    SELECT 'Неон', 'Химия/Неметаллы/Газ' UNION ALL
    SELECT 'Аргон', 'Химия/Неметаллы/Газ' UNION ALL
    SELECT 'Криптон', 'Химия/Неметаллы/Газ' UNION ALL
    SELECT 'Ксенон', 'Химия/Неметаллы/Газ' UNION ALL
    SELECT 'Радон', 'Химия/Неметаллы/Газ' UNION ALL
    SELECT 'Фтор', 'Химия/Неметаллы/Газ' UNION ALL
    SELECT 'Хлор', 'Химия/Неметаллы/Газ' UNION ALL
    SELECT 'Фосфор', 'Химия/Неметаллы/Твёрдое вещество' UNION ALL
    SELECT 'Сера', 'Химия/Неметаллы/Твёрдое вещество' UNION ALL
    SELECT 'Йод', 'Химия/Неметаллы/Твёрдое вещество' UNION ALL
    SELECT 'Углерод', 'Химия/Неметаллы/Твёрдое вещество' UNION ALL
    SELECT 'Кремний', 'Химия/Неметаллы/Твёрдое вещество' UNION ALL
    SELECT 'Бор', 'Химия/Неметаллы/Твёрдое вещество' UNION ALL
    SELECT 'Селен', 'Химия/Неметаллы/Твёрдое вещество' UNION ALL
    SELECT 'Теллур', 'Химия/Неметаллы/Твёрдое вещество' UNION ALL
    SELECT 'Мышьяк', 'Химия/Неметаллы/Твёрдое вещество' UNION ALL
    SELECT 'Бром', 'Химия/Неметаллы/Жидкость'
);