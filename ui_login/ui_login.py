import sys
from PySide6.QtWidgets import*
from PySide6.QtGui import*
from PySide6.QtCore import*
import sys
import os

basedir = os.path.dirname(__file__)

from ui_functions import register

class MiVentana(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(534, 400)
        self.setStyleSheet("background-color: white;")
        self.login()


    def login(self):
        #Establecer layout
        grid_layout = QGridLayout(self)
        
        #Definir y establecer logo
        lb_logo = QLabel(self)
        logo = QPixmap(os.path.join(basedir, "img", "logo_biblioteca2"))
        lb_logo.setPixmap(logo)
        lb_logo.adjustSize()
        grid_layout.addWidget(lb_logo, 0, 0, 7, 1)

        #Iconos
        lb_icon = QLabel(self)
        icon = QPixmap(os.path.join(basedir, "img", "icon_uni2"))
        lb_icon.setPixmap(icon)
        lb_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(lb_icon, 0, 1)

        #Titulo
        lb_title = QLabel("Biblioteca\nSoftpro\n")
        font = QFont("Play", 36)
        lb_title.setStyleSheet("color:#2F53D1")
        #font = lb_title.font()
        #font.setPointSize(26)
        
        lb_title.setFont(font)
        lb_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_layout.addWidget(lb_title, 1, 1)

        #user and password
        led_user = QLineEdit(self)
        led_user.setPlaceholderText("User")
        grid_layout.addWidget(led_user, 3, 1)
        led_user.setAlignment(Qt.AlignmentFlag.AlignCenter)
        

        led_pass = QLineEdit(self)
        led_pass.setPlaceholderText("Password")
        grid_layout.addWidget(led_pass, 4, 1)
        led_pass.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #registrate
        hor_layout = QHBoxLayout()
        lb_tienes = QLabel("¿No tienes una cuenta?")
        bt_registrar = QPushButton("Registrar")
        bt_registrar.setStyleSheet(
            """
            QPushButton {
                color: white;
                background-color: #2F53D1;
                border-style: outset;
                border-width: 2px;
                border-radius: 10px;
                border-color: beige;
                font: bold 12px;
                min-width: 7em;
                padding: 6px;
            }
            QPushButton:pressed {
                background-color: white;
                border-style: inset;
            }
            """
        )

        '''lb_registrate = QLabel()
        lb_registrate.setText('<a href="https://www.ejemplo.com">Registrar</a>')
        font_bold = lb_registrate.font()
        font_bold.setBold(True)
        lb_registrate.setFont(font_bold)
        lb_registrate.setOpenExternalLinks(True)'''

        hor_layout.addWidget(lb_tienes)
        hor_layout.addWidget(bt_registrar)
        #hor_layout.addWidget(lb_registrate)
        grid_layout.addLayout(hor_layout, 5, 1)
        #lb_registrate.linkActivated.connect(self.open_new_window)

        #Listeneres
        bt_registrar.clicked.connect(lambda: register(self))


    def open_new_window(self, link):
        # Aquí puedes definir el comportamiento para abrir una nueva ventana en tu aplicación
        # Por ahora, mostraremos un mensaje para simular el comportamiento
        QMessageBox.information(self, "Enlace Activado", f"Enlace activado: {link}")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MiVentana()
    window.show()
    sys.exit(app.exec())
