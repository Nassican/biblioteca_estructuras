from PySide6.QtWidgets import QApplication, QComboBox, QStyle
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtCore import Qt


class CustomComboBox(QComboBox):
    def __init__(self, parent=None):
        super(CustomComboBox, self).__init__(parent)
        self.setStyleSheet(
            "QComboBox {"
            "border-radius: 10px; "
            "padding: 5px; "
            "font-size: 15px; "
            "}"
            "QComboBox::drop-down {"
            "border: 0px; "
            "}"
            "QComboBox::down-arrow {"
            "image: url(:/arrow-down-combobox.png); "
            "width: 15px; "
            "height: 15px; "
            "}"
        )

    def paintEvent(self, event):
        painter = QPainter(self)
        option = QStyle.OptionComboBox()
        self.initStyleOption(option)

        # Dibujar la flecha personalizada aquí si es necesario

        self.style().drawComplexControl(QStyle.CC_ComboBox, option, painter, self)


def main():
    app = QApplication([])
    combo_box = CustomComboBox()
    combo_box.addItem("Opción 1")
    combo_box.addItem("Opción 2")
    combo_box.addItem("Opción 3")
    combo_box.show()
    app.exec()


if __name__ == "__main__":
    main()
