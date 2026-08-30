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
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Value TEXT UNIQUE NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PartsOfSpeech (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Value TEXT UNIQUE NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Cases (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Value TEXT UNIQUE NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Genders (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Value TEXT UNIQUE NOT NULL
        )
    ''')
    
    # === Основная таблица (без caseId) ===
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS UltraWords (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Value TEXT NOT NULL,
            TypeId INTEGER NOT NULL,
            PartOfSpeechId INTEGER,
            IsDeclinable BOOLEAN,
            Popularity BOOLEAN DEFAULT FALSE,
            IsModern BOOLEAN DEFAULT TRUE,
            Comment TEXT,
            Link TEXT,
            DateTimeSaving DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(value, typeId),
            FOREIGN KEY (typeId) REFERENCES Types(id) ON DELETE CASCADE,
            FOREIGN KEY (partOfSpeechId) REFERENCES PartsOfSpeech(id) ON DELETE SET NULL
        )
    ''')
    
    # === Таблица для падежей ===
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS UltraWordsCases (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            WordId INTEGER NOT NULL,
            CaseId INTEGER NOT NULL,
            Value TEXT NOT NULL,
            Multiplicity BOOLEAN,
            GenderId INTEGER,
            FOREIGN KEY (wordId) REFERENCES UltraWords(id) ON DELETE CASCADE,
            FOREIGN KEY (caseId) REFERENCES Cases(id) ON DELETE CASCADE,
            FOREIGN KEY (genderId) REFERENCES Genders(id) ON DELETE CASCADE,
            UNIQUE(wordId, caseId)
        )
    ''')
    
    # === Таблица Words (для совместимости) ===
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Words (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            Value TEXT UNIQUE NOT NULL
        )
    ''')
    
    # === Представление ===
    cursor.execute('''
        CREATE VIEW IF NOT EXISTS UltraWordsX AS
        SELECT 
            uw.id,
            uw.value AS Word,
            t.value AS Type,
            ps.value AS PartOfSpeech,         
            uw.isDeclinable,
            uw.Popularity,
            uw.IsModern,
            uw.comment,
            uw.DateTimeSaving,
            uw.link AS Link
        FROM UltraWords uw
        LEFT JOIN Types t ON uw.typeId = t.id
        LEFT JOIN PartsOfSpeech ps ON uw.partOfSpeechId = ps.id
        ORDER BY t.value, uw.value
    ''')
    
    # === Начальное заполнение справочников ===
    cursor.executemany('INSERT OR IGNORE INTO PartsOfSpeech (value) VALUES (?)', [
        ('Существительное',), ('Прилагательное',), ('Глагол',),
        ('Наречие',), ('Местоимение',), ('Числительное',),
        ('Предлог',), ('Союз',), ('Частица',),
        ('Междометие',), ('Причастие',), ('Деепричастие',),
        ('Собственное',)
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