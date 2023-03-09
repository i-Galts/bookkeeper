import sys
from typing import Callable
from PySide6 import QtWidgets, QtCore, QtGui

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget

from bookkeeper.view.expenses_table import ExpensesTable, ExpensesListWidget
from bookkeeper.view.budget_widget import BudgetWidget
from bookkeeper.view.expenses_edit_panel import AmountEdit, CommentEdit, CategoryChoice

def handle_error(widget, handler):
    def inner(*args, **kwargs):
        try:
            handler(*args, **kwargs)
        except ValidationError as ex:
            QtWidgets.QMessageBox.critical(widget, 'Ошибка', str(ex))
    return inner

class BookkeeperMainWindow(QtWidgets.QMainWindow):
    """
    Класс главного окна. Детали интерфейса описаны
    в отдельных файлах для каждого виджета.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setWindowTitle("PyBookKeeper App")
        self.resize(800, 900)
        self.central_widget = QtWidgets.QTabWidget()
        self.setCentralWidget(self.central_widget)
        # to do: add tooltips for different widgets
        self.vertical_layout = QtWidgets.QVBoxLayout()

        self.create_menu()

        self.expenses_table_layout = QtWidgets.QStackedLayout()

        self.vertical_layout.addWidget(QtWidgets.QLabel("Последние расходы"))
        self.expenses_table = ExpensesTable([])
        self.expenses_table_layout.addWidget(self.expenses_table.create())

        self.amount_edit = AmountEdit()
        self.comment_edit = CommentEdit()

        # self.button_layout = QtWidgets.QHBoxLayout()

        # self.vertical_layout.addLayout(self.button_layout)
        self.vertical_layout.addLayout(self.expenses_table_layout)
        self.central_widget.setLayout(self.vertical_layout)

    def create_menu(self):
        self.file_menu = self.menuBar().addMenu("Файл")
        self.edit_menu = self.menuBar().addMenu("Редактировать")

        self.edit_category_action = QtGui.QAction("Правка категорий", self)
        self.edit_category_action.triggered.connect(self.edit_category_button_clicked)
        self.edit_menu.addAction(self.edit_category_action)

        self.edit_budget_action = QtGui.QAction("Правка бюджета", self)
        self.edit_menu.addAction(self.edit_budget_action)

        self.exit_action = QtGui.QAction("Закрыть", self)
        self.exit_action.triggered.connect(self.exit_app)
        self.file_menu.addAction(self.exit_action)

    @QtCore.Slot()
    def edit_expense_button_clicked(self):
        pass
    
    def refresh_expenses_table(self, exp_list: list[str]):
        self.expenses_table = ExpensesTable(exp_list)
        self.expenses_table_layout.addWidget(self.expenses_table.create())
        p = (self.expenses_table_layout.currentIndex() + 1) % self.expenses_table_layout.count()
        self.expenses_table_layout.setCurrentIndex(p)

    def create_delete_expense_button(self):
        self.delete_expense_button = QtWidgets.QPushButton("Удалить последнюю запись")
        self.vertical_layout.addWidget(self.delete_expense_button)
        self.delete_expense_button.clicked.connect(
                                                self.delete_expense_button_clicked)

    def create_budget_table(self):
        self.vertical_layout.addWidget(QtWidgets.QLabel("Бюджет"))
        self.budget_widget = BudgetWidget()
        data = [
            ['705.43', '1000'],
            ['6719.43', '7000'],
            ['10592.96', '30000']
        ]
        self.budget_widget.set_data(data)
        self.budget_widget.resize(300, 300)
        self.vertical_layout.addWidget(self.budget_widget.create())

    def create_expense_edit_panel(self):
        self.vertical_layout.addLayout(self.amount_edit.create())
        self.vertical_layout.addLayout(self.comment_edit.create())
        self.vertical_layout.addLayout(self.cat_choice.create())
        self.add_expense_button = QtWidgets.QPushButton("Добавить")
        self.vertical_layout.addWidget(self.add_expense_button)
        self.add_expense_button.clicked.connect(
                                    self.add_expense_button_clicked)

    def create(self):
        return self
    
    @QtCore.Slot()
    def exit_app(self):
        self.close()

    def set_category_list(self, cat_list: list[Category]) -> None:
        cat_to_str = [repr(cat) for cat in cat_list]
        self.cat_choice = CategoryChoice(cat_to_str)

    def set_expense_list(self, exp_list: list[Expense]) -> None:
        exp_to_str = [repr(exp).split(',') for exp in reversed(exp_list)]
        self.refresh_expenses_table(exp_to_str)

    def show_budget_widget(self) -> None:
        self.create_budget_table()

    @QtCore.Slot()
    def register_expense_adder(self,
                               handler: Callable[[int, str], None]):
        def add_expense_button_clicked():
            handler(self.amount_edit.get_amount(), 
                    self.cat_choice.get_category(),
                    self.comment_edit.get_comment())
        self.add_expense_button_clicked = add_expense_button_clicked

    def register_expense_deleter(self,
                                handler: Callable[[None], None]):
        def delete_expense_button_clicked():
            handler()
        self.delete_expense_button_clicked = delete_expense_button_clicked

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())