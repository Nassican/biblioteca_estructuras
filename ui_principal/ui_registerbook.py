import os
import sys
import shutil
import json

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

json_path = os.path.join(os.path.dirname(__file__), "../databases/libros_db.json")

class MessageWidget(QMessageBox):
    def __init__(self):
        super(MessageWidget, self).__init__()
        self.setWindowTitle("Biblioteca SoftPro - Imagen de perfil")
        self.button_message = QPushButton("Aceptar")
        self.button_message.setCursor(Qt.PointingHandCursor)
        self.addButton(self.button_message, QMessageBox.AcceptRole)
        self.setIcon(QMessageBox.Critical)
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "../media/img/libro.png")))
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

        central_layout = QVBoxLayout()
        # Title
        form_container = QWidget()
        form_container.setContentsMargins(0, 0, 0, 0)
        form_layout = QHBoxLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)

        form_container_left_side = QWidget()
        form_left_side = QVBoxLayout()
        form_left_side.setContentsMargins(0, 0, 0, 0)
        form_container_right_side = QWidget()
        form_right_side = QVBoxLayout()
        form_right_side.setContentsMargins(0, 0, 0, 0)

        form_botons = QHBoxLayout()
        form_botons.setContentsMargins(0, 0, 0, 0)
        button_añadir = QPushButton("Añadir Nuevo Libro")
        button_editar = QPushButton("Editar Libro")
        form_botons.addWidget(button_añadir)
        form_botons.addWidget(button_editar)

        self.imagen_label = QLabel()
        button_escoger_imagen = QPushButton("Escoger Imagen Libro")
        button_escoger_imagen.setCursor(Qt.PointingHandCursor)
        button_escoger_imagen.clicked.connect(self.select_image)

        form_left_side.addLayout(form_botons)
        form_left_side.addWidget(self.imagen_label)
        form_left_side.addWidget(button_escoger_imagen)
        form_container_left_side.setLayout(form_left_side)

        self.line_edit_titulo = QLineEdit()
        self.line_edit_titulo.setPlaceholderText("Titulo (*)")
        self.line_edit_autor = QLineEdit()
        self.line_edit_autor.setPlaceholderText("Autor (*)")
        self.line_edit_editorial = QLineEdit()
        self.line_edit_editorial.setPlaceholderText("Editorial (*)")
        self.line_edit_isbn = QLineEdit()
        self.line_edit_isbn.setPlaceholderText("ISBN (*)")

        h_año_idioma = QHBoxLayout()
        self.line_edit_año = QLineEdit()
        self.line_edit_año.setPlaceholderText("Año de publicación")
        self.line_edit_idioma = QLineEdit()
        self.line_edit_idioma.setPlaceholderText("Idioma")
        h_año_idioma.addWidget(self.line_edit_año)
        h_año_idioma.addWidget(self.line_edit_idioma)

        h_ejemplares_categoria = QHBoxLayout()
        self.line_edit_ejemplares = QLineEdit()
        self.line_edit_ejemplares.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.line_edit_ejemplares.setPlaceholderText("Ejemplares (*)")
        self.combobox_categoria = QComboBox()
        self.combobox_categoria.addItem("Sin categoría")
        self.load_categories()
        self.combobox_categoria.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        h_ejemplares_categoria.addWidget(self.line_edit_ejemplares)
        h_ejemplares_categoria.addWidget(self.combobox_categoria)

        self.line_edit_sinopsis = QLineEdit()
        self.line_edit_sinopsis.setPlaceholderText("Sinopsis")
        self.line_edit_sinopsis.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

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
        form_container_left_side.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        form_layout.addWidget(form_container_right_side)

        form_container.setLayout(form_layout)

        h_important_buttons = QHBoxLayout()
        button_guardar = QPushButton("Guardar Libro / Cambios")
        button_guardar.clicked.connect(self.guardar_datos)
        button_eliminar = QPushButton("Eliminar")
        button_ver_prestamos = QPushButton("Ver Prestamos")
        button_añadir_categoria = QPushButton("Añadir Categoria")

        h_important_buttons.addWidget(button_guardar)
        h_important_buttons.addWidget(button_eliminar)
        h_important_buttons.addWidget(button_ver_prestamos)
        h_important_buttons.addWidget(button_añadir_categoria)

        # Agregar un espacio elástico al final de central_layout
        central_layout.addWidget(form_container)
        central_layout.addLayout(h_important_buttons)

        self.setLayout(central_layout)

    def guardar_datos(self):
        titulo = self.line_edit_titulo.text()
        autor = self.line_edit_autor.text()
        editorial = self.line_edit_editorial.text()
        isbn = self.line_edit_isbn.text()
        año = self.line_edit_año.text()
        idioma = self.line_edit_idioma.text()
        ejemplares = self.line_edit_ejemplares.text()
        categoria = self.combobox_categoria.currentText()
        sinopsis = self.line_edit_sinopsis.text()

        directorio_imagen = os.path.join(os.path.dirname(__file__), f"../media/librosCovers/{isbn}")
        if not os.path.exists(directorio_imagen):
            os.makedirs(directorio_imagen)

        # Crear la ruta completa de la imagen
        ruta_imagen = os.path.join(directorio_imagen, "coverBook.png")

        # Guardar la imagen
        if self.imagen_label.pixmap():
            self.imagen_label.pixmap().save(ruta_imagen)

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

        libros_db = self.load_database_books()
        libros_db.append(new_book)
        self.actualizar_base_de_datos(libros_db)

        self.message = MessageWidget()
        self.message.setText("Libro guardado con éxito")
        self.message.setIcon(QMessageBox.Information)
        self.message.exec()

    def load_database_books(self):
        try:
          with open(json_path, "r", encoding="utf-8") as json_file:
            data = json.load(json_file)
            return data.get('Libros', [])
        except FileNotFoundError:
          return []
    
    def actualizar_base_de_datos(self, libros_db):
        with open(json_path, "w", encoding="utf-8") as json_file:
          json.dump({"Libros": libros_db}, json_file, ensure_ascii=False, indent=2)
    
    
    def load_categories(self):
        json_path = os.path.join(os.path.dirname(__file__), "../databases/categorias.json")

        try:
            with open(json_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                categories = data.get("categorias_libros", [])
                for category_data in categories:
                    category = category_data.get("categoria", "")
                    if category:
                        self.combobox_categoria.addItem(category)
        except Exception as e:
            print(f"Error al cargar las categorías: {str(e)}")

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
                self.load_and_display_image(image_path)

    def load_and_display_image(self, image_path):
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(
                self.imagen_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.imagen_label.setPixmap(scaled_pixmap)
            self.imagen_label.setAlignment(Qt.AlignCenter)
            #self.imagen_label.setScaledContents(True)  # Hace que la imagen se adapte al tamaño de QLabel
        else:
            print("La ruta de la imagen no es válida o la imagen no existe.")

def main():
    app = QApplication(sys.argv)
    ui = Ui_RegisterBook()
    ui.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()