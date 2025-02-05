import sys
from PyQt5.QtWidgets import QApplication
from controller import FocusMindApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FocusMindApp()
    window.show()
    sys.exit(app.exec_())
