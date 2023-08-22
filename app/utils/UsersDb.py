import sqlite3
from datetime import datetime


class Users:
    def __init__(self, db_path="app/db/users.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    telegram_id INTEGER PRIMARY KEY,
                    request_count INTEGER DEFAULT 0,
                    wallet_count INTEGER DEFAULT 0,
                    time_wait TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def increase_request_count(self, user_id):
        try:
            self.cursor.execute("""
                INSERT OR IGNORE INTO users (telegram_id) VALUES (?)
            """, (user_id,))
            self.cursor.execute("""
                UPDATE users SET request_count = request_count + 1 WHERE telegram_id = ?
            """, (user_id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error increasing request count: {e}")

    def set_max_wallets_count(self, user_id, wallet_count):
        try:
            self.cursor.execute("""
                INSERT OR IGNORE INTO users (telegram_id) VALUES (?)
            """, (user_id,))
            self.cursor.execute("""
                UPDATE users SET wallet_count = ? WHERE telegram_id = ?
            """, (wallet_count, user_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error setting max wallets count: {e}")

    def get_request_count(self, user_id):
        try:
            self.cursor.execute("""
                SELECT request_count FROM users WHERE telegram_id = ?
            """, (user_id,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Error fetching request count: {e}")
            return None

    def get_premium_users(self):
        try:
            self.cursor.execute("SELECT telegram_id FROM users WHERE request_count = 100")
            premium_users = self.cursor.fetchall()
            premium_users_list = [item[0] for item in premium_users]
            return premium_users_list
        except sqlite3.Error as e:
            print(f"Error fetching premium users: {e}")
            return None

    def get_max_wallets(self, user_id):
        try:
            self.cursor.execute("""
                SELECT wallet_count FROM users WHERE telegram_id = ?
            """, (user_id,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Error fetching max wallets: {e}")
            return None

    def get_time_wait(self, user_id):
        try:
            self.cursor.execute("""
                SELECT time_wait FROM users WHERE telegram_id = ?
            """, (user_id,))
            result = self.cursor.fetchone()
            return datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S') if result else None
        except sqlite3.Error as e:
            print(f"Error fetching time wait: {e}")
            return None

    def add_user(self, user_id, time_wait, request_count=0, wallet_count=0):
        try:
            self.cursor.execute("""
                INSERT OR REPLACE INTO users (telegram_id, request_count, wallet_count, time_wait)
                VALUES (?, ?, ?, ?)
            """, (user_id, request_count, wallet_count, time_wait))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error adding user: {e}")

    def set_request_count_and_date(self, user_id, count, last_request_date):
        try:
            self.cursor.execute("""
                UPDATE users
                SET request_count = ?, time_wait = ?
                WHERE telegram_id = ?
            """, (count, last_request_date, user_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error setting request count and date: {e}")

    def set_request_count(self, user_id, count):
        try:
            self.cursor.execute("""
                UPDATE users
                SET request_count = ?
                WHERE telegram_id = ?
            """, (count, user_id))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error setting request count and date: {e}")

    def close(self):
        self.conn.close()
