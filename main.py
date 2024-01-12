import sys
import os

from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

basedir = os.path.abspath(os.path.dirname(__file__))
from ui_login.ui_login_copy import MiVentana

# Creacion archivo prestamos.json
prestamos_json_name = "prestamos.json"
prestamos_json_path = os.path.join(basedir, "databases", prestamos_json_name)
if not os.path.exists(prestamos_json_path):
    with open(prestamos_json_path, "w", encoding="utf-8") as file:
        file.write("{}")

def main():
    app = QApplication(sys.argv)
    window = MiVentana()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()