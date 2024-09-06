import sqlite3 as sq
import uuid
from werkzeug.security import check_password_hash, generate_password_hash
from models import User, Group

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
            

#TABLE USERS   
def get_user_byid(id):
    with Database() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email FROM users WHERE id = ?", [id])
        data = cursor.fetchone()
        if data is None:
            return None
        return User(id=data[0], username=data[1], email=data[2])
    
def get_user_byusername(username):
    with Database() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, email FROM users WHERE username = ?", [username])
        data = cursor.fetchone()
        if data is None:
            return None
        return User(id=data[0], username=data[1],email=data[2])
    
def get_user_byemail(email):
    with Database() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username,email FROM users WHERE email = ?", [email])
        data = cursor.fetchone()
        if data is None:
            return None
        return User(id=data[0], username=data[1], email=data[2])
    
         
def register(username, email, password):
    with Database() as conn:
        cursor = conn.cursor()
        hashed_password = generate_password_hash(password)
        try:
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?,?, ?)", (username,email, hashed_password))
            conn.commit()
            return sign_in(email, password)
        except Exception as e:
            conn.rollback()
            return False

def sign_in(username, password):
    with Database() as conn:
        cursor = conn.cursor()
        
        if username is None:
            return None
        
        cursor.execute("SELECT id, username,email, password FROM users WHERE email = ?", [username])
        data = cursor.fetchone()
        
        if data is None:
            cursor.execute("SELECT id, username,email, password FROM users WHERE username = ?", [username])
            data = cursor.fetchone()

        if data is None:
            return None
        if not check_password_hash(data[3], password):
            return None
        return User(id=data[0], username=data[1], email=data[2])

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

#TABLE GROUPS
def get_group_byid(id_bytes):
    # Converti l'ID stringa in bytes (se è un UUID in formato stringa)
    
    
    with Database() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM groups WHERE id = ?", [id_bytes])
        data = cursor.fetchone()
        if data is None:
            return None
        return Group(id=uuid.UUID(bytes=data[0]), name=data[1])

def get_group_byuser(user_id):
    with Database() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT g.id,g.name FROM groups g INNER JOIN members m ON g.id = m.fk_group WHERE m.fk_user = ?", [user_id])
        data = cursor.fetchall()
        
        # Se non ci sono risultati, ritorna None
        if not data:
            return None
        
        # Trasforma i risultati in una lista di dizionari
        result = []
        for row in data:
            result.append(Group(id=uuid.UUID(bytes=row[0]), name=row[1]).to_dict())
        
        return result


def create_group(name, user_id):
    with Database() as conn:
        cursor = conn.cursor()
        id=uuid.uuid4().bytes
        try:
            cursor.execute("INSERT INTO groups (id, name) VALUES (?, ?)", (id, name))
            cursor.execute("INSERT INTO members (admin, fk_user, fk_group) VALUES (1, ?, ?)", (user_id, id))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            return False
        
#group id può essere passato sia come stringa che come bytes
def join_group(group_id, user_id):
    with Database() as conn:
        cursor = conn.cursor()
        
        if(type(group_id) is str):
            id_bytes = uuid.UUID(group_id).bytes
        else:
            id_bytes = group_id
            
        if get_group_byid(id_bytes) is None:
            return False
        
        
        try:
            cursor.execute("INSERT INTO members (fk_user, fk_group) VALUES (?, ?)", (user_id, id_bytes))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            return False

def quit_group(group_id, user_id):
    with Database() as conn:
        cursor = conn.cursor()
        
        if(type(group_id) is str):
            id_bytes = uuid.UUID(group_id).bytes
        else:
            id_bytes = group_id
            
        if get_group_byid(id_bytes) is None:
            return False
        
        try:
            cursor.execute("DELETE FROM members WHERE fk_user = ? AND fk_group = ?", (user_id, id_bytes))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            return False