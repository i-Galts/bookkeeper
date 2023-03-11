"""
Виджет диалогового окна для редактирования списка категорий.
"""
from typing import Callable
from PySide6 import QtWidgets, QtCore

# def catch_error(widget, handler):
#     def inner(*args, **kwargs):
#         try:
#             handler(*args, **kwargs)
#         except IndexError as ex:
#             QtWidgets.QMessageBox.critical(widget, 'Ошибка', str(ex))
#             return
#     return inner


class AddCategoryInput(QtWidgets.QWidget):
    """
    Класс, описывающий строку с добавлением новой категории.
    """
    def __init__(self, cat_list: list[str],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.horiz_layout = QtWidgets.QHBoxLayout()
        self.cat_name = QtWidgets.QLineEdit()
        self.cat_name.setPlaceholderText('Введите название')
        self.horiz_layout.addWidget(self.cat_name)

        self.parent_names = QtWidgets.QComboBox()
        self.parent_names.addItem('Выберите родителя')
        for cat in cat_list:
            self.parent_names.addItem(cat.split(',')[0].capitalize())
        self.parent_names.setCurrentIndex(0)
        self.horiz_layout.addWidget(self.parent_names)

    def get_cat_name(self) -> str:
        """
        Получение названия категории из формочки ввода.
        """
        return self.cat_name.text() or ''

    def get_parent(self) -> str:
        """
        Получение родительской категории из выпадающего списка.
        """
        cur_text = self.parent_names.currentText()
        if cur_text == 'Выберите родителя':
            return ''
        return cur_text

    def create_input(self) -> QtWidgets.QHBoxLayout:
        """
        Создание строки добавления категории.
        """
        return self.horiz_layout


class DeleteCategoryInput(QtWidgets.QWidget):
    """
    Класс, описывающий строку с удалением категории.
    """
    def __init__(self, cat_list: list[str],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.horiz_layout = QtWidgets.QHBoxLayout()
        self.cat_name = QtWidgets.QLineEdit()

        self.cat_names = QtWidgets.QComboBox()
        self.cat_names.addItem('Выберите категорию')
        for cat in cat_list:
            self.cat_names.addItem(cat.split(',')[0].capitalize())
        self.cat_names.setCurrentIndex(0)
        self.horiz_layout.addWidget(self.cat_names)

    def get_cat_name(self) -> str:
        """
        Получение названия категории из выпадающего списка.
        """
        cur_text = self.cat_names.currentText()
        if cur_text == 'Выберите категорию':
            return ''
        return cur_text

    def create_input(self) -> QtWidgets.QHBoxLayout:
        """
        Создание строки удаления категории.
        """
        return self.horiz_layout


class EditCategoryWidget(QtWidgets.QDialog):
    """
    Главный класс диалогового окна.
    """
    def __init__(self, cat_list: list[str],
                 signal_add_cat: Callable[[str, str], None],
                 signal_delete_cat: Callable[[None], None],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Редактировать список категорий")
        self.resize(700, 300)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)

        self.main_layout.addWidget(QtWidgets.QLabel("Добавление категории"))
        self.add_cat_wdt = AddCategoryInput(cat_list)
        self.main_layout.addLayout(self.add_cat_wdt.create_input())

        self.add_button = QtWidgets.QPushButton('Добавить')
        self.main_layout.addWidget(self.add_button)
        self.register_category_adder(signal_add_cat)
        self.add_button.clicked.connect(
                                self.add_category_button_clicked)

        self.main_layout.addWidget(QtWidgets.QLabel("Удаление категории"))
        self.del_cat_wdt = DeleteCategoryInput(cat_list)
        self.main_layout.addLayout(self.del_cat_wdt.create_input())

        self.delete_button = QtWidgets.QPushButton('Удалить')
        self.main_layout.addWidget(self.delete_button)
        self.register_category_deleter(signal_delete_cat)
        self.delete_button.clicked.connect(
                                self.delete_category_button_clicked)

        self.exec()

    @QtCore.Slot()
    def register_category_adder(self,
                                handler: Callable[[str, str], None]) -> None:
        """
        Принимает функцию, привязываемую к нажатию
        на кнопку добавления категории.
        """
        def add_category_button_clicked() -> None:
            try:
                handler(self.add_cat_wdt.get_cat_name(),
                        self.add_cat_wdt.get_parent())
            except IndexError as ex:
                QtWidgets.QMessageBox.critical(self, 'Ошибка', str(ex))
        self.add_category_button_clicked = add_category_button_clicked

    @QtCore.Slot()
    def register_category_deleter(self,
                                  handler: Callable[[None], None]) -> None:
        """
        Принимает функцию, привязываемую к нажатию
        на кнопку удаления категории.
        """
        def delete_category_button_clicked() -> None:
            try:
                handler()
            except IndexError as ex:
                QtWidgets.QMessageBox.critical(self, 'Ошибка', str(ex))
        self.delete_category_button_clicked = delete_category_button_clicked
