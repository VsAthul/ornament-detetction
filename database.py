import sqlite3


DB_PATH = " detection.db"

def get_db_connection():
    return sqlite3.connect(DB_PATH)

def initialize_db():
    with get_db_connection() as conn:
        conn.execute("""
            create table if not exists detections (
                     id integer primary key autoincrement,
                     filename text,
                     item_type text not null,
                     quantity integer not null,
                     created_at datetime default current_timestamp
                     )""")
        conn.commit()