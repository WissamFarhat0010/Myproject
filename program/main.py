import sys
from PyQt5.QtWidgets import QApplication
from log import FocusMindApp

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        window = FocusMindApp()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Application error: {e}")
        