import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QProgressBar
from PyQt5.QtCore import QTimer, Qt

class BreathingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.sessions_completed = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.time_left = 10
#
    def go_back(self):
        from log import FeelApp  
        self.feel_window = FeelApp()  
        self.feel_window.show()
        self.close()  

    def init_ui(self):
        self.setGeometry(100, 100, 500, 500) 
       
        screen = QApplication.desktop().screenGeometry()
        self.move((screen.width() - self.width()) // 2, (screen.height() - self.height()) // 2)

        layout = QVBoxLayout()
        self.setStyleSheet("background-color: #A7D7A9;")

        self.character_label = QLabel("😀", self)
        self.character_label.setAlignment(Qt.AlignCenter)
        self.character_label.setStyleSheet("font-size: 50px;")
        layout.addWidget(self.character_label)

        self.motivation_label = QLabel("Take a deep breath and enjoy the moment! 🍃", self)
        self.motivation_label.setAlignment(Qt.AlignCenter)
        self.motivation_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #0077B6;")
        layout.addWidget(self.motivation_label)

        self.timer_label = QLabel("10", self)
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(self.timer_label)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMaximum(10)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        self.start_button = QPushButton("Start Session", self)
        self.start_button.setStyleSheet("background-color: #4CAF50; color: white; font-size: 16px; padding: 10px;")
        self.start_button.clicked.connect(self.start_session)
        layout.addWidget(self.start_button)

        self.restart_button = QPushButton("Restart", self)
        self.restart_button.setStyleSheet("background-color: #FFC107; color: white; font-size: 16px; padding: 10px;")
        self.restart_button.clicked.connect(self.start_session)
        self.restart_button.setEnabled(False)
        layout.addWidget(self.restart_button)

        self.close_button = QPushButton("Close Session", self)
        self.close_button.setStyleSheet("background-color: #FF5733; color: white; font-size: 16px; padding: 10px;")
        self.close_button.clicked.connect(self.close_session)
        self.close_button.setEnabled(False)
        layout.addWidget(self.close_button)
#
        self.back_button = QPushButton("Back", self)
        self.back_button.setStyleSheet("background-color: #D3D3D3; font-size: 16px; padding: 10px;")
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)#


        self.setLayout(layout)
        self.setWindowTitle("Breathing Exercise")

    def start_session(self):
        self.time_left = 10
        self.update_emoji("😌", enlarge=True)
        self.timer.start(1000)
        self.progress_bar.setValue(0)
        self.timer_label.setText(str(self.time_left))
        self.close_button.setEnabled(False)
        self.restart_button.setEnabled(False)
        self.motivation_label.setText("You're doing great! Keep going! 💪")

    def update_timer(self):
        if self.time_left > 5:
            self.update_emoji("😌", enlarge=True)
            self.motivation_label.setText("Take a deep breath... 😌")
        elif self.time_left > 0:
            self.update_emoji("😊", enlarge=False)
            self.motivation_label.setText("Exhale slowly... 😊")
        else:
            self.update_emoji("🎉")
            self.timer.stop()
            self.close_button.setEnabled(True)
            self.restart_button.setEnabled(True)

            self.character_label.setText("🎉 Great! You've finished the session! 💖")
            self.character_label.setWordWrap(True)
            self.character_label.setStyleSheet("font-size: 20px;")

            self.motivation_label.setText("Well done! Always take care of yourself. 🌟")

        self.progress_bar.setValue(10 - self.time_left)
        self.timer_label.setText(str(self.time_left))
        self.time_left -= 1

    def update_emoji(self, emoji, enlarge=False):
        self.character_label.setText(emoji)
        if enlarge:
            self.character_label.setStyleSheet("font-size: 70px;")
        else:
            self.character_label.setStyleSheet("font-size: 50px;")

    def close_session(self):
        self.close()


class BreathingMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 500, 500)  
        self.setWindowTitle("Breathing Timer")

        self.timer_label = QLabel("Ready to Breathe?", self)
        self.start_button = QPushButton("Start Timer", self)
        self.start_button.clicked.connect(self.start_timer)

        layout = QVBoxLayout()
        layout.addWidget(self.timer_label)
        layout.addWidget(self.start_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.time_left = 10

    def start_timer(self):
        self.time_left = 10
        self.timer_label.setText(f"Time Left: {self.time_left}")
        self.timer.start(1000)

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.setText(f"Time Left: {self.time_left}")
        else:
            self.timer.stop()
            self.timer_label.setText("Done! Great job! 🎉")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window1 = BreathingApp()
    window2 = BreathingMainWindow()

    window1.show()
    window2.show()

    sys.exit(app.exec_())
