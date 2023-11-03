import sys
from PySide6.QtWidgets import*
from PySide6.QtGui import*
from PySide6.QtCore import*
import sys
import os
basedir = os.path.dirname(__file__)

def register(MiVentana):
    #Opciones principales
    registro = QMainWindow(MiVentana)
    registro.setWindowTitle("Registro")
    registro.setFixedSize(600, 400)

    #layout con logo
    grid_layout = QGridLayout()
    lb_logo = QLabel(registro)
    logo = QPixmap(os.path.join(basedir, "img", "logo_biblioteca2"))
    lb_logo.setPixmap(logo)
    lb_logo.adjustSize()
    grid_layout.addWidget(lb_logo, 0, 0, 9, 1)

    #Icono y titulo
    lb_icon = QLabel(registro)
    icon = QPixmap(os.path.join(basedir, "img", "icon_uni2"))
    lb_icon.setPixmap(icon)
    lb_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
    lb_icon.adjustSize()
    grid_layout.addWidget(lb_icon, 0, 1)
    

    #Titulo
    lb_title = QLabel("Registro")
    lb_title.setStyleSheet("color:#2F53D1;")
    font = QFont("Play", 30)
    lb_title.setFont(font)
    lb_title.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
    grid_layout.addWidget(lb_title, 1, 1)

    #Inputs
    led_name = QLineEdit()
    led_name.setPlaceholderText("Nombre")
    led_doc = QLineEdit()
    led_doc.setPlaceholderText("Documento")
    led_cel = QLineEdit()
    led_cel.setPlaceholderText("Celular")
    led_user = QLineEdit()
    led_user.setPlaceholderText("Nombre de usuario")

    led_rol = QLineEdit()
    led_rol.setPlaceholderText("Rol")
    led_pass = QLineEdit()
    led_pass.setPlaceholderText("Contraseña")

    grid_layout.addWidget(led_name, 2, 1)
    grid_layout.addWidget(led_doc, 3, 1)
    grid_layout.addWidget(led_cel, 4, 1)
    grid_layout.addWidget(led_user, 5, 1)
    grid_layout.addWidget(led_rol, 6, 1)
    grid_layout.addWidget(led_pass, 7, 1)

    #Boton
    bt_reg = QPushButton("Registrar")
    bt_reg.setStyleSheet(
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
    
    grid_layout.addWidget(bt_reg, 8, 1)


    #Establecer ventana con layout
    widget_principal = QWidget()
    widget_principal.setLayout(grid_layout)
    registro.setCentralWidget(widget_principal)

    registro.show()