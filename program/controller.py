from PyQt5.QtWidgets import QMainWindow, QMessageBox
from program.log import Ui_MainWindow


class FocusMindApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

       
        self.user = None  # Store logged-in user

        self.pushButton_2.clicked.connect(self.login)
        self.pushButton.clicked.connect(self.logout)

    def login(self):
        """Handles user login and loads tasks from Firebase."""
        email = self.lineEdit.text()
        password = self.lineEdit_2.text()

        if not email or not password:
            QMessageBox.warning(self, "Login Error", "Please enter your email and password!")
            return
        
        user = self.db.login(email, password)
        if user:
            self.user = user
            QMessageBox.information(self, "Success", "Login successful!")
            
            # Load tasks
            tasks = self.db.get_tasks(self.user['localId'])
            if tasks:
                task_list = "\n".join([task["task"] for task in tasks])
                self.task_input.setText(task_list)
        else:
            QMessageBox.warning(self, "Login Error", "Invalid email or password.")
