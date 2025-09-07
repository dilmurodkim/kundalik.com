import sqlite3
from config import DB_NAME

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ism TEXT,
        familya TEXT,
        login TEXT,
        parol TEXT,
        rol TEXT
    )
    """)
    conn.commit()
    conn.close()

def add_user(ism, familya, login, parol, rol):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (ism, familya, login, parol, rol) VALUES (?, ?, ?, ?, ?)",
                   (ism, familya, login, parol, rol))
    conn.commit()
    conn.close()

def list_users():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT ism, familya, login, parol, rol FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def delete_user(ism, familya):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE ism=? AND familya=?", (ism, familya))
    deleted = cursor.rowcount
    conn.commit()
    conn.close()
    return deleted

def find_user(ism, familya):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT login, parol, rol FROM users WHERE ism=? AND familya=?", (ism, familya))
    user = cursor.fetchone()
    conn.close()
    return user
