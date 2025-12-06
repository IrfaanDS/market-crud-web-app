from flask_login import UserMixin
from market import bcrypt, login_manager
from market.db_connect import get_connection


@login_manager.user_loader
def load_user(user_id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        data = cursor.fetchone()
    conn.close()

    return User(**data) if data else None


class User(UserMixin):
    def __init__(self, id, username, email_address, password_hash, budget, **kwargs):
        self.id = id
        self.username = username
        self.email_address = email_address
        self.password_hash = password_hash
        self.budget = budget

    @property
    def prettier_budget(self):
        return f"{self.budget:,}$"

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, plain):
        self.password_hash = bcrypt.generate_password_hash(plain).decode("utf-8")

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

    def save(self):
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE users SET budget=%s, password_hash=%s WHERE id=%s",
                (self.budget, self.password_hash, self.id)
            )
        conn.commit()
        conn.close()


class Item:
    def __init__(self, id, name, price, barcode, description, owner, **kwargs):
        self.id = id
        self.name = name
        self.price = price
        self.barcode = barcode
        self.description = description
        self.owner = owner

    @staticmethod
    def get_available_items():
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM items WHERE owner IS NULL")
            rows = cursor.fetchall()
        conn.close()
        return [Item(**item) for item in rows]

    @staticmethod
    def get_owned_items(user_id):
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM items WHERE owner=%s", (user_id,))
            rows = cursor.fetchall()
        conn.close()
        return [Item(**item) for item in rows]

    @staticmethod
    def get_by_name(name):
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM items WHERE name=%s", (name,))
            row = cursor.fetchone()
        conn.close()
        return Item(**row) if row else None

    def buy(self, user):
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("UPDATE items SET owner=%s WHERE id=%s", (user.id, self.id))
            cursor.execute("UPDATE users SET budget=budget-%s WHERE id=%s", (self.price, user.id))
        conn.commit()
        conn.close()

    def sell(self, user):
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("UPDATE items SET owner=NULL WHERE id=%s", (self.id,))
            cursor.execute("UPDATE users SET budget=budget+%s WHERE id=%s", (self.price, user.id))
        conn.commit()
        conn.close()
