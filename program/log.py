import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton, QLabel, QLineEdit, QWidget, QVBoxLayout
from PyQt5.QtGui import QPalette, QColor


class LoginApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.create_database()

    def initUI(self):
        self.setWindowTitle("Login System")
        self.setGeometry(100, 100, 300, 200)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(0,128,0)) 
        self.setPalette(palette)

        layout = QVBoxLayout()
        
        self.label_username = QLabel("Username:")
        layout.addWidget(self.label_username)
        self.input_username = QLineEdit(self)
        layout.addWidget(self.input_username)

        self.label_password = QLabel("Password:")
        layout.addWidget(self.label_password)
        self.input_password = QLineEdit(self)
        self.input_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.input_password)

        self.button_login = QPushButton("Login", self)
        self.button_login.setStyleSheet("background-color: lightgreen;")
        self.button_login.clicked.connect(self.login)
        layout.addWidget(self.button_login)

        self.button_signup = QPushButton("Sign Up", self)
        self.button_signup.setStyleSheet("background-color: lightgreen;")
        self.button_signup.clicked.connect(self.open_signup)
        layout.addWidget(self.button_signup)

        self.button_reset_password = QPushButton("Forgot Password?", self)
        self.button_reset_password.setStyleSheet("background-color: lightgreen;")
        self.button_reset_password.clicked.connect(self.open_password_reset)
        layout.addWidget(self.button_reset_password)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def create_database(self):
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            full_name TEXT NOT NULL
        )
        """)
        conn.commit()
        conn.close()

    def login(self):
        username = self.input_username.text()
        password = self.input_password.text()
        
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            QMessageBox.information(self, "Login Success", "Welcome!")
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

    def open_signup(self):
        self.signup_window = SignupApp()
        self.signup_window.show()

    def open_password_reset(self):
        self.reset_window = PasswordResetApp()
        self.reset_window.show()


class PasswordResetApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Reset Password")
        self.setGeometry(150, 150, 300, 200)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(144, 238, 144))  
        self.setPalette(palette)

        layout = QVBoxLayout()
        
        self.label_username = QLabel("Username:")
        layout.addWidget(self.label_username)
        self.input_username = QLineEdit(self)
        layout.addWidget(self.input_username)
        
        self.label_new_password = QLabel("New Password:")
        layout.addWidget(self.label_new_password)
        self.input_new_password = QLineEdit(self)
        self.input_new_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.input_new_password)
        
        self.button_reset = QPushButton("Reset Password", self)
        self.button_reset.setStyleSheet("background-color: lightgreen;")
        self.button_reset.clicked.connect(self.reset_password)
        layout.addWidget(self.button_reset)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def reset_password(self):
        username = self.input_username.text()
        new_password = self.input_new_password.text()

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password=? WHERE username=?", (new_password, username))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Password Reset", "Your password has been updated.")
        self.close()


class SignupApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Sign Up")
        self.setGeometry(150, 150, 300, 200)

        layout = QVBoxLayout()

        self.label_username = QLabel("Username:")
        layout.addWidget(self.label_username)
        self.input_username = QLineEdit(self)
        layout.addWidget(self.input_username)

        self.label_password = QLabel("Password:")
        layout.addWidget(self.label_password)
        self.input_password = QLineEdit(self)
        self.input_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.input_password)

        self.label_email = QLabel("Email:")
        layout.addWidget(self.label_email)
        self.input_email = QLineEdit(self)
        layout.addWidget(self.input_email)

        self.label_full_name = QLabel("Full Name:")
        layout.addWidget(self.label_full_name)
        self.input_full_name = QLineEdit(self)
        layout.addWidget(self.input_full_name)

        self.button_signup = QPushButton("Sign Up", self)
        self.button_signup.clicked.connect(self.signup)
        layout.addWidget(self.button_signup)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def signup(self):
        username = self.input_username.text()
        password = self.input_password.text()
        email = self.input_email.text()
        full_name = self.input_full_name.text()

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, email, full_name) VALUES (?, ?, ?, ?)",
                       (username, password, email, full_name))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Sign Up", "User registered successfully!")
        self.close()


def test_password_reset():
    app = QApplication(sys.argv)
    reset_app = PasswordResetApp()
    reset_app.input_username.setText("testuser")
    reset_app.input_new_password.setText("newpassword123")
    reset_app.reset_password()
    print("Password reset test completed.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginApp()
    window.show()
    sys.exit(app.exec_())
