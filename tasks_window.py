from PySide6.QtWidgets import (
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout, 
    QLabel, 
    QLineEdit, 
    QPushButton, 
    QTextEdit, 
    QListWidget,
    QListWidgetItem, 
    QMessageBox, 
    QComboBox
)

from PySide6.QtCore import Qt
from database import DatabaseManager

class TasksWindow(QWidget):
    def __init__(self, stacked_widget, db_manager, main_window):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.db_manager = db_manager
        self.main_window = main_window
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Управление задачами')
        
        layout = QVBoxLayout()
        
        title = QLabel('ЕЖЕДНЕВНИК - Управление задачами')
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Список задач
        self.tasks_list = QListWidget()
        layout.addWidget(QLabel('Ваши задачи:'))
        layout.addWidget(self.tasks_list)
        
        form_layout = QVBoxLayout()
        
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText('Введите задачу')
        form_layout.addWidget(QLabel('Задача:'))
        form_layout.addWidget(self.task_input)
        
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText('Введите описание задачи')
        form_layout.addWidget(QLabel('Описание:'))
        form_layout.addWidget(self.description_input)
        
        layout.addLayout(form_layout)
        
        buttons_layout = QHBoxLayout()
        
        self.btn_add = QPushButton('Добавить задачу')
        self.btn_update = QPushButton('Изменить описание')
        self.btn_delete = QPushButton('Удалить задачу')
        self.btn_refresh = QPushButton('Обновить статус')
        self.btn_back = QPushButton('Выйти')
        
        self.btn_add.clicked.connect(self.add_task)
        self.btn_update.clicked.connect(self.update_task)
        self.btn_delete.clicked.connect(self.delete_task)
        self.btn_refresh.clicked.connect(self.update_status)
        self.btn_back.clicked.connect(self.go_back)
        self.tasks_list.itemClicked.connect(self.on_task_selected)
        
        buttons_layout.addWidget(self.btn_add)
        buttons_layout.addWidget(self.btn_update)
        buttons_layout.addWidget(self.btn_delete)
        buttons_layout.addWidget(self.btn_refresh)
        buttons_layout.addWidget(self.btn_back)
        
        layout.addLayout(buttons_layout)

        self.status_combo = QComboBox()
        self.status_combo.addItems(['НЕ ВЫПОЛНЕНА', 'ВЫПОЛНЕНА'])
        layout.addWidget(QLabel('Статус:'))
        layout.addWidget(self.status_combo)
        
        self.setLayout(layout)
    
    def showEvent(self, event):
        self.refresh_tasks()
        super().showEvent(event)
    
    def refresh_tasks(self):
        if not self.main_window.current_user_id:
            QMessageBox.warning(self, 'Ошибка', 'User ID не установлен!')
            return
            
        self.tasks_list.clear()
        tasks = self.db_manager.get_user_tasks(self.main_window.current_user_id)
        for task in tasks:
            item_text = f"ID: {task[0]} | {task[2]} | Описание: {task[3]} | Статус: {task[4]}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, task[0])  
            self.tasks_list.addItem(item)
    
    def on_task_selected(self, item):
        task_id = item.data(Qt.UserRole)
        tasks = self.db_manager.get_user_tasks(self.main_window.current_user_id)
        for task in tasks:
            if task[0] == task_id:
                self.task_input.setText(task[2])
                self.description_input.setPlainText(task[3] if task[3] else '')
                index = self.status_combo.findText(task[4])
                if index >= 0:
                    self.status_combo.setCurrentIndex(index)
                break
    
    def add_task(self):
        if not self.main_window.current_user_id:
            QMessageBox.warning(self, 'Ошибка', 'User ID не установлен!')
            return
            
        task = self.task_input.text().strip().lower()
        description = self.description_input.toPlainText().strip().lower()
        
        if not task:
            QMessageBox.warning(self, 'Ошибка', 'Задача не может быть пустой!')
            return
        
        self.db_manager.add_task(self.main_window.current_user_id, task, description)
        QMessageBox.information(self, 'Good job',  'Задача с описанием добавлена!')
        self.clear_form()
        self.refresh_tasks()
    
    def update_task(self):
        if not self.main_window.current_user_id:
            QMessageBox.warning(self, 'Ошибка', 'User ID не установлен!')
            return
            
        selected_items = self.tasks_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'Ошибка', 'Выберите задачу для изменения!')
            return
        
        task_id = selected_items[0].data(Qt.UserRole)
        new_description = self.description_input.toPlainText().strip().lower()
        
        tasks = self.db_manager.get_user_tasks(self.main_window.current_user_id)
        task_name = None
        for task in tasks:
            if task[0] == task_id:
                task_name = task[2]
                break
        
        if task_name:
            self.db_manager.update_task_description(self.main_window.current_user_id, task_name, new_description)
            QMessageBox.information(self, 'Good job', 'Описание задачи обновлено!')
            self.refresh_tasks()
    
    def delete_task(self):
        if not self.main_window.current_user_id:
            QMessageBox.warning(self, 'Ошибка', 'User ID не установлен!')
            return
            
        selected_items = self.tasks_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'Ошибка', 'Выберите задачу для удаления!')
            return
        
        task_id = selected_items[0].data(Qt.UserRole)

        tasks = self.db_manager.get_user_tasks(self.main_window.current_user_id)
        task_name = None
        for task in tasks:
            if task[0] == task_id:
                task_name = task[2]
                break
        
        if task_name:
            self.db_manager.delete_task(self.main_window.current_user_id, task_name)
            QMessageBox.information(self, 'Good job', 'Задача успешно удалена')
            self.clear_form()
            self.refresh_tasks()
    
    def update_status(self):
        if not self.main_window.current_user_id:
            QMessageBox.warning(self, 'Ошибка', 'User ID не установлен!')
            return
            
        selected_items = self.tasks_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'Ошибка', 'Выберите задачу для изменения статуса!')
            return
        
        task_id = selected_items[0].data(Qt.UserRole)
        new_status = self.status_combo.currentText()
        
        self.db_manager.update_task_status(self.main_window.current_user_id, task_id, new_status)
        QMessageBox.information(self, 'Good job', f'Статус задачи обновлен на: {new_status}')
        self.refresh_tasks()
    
    def clear_form(self):
        self.task_input.clear()
        self.description_input.clear()
        self.status_combo.setCurrentIndex(0)
    
    def go_back(self):
        self.clear_form()
        self.main_window.current_user_id = None
        self.stacked_widget.setCurrentIndex(0)