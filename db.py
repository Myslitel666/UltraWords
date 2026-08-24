import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'UltraWords.db')

def get_connection():
    return sqlite3.connect(DB_PATH, timeout=10)

def capitalize_first(s):
    if not s:
        return s
    return s[0].upper() + s[1:] if len(s) > 1 else s.upper()

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    
    # === Справочные таблицы ===
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value TEXT UNIQUE NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PartsOfSpeech (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value TEXT UNIQUE NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value TEXT UNIQUE NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Genders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value TEXT UNIQUE NOT NULL
        )
    ''')
    
    # === Основная таблица (без caseId) ===
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS UltraWords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value TEXT NOT NULL,
            typeId INTEGER NOT NULL,
            link TEXT,
            partOfSpeechId INTEGER,
            isDeclinable BOOLEAN,
            genderId INTEGER,
            UNIQUE(value, typeId),
            FOREIGN KEY (typeId) REFERENCES Types(id) ON DELETE CASCADE,
            FOREIGN KEY (partOfSpeechId) REFERENCES PartsOfSpeech(id) ON DELETE SET NULL,
            FOREIGN KEY (genderId) REFERENCES Genders(id) ON DELETE SET NULL
        )
    ''')
    
    # === Таблица для падежей ===
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS UltraWordsCases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wordId INTEGER NOT NULL,
            caseId INTEGER NOT NULL,
            value TEXT NOT NULL,
            multiplicity BOOLEAN,
            FOREIGN KEY (wordId) REFERENCES UltraWords(id) ON DELETE CASCADE,
            FOREIGN KEY (caseId) REFERENCES Cases(id) ON DELETE CASCADE,
            UNIQUE(wordId, caseId)
        )
    ''')
    
    # === Таблица Words (для совместимости) ===
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            value TEXT UNIQUE NOT NULL
        )
    ''')
    
    # === Представление ===
    cursor.execute('''
        CREATE VIEW IF NOT EXISTS UltraWordsX AS
        SELECT 
            uw.id,
            uw.value AS Word,
            t.value AS Type,
            uw.link AS Link,
            ps.value AS PartOfSpeech,         
            uw.isDeclinable,
            g.value AS Gender
        FROM UltraWords uw
        LEFT JOIN Types t ON uw.typeId = t.id
        LEFT JOIN PartsOfSpeech ps ON uw.partOfSpeechId = ps.id
        LEFT JOIN Genders g ON uw.genderId = g.id
        ORDER BY t.value, uw.value
    ''')
    
    # === Начальное заполнение справочников ===
    cursor.executemany('INSERT OR IGNORE INTO PartsOfSpeech (value) VALUES (?)', [
        ('Существительное',), ('Прилагательное',), ('Глагол',),
        ('Наречие',), ('Местоимение',), ('Числительное',),
        ('Предлог',), ('Союз',), ('Частица',),
        ('Междометие',), ('Причастие',), ('Деепричастие',)
    ])
    
    cursor.executemany('INSERT OR IGNORE INTO Cases (value) VALUES (?)', [
        ('Именительный',), ('Родительный',), ('Дательный',),
        ('Винительный',), ('Творительный',), ('Предложный',)
    ])
    
    cursor.executemany('INSERT OR IGNORE INTO Genders (value) VALUES (?)', [
        ('Мужской',), ('Женский',), ('Средний',)
    ])
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
    print("✅ Таблицы созданы")
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM UltraWords')
    print(f"📊 Всего слов: {cursor.fetchone()[0]}")
    conn.close()