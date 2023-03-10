from PySide6 import QtWidgets, QtCore
from typing import Callable
from functools import partial

class AddCategoryInput(QtWidgets.QWidget):
    def __init__(self, cat_list: list[str], 
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.hl = QtWidgets.QHBoxLayout()
        self.cat_name = QtWidgets.QLineEdit()
        self.cat_name.setPlaceholderText('Введите название')
        self.hl.addWidget(self.cat_name)

        self.parent_names = QtWidgets.QComboBox()
        self.parent_names.addItem('Выберите родителя')
        for cat in cat_list:
            self.parent_names.addItem(cat.split(',')[0].capitalize())
        self.parent_names.setCurrentIndex(0)
        self.hl.addWidget(self.parent_names)

    def get_cat_name(self) -> str:
        return self.cat_name.text() or ''
    
    def get_parent(self) -> str:
        cur_text = self.parent_names.currentText()
        if (cur_text == 'Выберите родителя'):
            return ''
        return cur_text
    
    def create(self) -> QtWidgets.QHBoxLayout:
        return self.hl

class EditCategoryWidget(QtWidgets.QDialog):
    def __init__(self, cat_list: list[str], 
                 signal_add_cat: Callable,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Редактировать список категорий")
        self.resize(700, 300)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)

        self.main_layout.addWidget(QtWidgets.QLabel("Добавление категории"))
        self.add_cat_wdt = AddCategoryInput(cat_list)
        self.main_layout.addLayout(self.add_cat_wdt.create())

        self.add_button = QtWidgets.QPushButton('Добавить')
        self.main_layout.addWidget(self.add_button)
        self.register_category_adder(signal_add_cat)
        self.add_button.clicked.connect(
                                self.add_category_button_clicked)

        self.exec()

    @QtCore.Slot()
    def register_category_adder(self,
                               handler: Callable[[int, str], None]):
        def add_category_button_clicked():
            handler(self.add_cat_wdt.get_cat_name(),
                    self.add_cat_wdt.get_parent())
        self.add_category_button_clicked = add_category_button_clicked



if __name__ == "__main__":
    cat_list = ['Молоко, 2', 'Хлеб, 1']
    add_cat = AddCategoryWidget()