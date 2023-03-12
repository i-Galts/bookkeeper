"""
Виджет диалогового окна для редактирования бюджета.
"""
from typing import Callable
from PySide6 import QtWidgets, QtCore


class AddBudgetInput(QtWidgets.QWidget):
    """
    Класс, описывающий строку с добавлением нового бюджета.
    """
    def __init__(self, cat_list: list[str],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.horiz_layout = QtWidgets.QHBoxLayout()

        self.cat_names = QtWidgets.QComboBox()
        self.cat_names.addItem('Выберите категорию')
        for cat in cat_list:
            self.cat_names.addItem(cat.split(',')[0].capitalize())
        self.cat_names.setCurrentIndex(0)
        self.horiz_layout.addWidget(self.cat_names)

        self.period = QtWidgets.QLineEdit()
        self.period.setPlaceholderText('Введите период')
        self.horiz_layout.addWidget(self.period)

        self.amount = QtWidgets.QLineEdit()
        self.amount.setPlaceholderText('Введите сумму')
        self.horiz_layout.addWidget(self.amount)

    def get_cat_name(self) -> str:
        """
        Получение названия категории из выпадающего списка.
        """
        cur_text = self.cat_names.currentText()
        if cur_text == 'Выберите категорию':
            return ''
        return cur_text

    def get_period(self) -> str:
        """
        Получение периода из формочки ввода.
        """
        return self.period.text() or ''

    def get_amount(self) -> str:
        """
        Получение суммы из формочки ввода.
        """
        return self.amount.text() or ''

    def create_input(self) -> QtWidgets.QHBoxLayout:
        """
        Создание строки добавления бюджета.
        """
        return self.horiz_layout


class DeleteCategoryInput(QtWidgets.QWidget):
    """
    Класс, описывающий строку с удалением бюджета.
    """
    def __init__(self, cat_list: list[str],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.horiz_layout = QtWidgets.QHBoxLayout()

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
        Создание строки удаления бюджета.
        """
        return self.horiz_layout


class EditBudgetWidget(QtWidgets.QDialog):
    """
    Главный класс диалогового окна.
    """
    def __init__(self, cat_list: list[str],
                 signal_add_bud: Callable[[str, str, str], None],
                 signal_delete_bud: Callable[[str], None],
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle("Редактировать бюджет")
        self.resize(700, 300)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)

        self.main_layout.addWidget(QtWidgets.QLabel("Добавление бюджета"))
        self.add_bud_wdt = AddBudgetInput(cat_list)
        self.main_layout.addLayout(self.add_bud_wdt.create_input())

        self.add_button = QtWidgets.QPushButton('Добавить')
        self.main_layout.addWidget(self.add_button)
        self.register_budget_adder(signal_add_bud)
        self.add_button.clicked.connect(
                                self.add_budget_button_clicked)

        self.main_layout.addWidget(QtWidgets.QLabel("Удаление бюджета"))
        self.del_bud_wdt = DeleteCategoryInput(cat_list)
        self.main_layout.addLayout(self.del_bud_wdt.create_input())

        self.delete_button = QtWidgets.QPushButton('Удалить')
        self.main_layout.addWidget(self.delete_button)
        self.register_budget_deleter(signal_delete_bud)
        self.delete_button.clicked.connect(
                                self.delete_budget_button_clicked)

    @QtCore.Slot()
    def register_budget_adder(self,
                              handler: Callable[[str, str, str], None]) -> None:
        """
        Принимает функцию, привязываемую к нажатию
        на кнопку добавления бюджета.
        """
        def add_budget_button_clicked() -> None:
            try:
                handler(self.add_bud_wdt.get_cat_name(),
                        self.add_bud_wdt.get_period(),
                        self.add_bud_wdt.get_amount())
            except IndexError as ex:
                QtWidgets.QMessageBox.critical(self, 'Ошибка', str(ex))
        self.add_budget_button_clicked = add_budget_button_clicked

    @QtCore.Slot()
    def register_budget_deleter(self,
                                handler: Callable[[str], None]) -> None:
        """
        Принимает функцию, привязываемую к нажатию
        на кнопку удаления бюджета.
        """
        def delete_budget_button_clicked() -> None:
            try:
                handler(self.del_bud_wdt.get_cat_name())
            except IndexError as ex:
                QtWidgets.QMessageBox.critical(self, 'Ошибка', str(ex))
        self.delete_budget_button_clicked = delete_budget_button_clicked
