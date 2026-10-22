import sqlite3

def create_test_db():
    # Создает файл базы данных и устанавливает соединение.
    conn = sqlite3.connect("test.sqlite")
    cursor = conn.cursor()
    
    # Создает тестовую таблицу для инициализации системного каталога sqlite_master.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT
        )
    """)
    
    # Создает дополнительную таблицу для наглядности выборки.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            total_amount REAL
        )
    """)
    
    # Фиксирует изменения и закрывает соединение.
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_test_db()