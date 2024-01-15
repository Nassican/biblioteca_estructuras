import sys
import os
import json
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import Signal

basedir = os.path.abspath(os.path.dirname(__file__))

class ConfirmacionDevolverDialog(QDialog):
    def __init__(self, parent=None, titulo="", isbn=""):
        super().__init__(parent)
        self.setWindowTitle("Confirmar Devolucion")
        self.setFixedHeight(100)

        self.layout = QVBoxLayout(self)

        self.label = QLabel(f"¿Estás seguro de que deseas devolver el libro {titulo} con codigo ISBN {isbn}?", self)
        self.layout.addWidget(self.label)

        self.layout_botones = QHBoxLayout()

        self.boton_aceptar = QPushButton("Confirmar", self)
        self.boton_aceptar.setCursor(Qt.PointingHandCursor)
        self.boton_aceptar.setStyleSheet("background-color: #B72E2E;")
        self.boton_cancelar = QPushButton("Cancelar", self)
        self.boton_cancelar.setCursor(Qt.PointingHandCursor)

        self.boton_aceptar.clicked.connect(self.accept)
        self.boton_cancelar.clicked.connect(self.reject)

        self.layout_botones.addWidget(self.boton_aceptar)
        self.layout_botones.addWidget(self.boton_cancelar)

        self.layout.addLayout(self.layout_botones)

        self.setStyleSheet(
          "QLabel {"
          "font-size: 15px; "
          "}"
          "QLineEdit {"
          "border: 1px solid #2F53D1; "
          "border-radius: 5px; "
          "padding: 5px; "
          "font-size: 15px; "
          "}"
          "QDialog {"
          "border: 10px; "
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

class Ui_Prestamos_admin(QWidget):
    def __init__(self):
        super().__init__()

        json_prestamos_db = os.path.join(basedir, "../databases/prestamos.json")
        self.prestamos_data = self.load_prestamos_data(json_prestamos_db)

        self.setGeometry(100, 100, 800, 500)  # Ajusta el tamaño según sea necesario
        self.setWindowTitle("Administración de Préstamos")

        self.setup_ui()

    def load_prestamos_data(self, json_path):
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data.get('prestamos', [])

    def setup_ui(self):
        self.label_vacio = QLabel()
        self.titulo_prestamos = QLabel("Vista Administrador", self)
        self.titulo_prestamos.setStyleSheet(
            """
            QLabel {
                text-align: left;
                font-weight: bold;
                font-size: 20px;
            }
            """)

        self.barra_busqueda = QLineEdit(self)
        self.barra_busqueda.setPlaceholderText("Buscar por autor, usuario, ISBN o título...")
        self.barra_busqueda.setGeometry(10, 60, 280, 20)
        self.barra_busqueda.textChanged.connect(self.filtrar_tabla)
        self.barra_busqueda.setStyleSheet(
            "QLineEdit {"
            "border: 1px solid #2F53D1; "
            "border-radius: 5px; "
            "padding: 5px; "
            "font-size: 15px; "
            "}"
        )

        layout_botones = QHBoxLayout()
        layout_botones.addWidget(self.titulo_prestamos)
        layout_botones.addWidget(self.label_vacio)
        layout_botones.addWidget(self.label_vacio)
        layout_botones.addWidget(self.label_vacio)
        layout_botones.addWidget(self.barra_busqueda)

        self.tabla = QTableWidget(self)
        self.tabla.setGeometry(10, 90, 780, 300)  # Tamaño de la tabla
        self.tabla.setColumnCount(5)  # Columnas
        self.tabla.setHorizontalHeaderLabels(["Nombre de Usuario", "ISBN", "Título", "Autor", "Fecha del pedido"])  # Encabezados de las columnas
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)  # No permite editar los datos de la tabla
        self.tabla.setAlternatingRowColors(True)

        self.tabla.setStyleSheet("""
            QScrollBar:vertical {
                width: 10px;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical {
                background-color: #2F53D1;
                border-radius: 4px;
            }

            QScrollBar::add-line:vertical {
                height: 0px;
            }

            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QHeaderView::section {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                  stop:0 #2F53D1, stop: 0.5 #2F53D1,
                                                  stop: 0.6 #2F5399, stop:1 #2F5399);
                color: white;
                padding-left: 4px;
                border-radius: 5px;
                border: 1px solid #EEEEEE;
            }
            QHeaderView::section:checked
            {
                background-color: #102A94;
            }
            QHeaderView::section:horizontal
            {
                border-top: 1px solid #2F53D1;
            }
            QHeaderView::section:vertical
            {
                border-left: 1px solid #2F53D1;
            }

            QTableWidget {
                border: 1px solid #2F53D1;
                border-radius: 5px;
                font-size: 15px;
                padding: 5px;
            }
            QTableWidget:item {
               background-color: white;
               color: black;
            }
            QTableWidget:item:alternate {
               background-color: #EEEEEE;
            }
            
            
        """)

        layout_principal = QVBoxLayout(self)
        layout_principal.addLayout(layout_botones)
        layout_principal.addWidget(self.label_vacio)
        layout_principal.addWidget(self.tabla)
        
        
        self.populate_table()



        self.setLayout(layout_principal)

    def populate_table(self):
        self.tabla.setRowCount(sum(len(p.get('prestamos', [])) for p in self.prestamos_data))

        # Cargar datos de usuarios
        json_usuarios_db = os.path.join(basedir, "../databases/usuarios.json")
        usuarios_data = self.load_usuarios_data(json_usuarios_db)

        row = 0
        for prestamo in self.prestamos_data:
            uuid_usuario = prestamo.get('uuid', '')
            libros_prestamo = prestamo.get('prestamos', '')

            # Buscar el nombre de usuario correspondiente a la UUID
            username = ""
            for usuario in usuarios_data:
                if usuario.get('uuid', '') == uuid_usuario:
                    username = usuario.get('username', '')
                    break

            for libro in libros_prestamo:
                isbn = libro.get('ISBN', '')
                titulo = libro.get('Titulo', '')
                autor = libro.get('Autor', '')
                fecha = libro.get('Fecha', '')

                self.tabla.setItem(row, 0, QTableWidgetItem(username))
                self.tabla.setItem(row, 1, QTableWidgetItem(isbn))
                self.tabla.setItem(row, 2, QTableWidgetItem(titulo))
                self.tabla.setItem(row, 3, QTableWidgetItem(autor))
                self.tabla.setItem(row, 4, QTableWidgetItem(fecha))

                row += 1

    def load_usuarios_data(self, json_path):
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data.get('usuarios', [])

    def filtrar_tabla(self):
        texto_busqueda = self.barra_busqueda.text().lower()

        for fila in range(self.tabla.rowCount()):
            fila_visible = False
            texto_fila = []

            for col in range(self.tabla.columnCount()):
                item_celda = self.tabla.item(fila, col)

                if item_celda is not None:
                    texto_celda = item_celda.text().lower()
                    texto_fila.append(texto_celda)

                    if texto_busqueda in texto_celda:
                        fila_visible = True
                        break  # No es necesario seguir buscando si encontramos una coincidencia
                else:
                    texto_fila.append('')  # Si la celda es None, agregamos una cadena vacía

            self.tabla.setRowHidden(fila, not fila_visible)

    def update_table(self):
        print("Se actualizó el archivo de prestamos")
        # Volver a cargar los datos de préstamos y actualizar la tabla
        json_prestamos_db = os.path.join(basedir, "../databases/prestamos.json")
        self.prestamos_data = self.load_prestamos_data(json_prestamos_db)
        self.populate_table()

class Ui_Prestamos_user(QWidget):
    def __init__(self, data_user):
        super().__init__()
        self.data_user = data_user
        self.boton_libro_devuelto = Signal()
        json_prestamos_db = os.path.join(basedir, "../databases/prestamos.json")
        self.prestamos_data = self.load_prestamos_data(json_prestamos_db)

        self.setGeometry(100, 100, 800, 500)  # Ajusta el tamaño según sea necesario
        self.setWindowTitle("Administración de Préstamos")

        self.setup_ui()

    def load_prestamos_data(self, json_path):
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data.get('prestamos', [])

    def setup_ui(self):
        self.label_vacio = QLabel()
        self.titulo_prestamos = QLabel("Mis Prestamos", self)
        self.titulo_prestamos.setStyleSheet(
            """
            QLabel {
                text-align: left;
                font-weight: bold;
                font-size: 20px;
            }
            """)

        self.barra_busqueda = QLineEdit(self)
        self.barra_busqueda.setPlaceholderText("Buscar por autor, usuario, ISBN o título...")
        self.barra_busqueda.setGeometry(10, 60, 280, 20)
        self.barra_busqueda.textChanged.connect(self.filtrar_tabla)
        self.barra_busqueda.setStyleSheet(
            "QLineEdit {"
            "border: 1px solid #2F53D1; "
            "border-radius: 5px; "
            "padding: 5px; "
            "font-size: 15px; "
            "}"
        )

        layout_botones = QHBoxLayout()
        layout_botones.addWidget(self.titulo_prestamos)
        layout_botones.addWidget(self.label_vacio)
        layout_botones.addWidget(self.label_vacio)
        layout_botones.addWidget(self.label_vacio)
        layout_botones.addWidget(self.barra_busqueda)

        self.tabla = QTableWidget(self)
        self.tabla.setGeometry(10, 90, 780, 300)  # Tamaño de la tabla
        self.tabla.setColumnCount(6)  # Columnas
        self.tabla.setHorizontalHeaderLabels(["Nombre de Usuario", "ISBN", "Título", "Autor", "Fecha del pedido", ""])  # Encabezados de las columnas
        self.tabla.setEditTriggers(QAbstractItemView.NoEditTriggers)  # No permite editar los datos de la tabla
        self.tabla.setAlternatingRowColors(True)
        #self.tabla.verticalHeader().setVisible(False)
        #self.tabla.horizontalHeader().setVisible(False)
        #self.tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.setSelectionMode(QTableWidget.NoSelection)
        self.tabla.setShowGrid(False)
        self.tabla.setFocusPolicy(Qt.NoFocus)
        self.tabla.setAlternatingRowColors(True)
        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tabla.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)

        self.tabla.setStyleSheet("""
            QScrollBar:vertical {
                width: 10px;
                border-radius: 4px;
            }

            QScrollBar::handle:vertical {
                background-color: #2F53D1;
                border-radius: 4px;
            }

            QScrollBar::add-line:vertical {
                height: 0px;
            }

            QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QHeaderView::section {
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                  stop:0 #2F53D1, stop: 0.5 #2F53D1,
                                                  stop: 0.6 #2F5399, stop:1 #2F5399);
                color: white;
                padding-left: 4px;
                border: 1px solid #EEEEEE;
                border-radius: 5px;
            }
            QHeaderView::section:checked
            {
                background-color: #102A94;
            }
            QHeaderView::section:horizontal
            {
                border-top: 1px solid #2F53D1;
            }
            QHeaderView::section:vertical
            {
                border-left: 1px solid #2F53D1;
            }

            QTableWidget {
                border: 1px solid #2F53D1;
                border-radius: 5px;
                font-size: 15px;
                padding: 5px;
            }
            QTableWidget:item {
               background-color: white;
               color: black;
            }
            QTableWidget:item:alternate {
               background-color: #EEEEEE;
            }
            
            
        """)

        layout_principal = QVBoxLayout(self)
        layout_principal.addLayout(layout_botones)
        layout_principal.addWidget(self.label_vacio)
        layout_principal.addWidget(self.tabla)
        self.populate_table()
        self.setLayout(layout_principal)

    def populate_table(self):
        user_uuid = self.data_user.get('uuid', '')
        user_prestamos = [prestamo for prestamo in self.prestamos_data if prestamo.get('uuid', '') == user_uuid]

        self.tabla.setRowCount(sum(len(p.get('prestamos', [])) for p in user_prestamos))


        row = 0
        for prestamo in user_prestamos:
            libros_prestamo = prestamo.get('prestamos', '')

            for libro in libros_prestamo:
                isbn = libro.get('ISBN', '')
                titulo = libro.get('Titulo', '')
                autor = libro.get('Autor', '')
                fecha = libro.get('Fecha', '')

                # Agregar elementos a las celdas
                self.tabla.setItem(row, 0, QTableWidgetItem(self.data_user.get('username', '')))
                self.tabla.setItem(row, 1, QTableWidgetItem(isbn))
                self.tabla.setItem(row, 2, QTableWidgetItem(titulo))
                self.tabla.setItem(row, 3, QTableWidgetItem(autor))
                self.tabla.setItem(row, 4, QTableWidgetItem(fecha))

                # Agregar un botón de devolución en la columna 5
                path_to_icon_devolver = os.path.join(os.path.dirname(__file__), "../media/img/basura_icon.png")
                boton_devolver = QPushButton("", self)
                self.boton_devolver = boton_devolver
                boton_devolver.setIcon(QIcon(path_to_icon_devolver))
                boton_devolver.setFixedSize(30, 30)
                boton_devolver.setCursor(Qt.PointingHandCursor)
                boton_devolver.setStyleSheet(
                    "QPushButton {"
                    "background-color: transparent; "
                    "border: none; "
                    "font-weight: bold; "
                    "padding: 5px; "
                    "border-radius: 5px;"
                    "}"
                    "QPushButton::hover {"
                    "background-color: #E5E5E5; "
                    "}"
                    "QPushButton:pressed {"
                    "background-color: #D1D1D1"
                    "}"
                )
                # Agregar un botón de devolución en la columna 5
                isbn = libros_prestamo[row].get('ISBN', '')
                boton_devolver.clicked.connect(self.create_devolver_libro_function(row))
                self.boton_devolver.clicked.connect(lambda: self.window().actualizar_lista_prestamos())
                self.tabla.setCellWidget(row, 5, boton_devolver)


                row += 1

    def create_devolver_libro_function(self, row):
        def devolver_libro():

            isbn = self.tabla.item(row, 1).text()
            titulo = self.tabla.item(row, 2).text()
            print(f"Devolver libro en la fila {row} con ISBN: {isbn}")
            user_uuid = self.data_user.get('uuid', '')

            dialogo_confirmacion = ConfirmacionDevolverDialog(self, titulo=titulo, isbn=isbn)

            if dialogo_confirmacion.exec() == QDialog.Accepted:
                for prestamo in self.prestamos_data:
                    if prestamo.get('uuid', '') == user_uuid:
                        libros_prestamo = prestamo.get('prestamos', [])
                        for libro in libros_prestamo:
                            if libro.get('ISBN', '') == isbn:
                                libros_prestamo.remove(libro)
                                break  # Rompemos el bucle después de eliminar el libro una vez
                # Actualizar el archivo JSON de préstamos
                json_prestamos_db = os.path.join(basedir, "../databases/prestamos.json")
                with open(json_prestamos_db, 'w', encoding='utf-8') as file:
                    json.dump({"prestamos": self.prestamos_data}, file, ensure_ascii=False, indent=4)
                # Sumar 1 al número de ejemplares en la base de datos de libros
                json_libros_db = os.path.join(basedir, "../databases/libros_db.json")
                with open(json_libros_db, 'r+', encoding='utf-8') as file:
                    libros_data = json.load(file)
                for libro in libros_data.get('Libros', []):
                    if libro.get('ISBN', '') == isbn:
                        libro['Ejemplares'] = str(int(libro["Ejemplares"]) + 1)
                        break
                with open(json_libros_db, 'w', encoding='utf-8') as file:
                    json.dump(libros_data, file, ensure_ascii=False, indent=2)
                # Volver a cargar los datos de préstamos y actualizar la tabla
                self.prestamos_data = self.load_prestamos_data(json_prestamos_db)
                self.populate_table()

        
        return devolver_libro

    def load_usuarios_data(self, json_path):
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data.get('usuarios', [])

    def filtrar_tabla(self):
        texto_busqueda = self.barra_busqueda.text().lower()

        for fila in range(self.tabla.rowCount()):
            fila_visible = False
            texto_fila = []

            for col in range(self.tabla.columnCount()):
                item_celda = self.tabla.item(fila, col)

                if item_celda is not None:
                    texto_celda = item_celda.text().lower()
                    texto_fila.append(texto_celda)

                    if texto_busqueda in texto_celda:
                        fila_visible = True
                        break  # No es necesario seguir buscando si encontramos una coincidencia
                else:
                    texto_fila.append('')  # Si la celda es None, agregamos una cadena vacía

            self.tabla.setRowHidden(fila, not fila_visible)

    def update_table(self):
        print("Se actualizó el archivo de prestamos")
        # Volver a cargar los datos de préstamos y actualizar la tabla
        json_prestamos_db = os.path.join(basedir, "../databases/prestamos.json")
        self.prestamos_data = self.load_prestamos_data(json_prestamos_db)
        self.populate_table()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ui_Prestamos_admin()
    ventana.show()
    sys.exit(app.exec())
