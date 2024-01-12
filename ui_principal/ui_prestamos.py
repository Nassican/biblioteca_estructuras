import sys
from PySide6.QtWidgets import *

class Ui_Prestamos_admin(QWidget):
    def __init__(self):
        super().__init__()
        # Pal commit diario
        # Establece la ventana principal como un cuadrado
        self.setGeometry(100, 100, 600, 500)  # Ajusta el tamaño según sea necesario
        self.setWindowTitle("Mi Aplicación")  # Cambia el título de la ventana

        # Crea la etiqueta del título
        titulo_prestamos = QLabel("Prestamos Administrador", self)
        titulo_prestamos.setStyleSheet("text-align: left; font-weight: bold;")
        label_vacio=QLabel()

        # Crea los botones
        boton_ver_usuario = QPushButton("Ver por usuario", self)
        boton_ver_libro = QPushButton("Ver por libro", self)
        line_edit_buscar = QLineEdit(self)
        line_edit_buscar.setPlaceholderText("Buscar por nombre")

        # layout botones
        layout_botones = QHBoxLayout()
        layout_botones.addWidget(titulo_prestamos)
        layout_botones.addWidget(boton_ver_usuario)
        layout_botones.addWidget(boton_ver_libro)

        #boton buscar añadir
        layout_botones_buscar = QHBoxLayout()
        layout_botones_buscar.addWidget(label_vacio)
        layout_botones_buscar.addWidget(label_vacio)
        layout_botones_buscar.addWidget(line_edit_buscar)

        # TABLA
        self.tabla = QTableWidget(self)
        self.tabla.setGeometry(10, 90, 280, 200)  #tamaño table
        self.tabla.setColumnCount(3)  #columnas
        self.tabla.setHorizontalHeaderLabels(["titulo", "fechaing", "fechafinal"])  #names items

        # Agrega datos a la tabla (puedes modificar esto según tus necesidades)
        data = {"titulo": ["1", "2", "3"], "fechaing": ["4", "5", "6"], "fechafinal": ["7", "8", "9"]}
        for row, key in enumerate(sorted(data.keys())):
            for col, item in enumerate(data[key]):
                self.tabla.setItem(row, col, QTableWidgetItem(item))

        #estilos aqui
        self.tabla.setStyleSheet("QTableWidget {border-radius: 10px; border: 2px solid gray;} QTableCornerButton::section {border-radius: 10px;}")

        # layout principal
        layout_principal = QVBoxLayout(self)
        layout_principal.addLayout(layout_botones)
        layout_principal.addLayout(layout_botones_buscar)
        layout_principal.addWidget(self.tabla)

        # Establece el diseño principal para la ventana
        self.setLayout(layout_principal)

class Ui_Prestamos_user(QWidget):
    def __init__(self, parent, user_data):
        super(Ui_Prestamos_user, self).__init__()
        self.user_data = user_data
        self.parent = parent
        # Pal commit diario
        # Establece la ventana principal como un cuadrado
        self.setGeometry(100, 100, 600, 500)  # Ajusta el tamaño según sea necesario
        self.setWindowTitle("Mi Aplicación")  # Cambia el título de la ventana

        # Crea la etiqueta del título
        titulo_prestamos = QLabel("Prestamos Usuario", self)
        titulo_prestamos.setStyleSheet("text-align: left; font-weight: bold;")
        label_vacio=QLabel()

        # Crea los botones
        boton_ver_usuario = QPushButton("Ver por usuario", self)
        boton_ver_libro = QPushButton("Ver por libro", self)
        line_edit_buscar = QLineEdit(self)
        line_edit_buscar.setPlaceholderText("Buscar por nombre")

        # layout botones
        layout_botones = QHBoxLayout()
        layout_botones.addWidget(titulo_prestamos)
        layout_botones.addWidget(boton_ver_usuario)
        layout_botones.addWidget(boton_ver_libro)

        #boton buscar añadir
        layout_botones_buscar = QHBoxLayout()
        layout_botones_buscar.addWidget(label_vacio)
        layout_botones_buscar.addWidget(label_vacio)
        layout_botones_buscar.addWidget(line_edit_buscar)

        # TABLA
        self.tabla = QTableWidget(self)
        self.tabla.setGeometry(10, 90, 280, 200)  #tamaño table
        self.tabla.setColumnCount(3)  #columnas
        self.tabla.setHorizontalHeaderLabels(["titulo", "fechaing", "fechafinal"])  #names items

        # Agrega datos a la tabla (puedes modificar esto según tus necesidades)
        data = {"titulo": ["1", "2", "3"], "fechaing": ["4", "5", "6"], "fechafinal": ["7", "8", "9"]}
        for row, key in enumerate(sorted(data.keys())):
            for col, item in enumerate(data[key]):
                self.tabla.setItem(row, col, QTableWidgetItem(item))

        #estilos aqui
        self.tabla.setStyleSheet("QTableWidget {border-radius: 10px; border: 2px solid gray;} QTableCornerButton::section {border-radius: 10px;}")

        # layout principal
        layout_principal = QVBoxLayout(self)
        layout_principal.addLayout(layout_botones)
        layout_principal.addLayout(layout_botones_buscar)
        layout_principal.addWidget(self.tabla)

        # Establece el diseño principal para la ventana
        self.setLayout(layout_principal)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = Ui_Prestamos_admin()
    ventana.show()
    sys.exit(app.exec())
