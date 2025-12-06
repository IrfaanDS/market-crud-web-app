import pymysql

def get_connection():
    return pymysql.connect(
        host="market-db",
        user="root",
        password="root123",
        database="marketdb",
        cursorclass=pymysql.cursors.DictCursor
    )

def fetch_one(query, params=None):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()
    finally:
        conn.close()

def fetch_all(query, params=None):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    finally:
        conn.close()

def execute_query(query, params=None):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            conn.commit()
    finally:
        conn.close()
