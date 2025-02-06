import sys
import pyrebase
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton, QLabel, QLineEdit, QWidget, QVBoxLayout
from PyQt5.QtGui import QPalette, QColor

# Firebase configuration
firebase_config = { 
      "apiKey": "AIzaSyAW2QHXrcXseMXaxa7Jet662FSCumMveTI",
  "authDomain": "focus-71f5f.firebaseapp.com",
  "databaseURL": "https://focus-71f5f-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "focus-71f5f",
  "storageBucket": "focus-71f5f.firebasestorage.app",
  "messagingSenderId": "596802463261",
  "appId": "1:596802463261:web:cbc1c7e10b2b17168a88f4",
  "measurementId": "G-3VGLMKD90G"
}


firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

class LoginApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Login System")
        self.setGeometry(100, 100, 300, 200)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(0, 128, 0))
        self.setPalette(palette)

        layout = QVBoxLayout()

        self.label_email = QLabel("Email:")
        layout.addWidget(self.label_email)
        self.input_email = QLineEdit(self)
        layout.addWidget(self.input_email)

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
        self.button_signup.clicked.connect(self.signup)
        layout.addWidget(self.button_signup)

        self.button_reset_password = QPushButton("Forgot Password?", self)
        self.button_reset_password.setStyleSheet("background-color: lightgreen;")
        self.button_reset_password.clicked.connect(self.reset_password)
        layout.addWidget(self.button_reset_password)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def login(self):
        email = self.input_email.text()
        password = self.input_password.text()
        try:
            auth.sign_in_with_email_and_password(email, password)
            QMessageBox.information(self, "Login Success", "Welcome!")
        except:
            QMessageBox.warning(self, "Login Failed", "Invalid email or password.")

    def signup(self):
        email = self.input_email.text()
        password = self.input_password.text()
        try:
            auth.create_user_with_email_and_password(email, password)
            QMessageBox.information(self, "Sign Up Success", "Account created successfully!")
        except:
            QMessageBox.warning(self, "Sign Up Failed", "Could not create account.")

    def reset_password(self):
        email = self.input_email.text()
        try:
            auth.send_password_reset_email(email)
            QMessageBox.information(self, "Reset Email Sent", "Check your email for reset link.")
        except:
            QMessageBox.warning(self, "Error", "Could not send reset email.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginApp()
    window.show()
    sys.exit(app.exec_())
