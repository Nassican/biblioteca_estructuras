import os

from PySide6.QtWidgets import (
  QVBoxLayout,
  QWidget,
  QPushButton,
  QLabel,
  QSizePolicy,
  QGraphicsDropShadowEffect,
  QApplication
)

from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize, Qt, Signal, QPropertyAnimation

basedir = os.path.abspath(os.path.dirname(__file__))

class SideMenu(QWidget):
    logout_signal = Signal()
    def __init__(self, parent, user_data):
        super(SideMenu, self).__init__()
        self.setFixedWidth(70)
        self.parent = parent
        self.user_data = user_data
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.is_expanded = False
        self.layout.setSpacing(10)
        self.setStyleSheet(
            "QPushButton {"
            "   padding: 10px;"
            "   text-align: left;"
            "   font-size: 18px;"
            "   border: none;"
            "   color: #FFFFFF;"
            "   border-radius: 10px;"
            "}"
            "QPushButton:hover {"
            "   background-color: #1C3D95;"
            "}"
            "QPushButton:pressed {"
            "   background-color: #2F5777"
            "}"
            "QWidget {"
            "   background-color: #2F53D1;"
            "}"
        )
        shadow1 = self.shadow_effect()
        shadow2 = self.shadow_effect()
        shadow3 = self.shadow_effect()
        shadow4 = self.shadow_effect()
        shadow5 = self.shadow_effect()
        shadow6 = self.shadow_effect()
        # Botones del menú
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # Ruta relativa al directorio de la carpeta "biblioteca_estructuras"
        img_path = os.path.join(script_dir, "..", "media", "img", "home.png")

        # Convertir a una ruta que Windows pueda entender
        img_path = os.path.normpath(img_path)
        self.button_home = QPushButton(" Inicio", icon=QIcon(img_path), iconSize=QSize(30, 30))
        self.button_home.setGraphicsEffect(shadow1)
        self.button_home.setFixedHeight(50)
        self.button_home.setCursor(Qt.PointingHandCursor)

        img_path = os.path.join(script_dir, "..", "media", "img", "prestamo_admin.png")
        img_path = os.path.normpath(img_path)
        self.button_prestamos_admin = QPushButton(" Prestamos", icon=QIcon(img_path), iconSize=QSize(30, 30))
        self.button_prestamos_admin.setGraphicsEffect(shadow2)
        self.button_prestamos_admin.setFixedHeight(50)
        self.button_prestamos_admin.setCursor(Qt.PointingHandCursor)

        img_path = os.path.join(script_dir, "..", "media", "img", "prestamo.png")
        img_path = os.path.normpath(img_path)
        self.button_prestamos_user = QPushButton(" Mis prestamos", icon=QIcon(img_path), iconSize=QSize(30, 30))
        self.button_prestamos_user.setGraphicsEffect(shadow2)
        self.button_prestamos_user.setFixedHeight(50)
        self.button_prestamos_user.setCursor(Qt.PointingHandCursor)

        img_path = os.path.join(script_dir, "..", "media", "img", "libros-sidemenu.png")
        img_path = os.path.normpath(img_path)
        self.button_admin_libros = QPushButton(" Gestion Libros", icon=QIcon(img_path), iconSize=QSize(30, 30))
        self.button_admin_libros.setGraphicsEffect(shadow3)
        self.button_admin_libros.setFixedHeight(50)
        self.button_admin_libros.setCursor(Qt.PointingHandCursor)

        img_path = os.path.join(script_dir, "..", "media", "img", "user.png")
        img_path = os.path.normpath(img_path)
        self.button_perfil = QPushButton(" Ver Perfil", icon=QIcon(img_path), iconSize=QSize(30, 30))
        self.button_perfil.setGraphicsEffect(shadow4)
        self.button_perfil.setFixedHeight(50)
        self.button_perfil.setCursor(Qt.PointingHandCursor)

        img_path = os.path.join(script_dir, "..", "media", "img", "logout.svg")
        img_path = os.path.normpath(img_path)
        self.button_close_session = QPushButton(" Cerrar sesión", icon=QIcon(img_path), iconSize=QSize(30, 30))
        self.button_close_session.setGraphicsEffect(shadow6)
        self.button_close_session.setFixedHeight(50)
        self.button_close_session.setCursor(Qt.PointingHandCursor)
        self.button_close_session.clicked.connect(self.close_session)

        # Botón para reducir o expandir el menú
        img_path = os.path.join(script_dir, "..", "media", "img", "menu.svg")
        img_path = os.path.normpath(img_path)
        self.toggle_button = QPushButton("", icon=QIcon(img_path), iconSize=QSize(30, 30))
        self.toggle_button.setStyleSheet(
            "QPushButton {"
            "   text-align: left;"
            "}"
        )
        self.toggle_button.setGraphicsEffect(shadow5)
        self.toggle_button.setFixedHeight(50)
        self.toggle_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.toggle_button.setCursor(Qt.PointingHandCursor)
        self.toggle_button.clicked.connect(self.toggle_menu)

        # Apilar los botones en el diseño vertical
        self.layout.addWidget(self.toggle_button)
        self.layout.addWidget(self.button_home)
        self.layout.addWidget(self.button_prestamos_user)
        if self.user_data['rol'] == 'admin':
            self.layout.addWidget(self.button_admin_libros)
            self.layout.addWidget(self.button_prestamos_admin)
        #spacer_item = QSpacerItem(20, 90, QSizePolicy.Minimum, QSizePolicy.Expanding)
        #self.layout.addItem(spacer_item)
        self.layout.addStretch()
        self.layout.addWidget(self.button_perfil)
        self.layout.addWidget(self.button_close_session)

        self.setLayout(self.layout)

        # Configurar la animación para el ancho del menú
        self.animation = QPropertyAnimation(self, b"minimumWidth")
        self.animation.setDuration(100)  # Duración de la animación en milisegundos
        self.animation.setStartValue(70)  # Ancho mínimo
        self.animation.setEndValue(200)  # Ancho máximo

    def shadow_effect(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(0)  # Ajusta según tus preferencias
        shadow.setColor(Qt.black)
        shadow.setOffset(0, 0)

        return shadow

    def toggle_menu(self):
        # Iniciar la animación al hacer clic en el botón de reducción/expansión
        self.is_expanded = not self.is_expanded

        if self.is_expanded:
            self.toggle_button.setText(" Cerrar Menu")
        else:
            self.toggle_button.setText("")

        self.animation.setDirection(QPropertyAnimation.Forward if self.is_expanded else QPropertyAnimation.Backward)
        self.animation.start()

        # Configurar el texto visible de los botones en función del estado del menú
        self.button_home.setText(" Inicio" if self.is_expanded else "")
        self.button_prestamos_admin.setText(" Prestamos" if self.is_expanded else "")
        self.button_prestamos_user.setText(" Mis Prestamos" if self.is_expanded else "")
        self.button_admin_libros.setText(" Gestión Libros" if self.is_expanded else "")
        self.button_perfil.setText(" Ver Perfil" if self.is_expanded else "")
        self.button_close_session.setText(" Cerrar sesión" if self.is_expanded else "")


    def close_session(self):
        self.parent.close()
        from ui_login.ui_login_copy import MiVentana
        window = MiVentana()
        window.show()

class ContentWidget(QWidget):
    def __init__(self):
        super(ContentWidget, self).__init__()

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Contenido de la aplicación
        label = QLabel("Contenido principal")
        label.setStyleSheet("background-color: #FFFFFF;")
        self.layout.addWidget(label)

        self.setLayout(self.layout)



if __name__ == "__main__":
    app = QApplication([])

    window = SideMenu(None, None)
    window.show()

    app.exec_()