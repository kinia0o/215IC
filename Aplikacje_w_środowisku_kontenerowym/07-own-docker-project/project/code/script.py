import sys
import psycopg2
import os

# Pobranie zmiennych środowiskowych do połączenia z bazą
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "mydb")
DB_USER = os.getenv("DB_USER", "user")
DB_PASS = os.getenv("DB_PASS", "password")

def connect_db():
    # Nawiązanie połączenia z bazą danych
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

def initialize_db():
    # Tworzenie tabeli imion jeśli nie istnieje
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS names (
            name TEXT PRIMARY KEY,
            count INTEGER DEFAULT 1
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def update_or_insert_name(name):
    # Dodanie imienia do bazy lub zwiększenie jego liczniku
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT count FROM names WHERE name = %s", (name,))
    row = cur.fetchone()

    if row:
        new_count = row[0] + 1
        cur.execute("UPDATE names SET count = %s WHERE name = %s", (new_count, name))
    else:
        cur.execute("INSERT INTO names (name, count) VALUES (%s, 1)", (name,))

    conn.commit()
    cur.close()
    conn.close()

def show_database():
    # Wyświetla zawartość bazy danych
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM names")
    rows = cur.fetchall()
    
    print("\n--- Zawartość bazy danych ---")
    for row in rows:
        print(f"Imię: {row[0]}, Licznik przywitań: {row[1]}")
    print("-----------------------------\n")

    cur.close()
    conn.close()

if __name__ == "__main__":
    name = sys.argv[1]
    print(f"Hello {name}! ^^")
    initialize_db()
    update_or_insert_name(name)
    show_database()
