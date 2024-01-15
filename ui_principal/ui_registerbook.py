import os
import sys
import shutil
import json

try:
    from ui_principal.ui_categorias import CategoriasWidget
except ImportError:
    print("No se ha encontrado el archivo ui_categorias.py")

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

basedir = os.path.abspath(os.path.dirname(__file__))

json_path = os.path.join(os.path.dirname(
    __file__), "../databases/libros_db.json")


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


class Ui_RegisterBook(QWidget):
    def __init__(self):
        super(Ui_RegisterBook, self).__init__()
        path_to_img = os.path.join(os.path.dirname(
            __file__), "./media/img/arrow-down-combobox.png")
        self.image_path = ""
        self.setStyleSheet(
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
            "background-color: #2F53D1"
            "}"
            "QLineEdit {"
            "border-radius: 10px; "
            "padding: 5px; "
            "font-size: 15px; "
            "}"
            "QLineEdit::focus {"
            "border: 1px solid #2F53D1; "
            "}"
            "QLineEdit::hover {"
            "border: 1px solid #2F53D1; "
            "}"
            "QLineEdit::disabled {"
            "background-color: #E5E5E5; "
            "}"
            "QComboBox {"
            "border-radius: 10px; "
            "padding: 5px; "
            "font-size: 15px; "
            "}"
            "QComboBox::drop-down {"
            "border: 0px; "
            "} "
            "QComboBox::down-arrow {"
            "image: url('./media/img/arrow-down-deactived-combobox.png'); "
            "width: 20px; "
            "height: 20px; "
            "margin-right: 15px; "
            "}"
            "QComboBox::hover {"
            "border: 1px solid #2F53D1; "
            "}"
            "QComboBox::disabled {"
            "background-color: #E5E5E5; "
            "}"
            "QLabel {"
            "font-size: 15px; "
            "border-radius: 10px; "
            "border: 5px solid #ffffff; "
            "}"
            "QTextEdit {"
            "border-radius: 10px; "
            "padding: 5px; "
            "font-size: 15px; "
            "}"
            "QTextEdit::focus {"
            "border: 1px solid #2F53D1; "
            "}"
            "QTextEdit::hover {"
            "border: 1px solid #2F53D1; "
            "}"
            "QTextEdit::disabled {"
            "background-color: #E5E5E5; "
            "}"

        )

        central_layout = QVBoxLayout()
        # Title
        form_container = QWidget()
        form_container.setContentsMargins(0, 0, 0, 0)
        form_layout = QHBoxLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)

        form_container_left_side = QWidget()
        form_left_side = QVBoxLayout()
        form_left_side.setContentsMargins(5, 5, 5, 5)
        form_container_right_side = QWidget()
        form_right_side = QVBoxLayout()
        form_right_side.setContentsMargins(5, 5, 5, 5)

        form_botons = QHBoxLayout()
        form_botons.setContentsMargins(0, 0, 0, 0)
        button_añadir = QPushButton("Añadir Nuevo Libro")
        button_añadir.setCursor(Qt.PointingHandCursor)
        button_añadir.setStyleSheet(
            "QPushButton {"
            "background-color: #067A14; color: white; font-weight: bold;"
            "}"
            "QPushButton::hover {"
            "background-color: #0B9B1E; "
            "}"
            "QPushButton:pressed {"
            "background-color: #067A14"
            "}"
        )
        button_añadir.clicked.connect(self.añadir_libro)
        self.button_editar = QPushButton("Editar Libro")
        self.button_editar.setCursor(Qt.PointingHandCursor)
        self.button_editar.setStyleSheet(
            "QPushButton {"
            "background-color: #095012; color: white; font-weight: bold;"
            "}"
            "QPushButton::hover {"
            "background-color: #0C7F17; "
            "}"
            "QPushButton:pressed {"
            "background-color: #095012"
            "}"
        )
        self.button_editar.clicked.connect(self.listar_libros)
        form_botons.addWidget(button_añadir)
        form_botons.addWidget(self.button_editar)

        self.widget_imagen = QWidget()
        self.layout_imagen = QVBoxLayout()
        self.imagen_label = QLabel()
        self.imagen_label.setStyleSheet(
            "border-radius: 10px; "
            "border: 5px solid #ffffff; "
            "background-color: #ffffff; "
            "margin-bottom: 10px;"
            "margin-top: 10px;"
        )
        self.button_escoger_imagen = QPushButton("Escoger Imagen Libro")
        shadow_label = self.shadow_effect()
        self.imagen_label.setGraphicsEffect(shadow_label)
        default_image_path = os.path.join(os.path.dirname(__file__), "../media/imgDefault/NO COVER.png")
        self.load_and_display_image(default_image_path, self.imagen_label.size())

        self.button_escoger_imagen.setEnabled(False)
        self.button_escoger_imagen.setStyleSheet(
            "QPushButton {"
            "background-color: #839AE7; color: white; font-weight: bold;"
            "}"
        )
        self.button_escoger_imagen.setCursor(Qt.PointingHandCursor)
        self.button_escoger_imagen.clicked.connect(self.select_image)

        form_left_side.addLayout(form_botons)

        self.widget_imagen.setLayout(self.layout_imagen)
        self.layout_imagen.addWidget(self.imagen_label)
        form_left_side.addWidget(self.widget_imagen)
        form_left_side.addWidget(self.button_escoger_imagen)
        form_container_left_side.setLayout(form_left_side)

        self.line_edit_titulo = QLineEdit()
        self.line_edit_titulo.setPlaceholderText("Titulo (*)")
        self.line_edit_titulo.setEnabled(False)
        self.line_edit_autor = QLineEdit()
        self.line_edit_autor.setPlaceholderText("Autor (*)")
        self.line_edit_autor.setEnabled(False)
        self.line_edit_editorial = QLineEdit()
        self.line_edit_editorial.setPlaceholderText("Editorial (*)")
        self.line_edit_editorial.setEnabled(False)
        self.line_edit_isbn = QLineEdit()
        self.line_edit_isbn.setPlaceholderText("ISBN (*)")
        self.line_edit_isbn.setEnabled(False)

        h_año_idioma = QHBoxLayout()
        self.line_edit_año = QLineEdit()
        self.line_edit_año.setPlaceholderText("Año de publicación")
        self.line_edit_año.setEnabled(False)
        self.line_edit_año.setValidator(QIntValidator())
        self.line_edit_idioma = QLineEdit()
        self.line_edit_idioma.setPlaceholderText("Idioma")
        self.line_edit_idioma.setEnabled(False)
        h_año_idioma.addWidget(self.line_edit_año)
        h_año_idioma.addWidget(self.line_edit_idioma)

        h_ejemplares_categoria = QHBoxLayout()
        self.line_edit_ejemplares = QLineEdit()
        self.line_edit_ejemplares.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.line_edit_ejemplares.setPlaceholderText("Ejemplares (*)")
        self.line_edit_ejemplares.setEnabled(False)
        self.line_edit_ejemplares.setValidator(QIntValidator())
        self.combobox_categoria = QComboBox()
        self.combobox_categoria.setCursor(Qt.PointingHandCursor)
        self.combobox_categoria.setEnabled(False)
        self.combobox_categoria.addItem("Sin categoría")
        self.load_categories(self.combobox_categoria)
        self.combobox_categoria.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed)
        h_ejemplares_categoria.addWidget(self.line_edit_ejemplares)
        h_ejemplares_categoria.addWidget(self.combobox_categoria)

        self.line_edit_sinopsis = QTextEdit()
        self.line_edit_sinopsis.setPlaceholderText("Sinopsis")
        self.line_edit_sinopsis.wordWrapMode()
        self.line_edit_sinopsis.setAlignment(Qt.AlignTop)
        self.line_edit_sinopsis.setEnabled(False)
        self.line_edit_sinopsis.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Configurar QSizePolicy para que los elementos ocupen todo el espacio horizontal disponible
        form_right_side.setSizeConstraint(QLayout.SetMinimumSize)
        form_layout.setSizeConstraint(QLayout.SetMinimumSize)
        form_left_side.setSizeConstraint(QLayout.SetMinimumSize)

        form_right_side.addWidget(self.line_edit_titulo)
        form_right_side.addWidget(self.line_edit_autor)
        form_right_side.addWidget(self.line_edit_editorial)
        form_right_side.addWidget(self.line_edit_isbn)
        form_right_side.addLayout(h_año_idioma)
        form_right_side.addLayout(h_ejemplares_categoria)
        form_right_side.addWidget(self.line_edit_sinopsis)

        form_container_right_side.setLayout(form_right_side)

        # Agregar espacios elásticos para distribuir equitativamente los elementos en form_layout
        form_layout.addWidget(form_container_left_side)
        form_container_left_side.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        form_layout.addWidget(form_container_right_side)

        form_container.setLayout(form_layout)

        h_important_buttons = QHBoxLayout()
        h_important_buttons.setContentsMargins(5, 5, 5, 5)
        self.button_guardar = QPushButton("Añadir Libro")
        self.button_guardar.setEnabled(False)
        self.button_guardar.clicked.connect(self.guardar_datos)
        #
        self.button_guardar.setCursor(Qt.PointingHandCursor)
        self.button_guardar.setStyleSheet(
            "QPushButton {"
            "background-color: #75D181; color: white; font-weight: bold;"
            "}"
        )

        self.button_ver_prestamos = QPushButton("Ver Prestamos")
        self.button_ver_prestamos.setCursor(Qt.PointingHandCursor)
        self.button_añadir_categoria = QPushButton("Añadir Categoria")
        self.button_añadir_categoria.setCursor(Qt.PointingHandCursor)
        self.button_añadir_categoria.clicked.connect(self.añadir_categoria)

        h_important_buttons.addWidget(self.button_guardar)
        h_important_buttons.addWidget(self.button_ver_prestamos)
        h_important_buttons.addWidget(self.button_añadir_categoria)

        # Agregar un espacio elástico al final de central_layout
        central_layout.addWidget(form_container)
        central_layout.addLayout(h_important_buttons)

        self.setLayout(central_layout)

    def resizeEvent(self, event):
        # Llamamos a la función para cargar y mostrar la imagen con el tamaño actual
        if self.image_path:
            self.load_and_display_image(
                self.image_path, self.imagen_label.size())

    def añadir_categoria(self):
        categoria_widget = CategoriasWidget()
        categoria_widget.exec()
        self.actualizar_categorias_combobox()

    def añadir_libro(self):
        # Activar botones
        self.button_escoger_imagen.setEnabled(True)
        self.button_escoger_imagen.setStyleSheet(
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
            "background-color: #2F53D1"
            "}"
        )
        self.line_edit_titulo.setEnabled(True)
        shadow_titulo = self.shadow_effect()
        self.line_edit_titulo.setGraphicsEffect(shadow_titulo)
        self.line_edit_autor.setEnabled(True)
        shadow_autor = self.shadow_effect()
        self.line_edit_autor.setGraphicsEffect(shadow_autor)
        self.line_edit_editorial.setEnabled(True)
        shadow_editorial = self.shadow_effect()
        self.line_edit_editorial.setGraphicsEffect(shadow_editorial)
        self.line_edit_isbn.setEnabled(True)
        shadow_isbn = self.shadow_effect()
        self.line_edit_isbn.setGraphicsEffect(shadow_isbn)
        self.line_edit_año.setEnabled(True)
        shadow_año = self.shadow_effect()
        self.line_edit_año.setGraphicsEffect(shadow_año)
        self.line_edit_idioma.setEnabled(True)
        shadow_idioma = self.shadow_effect()
        self.line_edit_idioma.setGraphicsEffect(shadow_idioma)
        self.line_edit_ejemplares.setEnabled(True)
        shadow_ejem = self.shadow_effect()
        self.line_edit_ejemplares.setGraphicsEffect(shadow_ejem)
        self.combobox_categoria.setEnabled(True)
        shadow_categoria = self.shadow_effect()
        self.combobox_categoria.setGraphicsEffect(shadow_categoria)
        self.combobox_categoria.setStyleSheet(
            "QComboBox::down-arrow {"
            "image: url('./media/img/arrow-down-actived-combobox.png'); "
            "width: 20px; "
            "height: 20px; "
            "margin-right: 15px; "
            "}"
        )
        self.line_edit_sinopsis.setEnabled(True)
        shadow_sinopsis = self.shadow_effect()
        self.line_edit_sinopsis.setAlignment(Qt.AlignTop)
        self.line_edit_sinopsis.setStyleSheet(
            "QTextEdit {"
            "border-radius: 10px; "
            "padding: 5px; "
            "font-size: 15px; "
            "}"
            "QTextEdit::focus {"
            "border: 1px solid #2F53D1; "
            "}"
            "QTextEdit::hover {"
            "border: 1px solid #2F53D1; "
            "}"
            "QTextEdit::enabled {"
            "background-color: #ffffff; "
            "}"
        )
        self.line_edit_sinopsis.setGraphicsEffect(shadow_sinopsis)
        self.button_guardar.setEnabled(True)
        shadow_guardar = self.shadow_effect()
        self.button_guardar.setGraphicsEffect(shadow_guardar)
        self.button_guardar.setStyleSheet(
            "QPushButton {"
            "background-color: #095012; color: white; font-weight: bold;"
            "}"
            "QPushButton::hover {"
            "background-color: #0C7F17; "
            "}"
            "QPushButton:pressed {"
            "background-color: #095012"
            "}"
        )

    def guardar_datos(self):
        titulo = self.line_edit_titulo.text()
        autor = self.line_edit_autor.text()
        editorial = self.line_edit_editorial.text()
        isbn = self.line_edit_isbn.text()
        año = self.line_edit_año.text()
        idioma = self.line_edit_idioma.text()
        ejemplares = self.line_edit_ejemplares.text()
        categoria = self.combobox_categoria.currentText()
        sinopsis = self.line_edit_sinopsis.toPlainText()

        directorio_imagen = os.path.join(os.path.dirname(__file__), f"../media/librosCovers/{isbn}")
        if not os.path.exists(directorio_imagen):
            os.makedirs(directorio_imagen)

        # Revisar si el codigo no existe en la base de datos
        self.message = MessageWidget()

        if not titulo or not autor or not editorial or not isbn or not año or not idioma or not ejemplares or not categoria or not sinopsis:
            self.message.setText("Todos los campos son obligatorios.")
            self.message.exec()
        elif not titulo:
            self.message.setText("El campo de titulo no puede estar vacío.")
            self.message.exec()
        elif not autor:
            self.message.setText("El campo de autor no puede estar vacío.")
            self.message.exec()
        elif not editorial:
            self.message.setText("El campo de editorial no puede estar vacío.")
            self.message.exec()
        elif not isbn:
            self.message.setText("El campo de ISBN no puede estar vacío.")
            self.message.exec()
        elif not año:
            self.message.setText(
                "El campo de Año de publicación no puede estar vacío.")
            self.message.exec()
        elif not idioma:
            self.message.setText("El campo de idioma no puede estar vacío.")
            self.message.exec()
        elif self.id_ISBN_esta_disponible(isbn) == True:
            self.message.setText("El número ISBN ya está en uso.")
            self.message.exec()
        elif not ejemplares:
            self.message.setText(
                "El campo de ejemplares no puede estar vacío.")
            self.message.exec()
        elif self.verificarInt(ejemplares) == False:
            self.message.setText("El campo de ejemplares solo acepta números.")
            self.message.exec()
        elif self.verificarInt(año) == False:
            self.message.setText("El campo de año solo acepta números.")
            self.message.exec()
        else:
            new_book = {
                "Titulo": titulo,
                "Autor": autor,
                "Editorial": editorial,
                "ISBN": isbn,
                "Año de publicacion": año,
                "Idioma": idioma,
                "Ejemplares": ejemplares,
                "Categoria": categoria,
                "Sinopsis": sinopsis,
            }

            try:
                libros_db = self.load_database_books()
                libros_db.append(new_book)
                self.actualizar_base_de_datos(libros_db)


                ruta_imagen = os.path.join(directorio_imagen, "coverBook.png")
                # Guardar la imagen
                if self.imagen_label.pixmap():
                    self.imagen_label.pixmap().save(ruta_imagen)

                self.message.setText("Libro guardado con éxito")
                self.message.setIcon(QMessageBox.Information)
                self.message.exec()
            except Exception as e:
                print(f"Error al copiar la imagen: {str(e)}")

    def listar_libros(self):
        # Obtener la lista de libros
        libros_db = self.load_database_books()

        # Crear una ventana emergente para mostrar la lista de libros
        dialog = QDialog(self)
        dialog.setWindowTitle("Lista de Libros")
        dialog.setGeometry(300, 300, 700, 350)

        layout = QVBoxLayout(dialog)

        # Agregar un QLineEdit para la búsqueda
        search_layout = QHBoxLayout()
        search_label = QLabel("Buscar:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ingrese título o ISBN")
        self.search_input.textChanged.connect(lambda: self.filtrar_libros(libros_db, table_widget))
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)

        layout.addLayout(search_layout)

        # Crear un QTableWidget para mostrar los títulos y códigos ISBN de los libros
        table_widget = QTableWidget(dialog)
        table_widget.setStyleSheet("""
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
        self.table_widget = table_widget
        table_widget.setColumnCount(2)
        table_widget.setHorizontalHeaderLabels(["Título", "ISBN"])
        table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # No permite editar los datos de la tabla
        table_widget.setAlternatingRowColors(True)
        table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Ajustar el ancho de las columnas
        table_widget.setColumnWidth(0, 400)
        table_widget.setColumnWidth(1, 200)

        # Rellenar la tabla con datos
        self.populate_table(libros_db, table_widget)

        # Conectar el evento itemDoubleClicked a la función para editar el libro seleccionado
        table_widget.itemDoubleClicked.connect(lambda item: self.editar_libro(libros_db, item.row(), dialog))

        layout.addWidget(table_widget)

        # Mostrar la ventana emergente
        dialog.exec()

    def filtrar_libros(self, libros, table_widget):
        # Obtener el texto de búsqueda
        search_text = self.search_input.text().lower()

        # Filtrar libros que coincidan con el título o el ISBN
        filtered_libros = [libro for libro in libros
                           if search_text in libro['Titulo'].lower() or search_text in libro['ISBN'].lower()]

        # Limpiar la tabla y volver a llenarla con los resultados filtrados
        table_widget.setRowCount(0)
        self.populate_table(filtered_libros, table_widget)

    def populate_table(self, libros, table_widget):
        # Rellenar la tabla con datos
        for row, libro in enumerate(libros):
            title_item = QTableWidgetItem(libro['Titulo'])
            isbn_item = QTableWidgetItem(libro['ISBN'])

            # Alinear los elementos en la tabla
            title_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            isbn_item.setTextAlignment(Qt.AlignCenter)

            table_widget.insertRow(row)
            table_widget.setItem(row, 0, title_item)
            table_widget.setItem(row, 1, isbn_item)

    def editar_libro(self, libros_db, index, parent=None):
        # Obtener el libro seleccionado
        libro_seleccionado = libros_db[index]

        # Crear una ventana de edición
        dialog = QDialog(parent)
        dialog.setWindowTitle("Editar Libro")
        dialog.setGeometry(300, 100, 600, 400)

        layout = QVBoxLayout(dialog)

        # Crear widgets de edición
        form_layout = QFormLayout()

        self.edit_title = QLineEdit(dialog)
        self.edit_title.setText(libro_seleccionado['Titulo'])
        self.edit_author = QLineEdit(dialog)
        self.edit_author.setText(libro_seleccionado['Autor'])
        self.edit_editorial = QLineEdit(dialog)
        self.edit_editorial.setText(libro_seleccionado['Editorial'])
        self.edit_isbn = QLineEdit(dialog)
        self.edit_isbn.setEnabled(False)
        self.edit_isbn.setText(libro_seleccionado['ISBN'])
        self.edit_year = QLineEdit(dialog)
        self.edit_year.setText(str(libro_seleccionado['Año de publicacion']))
        self.edit_language = QLineEdit(dialog)
        self.edit_language.setText(libro_seleccionado['Idioma'])
        self.edit_copies = QLineEdit(dialog)
        self.edit_copies.setText(str(libro_seleccionado['Ejemplares']))
        self.edit_category = QComboBox(dialog)
        self.load_categories(self.edit_category)
        self.edit_category.setCurrentText(libro_seleccionado['Categoria'])
        self.edit_synopsis = QTextEdit(dialog)
        self.edit_synopsis.setText(libro_seleccionado['Sinopsis'])
        # QLabel para mostrar la imagen actual
        self.cover_label = QLabel(dialog)
        self.cover_label.setScaledContents(True)
        self.cover_label.setGeometry(0, 0, 200, 500)
        default_image_path = os.path.join(basedir, f"../media/librosCovers/{libro_seleccionado['ISBN']}/coverBook.png")
        self.mostrar_imagen_portada(default_image_path, self.cover_label.size())
        # QPushButton para permitir la selección de una nueva imagen
        choose_cover_button = QPushButton("Seleccionar Portada")
        choose_cover_button.setCursor(Qt.PointingHandCursor)
        choose_cover_button.clicked.connect(self.seleccionar_portada)



        form_layout.addRow("Título:", self.edit_title)
        form_layout.addRow("Autor:", self.edit_author)
        form_layout.addRow("Editorial:", self.edit_editorial)
        form_layout.addRow("ISBN:", self.edit_isbn)
        form_layout.addRow("Año de publicación:", self.edit_year)
        form_layout.addRow("Idioma:", self.edit_language)
        form_layout.addRow("Ejemplares:", self.edit_copies)
        form_layout.addRow("Categoría:", self.edit_category)
        form_layout.addRow("Sinopsis:", self.edit_synopsis)
        
        form_layout.addRow("Portada:", self.cover_label)
        form_layout.addRow("", choose_cover_button)  # Fila vacía para el botón
        
        layout.addLayout(form_layout)

        # Agregar botones de confirmar y cancelar
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Guardar")
        self.save_button.setCursor(Qt.PointingHandCursor)
        self.save_button.clicked.connect(lambda: self.guardar_edicion(libros_db, index, dialog))
        self.save_button.clicked.connect(lambda: self.window().actualizar_lista_libros())
        cancel_button = QPushButton("Cancelar")
        cancel_button.setStyleSheet(
            """
            background-color: #D12F2F;
            """
        )
        cancel_button.setCursor(Qt.PointingHandCursor)
        cancel_button.clicked.connect(dialog.reject)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

        # Mostrar la ventana de edición
        dialog.exec()

    def mostrar_imagen_portada(self, image_path, size):
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            reescaled_pixmap = pixmap.scaled(
                size.width() - 50, size.height() - 50, Qt.KeepAspectRatio)
            self.cover_label.setPixmap(reescaled_pixmap)
            self.cover_label.setAlignment(Qt.AlignCenter)
        else:
            print("La ruta de la imagen no es válida o la imagen no existe.")

    #seleccionar_portada(self, label, libro):
    def seleccionar_portada(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setNameFilter("Images (*.png *.jpg *.bmp)")
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)
        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                edit_image_path = selected_files[0]
                self.mostrar_imagen_portada(edit_image_path, self.imagen_label.size())
            else:
                # Si el usuario no selecciona ningún archivo, asigna la imagen predeterminada
                default_image_path = os.path.join(basedir, "../media/imgDefault/NO COVER.png")
                self.image_path = default_image_path

    def guardar_edicion(self, libros_db, index, dialog):
        isbn_code = self.edit_isbn.text()
        # Obtener los valores editados
        nuevo_titulo = self.edit_title.text()
        nuevo_autor = self.edit_author.text()
        nuevo_editorial = self.edit_editorial.text()
        nuevo_año = self.edit_year.text()
        nuevo_idioma = self.edit_language.text()
        nuevo_ejemplares = self.edit_copies.text()
        nueva_categoria = self.edit_category.currentText()
        nueva_sinopsis = self.edit_synopsis.toPlainText()
        # Obtener más valores editados según sea necesario

        directorio_imagen = os.path.join(basedir, f"../media/librosCovers/{isbn_code}")
        if not os.path.exists(directorio_imagen):
            os.makedirs(directorio_imagen)

        ruta_imagen = os.path.join(directorio_imagen, "coverBook.png")
        # Guardar la imagen
        if self.cover_label.pixmap():
            self.cover_label.pixmap().save(ruta_imagen)

        # Actualizar el libro en la lista
        libros_db[index]['Titulo'] = nuevo_titulo
        libros_db[index]['Autor'] = nuevo_autor
        libros_db[index]['Editorial'] = nuevo_editorial
        libros_db[index]['Año de publicacion'] = nuevo_año
        libros_db[index]['Idioma'] = nuevo_idioma
        libros_db[index]['Ejemplares'] = nuevo_ejemplares
        libros_db[index]['Categoria'] = nueva_categoria
        libros_db[index]['Sinopsis'] = nueva_sinopsis
        # Actualizar más campos según sea necesario

        # Cargar el contenido actual del archivo JSON
        with open(json_path, 'r', encoding="utf-8") as json_file:
            data = json.load(json_file)

        # Encontrar y actualizar el elemento específico
        for i, libro in enumerate(data['Libros']):
            if libro['ISBN'] == libros_db[index]['ISBN']:
                data['Libros'][i] = libros_db[index]
                break

        # Escribir los datos actualizados en el archivo JSON
        try:
            with open(json_path, 'w', encoding="utf-8") as json_file:
                json.dump(data, json_file, indent=2, ensure_ascii=False)
            #print("Datos actualizados y guardados en", json_path)
        except Exception as e:
            print("Error al guardar datos:", str(e))
        # Cerrar la ventana de edición

        dialog.accept()
        self.search_input.clear()
        self.actualizar_tabla(libros_db)

    def actualizar_tabla(self, libros_db):
        self.table_widget.setRowCount(len(libros_db))

        for i, libro in enumerate(libros_db):
            item_titulo = QTableWidgetItem(libro.get("Titulo", ""))

            # Conectar señales utilizando un bucle for fuera de la función lambda

            # Insertar elementos en la tabla
            self.table_widget.setItem(i, 0, item_titulo)

    def load_database_books(self):
        try:
            with open(json_path, "r", encoding="utf-8") as json_file:
                data = json.load(json_file)
                return data.get('Libros', [])
        except FileNotFoundError:
            return []

    def actualizar_base_de_datos(self, libros_db):
        with open(json_path, "w", encoding="utf-8") as json_file:
            json.dump({"Libros": libros_db}, json_file,
                      ensure_ascii=False, indent=2)

    def id_ISBN_esta_disponible(self, isbn):
        libros = self.load_database_books()
        for libro in libros:
            if libro["ISBN"] == isbn:
                return True  # Ya existe un libro con ese isbn
        return False  # No existe un usuario libro con ese isbn

    def verificarInt(self, ejemplares):
        try:
            int(ejemplares)
            return True
        except ValueError:
            return False

    def load_categories(self, label):
        json_path = os.path.join(os.path.dirname(
            __file__), "../databases/categorias.json")

        try:
            with open(json_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                categories = data.get("categorias_libros", [])
                for category_data in categories:
                    category = category_data.get("categoria", "")
                    if category:
                        label.addItem(category)
        except Exception as e:
            print(f"Error al cargar las categorías: {str(e)}")

    def actualizar_categorias_combobox(self):
        self.combobox_categoria.clear()
        self.combobox_categoria.addItem("Sin categoría")
        self.load_categories(self.combobox_categoria)

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
                image_path = selected_files[0]
                
                self.load_and_display_image(image_path, self.imagen_label.size())
            else:
                # Si el usuario no selecciona ningún archivo, asigna la imagen predeterminada
                default_image_path = os.path.join(os.path.dirname(__file__), "../media/imgDefault/NO COVER.png")
                self.image_path = default_image_path

    def load_and_display_image(self, image_path, size):
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            reescaled_pixmap = pixmap.scaled(
                size.width() - 50, size.height() - 50, Qt.KeepAspectRatio)
            self.imagen_label.setPixmap(reescaled_pixmap)
            self.imagen_label.setAlignment(Qt.AlignCenter)
        else:
            print("La ruta de la imagen no es válida o la imagen no existe.")

    def shadow_effect(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(5)  # Ajusta según tus preferencias
        shadow.setColor(Qt.black)
        shadow.setOffset(0, 0)

        return shadow


def main():
    app = QApplication(sys.argv)
    ui = Ui_RegisterBook()
    ui.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
