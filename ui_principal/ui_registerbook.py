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
        path_to_img = os.path.join(os.path.dirname(__file__), "./media/img/arrow-down-combobox.png")
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
        button_editar = QPushButton("Editar Libro")
        button_editar.setCursor(Qt.PointingHandCursor)
        button_editar.setStyleSheet(
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
        form_botons.addWidget(button_añadir)
        form_botons.addWidget(button_editar)

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
        self.line_edit_idioma = QLineEdit()
        self.line_edit_idioma.setPlaceholderText("Idioma")
        self.line_edit_idioma.setEnabled(False)
        h_año_idioma.addWidget(self.line_edit_año)
        h_año_idioma.addWidget(self.line_edit_idioma)

        h_ejemplares_categoria = QHBoxLayout()
        self.line_edit_ejemplares = QLineEdit()
        self.line_edit_ejemplares.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.line_edit_ejemplares.setPlaceholderText("Ejemplares (*)")
        self.line_edit_ejemplares.setEnabled(False)
        self.line_edit_ejemplares.setValidator(QIntValidator())
        self.combobox_categoria = QComboBox()
        self.combobox_categoria.setCursor(Qt.PointingHandCursor)
        self.combobox_categoria.setEnabled(False)
        self.combobox_categoria.addItem("Sin categoría")
        self.load_categories()
        self.combobox_categoria.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        h_ejemplares_categoria.addWidget(self.line_edit_ejemplares)
        h_ejemplares_categoria.addWidget(self.combobox_categoria)

        self.line_edit_sinopsis = QTextEdit()
        self.line_edit_sinopsis.setPlaceholderText("Sinopsis")
        self.line_edit_sinopsis.wordWrapMode()
        self.line_edit_sinopsis.setAlignment(Qt.AlignTop)
        self.line_edit_sinopsis.setEnabled(False)
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
        h_important_buttons.setContentsMargins(5, 5, 5, 5)
        self.button_guardar = QPushButton("Guardar Libro / Cambios")
        self.button_guardar.setEnabled(False)
        self.button_guardar.clicked.connect(self.guardar_datos)
        self.button_guardar.setCursor(Qt.PointingHandCursor)
        self.button_guardar.setStyleSheet(
            "QPushButton {"
            "background-color: #75D181; color: white; font-weight: bold;"
            "}"
        )
        self.button_eliminar = QPushButton("Eliminar")
        self.button_eliminar.setCursor(Qt.PointingHandCursor)#D12F2F
        self.button_eliminar.setStyleSheet("background-color: #E38E8E; color: white; font-weight: bold;")
        self.button_eliminar.setEnabled(False)
        self.button_ver_prestamos = QPushButton("Ver Prestamos")
        self.button_ver_prestamos.setCursor(Qt.PointingHandCursor)
        self.button_añadir_categoria = QPushButton("Añadir Categoria")
        self.button_añadir_categoria.setCursor(Qt.PointingHandCursor)
        self.button_añadir_categoria.clicked.connect(self.añadir_categoria)

        h_important_buttons.addWidget(self.button_guardar)
        h_important_buttons.addWidget(self.button_eliminar)
        h_important_buttons.addWidget(self.button_ver_prestamos)
        h_important_buttons.addWidget(self.button_añadir_categoria)

        # Agregar un espacio elástico al final de central_layout
        central_layout.addWidget(form_container)
        central_layout.addLayout(h_important_buttons)

        self.setLayout(central_layout)

    def resizeEvent(self, event):
        # Llamamos a la función para cargar y mostrar la imagen con el tamaño actual
        if self.image_path:
            self.load_and_display_image(self.image_path, self.imagen_label.size())

    def añadir_categoria(self):
        categoria_widget = CategoriasWidget()
        categoria_widget.exec()
        self.actualizar_categorias_combobox()

    def añadir_libro(self):
        #Activar botones
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
        self.button_eliminar.setEnabled(True)
        self.button_eliminar.setStyleSheet(
            "QPushButton {"
            "background-color: #D12F2F; color: white; font-weight: bold;"
            "}"
            "QPushButton::hover {"
            "background-color: #E33E3E; "
            "}"
            "QPushButton:pressed {"
            "background-color: #D12F2F"
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

    def actualizar_categorias_combobox(self):
        self.combobox_categoria.clear()
        self.combobox_categoria.addItem("Sin categoría")
        self.load_categories()

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

    def load_and_display_image(self, image_path, size):
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            reescaled_pixmap = pixmap.scaled(size.width() - 50, size.height() - 50, Qt.KeepAspectRatio)
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