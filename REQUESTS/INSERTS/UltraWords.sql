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

-- Неметаллы (химические элементы с агрегатным состоянием)
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


-- ============================================================
-- ЧАСТЬ 5: ЦВЕТА (Н – Я)
-- ============================================================
INSERT OR IGNORE INTO UltraWords (value, typeId, partOfSpeechId, isDeclinable, link, comment, DateTimeSaving)
SELECT
    value,
    (SELECT id FROM Types WHERE value = 'Цвета и оттенки') AS typeId,
    (SELECT id FROM PartsOfSpeech WHERE value = 'Прилагательное') AS partOfSpeechId,
    1 AS isDeclinable,
    'https://colorscheme.ru/color-names.html' AS link,
    NULL AS comment,
    datetime('now', 'localtime') AS DateTimeSaving
FROM (
    SELECT 'Черновато-красный' AS value UNION ALL
    SELECT 'Черновато-пурпурный' UNION ALL
    SELECT 'Черновато-синий' UNION ALL
    SELECT 'Черный' UNION ALL
    SELECT 'Черный янтарь' UNION ALL
    SELECT 'Чертополох' UNION ALL
    SELECT 'Чертополох Крайола' UNION ALL
    SELECT 'Шамуа' UNION ALL
    SELECT 'Шапка Деда Мороза' UNION ALL
    SELECT 'Шапка Санта-Клауса' UNION ALL
    SELECT 'Шартрез' UNION ALL
    SELECT 'Шафраново-желтый' UNION ALL
    SELECT 'Шафрановый' UNION ALL
    SELECT 'Шелковица Крайола' UNION ALL
    SELECT 'Шокирующий розовый Крайола' UNION ALL
    SELECT 'Шоколадно-коричневый' UNION ALL
    SELECT 'Шоколадный' UNION ALL
    SELECT 'Экстравагантный розовый Крайола' UNION ALL
    SELECT 'Электрик' UNION ALL
    SELECT 'Электрик лайм' UNION ALL
    SELECT 'Электрик лайм Крайола' UNION ALL
    SELECT 'Ядовито-зеленый' UNION ALL
    SELECT 'Янтарный' UNION ALL
    SELECT 'Яркий желто-зеленый' UNION ALL
    SELECT 'Яркий желто-розовый' UNION ALL
    SELECT 'Яркий зеленовато-желтый' UNION ALL
    SELECT 'Яркий зеленый' UNION ALL
    SELECT 'Яркий красно-оранжевый' UNION ALL
    SELECT 'Яркий красно-пурпурный' UNION ALL
    SELECT 'Яркий красный' UNION ALL
    SELECT 'Яркий оранжево-желтый' UNION ALL
    SELECT 'Яркий оранжевый' UNION ALL
    SELECT 'Яркий пурпурно-красный' UNION ALL
    SELECT 'Яркий пурпурный' UNION ALL
    SELECT 'Яркий синевато-зеленый' UNION ALL
    SELECT 'Яркий фиолетовый Крайола' UNION ALL
    SELECT 'Ярко-бирюзовый' UNION ALL
    SELECT 'Ярко-желтый' UNION ALL
    SELECT 'Ярко-зеленый' UNION ALL
    SELECT 'Ярко-мандариновый' UNION ALL
    SELECT 'Ярко-розовый' UNION ALL
    SELECT 'Ярко-синий' UNION ALL
    SELECT 'Ярко-сиреневый' UNION ALL
    SELECT 'Ярко-фиолетовый'
);