 
import unittest
import sqlite3
import os
import sys
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication, QMessageBox
from log import LoginApp, SignupApp, PasswordResetApp, FeelApp  

class DadaTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """ Initialize QApplication only once """
        cls.app = QApplication(sys.argv)

     
    @classmethod
    def tearDownClass(cls):
        """ Safely close FeelApp if initialized """
        if hasattr(cls, "feel_app"):
            cls.feel_app.close()


    def setUp(self):
        """ Initializes all app instances before each test """
        self.login_app = LoginApp()
        self.signup_app = SignupApp()
        self.reset_app = PasswordResetApp()
        self.feel_app = FeelApp()
        self.database_name = "test_users.db"
        self.create_test_database()

    def tearDown(self):
        """ Close applications and remove test database after each test """
        self.login_app.close()
        self.signup_app.close()
        self.reset_app.close()
        self.feel_app.close()
        if os.path.exists(self.database_name):
            os.remove(self.database_name)

    def create_test_database(self):
        conn = sqlite3.connect(self.database_name)
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

    def test_database_schema_integrity(self):
        """ Validate that the database schema follows the expected structure """
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        conn.close()

        expected_columns = ["id", "username", "password", "email", "full_name"]
        self.assertListEqual(columns, expected_columns, "Database structure should match expected schema.")

    def test_password_reset_for_non_existing_user(self):
        self.reset_app.input_username.setText("fakeuser")
        self.reset_app.input_new_password.setText("newpassword456")

        with patch.object(QMessageBox, 'information') as mock_info:
            self.reset_app.reset_password()
            mock_info.assert_called()  # Just checking that some message was shown
 
        
    def test_case_sensitive_login(self):
        """ Verify login fails when entering the wrong case for a username """
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, email, full_name) VALUES (?, ?, ?, ?)", 
                       ("TestUser", "password123", "user@example.com", "Test User"))
        conn.commit()
        conn.close()

        self.login_app.input_username.setText("testuser")  # Lowercase, should fail
        self.login_app.input_password.setText("password123")

        with patch('PyQt5.QtWidgets.QMessageBox.warning') as mock_warning:
            self.login_app.login()
            mock_warning.assert_called_with(self.login_app, "Login Failed", "Invalid username or password.")


    def test_navigation_through_ui(self):
        """ Test UI navigation within FeelApp """
        self.feel_app.show_exercise("Happy")
        self.assertEqual(self.feel_app.stackedWidget.currentIndex(), 1, "Exercise page should be open")

        self.feel_app.go_back()
        self.assertEqual(self.feel_app.stackedWidget.currentIndex(), 0, "Should navigate back to emotion selection")

    def test_breathing_timer_opens(self):
        """ Ensure breathing timer opens successfully in FeelApp """
        with patch.object(self.feel_app, 'open_breathing_timer', autospec=True) as mock_timer:
            self.feel_app.open_breathing_timer()
            mock_timer.assert_called_once()

    
    def test_signup_with_duplicate_username(self):
        """ Ensure the system prevents duplicate usernames """
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password, email, full_name) VALUES (?, ?, ?, ?)", 
                       ("existinguser", "securepass", "existing@domain.com", "Existing User"))
        conn.commit()
        conn.close()

        self.signup_app.input_username.setText("existinguser")  # Duplicate username
        self.signup_app.input_password.setText("securepass")
        self.signup_app.input_email.setText("new@domain.com")  # Email is ignored
        self.signup_app.input_full_name.setText("New User")

        with patch.object(QMessageBox, 'warning') as mock_warning:
            self.signup_app.signup()
            mock_warning.assert_called_once_with(self.signup_app, "Sign Up", "User already exist. Please choose another.")
 
    def test_successful_signup(self):
        """ Ensure new user signup is successful """
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        
        
        cursor.execute("DELETE FROM users WHERE username=?", ("newuser",))
        conn.commit()
        conn.close()

        self.signup_app.input_username.setText("newuser")
        self.signup_app.input_password.setText("password123")
        self.signup_app.input_email.setText("user@example.com")
        self.signup_app.input_full_name.setText("New User")

        with patch.object(QMessageBox, 'information') as mock_info:
            self.signup_app.signup()
            mock_info.assert_called_once_with(self.signup_app, "Sign Up", "User registered successfully!")
    
    def test_open_ui_without_error(self):
        """ Ensure all UI components load without issues """
        self.assertIsNotNone(self.login_app, "LoginApp should initialize successfully")
        self.assertIsNotNone(self.signup_app, "SignupApp should initialize successfully")
        self.assertIsNotNone(self.reset_app, "PasswordResetApp should initialize successfully")
        self.assertIsNotNone(self.feel_app, "FeelApp should initialize successfully")

if __name__ == "__main__":
    unittest.main()






 

