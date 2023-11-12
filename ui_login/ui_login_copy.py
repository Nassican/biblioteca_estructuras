import sys
import os
import re
import json
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *

basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append('../')
try:
    from ui_login import backend
    from ui_principal.ui_principal import Ui_principal
except ImportError:
    print("Error al importar el archivo ui_principal.py")


class MyBar(QWidget):

    def __init__(self, parent):
        super(MyBar, self).__init__()
        self.parent = parent

        self.principal_layout = QVBoxLayout()
        self.principal_layout.setContentsMargins(0, 0, 0, 0)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Botón de cerrar
        self.btn_close = QPushButton()
        path = os.path.join(os.path.dirname(__file__), "../media/images/CloseBtn.png")
        icon = QIcon(path)
        self.btn_close.setIcon(icon)
        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.setFixedSize(25, 25)
        self.btn_close.setStyleSheet("QPushButton {border: 0px;} QPushButton::hover {background-color: #FF7777;}")
        self.btn_close.setCursor(Qt.PointingHandCursor)

        # Botón de minimizar
        self.btn_min = QPushButton()
        path = os.path.join(os.path.dirname(__file__), "../media/images/MinimizeBtn.png")
        icon = QIcon(path)
        self.btn_min.setIcon(icon)
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_min.setFixedSize(25, 25)
        self.btn_min.setStyleSheet("QPushButton {border: 0px;} QPushButton::hover {background-color: #1C3D95;}")
        self.btn_min.setCursor(Qt.PointingHandCursor)

        # Botón de maximizar
        self.btn_max = QPushButton()
        path_max = os.path.join(os.path.dirname(__file__), "../media/images/MaximizeBtn.png")
        self.icon_max = QIcon(path_max)
        self.btn_max.setIcon(self.icon_max)
        self.btn_max.clicked.connect(self.btn_max_clicked)
        self.btn_max.setFixedSize(25, 25)
        self.btn_max.setStyleSheet("QPushButton {border: 0px;} QPushButton::hover {background-color: #1C3D95;}")
        self.btn_max.setCursor(Qt.PointingHandCursor)

        icons_widget = QWidget()
        icons_widget.setMaximumWidth(100)
        icons_widget.setContentsMargins(0, 0, 0, 0)
        icons_layout = QHBoxLayout()
        icons_layout.setContentsMargins(0, 0, 0, 0)
        icons_layout.addWidget(self.btn_min)
        icons_layout.addWidget(self.btn_max)
        icons_layout.addWidget(self.btn_close)
        icons_widget.setLayout(icons_layout)
        icons_layout.setAlignment(Qt.AlignRight)

        name_library_widget = QLabel("Biblioteca SoftPro")
        name_library_widget.setStyleSheet("color: white; font-size: 15px; font-weight: bold;")
        name_library_widget.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.layout.addWidget(name_library_widget)
        self.layout.addWidget(icons_widget)

        self.principal_layout.addLayout(self.layout)
        self.setLayout(self.principal_layout)

        self.start = QPoint(0, 0)
        self.pressing = False

    def resizeEvent(self, QResizeEvent):
        super(MyBar, self).resizeEvent(QResizeEvent)

    def mousePressEvent(self, event):
        self.start = event.globalPos()
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            end = event.globalPos()
            self.parent.move(self.parent.pos() + end - self.start)
            self.start = end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False

    def btn_close_clicked(self):
        self.parent.close()

    def btn_max_clicked(self):
        if self.parent.isMaximized():
            self.btn_max.setIcon(self.icon_max)
            self.parent.showNormal()
        else:
            self.parent.showMaximized()
            path_rest = os.path.join(os.path.dirname(__file__), "../media/images/RestoreDownBtn.png")
            self.icon_rest = QIcon(path_rest)
            self.btn_max.setIcon(self.icon_rest)

    def btn_min_clicked(self):
        self.parent.showMinimized()

class Login(QWidget):
    def __init__(self):
        super().__init__()

        # Crear los widgets
        self.label_logo = QLabel()
        self.label_logo.setPixmap(QPixmap(os.path.join(basedir, "../media/img/logo_universidad_redimensioned.png")))
        self.label_logo.setFixedHeight(100)
        self.label_logo.setScaledContents(True)
        self.label_logo.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.label_user = QLabel("Usuario:")
        self.line_edit_user = QLineEdit()
        self.line_edit_user.setPlaceholderText("Usuario")

        self.label_password = QLabel("Contraseña:")
        self.line_edit_password = QLineEdit()
        self.line_edit_password.setPlaceholderText("Contraseña")
        self.line_edit_password.setEchoMode(QLineEdit.Password)

        self.show_password_button = QPushButton()
        self.show_password_button.setMaximumSize(50, 50)
        self.show_password_button.setCursor(Qt.PointingHandCursor)
        self.show_password_button.setCheckable(True)
        self.show_password_button.toggled.connect(self.toggle_password_visibility)
        self.show_password_button.setIcon(QIcon(os.path.join(basedir, "../media/img/eye-open.png")))

        self.contain_password = QWidget()
        self.contain_password_layout = QHBoxLayout()
        self.contain_password_layout.setContentsMargins(0, 0, 0, 0)
        self.contain_password_layout.setSpacing(0)
        self.contain_password_layout.addWidget(self.line_edit_password)
        self.contain_password_layout.addWidget(self.show_password_button)
        self.contain_password.setLayout(self.contain_password_layout)

        self.contain_password.setStyleSheet(
            "QWidget {"
            "border: 2px solid black; "
            "border-radius: 10px; "
            "padding: 10px; "
            "}"
            "QPushButton {"
            "background-color: transparent; "
            "border: none; "
            "padding: 5px;"
            "}"
        )
        self.line_edit_password.setStyleSheet(
            "background-color: transparent;"
            "border: 0px;"
            "border-radius: 10px; "
            "padding: 7px; "
            "font-size: 15px; "
        )

        self.button_login = QPushButton("Iniciar sesión")
        self.button_login.setCursor(Qt.PointingHandCursor)

        self.label_register = QLabel("¿No tienes cuenta?")
        self.label_register_button = QPushButton("Regístrate")
        self.label_register_button.setCursor(Qt.PointingHandCursor)

        # Agregar los widgets al layout
        separacion = 50
        layout = QVBoxLayout(self)
        layout.addWidget(self.label_logo)
        layout.addItem(QSpacerItem(separacion, separacion))
        #layout.addWidget(self.label_user)
        layout.addWidget(self.line_edit_user)
        #layout.addWidget(self.label_password)
        layout.addWidget(self.contain_password)
        layout.addItem(QSpacerItem(separacion, separacion))
        layout.addWidget(self.button_login)

        layout_register = QHBoxLayout()
        layout_register.setContentsMargins(0, separacion, 0, 0)
        layout_register.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_register.addWidget(self.label_register)
        layout_register.addWidget(self.label_register_button)

        layout.addLayout(layout_register)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet(
            "QLabel {"
            "font-size: 15px; "
            "font-weight: bold; "
            "} "
            "QLineEdit {"
            "border: 2px solid black; "
            "border-radius: 10px; "
            "padding: 5px; "
            "font-size: 15px; "
            "}"
            "QPushButton {"
            "background-color: #2F53D1; "
            "color: white; "
            "border-radius: 10px; "
            "padding: 5px; "
            "font-size: 15px; "
            "font-weight: bold; "
            "}"
            "QPushButton::hover {"
            "background-color: #1C3D95; "
            "}"
            "QPushButton:pressed {"
            "background-color: #2F5777"
            "}"
            )
        self.label_register_button.setStyleSheet("background-color: white; color: #2F53D1; font-weight: bold; text-decoration: underline;")
        self.setLayout(layout)

    def toggle_password_visibility(self, checked):
        if checked:
            self.line_edit_password.setEchoMode(QLineEdit.Normal)
            self.show_password_button.setIcon(QIcon(os.path.join(basedir, "../media/img/eye-close.png")))
        else:
            self.show_password_button.setIcon(QIcon(os.path.join(basedir, "../media/img/eye-open.png")))
            self.line_edit_password.setEchoMode(QLineEdit.Password)



class Register(QWidget):
    def __init__(self):
        super().__init__()

        # Crear los widgets
        self.label_logo = QLabel()
        self.label_logo.setPixmap(QPixmap(os.path.join(basedir, "../media/img/logo_universidad_redimensioned.png")))
        self.label_logo.setFixedHeight(100)
        self.label_logo.setScaledContents(True)
        self.label_logo.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.label_ident = QLabel("Identificación:")
        self.line_edit_ident = QLineEdit()
        self.line_edit_ident.setPlaceholderText("Número de identificación")
        self.line_edit_ident.setValidator(QIntValidator())

        self.label_user = QLabel("Usuario:")
        self.line_edit_user = QLineEdit()
        self.line_edit_user.setPlaceholderText("Usuario")

        self.label_names = QLabel("Nombre:")
        self.line_edit_names = QLineEdit()
        self.line_edit_names.setPlaceholderText("Nombre - Apellido")

        self.label_cellphone_number = QLabel("Celular")
        self.line_edit_cellphone_number = QLineEdit()
        self.line_edit_cellphone_number.setPlaceholderText("Celular")
        self.line_edit_cellphone_number.setValidator(QIntValidator())
        self.line_edit_cellphone_number.setMaxLength(10)

        self.label_password = QLabel("Contraseña:")
        self.line_edit_password = QLineEdit()
        self.line_edit_password.setPlaceholderText("Contraseña")
        self.line_edit_password.setEchoMode(QLineEdit.Password)

        self.show_password_button = QPushButton()
        self.show_password_button.setMaximumSize(50, 50)
        self.show_password_button.setCursor(Qt.PointingHandCursor)
        self.show_password_button.setCheckable(True)
        self.show_password_button.toggled.connect(self.toggle_password_visibility)
        self.show_password_button.setIcon(QIcon(os.path.join(basedir, "../media/img/eye-open.png")))

        self.contain_password = QWidget()
        self.contain_password_layout = QHBoxLayout()
        self.contain_password_layout.setContentsMargins(0, 0, 0, 0)
        self.contain_password_layout.setSpacing(0)
        self.contain_password_layout.addWidget(self.line_edit_password)
        self.contain_password_layout.addWidget(self.show_password_button)
        self.contain_password.setLayout(self.contain_password_layout)

        self.contain_password.setStyleSheet(
            "QWidget {"
            "border: 2px solid black; "
            "border-radius: 10px; "
            "padding: 10px; "
            "}"
            "QPushButton {"
            "background-color: transparent; "
            "border: none; "
            "padding: 5px;"
            "}"
        )
        self.line_edit_password.setStyleSheet(
            "background-color: transparent;"
            "border: 0px;"
            "border-radius: 10px; "
            "padding: 7px; "
            "font-size: 15px; "
        )

        self.label_confirm_password = QLabel("Confirmar Contraseña:")
        self.line_edit_confirm_password = QLineEdit()
        self.line_edit_confirm_password.setPlaceholderText("Confirmar Contraseña")
        self.line_edit_confirm_password.setEchoMode(QLineEdit.Password)

        self.show_confirm_password_button = QPushButton()
        self.show_confirm_password_button.setMaximumSize(50, 50)
        self.show_confirm_password_button.setCursor(Qt.PointingHandCursor)
        self.show_confirm_password_button.setCheckable(True)
        self.show_confirm_password_button.toggled.connect(self.toggle_confirm_password_visibility)
        self.show_confirm_password_button.setIcon(QIcon(os.path.join(basedir, "../media/img/eye-open.png")))

        self.contain_confirm_password = QWidget()
        self.contain_confirm_password_layout = QHBoxLayout()
        self.contain_confirm_password_layout.setContentsMargins(0, 0, 0, 0)
        self.contain_confirm_password_layout.setSpacing(0)
        self.contain_confirm_password_layout.addWidget(self.line_edit_confirm_password)
        self.contain_confirm_password_layout.addWidget(self.show_confirm_password_button)
        self.contain_confirm_password.setLayout(self.contain_confirm_password_layout)

        self.contain_confirm_password.setStyleSheet(
            "QWidget {"
            "border: 2px solid black; "
            "border-radius: 10px; "
            "padding: 10px; "
            "}"
            "QPushButton {"
            "background-color: transparent; "
            "border: none; "
            "padding: 5px;"
            "}"
        )
        self.line_edit_confirm_password.setStyleSheet(
            "background-color: transparent;"
            "border: 0px;"
            "border-radius: 10px; "
            "padding: 7px; "
            "font-size: 15px; "
        )

        # Conecta la señal textChanged del QLineEdit de confirmación de contraseña
        self.line_edit_confirm_password.textChanged.connect(self.validate_password)
        # Almacena la última contraseña válida
        self.validated_password = ""

        self.button_register = QPushButton("Registrarse")
        self.button_register.setCursor(Qt.PointingHandCursor)
        self.button_register.clicked.connect(self.boton_register_pressed)

        self.label_login = QLabel("¿Ya tienes cuenta?")
        self.label_login_button = QPushButton("Iniciar Sesion")
        self.label_login_button.setCursor(Qt.PointingHandCursor)

        # Agregar los widgets al layout
        separacion = 30
        layout = QVBoxLayout(self)
        layout.addWidget(self.label_logo)
        layout.addItem(QSpacerItem(separacion, separacion))
        layout.addWidget(self.line_edit_ident)
        layout.addWidget(self.line_edit_user)
        layout.addWidget(self.line_edit_names)
        layout.addWidget(self.line_edit_cellphone_number)

        #layout.addWidget(self.label_password)
        layout.addWidget(self.contain_password)
        layout.addWidget(self.contain_confirm_password)
        layout.addItem(QSpacerItem(separacion, separacion))
        layout.addWidget(self.button_register)

        layout_register = QHBoxLayout()
        layout_register.setContentsMargins(0, separacion, 0, 0)
        layout_register.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_register.addWidget(self.label_login)
        layout_register.addWidget(self.label_login_button)

        layout.addLayout(layout_register)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setStyleSheet(
            "QLabel {"
            "font-size: 15px; "
            "font-weight: bold; "
            "} "
            "QLineEdit {"
            "border: 2px solid black; "
            "border-radius: 10px; "
            "padding: 5px; "
            "font-size: 15px; "
            "}"
            "QPushButton {"
            "background-color: #2F53D1; "
            "color: white; "
            "border-radius: 10px; "
            "padding: 5px; "
            "font-size: 15px; "
            "font-weight: bold; "
            "}"
            "QPushButton::hover {"
            "background-color: #1C3D95; "
            "}"
            "QPushButton:pressed {"
            "background-color: #2F5777"
            "}"
            )
        self.stylebutton_login_register = (
            "QPushButton {"
            "background-color: #2F53D1; "
            "color: white; "
            "border-radius: 10px; "
            "padding: 5px; "
            "font-size: 15px; "
            "font-weight: bold; "
            "}"
            "QPushButton::hover {"
            "background-color: #1C3D95; "
            "}"
            "QPushButton:pressed {"
            "background-color: #2F5777"
            "}"
        )
        self.label_login_button.setStyleSheet("background-color: white; color: #2F53D1; font-weight: bold; text-decoration: underline;")
        self.setLayout(layout)

    def toggle_password_visibility(self, checked):
        if checked:
            self.line_edit_password.setEchoMode(QLineEdit.Normal)
            self.show_password_button.setIcon(QIcon(os.path.join(basedir, "../media/img/eye-close.png")))
        else:
            self.show_password_button.setIcon(QIcon(os.path.join(basedir, "../media/img/eye-open.png")))
            self.line_edit_password.setEchoMode(QLineEdit.Password)

    def toggle_confirm_password_visibility(self, checked):
        if checked:
            self.line_edit_confirm_password.setEchoMode(QLineEdit.Normal)
            self.show_confirm_password_button.setIcon(QIcon(os.path.join(basedir, "../media/img/eye-close.png")))
        else:
            self.show_confirm_password_button.setIcon(QIcon(os.path.join(basedir, "../media/img/eye-open.png")))
            self.line_edit_confirm_password.setEchoMode(QLineEdit.Password)

    def validate_password(self):
        password = self.line_edit_password.text()
        confirm_password = self.line_edit_confirm_password.text()

        if password == confirm_password:
            self.contain_confirm_password.setStyleSheet(
                "QWidget {"
                "border: 2px solid black; "
                "border-radius: 10px; "
                "padding: 10px; "
                "}"
                "QPushButton {"
                "background-color: transparent; "
                "border: none; "
                "padding: 5px;"
                "}"
                )  # Borra el estilo de texto rojo
            self.button_register.setEnabled(True)  # Habilita el botón de registro
            self.button_register.setStyleSheet(self.stylebutton_login_register)
            self.validated_password = password
        else:
            # Establece un estilo de texto rojo para indicar que no coinciden
            self.contain_confirm_password.setStyleSheet(
                "QWidget {"
                "border: 2px solid #991515; "
                "border-radius: 10px; "
                "padding: 10px; "
                "}"
                "QPushButton {"
                "background-color: transparent; "
                "border: none; "
                "padding: 5px;"
                "}"
            )
            self.button_register.setEnabled(False)  # Deshabilita el botón de registro
            self.button_register.setStyleSheet("background-color: #7995F9;")  # Establece el color de texto gris
            self.validated_password = ""

    def boton_register_pressed(self):
        ident = self.line_edit_ident.text()
        username = self.line_edit_user.text()
        names = self.line_edit_names.text()
        cellphone_number = self.line_edit_cellphone_number.text()
        password = self.validated_password


        alert_message = QMessageBox()
        alert_message.setWindowTitle("Error en formulario de registro")
        alert_message.setWindowIcon(QIcon(os.path.join(basedir, "../media/img/libro.png")))
        alert_message.setIcon(QMessageBox.Critical)
        alert_message_button = QPushButton("Aceptar")
        alert_message_button.setCursor(Qt.PointingHandCursor)
        alert_message.addButton(alert_message_button, QMessageBox.YesRole)
        alert_message.setStyleSheet(
            "QMessageBox{ "
            "border: 10px;"
            "font-size: 15px; "
            "}"
            "QPushButton {"
            "background-color: #2F53D1; "
            "color: white; "
            "border-radius: 10px; "
            "padding: 5px; "
            "padding-left: 10px; "
            "padding-right: 10px; "
            "font-size: 15px; "
            "font-weight: bold; "
            "}"
            "QPushButton::hover {"
            "background-color: #1C3D95; "
            "}"
            "QPushButton:pressed {"
            "background-color: #2F5777"
            "}"
        )

        if not ident and not username and not names and not cellphone_number and not password:
            alert_message.setText("Todos los campos son obligatorios.")
            alert_message.exec()
        elif not ident:
            alert_message.setText("El campo de identificación no puede estar vacío.")
            alert_message.exec()
        elif not username:
            alert_message.setText("El campo de usuario no puede estar vacío.")
            alert_message.exec()
        elif not names:
            alert_message.setText("El campo de nombre no puede estar vacío.")
            alert_message.exec()
        elif not cellphone_number:
            alert_message.setText("El campo de celular no puede estar vacío.")
            alert_message.exec()
        elif not password:
            alert_message.setText("El campo de contraseña no puede estar vacío.")
            alert_message.exec()
        elif len(cellphone_number) < 10:
            alert_message.setText("El número de celular debe tener 10 dígitos.")
            alert_message.exec()
        elif backend.id_personal_esta_disponible(int(ident)) == False:
            alert_message.setText("El número de identificación ya está en uso.")
            alert_message.exec()
        elif backend.usuario_esta_disponible(username) == False:
            alert_message.setText("El nombre de usuario ya está en uso.")
            alert_message.exec()
        else:
            uuid_generated = backend.generate_uuid()
            new_user = {
                "uuid": uuid_generated,
                "id_personal": int(ident),
                "username": username,
                "nombre": names,
                "cellphone": cellphone_number,
                "password": password,
                "rol": "usuario"
            }
            #print(new_user)
            #print(f"Registro exitoso con uuid: {uuid_generated}")
            try:
                backend.register_user_in_database(new_user)
                alert_message.setWindowTitle("Registro exitoso")
                alert_message.setIcon(QMessageBox.Information)
                alert_message.setText("Registro exitoso.")
                alert_message.exec()
                self.line_edit_ident.setText("")
                self.line_edit_user.setText("")
                self.line_edit_names.setText("")
                self.line_edit_cellphone_number.setText("")
                self.line_edit_password.setText("")
                self.line_edit_confirm_password.setText("")
            except Exception as e:
                print(e)
                alert_message.setIcon(QMessageBox.Critical)
                alert_message.setText("Ha ocurrido un error al registrar el usuario.")
                alert_message.exec()

class MiVentana(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setStyleSheet("background-color: white")

        self.setGeometry(50, 50, 800, 600)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.login()

    def login(self):
        central_layout = QHBoxLayout()
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)

        lb_logo = QLabel(self)
        lb_logo.setContentsMargins(0, 0, 0, 0)
        logo = QPixmap(os.path.join(basedir, "../media/img/libros-fondo.jpg"))  # Agrega la extensión del archivo de imagen
        lb_logo.setPixmap(logo)
        lb_logo.setScaledContents(True)
        lb_logo.setMinimumHeight(500)
        lb_logo.setMinimumWidth(600)

        login_widget = QWidget()
        login_widget.setMinimumWidth(400)
        login_widget.setContentsMargins(0, 0, 0, 0)
        login_layout = QVBoxLayout()
        login_layout.setSpacing(0)
        login_layout.setContentsMargins(0, 0, 0, 0)
        login_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        bar_widget = QWidget()
        bar_widget.setContentsMargins(0, 0, 0, 0)
        bar_widget.setStyleSheet("background-color: #2F53D1;")
        bar_layout = QHBoxLayout()

        bar_title = MyBar(self)
        bar_title.setContentsMargins(0, 0, 0, 0)
        bar_title.setMaximumHeight(40)
        bar_layout.addWidget(bar_title)
        bar_widget.setLayout(bar_layout)

        login_form_widget = QWidget()
        login_form_widget.setContentsMargins(0, 0, 0, 0)

        self.stacked_widget = QStackedWidget()
        self.login_widget = Login()
        self.register_widget = Register()

        self.stacked_widget.addWidget(self.login_widget)
        self.stacked_widget.addWidget(self.register_widget)

        self.stacked_widget.setContentsMargins(60, 0, 60, 0)
        self.label_register_button = self.login_widget.label_register_button
        self.label_register_button.clicked.connect(self.on_register_button_clicked)

        self.label_login_button = self.register_widget.label_login_button
        self.label_login_button.clicked.connect(self.on_login_button_clicked)

        self.login_widget.button_login.clicked.connect(self.loguearse_button_clicked)

        login_layout.addWidget(bar_widget)
        login_layout.addWidget(self.stacked_widget)
        login_widget.setLayout(login_layout)

        central_layout.addWidget(lb_logo)
        central_layout.addWidget(login_widget)

        self.setLayout(central_layout)

    def on_login_button_clicked(self):
        self.stacked_widget.setCurrentWidget(self.login_widget)

    def on_register_button_clicked(self):
        self.stacked_widget.setCurrentWidget(self.register_widget)

    def loguearse_button_clicked(self):
        username = self.login_widget.line_edit_user.text()
        password = self.login_widget.line_edit_password.text()

        self.message = QMessageBox()
        self.button_message = QPushButton("Aceptar")
        self.button_message.setCursor(Qt.PointingHandCursor)
        self.message.addButton(self.button_message, QMessageBox.AcceptRole)
        self.message.setIcon(QMessageBox.Critical)
        self.message.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "../media/img/libro.png")))
        self.message.setStyleSheet(
            "QMessageBox{ "
            "border: 10px;"
            "font-size: 15px; "
            "}"
            "QPushButton {"
            "background-color: #2F53D1; "
            "color: white; "
            "border-radius: 10px; "
            "padding: 5px; "
            "padding-left: 10px; "
            "padding-right: 10px; "
            "font-size: 15px; "
            "font-weight: bold; "
            "}"
            "QPushButton::hover {"
            "background-color: #1C3D95; "
            "}"
            "QPushButton:pressed {"
            "background-color: #2F5777"
            "}"
        )

        if username == "" or password == "":
            self.message.setWindowTitle("Biblioteca SoftPro - Error")
            self.message.setText("Usuario o contraseña incompletos.")
            self.message.exec()
            return

        authenticated = backend.verificar_credenciales(username, password)

        if authenticated:
            print("Autenticado correctamente.")
            print(f"¡Bienvenido, {authenticated['nombre']}!")
            ventana = Ui_principal(authenticated)
            self.close()
            ventana.show()

            if authenticated['rol'] == 'admin':
                print("Eres un administrador.")
            else:
                print("Eres un usuario estándar.")
        else:
            # Mostrar un mensaje de error en caso de autenticación fallida.
            self.message.setWindowTitle("Biblioteca SoftPro - Error")
            self.message.setText("Usuario o contraseña incorrectos.")
            self.message.exec()


def main():
    app = QApplication(sys.argv)
    window = MiVentana()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
