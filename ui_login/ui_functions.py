import sys
from PySide6.QtWidgets import*
from PySide6.QtGui import*
from PySide6.QtCore import*
import sys
import os

def register(MiVentana):
    print("Funciona")
    nueva_ventana = QMainWindow(MiVentana)
    
    nueva_ventana.setWindowTitle("Ventana secundaria")

    # Crea un layout vertical y agrega widgets a él
    layout_vertical = QVBoxLayout()

    etiqueta = QLabel("¡Hola desde la nueva ventana creada en la función!")
    layout_vertical.addWidget(etiqueta)

    # Establece el layout en la ventana
    widget_principal = QWidget()
    widget_principal.setLayout(layout_vertical)
    nueva_ventana.setCentralWidget(widget_principal)

    nueva_ventana.show()  # Muestra la nueva ventana