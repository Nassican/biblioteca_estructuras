import sys
from PySide6.QtWidgets import*
from PySide6.QtGui import*
from PySide6.QtCore import*
import sys
import os

basedir = os.path.dirname(__file__)

class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(550, 200, 400, 500)
        self.login()

    def login(self):
        h_layout = QHBoxLayout()
        self.setLayout(h_layout)
        lb_logo = QLabel(self)
        lb_logo.setPixmap(QPixmap(os.path.join(basedir, "img", "logo_biblioteca")))
        lb_logo.adjustSize()
        h_layout.addWidget(lb_logo)

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MiVentana()
    window.show()
    sys.exit(app.exec_())
