from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget

from PySide6 import QtWidgets, QtCore

from main_window import MainWindow

def handle_error(widget, handler):
    def inner(*args, **kwargs):
        try:
            handler(*args, **kwargs)
        except ValidationError as ex:
            QtWidgets.QMessageBox.critical(widget, 'Ошибка', str(ex))
    return inner

class Bookkeeper:
    """
    Класс для взаимодействия главного окна с bookkeeper. 
    Детали интерфейса описаны в классе MainWindow.
    Определены обработчики при работе с моделями.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        main_window = MainWindow()
        # main_window.some_method(...)

    def register_cat_modifier(
             self,
             handler: Callable[[Category], None]) -> None:
        self.cat_modifier = handle_error(self, handler)

    def register_cat_adder(
            self,
            handler: Callable[[Category], None]) -> None:
        self.cat_adder = handle_error(self, handler)

    def add_category(self):
        # получение данных из формочки
        # name = 
        # parent = 
        pass

    def delete_category(self):
        # cat = ... определить выбранную категорию
        # тут может быть отдельное окно, галочки, контекстное меню
        del_subcats, del_expenses = self.ask_del_cat()
        self.cat_deleter(cat, del_subcats,del_expenses)

    def add_expense_updater(self, callback):
        self.table.itemChanged.connect(self.on_table_change)
        self.expense_updater = callback

    def on_table_change(self, item):
        self.expense_updater(expense_from_item(item))