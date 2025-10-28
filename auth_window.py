from PySide6.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout, 
    QLabel, 
    QLineEdit, 
    QPushButton, 
    QMessageBox, 
    QStackedWidget

)
from PySide6.QtCore import Qt
from database import DatabaseManager
from PySide6.QtWidgets import QGridLayout

class AuthWindow(QWidget):
    def __init__(self, stacked_widget, db_manager, main_window):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.db_manager = db_manager
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Авторизация')

        layout = QVBoxLayout()
        title = QLabel('Добрый день! Дорогой Пользователь')
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        self.btn_existing = QPushButton('Существующий пользователь')
        self.btn_new = QPushButton('Новый пользователь')
        self.btn_exit = QPushButton('Выход')
        
        self.btn_existing.clicked.connect(self.show_existing_user_auth)
        self.btn_new.clicked.connect(self.show_new_user_auth)
        self.btn_exit.clicked.connect(self.close)
        
        layout.addWidget(self.btn_existing)
        layout.addWidget(self.btn_new)
        layout.addWidget(self.btn_exit)
        
        self.setLayout(layout)
    
    def show_existing_user_auth(self):
        self.stacked_widget.setCurrentIndex(1)
    
    def show_new_user_auth(self):
        self.stacked_widget.setCurrentIndex(2)
    
    def show_admin_window(self):
        self.stacked_widget.setCurrentIndex(4)

class ExistingUserWindow(QWidget):
    def __init__(self, stacked_widget, db_manager, main_window):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.db_manager = db_manager
        self.main_window = main_window
        self.attempts = 0
        self.max_attempts = 4
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        title = QLabel('Вход ')
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Введите имя пользователя')
        layout.addWidget(QLabel('Имя пользователя:'))
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Введите пароль')
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel('Пароль:'))
        layout.addWidget(self.password_input)
        
        self.btn_login = QPushButton('Войти')
        self.btn_back = QPushButton('Назад')
        
        self.btn_login.clicked.connect(self.login)
        self.btn_back.clicked.connect(self.go_back)
        
        layout.addWidget(self.btn_login)
        layout.addWidget(self.btn_back)
        
        self.setLayout(layout)
    
    def login(self):
        username = self.username_input.text().strip().lower()
        password = self.password_input.text().strip().lower()
        
        if not username:
            QMessageBox.warning(self, 'Ошибка', 'Введите имя пользователя!')
            return
        
        user = self.db_manager.get_user_by_username(username)
        if not user:
            QMessageBox.warning(self, 'Ошибка', f'Пользователь "{username}" не найден!')
            return
        
        verified_user = self.db_manager.verify_user(username, password)
        if verified_user:
            self.attempts = 0
            QMessageBox.information(self, 'Good job', 'Пароль введен правильно. Добро пожаловать в ежедневник!')
            self.main_window.set_current_user_id(verified_user[0])
            self.stacked_widget.setCurrentIndex(3)
            self.clear_form()
        else:
            self.attempts += 1
            remaining = self.max_attempts - self.attempts
            if remaining > 0:
                QMessageBox.warning(self, 'Ошибка', f'Пароль введен неправильно. Осталось попыток: {remaining}')
            else:
                QMessageBox.critical(self, 'Ошибка', 'Вы превысили лимит попыток. До свидания.')
                self.stacked_widget.setCurrentIndex(0)
    
    def clear_form(self):
        self.username_input.clear()
        self.password_input.clear()
    
    def go_back(self):
        self.clear_form()
        self.stacked_widget.setCurrentIndex(0)

class NewUserWindow(QWidget):
    def __init__(self, stacked_widget, db_manager, main_window):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.db_manager = db_manager
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        title = QLabel('Регистрация')
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Введите имя пользователя')
        layout.addWidget(QLabel('Имя пользователя:'))
        layout.addWidget(self.username_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Введите пароль')
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel('Пароль:'))
        layout.addWidget(self.password_input)
        
        self.btn_register = QPushButton('Зарегистрироваться')
        self.btn_back = QPushButton('Назад')
        
        self.btn_register.clicked.connect(self.register)
        self.btn_back.clicked.connect(self.go_back)
        
        layout.addWidget(self.btn_register)
        layout.addWidget(self.btn_back)
        
        self.setLayout(layout)
    
    def register(self):
        username = self.username_input.text().strip().lower()
        password = self.password_input.text().strip().lower()
        
        if not username:
            QMessageBox.warning(self, 'Ошибка', 'Имя не может быть пустым!')
            return
        
        if username == "-":
            QMessageBox.warning(self, 'Ошибка', 'Имя "-" запрещено для использования!')
            return
        
        if not password:
            QMessageBox.warning(self, 'Ошибка', 'Пароль не может быть пустым!')
            return
        
        user_id = self.db_manager.create_user(username, password)
        if user_id:
            QMessageBox.information(self, 'Good job', 'Ваш аккаунт создан! Добро пожаловать в ежедневник!')
            self.main_window.set_current_user_id(user_id)
            self.stacked_widget.setCurrentIndex(3) 
            self.clear_form()
        else:
            QMessageBox.warning(self,'Ошибка', f'Пользователь "{username}" уже существует!')
    
    def clear_form(self):
        self.username_input.clear()
        self.password_input.clear()
    
    def go_back(self):
        self.clear_form()
        self.stacked_widget.setCurrentIndex(0)