import sys
import json
import os
import requests
import shutil
from datetime import datetime

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
    QDialog,
    QGraphicsDropShadowEffect,
    QSizeGrip,
    QStackedWidget,
    QFileDialog,
)
from PySide6.QtGui import *
from PySide6.QtCore import *

basedir = os.path.abspath(os.path.dirname(__file__))
sys.path.append('../')

try:
    from ui_principal.ui_dashboard import SideMenu
    from ui_principal.ui_registerbook import Ui_RegisterBook
    from ui_principal.ui_prestamos import Ui_Prestamos_admin, Ui_Prestamos_user
    from ui_principal.libros import ListaLibros
    from ui_principal.prestamos import ListaPrestamos
    ListaLibros.try_cargar_libros_desde_json()
    ListaLibros.imprimir_libros()
    ListaPrestamos.try_cargar_prestamos_desde_json()
    ListaPrestamos.imprimir_prestamos()
    print("Exito al importar el SideMenu")
except ImportError:
    print("Error al importar el archivo ui_dashboard.py")

class MyBar(QWidget):
    search_triggered = Signal(str)  # Señal para la búsqueda

    def __init__(self, parent, user_data):
        super(MyBar, self).__init__()
        self.parent = parent
        self.user_data = user_data
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
        self.button = QPushButton("Biblioteca Softpro")
        self.button.setStyleSheet(
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
        self.button.setCursor(Qt.PointingHandCursor)

        # Barra de búsqueda en el centro
        search_container = QWidget()
        search_container.setFixedWidth(550)
        search_container.setFixedHeight(30)
        search_container.setStyleSheet("background-color: #FFFFFF; border-radius: 10px;")

        search_layout = QHBoxLayout()
        search_layout.setSpacing(0)

        self.search_bar = QLineEdit()
        self.search_bar.setContentsMargins(0, 0, 0, 0)
        self.search_bar.setStyleSheet("QLineEdit {font-size: 16px;}")
        self.search_bar.setPlaceholderText("Buscar por título, autor, ISBN, editorial, año, idioma, género...")
        self.search_bar.textChanged.connect(self.on_search_text_changed)

        search_button = QPushButton()
        icon_path = os.path.join(os.path.dirname(__file__), "../media/img/lupa.png")
        search_button.setStyleSheet("QPushButton {border-radius: 10px;}")
        search_button.setIcon(QIcon(icon_path))
        search_button.setFixedSize(30, 30)

        # Configura la alineación del botón y search_container en bar_layout
        bar_layout.addWidget(self.button, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        bar_layout.addWidget(search_container, alignment=Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        bar_layout.setContentsMargins(0, 2, 0, 0)

        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.addWidget(search_button)
        search_layout.addWidget(self.search_bar)

        search_container.setLayout(search_layout)
        bar_widget.setLayout(bar_layout)
        bar_layout.setStretch(1, 2)


        # ----------------------------------------------------------------------
        # Agrega los widgets a la barra de título
        self.layout.addWidget(bar_widget)
        self.layout.addWidget(self.btn_min)
        self.layout.addWidget(self.btn_max)
        self.layout.addWidget(self.btn_close)

        # Agrega el layout a la ventana y la barra de menús desplegables
        self.principal_layuot.addLayout(self.layout)

        # Establece el layout principal
        self.setLayout(self.principal_layuot)

        # ----------------------------------------------------------------------
        # Inicializa los valores para el drag and drop
        self.start = QPoint(0, 0)
        self.pressing = False

    def on_search_text_changed(self, search_text):
        print(f"Búsqueda: {search_text}")
        # Emite la señal de búsqueda cuando el texto cambia
        self.search_triggered.emit(search_text)

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

    def close_session(self):
        self.parent.close()
        from ui_login.ui_login_copy import MiVentana
        window = MiVentana()
        window.show()

class MessageWidget(QMessageBox):
    def __init__(self):
        super(MessageWidget, self).__init__()
        self.setWindowTitle("Biblioteca SoftPro - Imagen de perfil")
        self.button_message = QPushButton("Aceptar")
        self.button_message.setCursor(Qt.PointingHandCursor)
        self.addButton(self.button_message, QMessageBox.AcceptRole)
        self.setIcon(QMessageBox.Critical)
        self.setWindowIcon(
            QIcon(os.path.join(basedir, "../media/img/libro.png")))
        self.setStyleSheet(
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

class BookWidget(QWidget):
    def __init__(self, book_data, user_data):
        super().__init__()
        self.user_data = user_data

        image_label = QLabel()
        image_label.setFixedSize(200, 300)
        image_label.setStyleSheet(
            "QLabel {"
            "   background-color: white;"
            "   border-radius: 10px;"
            "   padding: 10px;"
            "}"
        )

        layout = QVBoxLayout()
        layout.addWidget(image_label)
        self.setLayout(layout)

        self.add_shadow(image_label)

        path_to_img = os.path.join(basedir, f"../media/librosCovers/{book_data['ISBN']}/coverBook.png")
        self.set_image(image_label, path_to_img)
        image_label.mousePressEvent = lambda event: self.show_book_info(book_data)

    def set_image(self, image_label, image_path):
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(200, 300, Qt.KeepAspectRatio)
            image_label.setPixmap(scaled_pixmap)
            image_label.setAlignment(Qt.AlignCenter)
            image_label.setCursor(Qt.PointingHandCursor)
        else:
            print(f"Error al cargar la imagen desde: {image_path}")

    def add_shadow(self, widget):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(5)
        shadow.setColor(Qt.black)
        shadow.setOffset(0, 0)
        widget.setGraphicsEffect(shadow)

    def show_book_info(self, book_data):
        book_widget = BookInfoWidget(book_data, self.user_data)
        book_widget.exec()

class BookGridVistaInicio(QWidget):
    def __init__(self, user_data):
        super().__init__()
        self.user_data = user_data

        self.max_books_to_show = 8

        central_layout = QVBoxLayout()
        central_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        central_layout.setContentsMargins(0, 0, 0, 0)
        central_layout.setSpacing(0)

        title = QLabel("LIBROS MÁS POPULARES")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 40px; font-weight: bold; color: black; padding: 5px; text-align: center;")

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        scroll_content = QWidget(self)
        scroll_content.setContentsMargins(0, 0, 0, 0)
        scroll_area.setWidget(scroll_content)
        scroll_area.setStyleSheet("QScrollArea{border: 20px;} QMessageBox{ border: 0px;}")
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        grid_layout = QGridLayout()
        self.grid_layout = grid_layout
        scroll_content.setLayout(grid_layout)
        grid_layout.setSpacing(0)

        num_columns = 4
        max_books_to_show = self.max_books_to_show

        # Mueve la lógica de lectura de datos del libro aquí
        data_books = self.load_book_data()

        grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        grid_layout.addWidget(title, 0, 0, 1, num_columns)

        row = 1
        for i, book in enumerate(data_books[:max_books_to_show]):
            book_widget = BookWidget(book, self.user_data)
            col = i % num_columns
            grid_layout.addWidget(book_widget, row, col)
            if col == num_columns - 1:
                row += 1

        scroll_content.adjustSize()
        self.scroll_content = scroll_content
        central_layout.addWidget(scroll_area)
        self.setLayout(central_layout)

    def update_books_on_search(self, search_text):
        # Actualiza la vista de libros según el texto de búsqueda
        # Puedes implementar la lógica de filtrado aquí
        print(f"Búsqueda: {search_text}")

        data_books = self.load_book_data()

        # Filtra libros según el texto de búsqueda
        search_text = search_text.lower()
        filtered_books = [book for book in data_books if
                          search_text in book['Titulo'].lower()
                          or search_text in book['Autor'].lower()
                          or search_text in book['ISBN'].lower()
                          or search_text in book['Año de publicacion'].lower()
                          or search_text in book['Idioma'].lower()
                          or search_text in book['Editorial'].lower()
                          or search_text in book['Categoria'].lower()]

        # Muestra los libros filtrados
        self.show_filtered_books(filtered_books)

    def show_filtered_books(self, filtered_books):
        # Oculta los widgets existentes en la cuadrícula
        for i in range(self.grid_layout.count()):
            widget = self.grid_layout.itemAt(i).widget()
            widget.hide()

        # Vuelve a crear la cuadrícula con los libros filtrados
        num_columns = 4
        row = 1

        title = QLabel("Se han encontrado los siguientes libros:")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 40px; font-weight: bold; color: black; padding: 5px; text-align: center;")

        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.grid_layout.addWidget(title, 0, 0, 1, num_columns)

        for i, book in enumerate(filtered_books):
            book_widget = BookWidget(book, self.user_data)
            col = i % num_columns
            self.grid_layout.addWidget(book_widget, row, col)
            if col == num_columns - 1:
                row += 1

            # Muestra el widget (o asegúrate de que esté visible)
            book_widget.show()

        # Ajusta el tamaño del contenido y la vista de desplazamiento
        self.scroll_content.adjustSize()

    def load_book_data(self):
        path_to_json = os.path.join(os.path.dirname(__file__), "../databases/libros_db.json")
        try:
            with open(path_to_json, "r", encoding="utf-8") as json_file:
                data = json.load(json_file)
                return data.get('Libros', [])
        except FileNotFoundError:
            print(f"Error: El archivo JSON no fue encontrado en la ruta: {path_to_json}")
            return []

    def closeEvent(self, event):
        # Detener el temporizador antes de cerrar la ventana
        self.timer.stop()
        event.accept()

    def update_books(self):
        data_books = self.load_book_data()
        print("Actualizando libros...")
        # Nuevo widget para reemplazar el widget anterior
        try:
            row = 1
            num_columns = 4
            max_books_to_show = self.max_books_to_show

            # Vuelve a crear la cuadrícula con los libros filtrados
            num_columns = 4
            row = 1

            title = QLabel("LIBROS MAS POPULARES:")
            title.setAlignment(Qt.AlignCenter)
            title.setStyleSheet("font-size: 40px; font-weight: bold; color: black; padding: 5px; text-align: center;")

            self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
            self.grid_layout.addWidget(title, 0, 0, 1, num_columns)

            for i, book in enumerate(data_books[:max_books_to_show]):
                book_widget = BookWidget(book, self.user_data)
                col = i % num_columns
                self.grid_layout.addWidget(book_widget, row, col)
                if col == num_columns - 1:
                    row += 1

                # Muestra el widget (o asegúrate de que esté visible)
                book_widget.show()

            # Ajusta el tamaño del contenido y la vista de desplazamiento
            self.scroll_content.adjustSize()
        except Exception as e:
            print("Error al actualizar libros: ", e)

class BookInfoWidget(QDialog):
    def __init__(self, book_data, user_data):
        super().__init__()
        self.book_data = book_data
        self.user_data = user_data
        self.messageBox = MessageWidget()
        self.setup_ui()
        self.load_book_info(book_data)

    def setup_ui(self):
        width, height = 600, 300
        self.setFixedSize(width, height)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet(
            "QDialog {"
            "background-color: white;"
            "border: 5px solid #2F53D1;"
            "}"
            "QLabel {"
            "font-size: 16px;"
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

        layout = QHBoxLayout(self)

        self.image_label = QLabel()
        self.image_label.setGraphicsEffect(QGraphicsDropShadowEffect(blurRadius=20, xOffset=0, yOffset=0))
        self.image_label.setMaximumSize(width/2, height)

        layout_info = QVBoxLayout()

        layout.addWidget(self.image_label)
        layout.addLayout(layout_info)

        self.info_label = QLabel(self)
        self.info_label.setWordWrap(True)
        self.info_label.setMaximumWidth(width/2)
        layout_info.addWidget(self.info_label)
        layout_info.setAlignment(Qt.AlignTop)


        hacer_pres = QPushButton("Pedir Libro")
        hacer_pres.setCursor(Qt.PointingHandCursor)
        hacer_pres.setMaximumHeight(30)
        hacer_pres.setLayoutDirection(Qt.RightToLeft)
        # TODO: Agregar la funcionalidad para pedir el libro
        hacer_pres.clicked.connect(self.hacer_prestamo)
        hacer_pres.setStyleSheet(
            """
            background-color: #067A14;
            """)
        layout_info.addWidget(hacer_pres)

        close_button = QPushButton("Cerrar", self)
        close_button.setCursor(Qt.PointingHandCursor)
        close_button.setMaximumHeight(30)
        close_button.setLayoutDirection(Qt.RightToLeft)
        close_button.clicked.connect(self.close)
        layout_info.addWidget(close_button)

        self.setLayout(layout)

    def hacer_prestamo(self):
        # Verificar ejemplares disponibles antes de hacer el préstamo
        ejemplares_disponibles = int(self.book_data['Ejemplares'])
        if ejemplares_disponibles > 0:
            # Restar un ejemplar al libro
            self.book_data['Ejemplares'] = str(ejemplares_disponibles - 1)

            # Lógica para realizar el préstamo y actualizar archivos JSON
            prestamo_info = {
                "ISBN": self.book_data["ISBN"],
                "Titulo": self.book_data["Titulo"],
                "Autor": self.book_data["Autor"],
                "Fecha": datetime.today().strftime('%Y-%m-%d')
            }

            # Actualiza el archivo de préstamos
            self.actualizar_prestamos(prestamo_info)

            # Actualiza el archivo libros_db.json restando un ejemplar
            self.actualizar_libros_db()
            ListaPrestamos.actualizar_prestamos(self)
            ListaPrestamos.imprimir_prestamos()
            ListaLibros.actualizar_libros(self)
            ListaLibros.imprimir_libros()

            # Cierra el diálogo después de realizar el préstamo
            self.close()
        else:
            self.messageBox.setText("No hay ejemplares disponibles de este libro.")
            self.messageBox.exec()

    def actualizar_prestamos(self, prestamo_info):
        # Carga los datos actuales de prestamos.json
        path_to_prestamos = os.path.join(basedir, "../databases/prestamos.json")
        try:
            with open(path_to_prestamos, "r", encoding="utf-8") as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            data = {"prestamos": []}

        # Busca si existe un registro de préstamo con el UUID actual
        uuid = self.user_data["uuid"]
        prestamo_existente = next((p for p in data["prestamos"] if p["uuid"] == uuid), None)

        # Si existe, agrega el nuevo préstamo
        if prestamo_existente:
            prestamo_existente["prestamos"].append(prestamo_info)
        else:
            # Si no existe, crea un nuevo registro de préstamo
            nuevo_prestamo = {"uuid": uuid, "prestamos": [prestamo_info]}
            data["prestamos"].append(nuevo_prestamo)

        # Guarda los datos actualizados en prestamos.json
        with open(path_to_prestamos, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=2, ensure_ascii=False)

    def actualizar_libros_db(self):
        # Resta un ejemplar al libro actual en libros_db.json
        path_to_libros_db = os.path.join(basedir, "../databases/libros_db.json")
        try:
            with open(path_to_libros_db, "r", encoding="utf-8") as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            print(f"Error: El archivo JSON no fue encontrado en la ruta: {path_to_libros_db}")
            return

        # Busca el libro actual en libros_db.json
        libro_actual = next((libro for libro in data["Libros"] if libro["ISBN"] == self.book_data["ISBN"]), None)
        # Si encuentra el libro, resta un ejemplar
        if libro_actual and "Ejemplares" in libro_actual:
            libro_actual["Ejemplares"] = str(int(libro_actual["Ejemplares"]) - 1)

            # Guarda los datos actualizados en libros_db.json
            with open(path_to_libros_db, "w", encoding="utf-8") as json_file:
                json.dump(data, json_file, indent=2, ensure_ascii=False)

            self.messageBox.setText(f"Se ha realizado un préstamo del libro: {self.book_data['Titulo']}")
            self.messageBox.setIcon(QMessageBox.Information)
            self.messageBox.exec()
            # print(f"Se ha realizado un préstamo del libro: {self.book_data['Titulo']}")
        else:
            print(f"No se pudo encontrar el libro en libros_db.json")

    def load_book_info(self, info):
        path_to_img = os.path.join(basedir, f"../media/librosCovers/{info['ISBN']}/coverBook.png")
        self.set_image(path_to_img)

        info_text = (
            f"Título: {info['Titulo']}\n"
            f"Autor: {info['Autor']}\n"
            f"Editorial: {info['Editorial']}\n"
            f"ISBN: {info['ISBN']}\n"
            f"Año de publicación: {info['Año de publicacion']}\n"
            f"Idioma: {info['Idioma']}\n"
            f"Ejemplares: {info['Ejemplares']}\n"
            f"Género: {info['Categoria']}\n"
            f"Sinopsis: {info['Sinopsis']}\n"
        )
        self.info_label.setText(info_text)

    def set_image(self, image_path):
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(200, 300, Qt.KeepAspectRatio)
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setAlignment(Qt.AlignCenter)
            self.image_label.setCursor(Qt.PointingHandCursor)
            shadow = self.add_shadow()
            self.image_label.setGraphicsEffect(shadow)
        else:
            print(f"Error al cargar la imagen desde: {image_path}")

    def add_shadow(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(Qt.black)
        shadow.setOffset(0, 0)
        return shadow

    def show_widget(self):
        self.show()

class ProfileImageWidget(QWidget):
    def __init__(self, user_data):
        super(ProfileImageWidget, self).__init__()
        self.user_data = user_data
        self.profile_image_path = None

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(5)  # Ajusta según tus preferencias
        shadow.setColor(Qt.black)
        shadow.setOffset(0, 0)

        shadow2 = QGraphicsDropShadowEffect(self)
        shadow2.setBlurRadius(5)  # Ajusta según tus preferencias
        shadow2.setColor(Qt.black)
        shadow2.setOffset(0, 0)

        self.message = QMessageBox()
        self.message.setWindowTitle("Biblioteca SoftPro - Imagen de perfil")
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

        # Interfaz de usuario
        self.layout = QVBoxLayout()

        self.image_label = QLabel("No hay imagen de perfil")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet(
            "QLabel {"
            "border: 2px solid #DDDDDD;"
            "}"
        )
        self.layout.addWidget(self.image_label)

        self.select_image_button = QPushButton("Seleccionar Imagen")
        self.select_image_button.clicked.connect(self.select_image)
        self.select_image_button.setMaximumHeight(30)
        self.select_image_button.setGraphicsEffect(shadow)
        self.select_image_button.setCursor(Qt.PointingHandCursor)
        self.select_image_button.setStyleSheet(
            "QPushButton {"
            "background-color: #2F53D1; "
            "color: white; "
            "border-radius: 10px; "
            "padding: 5px; "
            "padding-left: 10px; "
            "padding-right: 10px; "
            "font-size: 16px; "
            "font-weight: bold; "
            "}"
            "QPushButton::hover {"
            "background-color: #1C3D95; "
            "}"
            "QPushButton:pressed {"
            "background-color: #2F5777"
            "}"
        )
        self.layout.addWidget(self.select_image_button)

        self.save_image_button = QPushButton("Guardar Imagen")
        self.save_image_button.clicked.connect(self.save_profile_image)
        self.save_image_button.setMaximumHeight(30)
        self.save_image_button.setGraphicsEffect(shadow2)
        self.save_image_button.setCursor(Qt.PointingHandCursor)
        self.save_image_button.setStyleSheet(
            "QPushButton {"
            "background-color: #067A14;"
            "color: white; "
            "border-radius: 10px; "
            "padding: 5px; "
            "padding-left: 10px; "
            "padding-right: 10px; "
            "font-size: 16px; "
            "font-weight: bold; "
            "}"
            "QPushButton::hover {"
            "background-color: #1DAE13; "
            "}"
            "QPushButton:pressed {"
            "background-color: #6BD864"
            "}"
        )
        self.layout.addWidget(self.save_image_button)

        self.load_saved_image()
        self.setLayout(self.layout)

    def select_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("Images (*.png *.jpg *.bmp)")
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.profile_image_path = selected_files[0]
                self.load_and_display_image()

    def save_profile_image(self):
        if self.profile_image_path:
            user_uuid = self.user_data["uuid"]
            base_path = os.path.join(os.path.dirname(__file__), "../media/usuarios")
            user_media_path = os.path.join(base_path, user_uuid)

            if not os.path.exists(user_media_path):
                os.makedirs(user_media_path)

            destination_path = os.path.join(user_media_path, "perfil.png")

            try:
                # Copia la imagen seleccionada al destino
                shutil.copy2(self.profile_image_path, destination_path)

                self.message.setText("Imagen de perfil guardada correctamente.")
                self.message.setIcon(QMessageBox.Information)
                self.message.exec()

                print(f"Imagen de perfil guardada en: {destination_path}")
                self.load_and_display_image()
            except Exception as e:
                print(f"Error al guardar la imagen de perfil: {str(e)}")
        else:
            print("Por favor, seleccione una imagen de perfil antes de guardar.")

    def load_saved_image(self):
        user_uuid = self.user_data["uuid"]
        path = os.path.join(os.path.dirname(__file__), "../media/usuarios", user_uuid, "perfil.png")
        if os.path.exists(path):
            self.profile_image_path = path
            self.load_and_display_image()

    def load_and_display_image(self):
        if os.path.exists(self.profile_image_path):
            pixmap = QPixmap(self.profile_image_path)
            scaled_pixmap = pixmap.scaled(self.image_label.size(),Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setAlignment(Qt.AlignCenter)
            self.image_label.setScaledContents(True)  # Hace que la imagen se adapte al tamaño de la QLabel
        else:
            print("La ruta de la imagen no es válida o la imagen no existe.")

# Se puede usar como plantilla para confirmaciones
class ConfirmDeleteDialog(QDialog):
    def __init__(self, parent=None):
        super(ConfirmDeleteDialog, self).__init__(parent)
        self.setFixedWidth(400)
        self.setWindowTitle("Confirmar Eliminación de Cuenta")
        self.setStyleSheet(
            "QPushButton {"
            "background-color: #2F53D1; "
            "color: white; "
            "border-radius: 10px; "
            "padding: 5px; "
            "padding-left: 10px; "
            "padding-right: 10px; "
            "font-size: 16px; "
            "font-weight: bold; "
            "}"
            "QPushButton::hover {"
            "background-color: #1C3D95; "
            "}"
            "QPushButton:pressed {"
            "background-color: #2F5777"
            "}"
            "QLabel {"
            "font-size: 20px;"
            "margin-bottom: 20px;"
            "}"
        )

        layout = QVBoxLayout()

        label = QLabel("¿Está seguro de que desea eliminar su cuenta? Esta accion es irreversible.")
        label.setWordWrap(True)
        layout.addWidget(label)

        confirm_button = QPushButton("Eliminar Cuenta")
        confirm_button.clicked.connect(self.accept)
        confirm_button.setCursor(Qt.PointingHandCursor)
        confirm_button.setStyleSheet(
            "QPushButton {"
            "background-color: #FF0000; "
            "color: white; "
            "text-align: center;"
            "}"
            "QPushButton::hover {"
            "background-color: #CC0000; "
            "}"
            "QPushButton:pressed {"
            "background-color: #800000"
            "}"
        )

        cancel_button = QPushButton("Cancelar")
        cancel_button.setCursor(Qt.PointingHandCursor)
        cancel_button.clicked.connect(self.reject)

        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(confirm_button)
        layout_buttons.addWidget(cancel_button)

        layout.addLayout(layout_buttons)

        self.setLayout(layout)

class VistaUserProfile(QWidget):
    def __init__(self, parent, user_data):
        super(VistaUserProfile, self).__init__()
        self.user_data = user_data
        self.parent = parent
        self.setContentsMargins(100, 0, 100, 0)
        # Agrega widgets y elementos de interfaz gráfica según sea necesario
        self.setStyleSheet(
            "QPushButton {"
            "background-color: #2F53D1; "
            "color: white; "
            "border-radius: 10px; "
            "padding: 5px; "
            "padding-left: 10px; "
            "padding-right: 10px; "
            "font-size: 16px; "
            "font-weight: bold; "
            "}"
            "QPushButton::hover {"
            "background-color: #1C3D95; "
            "}"
            "QPushButton:pressed {"
            "background-color: #2F5777"
            "}"
        )
        self.layout = QVBoxLayout()

        informacion_central = QWidget()
        informacion_central.setStyleSheet("border-radius: 10px;")
        informacion_central.setContentsMargins(50, 0, 50, 0)
        informacion_central.setFixedHeight(360)

        informacion = QHBoxLayout()
        informacion.setAlignment(Qt.AlignmentFlag.AlignTop)
        informacion.setContentsMargins(0, 0, 0, 0)
        informacion.setSpacing(50)

        # Agrega la imagen de perfil por ruta
        self.image_label = ProfileImageWidget(self.user_data)
        informacion.addWidget(self.image_label)
        self.image_label.setStyleSheet(
            "QLabel {"
            "   background-color: white;"
            "   border-radius: 10px;"
            "   padding: 10px;"
            "}"
        )
        self.image_label.setMaximumWidth(300)
        self.image_label.setMinimumWidth(300)
        self.image_label.setMinimumHeight(360)
        self.image_label.setMaximumHeight(360)

        informacion_text_central = QWidget()
        informacion_text_central.setContentsMargins(0, 0, 0, 0)
        informacion_text_central.setStyleSheet("border-radius: 10px;")

        self.informacion_text = QVBoxLayout()
        self.informacion_text.setContentsMargins(0, 0, 0, 0)
        self.informacion_text.setSpacing(20)

        self.informacion_text.setAlignment(Qt.AlignmentFlag.AlignTop)
        lb_bienvendia = QLabel(f"👋 Hola {self.user_data['nombre']}!")
        lb_bienvendia.setStyleSheet("font-size: 30px; font-weight: bold; color: black; background-color: #E4E4E4; border-radius: 20px; padding: 5px; margin-top: 15px;")
        user_rol = self.user_or_admin()


        estilos_lb_info = "font-size: 20px; color: black; background-color: #E4E4E4; border-radius: 20px; padding: 10px;"
        lb_info_user_name = QLabel(f"Nombre: {self.user_data['nombre']}")
        lb_info_user_id_personal = QLabel(f"Identificación: {self.user_data['id_personal']}")
        lb_info_user_cellphone = QLabel(f"Celular: {self.user_data['cellphone']}")
        lb_info_user_role = QLabel(f"Rol: {user_rol}")

        lb_info_user_name.setStyleSheet(estilos_lb_info)
        lb_info_user_id_personal.setStyleSheet(estilos_lb_info)
        lb_info_user_cellphone.setStyleSheet(estilos_lb_info)
        lb_info_user_role.setStyleSheet(estilos_lb_info)

        self.informacion_text.addWidget(lb_bienvendia)
        self.informacion_text.addWidget(lb_info_user_name)
        self.informacion_text.addWidget(lb_info_user_id_personal)
        self.informacion_text.addWidget(lb_info_user_cellphone)
        self.informacion_text.addWidget(lb_info_user_role)

        informacion_text_central.setLayout(self.informacion_text)

        informacion.addWidget(informacion_text_central)
        informacion_central.setLayout(informacion)

        self.layout_buttom = QHBoxLayout()
        self.layout_buttom.setContentsMargins(0, 0, 0, 0)
        self.layout_buttom.setSpacing(50)

        self.boton_prestamos = QPushButton(" Mis prestamos")
        self.boton_prestamos.setMaximumWidth(200)
        self.boton_prestamos.setCursor(Qt.PointingHandCursor)
        self.layout_buttom.addWidget(self.boton_prestamos)

        self.boton_cambiar_contraseña = QPushButton("Cambiar Contraseña")
        self.boton_cambiar_contraseña.setMaximumWidth(200)
        self.boton_cambiar_contraseña.setCursor(Qt.PointingHandCursor)
        self.layout_buttom.addWidget(self.boton_cambiar_contraseña)

        self.boton_eliminar_cuenta = QPushButton("Eliminar Cuenta")
        self.boton_eliminar_cuenta.setCursor(Qt.PointingHandCursor)
        self.boton_eliminar_cuenta.setMaximumWidth(200)
        self.boton_eliminar_cuenta.setStyleSheet(
            "QPushButton {"
            "background-color: #FF0000; "
            "color: white; "
            "text-align: center;"
            "}"
            "QPushButton::hover {"
            "background-color: #CC0000; "
            "}"
            "QPushButton:pressed {"
            "background-color: #800000"
            "}"
        )
        self.layout_buttom.addWidget(self.boton_eliminar_cuenta)
        self.boton_eliminar_cuenta.clicked.connect(self.confirm_delete_account)
        self.boton_prestamos.clicked.connect(self.show_prestamos_user)

        self.layout.addWidget(informacion_central)
        self.layout.addLayout(self.layout_buttom)
        self.setLayout(self.layout)

    def user_or_admin(self):
        if self.user_data['rol'] == "admin":
            return "Administrador"
        else:
            return "Usuario"

    def confirm_delete_account(self):
        # Muestra el cuadro de diálogo de confirmación
        confirm_dialog = ConfirmDeleteDialog(self)
        result = confirm_dialog.exec()

        # Si el usuario confirma, realiza la acción de eliminación
        if result == QDialog.Accepted:
            self.close_and_eliminate_session()

    def close_and_eliminate_session(self):
        #index_eliminar = self.user_data["uuid"]
        uuid_user = self.user_data["uuid"]
        if uuid_user:
            path_to_json = os.path.join(os.path.dirname(__file__), "../databases/usuarios.json")

            with open(path_to_json, "r", encoding="utf-8") as json_file:
                all_users_data = json.load(json_file)
            # Encuentra el índice del usuario por su UUID
            index_eliminar = next(
                (index for (index, user) in enumerate(all_users_data["usuarios"]) if user["uuid"] == uuid_user),
                None
            )
            # Verifica si el usuario existe en la lista antes de intentar eliminarlo
            if index_eliminar is not None:
                # Elimina al usuario por su UUID
                del all_users_data["usuarios"][index_eliminar]
                # Guarda la lista actualizada en el archivo JSON
                with open(path_to_json, "w", encoding="utf-8") as json_file:
                    json.dump(all_users_data, json_file, indent=2)

        self.parent.close()
        from ui_login.ui_login_copy import MiVentana
        window = MiVentana()
        window.show()
        
    def show_prestamos_user(self):
        self.parent.switch_vista_prestamos_user()

class Dashboard(QWidget):
    def __init__(self, parent, user_data):
        super(Dashboard, self).__init__()
        self.parent = parent

        self.side_menu = SideMenu(parent, user_data)
        self.side_menu.button_close_session.clicked.connect(self.close_session)
        self.stacked_widget = QStackedWidget()
        self.setup_ui()

    def setup_ui(self):
        self.layout = QHBoxLayout()
        # Agregar el menú lateral a la izquierda
        self.layout.addWidget(self.side_menu)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Agregar el contenido principal al resto del espacio
        self.layout.addWidget(self.stacked_widget, 1)

        self.setLayout(self.layout)

    def close_session(self):
        self.parent.close()
        from ui_login.ui_login_copy import MiVentana
        window = MiVentana()
        window.show()

class Ui_principal(QMainWindow):
    logout_signal = Signal()
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
        self.setMinimumSize(1200, 600)
        path_icon = os.path.join(basedir, "../media/img/libro.png")
        icon = QIcon(path_icon)
        self.setWindowIcon(icon)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.size_grip = QSizeGrip(self)
        self.size_grip.setStyleSheet("QSizeGrip { background-color: transparent; }")
        self.size_grip.setFixedSize(20, 20)
        self.size_grip.setGeometry(self.width() - 20, self.height() - 20, 20, 20)

        # Barra horizontal con botón y barra de búsqueda
    def resizeEvent(self, event: QResizeEvent) -> None:
        super(Ui_principal, self).resizeEvent(event)
        self.size_grip.setGeometry(self.width() - 20, self.height() - 20, 20, 20)

    def interfaz(self):
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #2F53D1;")
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
        navbars_widget.setMaximumHeight(50)
        navbars_widget.setMinimumHeight(50)

        central_vbox.addWidget(navbars_widget)


        # Vista de inicio de la biblioteca
        self.principal_book_grid_widget = BookGridVistaInicio(self.user_data)
        
        navbar.search_triggered.connect(self.principal_book_grid_widget.update_books_on_search)
        navbar.search_bar.textChanged.connect(self.switch_principal)
        #navbar.search_bar.editingFinished.connect(self.principal_book_grid_widget.update_books)


        # Vista de perfil de usuario
        self.perfil_usuario = VistaUserProfile(self, self.user_data)
        self.register_book = Ui_RegisterBook()
        self.register_book.button_guardar.clicked.connect(self.actualizar_lista_libros)
        self.prestamos_books_admin = Ui_Prestamos_admin()
        self.prestamos_books_user = Ui_Prestamos_user(self.user_data)
        # Boton conectado a un signal PySide6
        
        self.register_book.button_editar.clicked.connect(self.switch_register_book_admin)
        self.register_book.button_ver_prestamos.clicked.connect(self.switch_vista_prestamos_admin)

        self.vista_administrador = Dashboard(self, self.user_data)
        self.vista_administrador.setStyleSheet("background-color: white;")
        self.vista_administrador.side_menu.button_home.clicked.connect(self.switch_principal)
        self.vista_administrador.side_menu.button_perfil.clicked.connect(self.switch_perfil_usuario)
        self.vista_administrador.side_menu.button_admin_libros.clicked.connect(self.switch_register_book_admin)
        self.vista_administrador.side_menu.button_prestamos_admin.clicked.connect(self.switch_vista_prestamos_admin)
        self.vista_administrador.side_menu.button_prestamos_user.clicked.connect(self.switch_vista_prestamos_user)
        #self.vista_administrador.side_menu.button_close_session.clicked.connect()
        self.vista_administrador.stacked_widget.addWidget(self.principal_book_grid_widget)
        self.vista_administrador.stacked_widget.addWidget(self.perfil_usuario)
        self.vista_administrador.stacked_widget.addWidget(self.register_book)
        self.vista_administrador.stacked_widget.addWidget(self.prestamos_books_admin)
        self.vista_administrador.stacked_widget.addWidget(self.prestamos_books_user)

        central_vbox.addWidget(self.vista_administrador)

        self.setCentralWidget(central_widget)
        #print(self.user_data)
        
    def actualizar_lista_prestamos(self):
        print("Actualizando lista de prestamos...")
        ListaPrestamos.actualizar_prestamos(self)
        ListaPrestamos.imprimir_prestamos()
        ListaLibros.actualizar_libros(self)
        ListaLibros.imprimir_libros()
        
    def actualizar_lista_libros(self):
        print("Actualizando lista de libros...")
        ListaLibros.actualizar_libros(self)
        ListaLibros.imprimir_libros()


    def switch_principal(self):
        #self.vista_administrador.side_menu.button_home.clicked.connect(self.principal_book_grid_widget.update_books)
        self.vista_administrador.stacked_widget.setCurrentWidget(self.principal_book_grid_widget)
        self.vista_administrador.setStyleSheet("background-color: white;")

    def switch_perfil_usuario(self):
        self.vista_administrador.stacked_widget.setCurrentWidget(self.perfil_usuario)
        self.vista_administrador.setStyleSheet("background-color: white;")

    def switch_vista_administrador(self):
        self.vistas_app.setCurrentWidget(self.vista_administrador)
        self.vistas_app.setStyleSheet("background-color: #1C3D95;")

    def switch_vista_prestamos_admin(self):
        self.vista_administrador.stacked_widget.setCurrentWidget(self.prestamos_books_admin)
        self.prestamos_books_admin.update_table()
        self.vista_administrador.setStyleSheet("background-color: white;")

    def switch_vista_prestamos_user(self):
        self.vista_administrador.stacked_widget.setCurrentWidget(self.prestamos_books_user)
        self.prestamos_books_user.update_table()
        self.vista_administrador.setStyleSheet("background-color: white;")

    def switch_register_book_admin(self):
        self.vista_administrador.stacked_widget.setCurrentWidget(self.register_book)
        self.vista_administrador.setStyleSheet("background-color: white;")
        



def main():
    app = QApplication(sys.argv)
    window = Ui_principal()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
