from PySide6 import QtWidgets, QtCore
from typing import Callable
from functools import partial

class EditCategoryWidget(QtWidgets.QDialog):
    def __init__(self, cat_list: list[str], 
                 signal_add_cat: Callable,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.signal_add_cat = signal_add_cat

        self.setWindowTitle("Редактировать список категорий")
        self.resize(700, 300)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)

        self.main_layout.addWidget(QtWidgets.QLabel("Добавление категории"))
        hl = QtWidgets.QHBoxLayout()
        self.cat_name = QtWidgets.QLineEdit()
        self.cat_name.setPlaceholderText('Введите название')
        hl.addWidget(self.cat_name)

        self.parent_names = QtWidgets.QComboBox()
        self.parent_names.addItem('Выберите родителя')
        for cat in cat_list:
            self.parent_names.addItem(cat.split(',')[0].capitalize())
        self.parent_names.setCurrentIndex(0)
        hl.addWidget(self.parent_names)
        self.main_layout.addLayout(hl)

        self.add_button = QtWidgets.QPushButton('Добавить')
        self.main_layout.addWidget(self.add_button)
        self.add_button.clicked.connect(
                        partial(self.signal_add_cat, 
                                self.cat_name.text(), self.parent_names.currentText()))

        # self.save_button = QtWidgets.QPushButton("Сохранить")
        # self.save_button.clicked.connect(self.save_editted)
        # self.main_layout.addWidget(self.save_button)

        print('olololo', self.cat_name.text(), self.parent_names.currentText())

        self.exec()

    @QtCore.Slot()
    def add_button_clicked_connect(self):
        return self.signal_add_cat



if __name__ == "__main__":
    cat_list = ['Молоко, 2', 'Хлеб, 1']
    add_cat = AddCategoryWidget()