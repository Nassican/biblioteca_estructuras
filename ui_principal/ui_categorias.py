from PySide6.QtWidgets import *
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
import json
import os

class NuevaCategoriaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nueva Categoría")

        self.layout = QVBoxLayout(self)

        self.label = QLabel("Nombre de la nueva categoría:", self)
        self.input_categoria = QLineEdit(self)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input_categoria)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        boton_aceptar = buttons.button(QDialogButtonBox.Ok)
        boton_aceptar.setText("Aceptar")
        buttons.rejected.connect(self.reject)
        boton_cancelar = buttons.button(QDialogButtonBox.Cancel)
        boton_cancelar.setText("Cancelar")


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

        self.layout.addWidget(buttons)

    def obtener_nombre_categoria(self):
        return self.input_categoria.text()

class ConfirmacionEliminarDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirmar Eliminación")
        self.setFixedHeight(100)

        self.layout = QVBoxLayout(self)

        self.label = QLabel("¿Estás seguro de que deseas eliminar esta categoría?", self)
        self.layout.addWidget(self.label)

        self.layout_botones = QHBoxLayout()

        self.boton_aceptar = QPushButton("Eliminar", self)
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

class EditarCategoriaDialog(QDialog):
    def __init__(self, categoria_actual, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Categoría")

        self.layout = QVBoxLayout(self)
        self.setFixedWidth(300)

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

        self.label = QLabel("Editar Categoría:", self)
        self.input_categoria = QLineEdit(self)
        self.input_categoria.setText(categoria_actual)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input_categoria)
        
        self.layout_botones = QHBoxLayout()

        self.boton_aceptar = QPushButton("Aceptar", self)
        self.boton_aceptar.setCursor(Qt.PointingHandCursor)
        self.boton_aceptar.setStyleSheet("background-color: #067A14;")
        self.boton_cancelar = QPushButton("Cancelar", self)
        self.boton_cancelar.setCursor(Qt.PointingHandCursor)

        self.boton_aceptar.clicked.connect(self.accept)
        self.boton_cancelar.clicked.connect(self.reject)

        self.layout_botones.addWidget(self.boton_aceptar)
        self.layout_botones.addWidget(self.boton_cancelar)

        self.layout.addLayout(self.layout_botones)

    def obtener_nueva_categoria(self):
        return self.input_categoria.text()

class CategoriasWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Categorías")
        self.setStyleSheet("background-color: white;")
        self.path_to_icon = os.path.join(os.path.dirname(__file__), "../media/img/libro.png")
        self.setWindowIcon(QIcon(self.path_to_icon))
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        self.setFixedWidth(400)
        # Cargar datos desde el JSON
        path_to_json = os.path.join(os.path.dirname(__file__), "../databases/categorias.json")
        with open(path_to_json, 'r', encoding='utf-8') as file:
            self.datos = json.load(file)

        # Crear una tabla con 2 columnas (categoria, acciones)
        self.tabla = QTableWidget(self)
        self.tabla.setColumnCount(3)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.horizontalHeader().setVisible(False)
        self.tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.setSelectionMode(QTableWidget.NoSelection)
        self.tabla.setShowGrid(False)
        self.tabla.setFocusPolicy(Qt.NoFocus)
        self.tabla.setAlternatingRowColors(True)
        self.tabla.resizeColumnsToContents()


        self.boton_nuevo = QPushButton("Nuevo", self)
        self.boton_nuevo.clicked.connect(self.agregar_nueva_categoria)
        self.boton_nuevo.setCursor(Qt.PointingHandCursor)
        self.boton_nuevo.setStyleSheet(
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

        # Crear una barra de búsqueda
        self.barra_busqueda = QLineEdit(self)
        self.barra_busqueda.setPlaceholderText("Buscar categoría...")
        self.barra_busqueda.textChanged.connect(self.filtrar_tabla)
        self.barra_busqueda.setStyleSheet(
            "QLineEdit {"
            "border: 1px solid #2F53D1; "
            "border-radius: 5px; "
            "padding: 5px; "
            "font-size: 15px; "
            "}"
        )

        self.barra_categorias = QHBoxLayout()
        self.barra_categorias.addWidget(self.boton_nuevo)
        self.barra_categorias.addWidget(self.barra_busqueda)


        # Llenar la tabla con datos del JSON
        self.actualizar_tabla()

        # Diseñar la interfaz
        layout = QVBoxLayout(self)
        layout.addLayout(self.barra_categorias)
        layout.addWidget(self.tabla)
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
            QTableWidget {
                border: 1px solid #2F53D1;
                border-radius: 5px;
                font-size: 15px;
                padding: 5px;
            }
            QTableWidget:item {
               background-color: white;
            }
            QTableWidget:item:alternate {
               background-color: #EEEEEE;
            }
        """)

    def actualizar_tabla(self):
        self.tabla.setRowCount(len(self.datos["categorias_libros"]))

        for i, categoria in enumerate(self.datos["categorias_libros"]):
            item_categoria = QTableWidgetItem(categoria.get("categoria", ""))

            # Crear botones para cada fila
            path_to_icon_editar = os.path.join(os.path.dirname(__file__), "../media/img/editar-icon.png")
            boton_editar = QPushButton("", self)
            boton_editar.setFixedSize(30, 30)
            boton_editar.setIcon(QIcon(path_to_icon_editar))
            boton_editar.setCursor(Qt.PointingHandCursor)
            boton_editar.setStyleSheet(
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
            path_to_icon_eliminar = os.path.join(os.path.dirname(__file__), "../media/img/basura_icon.png")
            boton_eliminar = QPushButton("", self)
            boton_eliminar.setIcon(QIcon(path_to_icon_eliminar))
            boton_eliminar.setFixedSize(30, 30)
            boton_eliminar.setCursor(Qt.PointingHandCursor)
            boton_eliminar.setStyleSheet(
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

            # Conectar señales utilizando un bucle for fuera de la función lambda
            boton_editar.clicked.connect(self.crear_funcion_editar(i))
            boton_eliminar.clicked.connect(self.crear_funcion_eliminar(i))

            # Insertar elementos en la tabla
            self.tabla.setItem(i, 0, item_categoria)
            self.tabla.setCellWidget(i, 1, boton_editar)
            self.tabla.setCellWidget(i, 2, boton_eliminar)

        self.tabla.sortByColumn(0, Qt.AscendingOrder)

    def filtrar_tabla(self):
        texto_busqueda = self.barra_busqueda.text().lower()
        for fila in range(self.tabla.rowCount()):
            texto_fila = self.tabla.item(fila, 0).text().lower()
            self.tabla.setRowHidden(fila, texto_busqueda not in texto_fila)

    def crear_funcion_editar(self, fila_visible):
        def editar():
            # Obtener la categoría directamente de la fila visible
            categoria_actual = self.datos["categorias_libros"][fila_visible]["categoria"]
            dialogo = EditarCategoriaDialog(categoria_actual, self)
            if dialogo.exec():
                nueva_categoria = dialogo.obtener_nueva_categoria()

                # Verificar si la nueva categoría ya existe (excluyendo la categoría actual)
                categorias_existentes = [categoria["categoria"] for i, categoria in enumerate(self.datos["categorias_libros"]) if i != fila_visible]
                if nueva_categoria in categorias_existentes:
                    mensaje = QMessageBox()
                    mensaje.setWindowIcon(QIcon(self.path_to_icon))
                    mensaje.setWindowTitle("Advertencia")
                    mensaje.setText("La categoría ya existe.")
                    mensaje.setIcon(QMessageBox.Warning)
                    boton_aceptar = QPushButton("Aceptar")
                    mensaje.addButton(boton_aceptar, QMessageBox.AcceptRole)
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
                    mensaje.exec()
                else:
                    # Realizar la edición
                    self.datos["categorias_libros"][fila_visible]["categoria"] = nueva_categoria
                    self.actualizar_tabla()
                    self.guardar_en_archivo()

        return editar

    def crear_funcion_eliminar(self, fila):
        def eliminar():
            dialogo_confirmacion = ConfirmacionEliminarDialog(self)
            if dialogo_confirmacion.exec() == QDialog.Accepted:
                del self.datos["categorias_libros"][fila]
                self.actualizar_tabla()
                self.guardar_en_archivo()

        return eliminar

    def agregar_nueva_categoria(self):
        dialogo_nueva_categoria = NuevaCategoriaDialog(self)
        if dialogo_nueva_categoria.exec():
            nueva_categoria = dialogo_nueva_categoria.obtener_nombre_categoria()

            # Verificar si la categoría ya existe
            if any(categoria["categoria"] == nueva_categoria for categoria in self.datos["categorias_libros"]):
                mensaje = QMessageBox()
                mensaje.setWindowIcon(QIcon(self.path_to_icon))
                mensaje.setWindowTitle("Advertencia")
                mensaje.setText("La categoría ya existe.")
                mensaje.setIcon(QMessageBox.Warning)
                boton_aceptar = QPushButton("Aceptar")
                mensaje.addButton(boton_aceptar, QMessageBox.AcceptRole)
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
                mensaje.exec()
            else:
                # Agregar la nueva categoría al JSON
                self.datos["categorias_libros"].append({"categoria": nueva_categoria})
                self.actualizar_tabla()
                self.guardar_en_archivo()

    def guardar_en_archivo(self):
        path_to_json = os.path.join(os.path.dirname(__file__), "../databases/categorias.json")
        with open(path_to_json, 'w', encoding='utf-8') as file:
            json.dump(self.datos, file, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    app = QApplication([])
    ventana = CategoriasWidget()
    ventana.show()
    app.exec()
