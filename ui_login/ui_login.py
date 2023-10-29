import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QHBoxLayout
from PySide6.QtGui import QPixmap

class MiVentana(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Interfaz con PySide6")
        self.setGeometry(100, 100, 800, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout()

        # Mitad izquierda con una imagen
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        image_label = QLabel()
        #pixmap = QPixmap("./img/fondo1.jpg")  # Reemplaza "imagen.jpg" con la ruta de tu imagen
        #image_label.setPixmap(pixmap)
        left_layout.addWidget(image_label)
        left_widget.setLayout(left_layout)

        # Mitad derecha con varios elementos
        right_widget = QWidget()
        right_layout = QVBoxLayout()

        # Agrega los elementos que desees en la mitad derecha
        form_label = QLabel("Formulario Esteban:")
        name_input = QLineEdit()
        email_input = QLineEdit()
        submit_button = QPushButton("Enviar")
        result_text = QTextEdit()

        right_layout.addWidget(form_label)
        right_layout.addWidget(name_input)
        right_layout.addWidget(email_input)
        right_layout.addWidget(submit_button)
        right_layout.addWidget(result_text)
        right_widget.setLayout(right_layout)

        layout.addWidget(left_widget)
        layout.addWidget(right_widget)

        central_widget.setLayout(layout)

def main():
    app = QApplication(sys.argv)
    window = MiVentana()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
