import sys
from PySide6 import QtWidgets, QtCore, QtGui

from bookkeeper.view.expenses_table import ExpensesTable, ExpensesListWidget
from bookkeeper.view.budget_widget import BudgetWidget
from bookkeeper.view.edit_panel import AmountEdit, CategoryChoice

class BookkeeperMainWindow(QtWidgets.QMainWindow):
    """
    Класс главного окна. Детали интерфейса описаны
    в отдельных файлах для каждого виджета.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setWindowTitle("PyBookKeeper App")
        self.resize(500, 600)
        self.central_widget = QtWidgets.QTabWidget()
        self.setCentralWidget(self.central_widget)
        # to do: add tooltips for different widgets
        self.vertical_layout = QtWidgets.QVBoxLayout()

        # self.button_layout = QtWidgets.QHBoxLayout()
        # self.add_expense_button = QtWidgets.QPushButton("Добавить")
        # self.add_expense_button.clicked.connect(self.add_expense_button_clicked)
        # self.button_layout.addWidget(self.add_expense_button)

        # self.vertical_layout.addLayout(self.button_layout)
        self.central_widget.setLayout(self.vertical_layout)

    def create_menu(self):
        self.file_menu = self.menuBar().addMenu("Файл")
        self.edit_menu = self.menuBar().addMenu("Редактировать")

        self.edit_expenses_action = QtGui.QAction("Правка расходов", self)
        self.edit_expenses_action.triggered.connect(self.edit_expense_button_clicked)
        self.edit_menu.addAction(self.edit_expenses_action)

        self.edit_budget_action = QtGui.QAction("Правка бюджета", self)
        self.edit_menu.addAction(self.edit_budget_action)

        self.exit_action = QtGui.QAction("Закрыть", self)
        self.exit_action.triggered.connect(self.exit_app)
        self.file_menu.addAction(self.exit_action)

    @QtCore.Slot()
    def edit_expense_button_clicked(self):
        ExpensesListWidget()

    def create_expenses_table(self, cat_list: list[str]):
        self.vertical_layout.addWidget(QtWidgets.QLabel("Последние расходы"))
        self.expenses_table = ExpensesTable(cat_list)
        self.vertical_layout.addWidget(self.expenses_table.create())

    def create_budget_table(self):
        self.vertical_layout.addWidget(QtWidgets.QLabel("Бюджет"))
        self.vertical_layout.addLayout(CategoryChoice().create())
        self.budget_widget = BudgetWidget()
        data = [
            ['705.43', '1000'],
            ['6719.43', '7000'],
            ['10592.96', '30000']
        ]
        self.budget_widget.set_data(data)
        self.budget_widget.resize(300, 300)
        self.vertical_layout.addWidget(self.budget_widget.create())

    def create_amount_edit_widget(self):
        self.vertical_layout.addLayout(AmountEdit().create())

    def create_category_choice_widget(self):
         self.vertical_layout.addLayout(CategoryChoice().create())

    @QtCore.Slot()
    def add_expense_button_clicked(self):
        pass

    def create(self):
        return self
    
    @QtCore.Slot()
    def exit_app(self):
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())