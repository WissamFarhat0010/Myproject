from PyQt5.QtWidgets import QMainWindow, QMessageBox, QSpinBox, QLabel, QVBoxLayout, QTextEdit
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont
from log import Ui_MainWindow 

class FocusMindApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  

        
        self.btn_login = self.pushButton_2
        self.btn_logout = self.pushButton
        self.btn_change_password = self.pushButton_3
        self.btn_account = self.pushButton_4
        self.btn_set_timer = self.pushButton_5 

        self.task_input = QTextEdit(self)
        self.task_input.setPlaceholderText("Enter your task here...")
        self.task_input.setGeometry(50, 250, 300, 50)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.time_left = 25 * 60  
        self.sessions_completed = 0

        
        self.break_time_left = 5 * 60  
        self.is_on_break = False

        
        self.btn_login.clicked.connect(self.login)
        self.btn_logout.clicked.connect(self.logout)
        self.btn_change_password.clicked.connect(self.change_password)
        self.btn_account.clicked.connect(self.open_account)
        self.btn_set_timer.clicked.connect(self.set_timer)

        # Timer Display
        self.label_timer = self.create_timer_label()

        # Ensure password field is hidden
        self.lineEdit_2.setEchoMode(self.lineEdit_2.Password)

    def create_timer_label(self):
        """Creates a QLabel for the Pomodoro timer."""
        label = QLabel("25:00", self)
        label.setGeometry(350, 180, 100, 40)
        label.setFont(QFont("Arial", 16, QFont.Bold))
        label.setStyleSheet("color: red;")
        label.show()
        return label

    def start_timer(self):
        """Starts the Pomodoro timer."""
        if not self.timer.isActive():
            self.timer.start(1000)

    def start_break_timer(self):
        """Starts the break timer."""
        if not self.timer.isActive():
            self.timer.start(1000)

    def update_timer(self):
        """Updates the countdown timer."""
        if self.is_on_break:
            if self.break_time_left > 0:
                self.break_time_left -= 1
                minutes, seconds = divmod(self.break_time_left, 60)
                self.label_timer.setText(f"Break: {minutes:02}:{seconds:02}")
            else:
                self.timer.stop()
                self.label_timer.setText("Break is over! Back to work.")
                QMessageBox.information(self, "Break Time", "Break is over! Back to work.")
                self.is_on_break = False
                self.time_left = self.get_pomodoro_duration() * 60  
                self.start_timer()

        else:
            if self.time_left > 0:
                self.time_left -= 1
                minutes, seconds = divmod(self.time_left, 60)
                self.label_timer.setText(f"{minutes:02}:{seconds:02}")
            else:
                self.timer.stop()
                self.sessions_completed += 1
                self.label_timer.setText("Time's up! Take a break.")
                QMessageBox.information(self, "Pomodoro", "Time's up! Take a break.")
                self.start_break()

    def get_pomodoro_duration(self):
        """Returns the Pomodoro duration set by the user."""
        return self.spinBox_pomodoro.value()  

    def start_break(self):
        """Start break timer based on the number of Pomodoro sessions completed."""
        if self.sessions_completed % 4 == 0:
            
            self.break_time_left = 15 * 60  
        else:
            
            self.break_time_left = 5 * 60  

        self.is_on_break = True
        self.start_break_timer()

    def set_timer(self):
        """Sets the Pomodoro duration based on user input."""
        duration = self.spinBox_pomodoro.value()  
        self.time_left = duration * 60
        self.label_timer.setText(f"{duration:02}:00")
        QMessageBox.information(self, "Pomodoro Duration", f"Pomodoro duration set to {duration} minutes.")

    def login(self):
        """Handles login action."""
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()

        if not username or not password:
            QMessageBox.warning(self, "Login Error", "Please enter username and password!")
            return

        print("Login successful!")
        self.start_timer()

    def logout(self):
        """Handles logout action."""
        reply = QMessageBox.question(self, "Logout", "Are you sure you want to log out?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.timer.stop()
            self.time_left = 25 * 60
            self.sessions_completed = 0
            self.label_timer.setText("25:00")
            self.is_on_break = False
            self.break_time_left = 5 * 60 

    def change_password(self):
        """Handles password change."""
        QMessageBox.information(self, "Change Password", "Feature coming soon!")

    def open_account(self):
        """Handles account management."""
        QMessageBox.information(self, "Account", "Feature coming soon!")
