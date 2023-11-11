import sys

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from ui_login.ui_login_copy import MiVentana


def main():
    app = QApplication(sys.argv)
    window = MiVentana()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()