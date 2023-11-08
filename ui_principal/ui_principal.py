import sys
import json
import os
import requests

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QMenu,
    QMenuBar,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QMessageBox,
    QScrollArea,
    QSizePolicy,
    QSpacerItem
)
from PySide6.QtGui import *
from PySide6.QtCore import Qt, QThread, Signal, QPoint

class MyBar(QWidget):

    def __init__(self, parent, user_data):
        super(MyBar, self).__init__()
        self.parent = parent
        self.user_data = user_data
        print(self.parent.width())
        self.principal_layuot = QVBoxLayout()
        self.principal_layuot.setContentsMargins(0,0,0,0)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0,0,10,0)

        # ----------------------------------------------------------------------
        # Seccion de botones de la barra de titulo
        btn_size = 25

        # Boton de cerrar
        self.btn_close = QPushButton()
        path = os.path.join(os.path.dirname(__file__), "../media/images/CloseBtn.png")
        icon = QIcon(path)
        self.btn_close.setIcon(QIcon(icon))
        self.btn_close.clicked.connect(self.btn_close_clicked)
        self.btn_close.setFixedSize(btn_size,btn_size)
        self.btn_close.setStyleSheet("QPushButton {border: 0px;} QPushButton::hover {background-color: #FF7777;}")
        self.btn_close.setCursor(Qt.PointingHandCursor)

        # Boton de minimizar
        self.btn_min = QPushButton()
        path = os.path.join(os.path.dirname(__file__), "../media/images/MinimizeBtn.png")
        icon = QIcon(path)
        self.btn_min.setIcon(QIcon(icon))
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_min.setFixedSize(btn_size, btn_size)
        self.btn_min.setStyleSheet("QPushButton {border: 0px;} QPushButton::hover {background-color: #1C3D95;}")
        self.btn_min.setCursor(Qt.PointingHandCursor)

        # Boton de maximizar
        self.btn_max = QPushButton()
        path_max = os.path.join(os.path.dirname(__file__), "../media/images/MaximizeBtn.png")
        self.icon_max = QIcon(path_max)
        self.btn_max.setIcon(QIcon(self.icon_max))
        self.btn_max.clicked.connect(self.btn_max_clicked)
        self.btn_max.setFixedSize(btn_size, btn_size)
        self.btn_max.setStyleSheet("QPushButton {border: 0px;} QPushButton::hover {background-color: #1C3D95;}")
        self.btn_max.setCursor(Qt.PointingHandCursor)

        # Icono de restaurar
        path_rest = os.path.join(os.path.dirname(__file__), "../media/images/RestoreDownBtn.png")
        self.icon_rest = QIcon(path_rest)

        # ----------------------------------------------------------------------
        # BARRA DE TITULO (BOTON Y BARRA DE BUSQUEDA)
        bar_widget = QWidget()
        bar_widget.setMaximumHeight(50)
        bar_widget.setMinimumHeight(50)

        bar_layout = QHBoxLayout()
        bar_layout.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        bar_widget.setContentsMargins(0, 0, 0, 0)
        bar_layout.setContentsMargins(0, 0, 0, 0)

        # Botón a la izquierda
        button = QPushButton("Biblioteca Softpro")
        button.setStyleSheet(
            "QPushButton {"
            "background-color: transparent; "
            "color: white; "
            "border-radius: 0px; "
            "font-size: 28px; "
            "font-weight: bold; "
            "text-align: left; "  # Alinea el texto a la izquierda
            "padding-left: 10px;"
            "border-radius: 20px;"
            "}"
        )
        button.setCursor(Qt.PointingHandCursor)

        # Barra de búsqueda en el centro
        search_container = QWidget()
        search_container.setFixedWidth(400)
        search_container.setFixedHeight(30)
        search_container.setStyleSheet("background-color: #FFFFFF; border-radius: 10px;")

        search_layout = QHBoxLayout()
        search_layout.setSpacing(0)

        search_bar = QLineEdit()
        search_bar.setContentsMargins(0, 0, 0, 0)
        search_bar.setStyleSheet("QLineEdit {font-size: 16px;}")
        search_bar.setPlaceholderText("Buscar")

        search_button = QPushButton()
        icon_path = os.path.join(os.path.dirname(__file__), "../media/img/lupa.png")
        search_button.setStyleSheet("QPushButton {border-radius: 10px;}")
        search_button.setIcon(QIcon(icon_path))
        search_button.setFixedSize(30, 30)

        # Configura la alineación del botón y search_container en bar_layout
        bar_layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        bar_layout.addWidget(search_container, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        bar_layout.setContentsMargins(0, 2, 0, 0)

        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.addWidget(search_button)
        search_layout.addWidget(search_bar)

        search_container.setLayout(search_layout)
        bar_widget.setLayout(bar_layout)
        bar_layout.setStretch(1, 2)

        # ----------------------------------------------------------------------
        # BARRA DE MENÚS DESPLEGABLES
        menu_layout = QHBoxLayout()
        menu_layout.setSpacing(0)
        menu_bar = QMenuBar()
        menu_bar.setContentsMargins(0, 0, 0, 0)
        menu_bar.setMaximumHeight(25)
        menu_bar.setMinimumHeight(25)
        menu_bar.setCursor(Qt.PointingHandCursor)

        # Hoja de estilo a la barra de menú
        menu_bar.setStyleSheet(
            "QMenuBar { "
            "background-color: #1C3D95;"
            "color: white;"
            "font-size: 14px;"
            "padding-left: 10px;"
            "}"
            "QMenuBar::item:selected { "
            "background-color: #2F53D1; "
            "}"
            )

        # Menú 1
        menu1 = QMenu("Categorias", self)
        menu1.setStyleSheet(
            "QMenu { "
            "background-color: #2F53D1;"
            "color: white;"
            "font-size: 14px;"
            "}"
            "QMenu::item:selected { "
            "background-color: #1C3D95; "
            "}"
            )
        menu1.setCursor(Qt.PointingHandCursor)
        # Opción 1.1 -----------------------------------------------------------
        icon_path = os.path.join(os.path.dirname(__file__), "../media/img/lupa.png")
        icon1_1 = QIcon(icon_path)  # Reemplaza con la ruta al ícono
        option_1_1 = QAction(icon1_1, "Opción 1.1", self)
        option_1_1.triggered.connect(self.option_1_1)
        menu1.addAction(option_1_1)

        # Opción 1.2 -----------------------------------------------------------
        icon_path = os.path.join(os.path.dirname(__file__), "../media/img/lupa.png")
        icon1_2 = QIcon(icon_path)  # Reemplaza con la ruta al ícono
        option_1_2 = QAction(icon1_1, "Opción 1.2", self)
        option_1_2.triggered.connect(self.option_1_2)
        menu1.addAction(option_1_2)

        # Menú 2
        menu2 = QMenu("Ayuda", self)
        menu2.setCursor(Qt.PointingHandCursor)
        menu2.setStyleSheet(
            "QMenu { "
            "background-color: #2F53D1;"
            "color: white;"
            "font-size: 14px;"
            "}"
            "QMenu::item:selected { "
            "background-color: #1C3D95; "
            "}"
        )
        # Opción 2.1
        menu2.addAction("Opción 2.1").triggered.connect(self.option_2_1)
        # Opción 2.2
        menu2.addAction("Opción 2.2").triggered.connect(self.option_2_2)


        #Menu 3 - MENU PERFIL
        menuPerfil = QMenu("Perfil", self)
        menuPerfil.setCursor(Qt.PointingHandCursor)
        menuPerfil.setStyleSheet(
            "QMenu { "
            "background-color: #2F53D1;"
            "color: white;"
            "font-size: 14px;"
            "}"
            "QMenu::item:selected { "
            "background-color: #1C3D95; "
            "}"
        )

        menu_bar.addMenu(menu1)
        menu_bar.addMenu(menu2)

        menu_bar_perfil = QMenuBar()
        menu_bar_perfil.setContentsMargins(0, 0, 0, 0)
        menu_bar_perfil.setMaximumHeight(25)
        menu_bar_perfil.setMinimumHeight(25)
        menu_bar_perfil.setCursor(Qt.PointingHandCursor)
        # Hoja de estilo a la barra de menú
        menu_bar_perfil.setStyleSheet(
            "QMenuBar { "
            "background-color: #1C3D95;"
            "color: white;"
            "font-size: 15px;"
            "padding-left: 10px;"
            "font-weight: bold;"
            "}"
            "QMenuBar::item:selected { "
            "background-color: #2F53D1; "
            "}"
            )

        menuPerfilUsuario = QMenu(f" {self.user_data['nombre']} ", self)
        menuPerfilUsuario.setStyleSheet(
            "QMenu { "
            "background-color: #2F53D1;"
            "color: red;"
            "font-size: 14px;"
            "}"
            "QMenu::item:selected { "
            "background-color: #1C3D95; "
            "}"
            )
        

        menu_bar_perfil.addMenu(menuPerfilUsuario)

        menu_layout.addWidget(menu_bar)
        menu_layout.addWidget(menu_bar_perfil)
        menu_layout.setStretch(0, 1)


        # ----------------------------------------------------------------------
        # Agrega los widgets a la barra de título
        self.layout.addWidget(bar_widget)
        self.layout.addWidget(self.btn_min)
        self.layout.addWidget(self.btn_max)
        self.layout.addWidget(self.btn_close)

        # Agrega el layout a la ventana y la barra de menús desplegables
        self.principal_layuot.addLayout(self.layout)
        self.principal_layuot.addLayout(menu_layout)

        # Establece el layout principal
        self.setLayout(self.principal_layuot)

        # ----------------------------------------------------------------------
        # Inicializa los valores para el drag and drop
        self.start = QPoint(0, 0)
        self.pressing = False

    # ----------------------------------------------------------------------
    # FUNCIONES DE LA BARRA DE TITULO (DRAG AND DROP)
    def resizeEvent(self, QResizeEvent):
        super(MyBar, self).resizeEvent(QResizeEvent)

    def mousePressEvent(self, event):
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing:
            self.end = self.mapToGlobal(event.pos())
            self.movement = self.end-self.start
            self.parent.setGeometry(self.mapToGlobal(self.movement).x(),
                                self.mapToGlobal(self.movement).y(),
                                self.parent.width(),
                                self.parent.height())
            self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        self.pressing = False

    def btn_close_clicked(self):
        self.parent.close()

    def btn_max_clicked(self):
            # Si la ventana ya está maximizada
        if self.parent.isMaximized():
            # Restaurar la ventana a su tamaño normal
            self.btn_max.setIcon(QIcon(self.icon_max))
            self.parent.showNormal()
        else:
            # Maximizar la ventana
            self.parent.showMaximized()
            self.btn_max.setIcon(QIcon(self.icon_rest))

    def btn_min_clicked(self):
        self.parent.showMinimized()

    # ----------------------------------------------------------------------
    # FUNCIONES DE LA BARRA DE MENÚS DESPLEGABLES
    def option_1_1(self):
        print("Opción 1.1 seleccionada")

    def option_1_2(self):
        print("Opción 1.2 seleccionada")

    def option_2_1(self):
        print("Opción 2.1 seleccionada")

    def option_2_2(self):
        print("Opción 2.2 seleccionada")

class ImageLoader(QThread):
    image_loaded = Signal(bytes)  # Señal para comunicar la imagen cargada

    def __init__(self, image_url):
        super().__init__()
        self.image_url = image_url

    def run(self):
        response = requests.get(self.image_url)
        if response.status_code == 200:
            self.image_loaded.emit(response.content)

class BookWidget(QWidget):
    def __init__(self, book_data):
        super().__init__()

        self.image_label = QLabel()
        image_url = book_data.get("imagen_url", "")
        self.image_loader = ImageLoader(image_url)

        # Conecta la señal para cargar la imagen al método que maneja la imagen cargada
        self.image_loader.image_loaded.connect(self.set_image)

        self.image_loader.start()

        # Crea un layout vertical para el widget del libro
        layout = QVBoxLayout()

        # Agrega la etiqueta de imagen al layout
        layout.addWidget(self.image_label)

        # Establece el layout para el widget
        self.setLayout(layout)
        self.book_data = book_data

    def set_image(self, image_data):
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        scaled_pixmap = pixmap.scaled(200, 300, Qt.KeepAspectRatio)
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setCursor(Qt.PointingHandCursor)
        self.image_label.mousePressEvent = self.show_book_info  # Conecta el evento de clic


    def show_book_info(self, event):
        # Muestra una ventana emergente con la información del libro
        info = self.book_data
        info_text = f"Título: {info['titulo']}\nAutor: {info['autor']}\nAño: {info['año_publicacion']}\nGénero: {info['genero']}\nEditorial: {info['editorial']}"
        msg_box = QMessageBox()
        msg_box.information(self, "Información del libro", info_text)

class Ui_principal(QMainWindow):
    color_bar = "#2F53D1"
    def __init__(self, user_data=None):
        super().__init__()
        #print(user_data)
        self.user_data = user_data
        mensaje = QMessageBox()
        boton_aceptar = QPushButton("Aceptar")
        boton_aceptar.setCursor(Qt.PointingHandCursor)
        mensaje.setText("Debes iniciar sesión para acceder a la biblioteca")
        mensaje.setWindowTitle("Biblioteca SoftPro - Error")
        mensaje.addButton(boton_aceptar, QMessageBox.AcceptRole)
        mensaje.setIcon(QMessageBox.Critical)
        mensaje.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "../media/img/libro.png")))

        mensaje.setStyleSheet(
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

        if user_data:
            self.interfaz()
        else:
            mensaje.exec()
            sys.exit(1)

        self.setWindowTitle("Bienvenido a Biblioteca Softpro")
        self.setGeometry(50, 50, 1280, 720)
        self.setMinimumSize(1280, 720)
        path_icon = os.path.join(os.path.dirname(__file__), "../media/img/libro.png")
        icon = QIcon(path_icon)
        self.setWindowIcon(icon)
        self.setWindowFlags(Qt.FramelessWindowHint)


        # Barra horizontal con botón y barra de búsqueda


    def fill_grid_layout(self, widget):
        #QScrollArea que contendrá el grid_layout
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Ajusta el contenido al tamaño del área
        widget.addWidget(scroll_area)

        #QWidget para alojar el grid_layout
        scroll_content = QWidget()
        scroll_content.setContentsMargins(80, 0, 80, 0)
        scroll_area.setWidget(scroll_content)
        scroll_area.setStyleSheet("QScrollArea{border: 20px;} QMessageBox{ border: 0px;}")
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Desactiva la barra de desplazamiento horizontal
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        #QGridLayout
        grid_layout = QGridLayout()
        scroll_content.setLayout(grid_layout)

        # Establece el espaciado entre elementos a 0
        grid_layout.setSpacing(0)

        num_columns = 4  # Define el número de columnas en el QGridLayout
        row = 0  # Inicializa la fila en 0
        max_books_to_show = 12  # Define el número máximo de libros a mostrar
        path_to_json = os.path.join(os.path.dirname(__file__), "../databases/librosConImagenes.json")

        # Lee los datos de libros desde el archivo libros.json
        with open(path_to_json, "r", encoding="utf-8") as json_file:
            books_data = json.load(json_file)

        for i, book in enumerate(books_data[:max_books_to_show]):
            # Crea un widget para el libro y pasa los datos del libro como argumento
            book_widget = BookWidget(book)

            # Calcula la fila y la columna actual en función del índice
            row = i // num_columns
            col = i % num_columns

            # Agrega el widget del libro al QGridLayout en la fila y columna calculadas
            grid_layout.addWidget(book_widget, row, col)

        # Agrega el QGridLayout al QWidget
        scroll_content.adjustSize()

    def interfaz(self):
        central_widget = QWidget()
        central_vbox = QVBoxLayout()
        central_widget.setContentsMargins(0, 0, 0, 0)
        central_vbox.setContentsMargins(0, 0, 0, 0)
        central_vbox.setSpacing(0)

        central_widget.setLayout(central_vbox)
        central_vbox.setAlignment(Qt.AlignTop)

        navbars_widget = QWidget()
        navbars_layout = QVBoxLayout()
        navbars_widget.setStyleSheet(f"background-color:{self.color_bar};")

        navbars_layout.setAlignment(Qt.AlignTop)
        navbars_widget.setContentsMargins(0, 0, 0, 0)
        navbars_layout.setContentsMargins(0, 0, 0, 0)
        # ------- Barra horizontal con botón y barra de búsqueda -------
        # Agrega la barra horizontal con botón y barra de búsqueda en la parte superior
        navbar = MyBar(self, self.user_data)
        navbars_layout.addWidget(navbar)
        # Agrega la barra de menús desplegables en la parte inferior
        #self.create_menu_bar(navbars_layout)
        # ----------------------------------------------------------------
        navbars_widget.setLayout(navbars_layout)
        navbars_widget.setMaximumHeight(75)
        navbars_widget.setMinimumHeight(75)

        central_vbox.addWidget(navbars_widget)
        self.fill_grid_layout(central_vbox)
        self.setCentralWidget(central_widget)
        print(self.user_data)


def main():
    app = QApplication(sys.argv)
    window = Ui_principal()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
