import sqlite3 as sq
from werkzeug.security import check_password_hash, generate_password_hash
from models import User

class Database:
    def __init__(self, db_name='mydb.db'):
        self.db_name = db_name
        self.connection = None
    
    def __enter__(self):
        self.connection = sq.connect(self.db_name)
        return self.connection
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()
            
def register(username, email, password):
    with Database() as conn:
        cursor = conn.cursor()
        hashed_password = generate_password_hash(password)
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?,?, ?)", (username,email, hashed_password))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            return False

def sign_in(username, password):
    with Database() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password FROM users WHERE username = ?", [username])
        data = cursor.fetchone()

        if data is None:
            return None
        if not check_password_hash(data[2], password):
            return None
        return User(id=data[0], username=data[1])

def change_password(id, old_password, new_password):
    with Database() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE id = ?", [id])
        data = cursor.fetchone()

        if data is None:
            return False
        if not check_password_hash(data[0], old_password):
            return False

        hashed_password = generate_password_hash(new_password)
        try:
            cursor.execute("UPDATE users SET password = ? WHERE id = ?", (hashed_password, id))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            return False
