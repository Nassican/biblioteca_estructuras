import sys
import json
import os
import requests

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

from ui_principal.ui_principal import Ui_principal
from ui_login.ui_login import MiVentana


def main():
    app = QApplication(sys.argv)
    window = MiVentana()
    window = Ui_principal()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()