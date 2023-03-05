import sys
from PySide6 import QtWidgets

def widget_with_label(text, widget):
    hl = QtWidgets.QHBoxLayout()
    hl.addWidget(QtWidgets.QLabel(text))
    hl.addWidget(widget)
    return hl

class AmountEdit(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.amount_edit = widget_with_label(
            'Сумма',
            QtWidgets.QLineEdit('0')
        )

    def create(self) -> QtWidgets.QHBoxLayout:
        return self.amount_edit
    
class CategoryChoice(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.combobox = QtWidgets.QComboBox()
        self.combobox.addItem('Продукты')
        self.combobox.addItem('Кефир')
        self.combobox.addItem('Хлеб')
        self.combobox.addItem('Сыр')

        self.category_choice = widget_with_label(
            'Категория',
            self.combobox
        )

    def create(self) -> QtWidgets.QHBoxLayout:
        return self.category_choice

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    window.resize(300, 300)
    central_widget = QtWidgets.QTabWidget()
    window.setCentralWidget(central_widget)
    amount_edit = AmountEdit().create()
    category_choice = CategoryChoice().create()

    vertical_layout = QtWidgets.QVBoxLayout()
    vertical_layout.addLayout(amount_edit)
    vertical_layout.addLayout(category_choice)

    central_widget.setLayout(vertical_layout)
    window.show()

    sys.exit(app.exec())