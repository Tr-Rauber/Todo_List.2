import sqlite3

class DatabaseManager:
    def __init__(self):
        self.init_databases()
    
    def init_databases(self):
        # Инициализация базы пользователей
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL  
        )
        ''')
        connection.commit()
        connection.close()
        
        # Инициализация базы задач
        self.baza_zametok()
    
    def baza_zametok(self):
        connection = sqlite3.connect('tasks.db')
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS permanent_tasks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        task TEXT NOT NULL,
        description TEXT,
        status TEXT NOT NULL
        )
        ''')
        connection.commit()
        connection.close()
    
    # Методы для работы с пользователями
    def create_user(self, username, password):
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            connection.commit()
            user_id = cursor.lastrowid
            connection.close()
            return user_id
        except sqlite3.IntegrityError:
            connection.close()
            return None
    
    def get_user_by_username(self, username):
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        result = cursor.fetchone()
        connection.close()
        return result
    
    def verify_user(self, username, password):
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        result = cursor.fetchone()
        connection.close()
        return result
    
    def get_all_users(self):
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users')
        result = cursor.fetchall()
        connection.close()
        return result
    
    def update_user_password(self, username, new_password):
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute('UPDATE users SET password = ? WHERE username = ?', (new_password, username))
        connection.commit()
        connection.close()
    
    def update_user_username(self, old_username, new_username):
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute('UPDATE users SET username = ? WHERE username = ?', (new_username, old_username))
        connection.commit()
        connection.close()
    
    def delete_user(self, username):
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute('DELETE FROM users WHERE username = ?', (username,))
        connection.commit()
        connection.close()
    
    # Методы для работы с задачами
    def add_task(self, user_id, task, description):
        connection = sqlite3.connect('tasks.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO permanent_tasks (user_id, task, description, status) VALUES (?, ?, ?, ?)', 
                      (user_id, task, description, 'НЕ ВЫПОЛНЕНА'))
        connection.commit()
        connection.close()
    
    def get_user_tasks(self, user_id):
        connection = sqlite3.connect('tasks.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM permanent_tasks WHERE user_id = ?', (user_id,))
        result = cursor.fetchall()
        connection.close()
        return result
    
    def update_task_description(self, user_id, task_name, new_description):
        connection = sqlite3.connect('tasks.db')
        cursor = connection.cursor()
        cursor.execute('UPDATE permanent_tasks SET description = ? WHERE task = ? AND user_id = ?', 
                      (new_description, task_name, user_id))
        connection.commit()
        connection.close()
    
    def delete_task(self, user_id, task_name):
        connection = sqlite3.connect('tasks.db')
        cursor = connection.cursor()
        cursor.execute('DELETE FROM permanent_tasks WHERE task = ? AND user_id = ?', (task_name, user_id))
        connection.commit()
        connection.close()
    
    def update_task_status(self, user_id, task_id, new_status):
        connection = sqlite3.connect('tasks.db')
        cursor = connection.cursor()
        cursor.execute('UPDATE permanent_tasks SET status = ? WHERE id = ? AND user_id = ?', 
                      (new_status, task_id, user_id))
        connection.commit()
        connection.close()