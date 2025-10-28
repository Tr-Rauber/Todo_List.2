import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from database import DatabaseManager
from auth_window import AuthWindow, ExistingUserWindow, NewUserWindow
from tasks_window import TasksWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.current_user_id = None  
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Ежедневник')
        
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        self.auth_window = AuthWindow(self.stacked_widget, self.db_manager, self)
        self.existing_user_window = ExistingUserWindow(self.stacked_widget, self.db_manager, self)
        self.new_user_window = NewUserWindow(self.stacked_widget, self.db_manager, self)
        self.tasks_window = TasksWindow(self.stacked_widget, self.db_manager, self)
        
        self.stacked_widget.addWidget(self.auth_window)           
        self.stacked_widget.addWidget(self.existing_user_window)  
        self.stacked_widget.addWidget(self.new_user_window)       
        self.stacked_widget.addWidget(self.tasks_window)          
        self.stacked_widget.setCurrentIndex(0)
    
    def set_current_user_id(self, user_id):
        self.current_user_id = user_id

def main():
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()