from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget

from PySide6 import QtWidgets, QtCore

from bookkeeper.view.expenses_table import ExpensesTable
from bookkeeper.view.budget_widget import BudgetWidget

def handle_error(widget, handler):
    def inner(*args, **kwargs):
        try:
            handler(*args, **kwargs)
        except ValidationError as ex:
            QtWidgets.QMessageBox.critical(widget, 'Ошибка', str(ex))
    return inner

class MainWindow(QtWidgets.QMainWindow):
    """
    Класс главного окна. Детали интерфейса описаны
    в отдельных файлах для каждого виджета.
    Определены обработчики при работе с моделями.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setWindowTitle("PyBookKeeper App")

        self.vertical_layout = QtWidgets.QVBoxLayout()

        self.expenses_label = QtWidgets.QLabel("Последние расходы")
        self.vertical_layout.addWidget(self.expenses_label)
        self.expenses_table = ExpensesTable()
        self.vertical_layout.addWidget(self.expenses_table)
        # if user changes smth in expenses table,
        # it will call method set_data from a given list
        # then expenses_table must be reloaded

        self.budget_label = QtWidgets.QLabel("Бюджет")
        self.vertical_layout.addWidget(self.budget_label)
        self.budget_widget = BudgetWidget()
        self.vertical_layout.addWidget(self.budget_widget)

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