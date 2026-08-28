-- КРИНЖ, который нужно удалять из базы
-- Слова из 2 букв
DELETE FROM WORDS WHERE ID in (
    SELECT DISTINCT ID FROM (
        SELECT ID
        FROM Words
        WHERE LENGTH(value) = 2
          AND value not in ('ад', 'ум', 'ус', 'яд', 'ас', 'ям', 'ос', 'вы', 'ра', 'во', 'ко')
        UNION ALL
        -- Слова, начинающиеся на невозможную букву
        SELECT ID
        FROM Words
        WHERE SUBSTR(lower(value), 1, 1) IN ('й', 'ь', 'ъ', 'ы')
          AND value not like 'йог%'
          AND value not like 'йот%'
          AND value not like 'йод%'
        UNION ALL
        -- Исключаем неадекватные сочетания гласных/согласных
        SELECT ID
        FROM Words
        WHERE (
            value GLOB '[уеъыаоэяиюь][бвгджзйклмнпрстфхцчшщ][бвгджзйклмнпрстфхцчшщ]'
            OR 
            value GLOB '[уеъыаоэяиюь][бвгджзйклмнпрстфхцчшщ][бвгджзйклмнпрстфхцчшщ][бвгджзйклмнпрстфхцчшщ]'
            OR 
            value GLOB '[уеъыаоэяиюь][бвгджзйклмнпрстфхцчшщ][бвгджзйклмнпрстфхцчшщ][бвгджзйклмнпрстфхцчшщ][бвгджзйклмнпрстфхцчшщ]'
            OR
            value GLOB '[уеъыаоэяиюь][уеъыаоэяиюь][уеъыаоэяиюь][бвгджзйклмнпрстфхцчшщ]'
            OR
            value GLOB '[уеъыаоэяиюь][уеъыаоэяиюь][уеъыаоэяиюь]'
            OR
            value GLOB '[уеъыаоэяиюь][уеъыаоэяиюь][уеъыаоэяиюь][уеъыаоэяиюь]'
        )
        AND value not in ('уст','акт', 'иоан', 'иоал')
        UNION ALL
        -- Исключаем слова, которые содержат дефис, но состоят при этом из небольшого количества букв
        SELECT ID FROM Words 
        WHERE value LIKE '%-%'
          AND LENGTH(value) in (3,4,5)
          AND value not in ('из-за')
        UNION ALL
        -- Исключаем все слова, которые содержат дефис вторым или предпоследним символом
        SELECT ID FROM Words 
        WHERE (value LIKE '_-%' AND value NOT LIKE 'в%')
          OR substr(value,-2,1) = '-'
        UNION ALL
        -- Несколько дефисов
        SELECT ID
        FROM Words
        WHERE value LIKE '%-%-%'
          AND value not in (
            'мало-по-малу',
            'ростов-на-дону',
            'рок-н-ролл',
            'рок-н-ролле',
            'свято-троице-сергиева',
            'владимир-на-клязьме',
            'точь-в-точь',
            'славянск-на-кубани'
        )
    )
);