import sys
from PySide6 import QtWidgets, QtGui

def widget_with_label(text, widget) -> QtWidgets.QHBoxLayout:
    hl = QtWidgets.QHBoxLayout()
    hl.addWidget(QtWidgets.QLabel(text))
    hl.addWidget(widget)
    return hl

class AmountEdit(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.amount = QtWidgets.QLineEdit()
        self.amount.setPlaceholderText('0')
        self.amount.setValidator(QtGui.QDoubleValidator(0.0, 1.0E8, 2, self))

        self.layout = widget_with_label(
            'Сумма',
            self.amount
        )

    def create_edit(self):
        return self.layout
    
    def get_amount(self) -> str:
        return self.amount.text() or ''
    
class CommentEdit(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.comment_edit = QtWidgets.QLineEdit()
        self.comment_edit.setPlaceholderText('введите комментарий')

        self.layout = widget_with_label(
            'Комментарий',
            self.comment_edit
        )

    def create_edit(self):
        return self.layout
    
    def get_comment(self) -> str:
        return self.comment_edit.text() or ''
    
class CategoryChoice(QtWidgets.QWidget):
    def __init__(self, cat_list: list[str], *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.combobox = QtWidgets.QComboBox()
        for cat in cat_list:
            self.combobox.addItem(cat.split(',')[0].capitalize())

        self.category_choice = widget_with_label(
            'Категория',
            self.combobox
        )

    def create_choice(self) -> QtWidgets.QHBoxLayout:
        return self.category_choice
    
    def get_category(self) -> str:
        return self.combobox.currentText()
    
# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     window = QtWidgets.QMainWindow()
#     window.resize(300, 300)
#     central_widget = QtWidgets.QTabWidget()
#     window.setCentralWidget(central_widget)
#     amount_edit = AmountEdit().create()
#     category_choice = CategoryChoice().create()

#     vertical_layout = QtWidgets.QVBoxLayout()
#     vertical_layout.addLayout(amount_edit)
#     vertical_layout.addLayout(category_choice)

#     central_widget.setLayout(vertical_layout)
#     window.show()

#     sys.exit(app.exec())