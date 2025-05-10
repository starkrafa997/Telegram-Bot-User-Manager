import sqlite3


def init_db():
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER UNIQUE,
                name TEXT,
                age INTEGER
            )
        ''')
        conn.commit()


def add_user(telegram_id: int, name: str, age: int):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (telegram_id, name, age)
            VALUES (?, ?, ?)
        ''', (telegram_id, name, age))
        conn.commit()


def user_exists_by_id(telegram_id: int) -> bool:
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM users WHERE telegram_id =?', (telegram_id,))
        return cursor.fetchone() is not None


def update_user_age_by_id(telegram_id: int, new_age: int):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE users SET age = ? WHERE telegram_id = ?
        ''', (new_age, telegram_id))
        conn.commit()
        print(f"[DEBUG] Обновлено строк: {cursor.rowcount}")


def delete_user_by_id(telegram_id: int):
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE telegram_id = ?', (telegram_id,))
        conn.commit()
        return cursor.rowcount > 0


def get_user_name_by_id(telegram_id: int) -> str | None:
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM users WHERE telegram_id = ?', (telegram_id,))
        result = cursor.fetchone()
        return result[0] if result else None


def get_all_users():
    with sqlite3.connect('users.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT name, age FROM users')
        return cursor.fetchall()
