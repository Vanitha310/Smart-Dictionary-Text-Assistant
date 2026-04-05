import sqlite3
from datetime import datetime

DB_NAME = "dictionary_history.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT,
            definition TEXT,
            searched_at TEXT,
            count INTEGER DEFAULT 1
        )
    """)
    
    conn.commit()
    conn.close()


def save_word(word, definition):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, count FROM history WHERE word = ?", (word,))
    result = cursor.fetchone()
    
    if result:
        cursor.execute(
            "UPDATE history SET count = count + 1 WHERE word = ?",
            (word,)
        )
    else:
        cursor.execute(
            "INSERT INTO history (word, definition, searched_at) VALUES (?, ?, ?)",
            (word, definition, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
    
    conn.commit()
    conn.close()


def get_top_words(limit=5):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT word, count FROM history ORDER BY count DESC LIMIT ?",
        (limit,)
    )
    
    results = cursor.fetchall()
    conn.close()
    return results