"""
Модуль с классом главного окна приложения.
"""
from typing import Callable
from PySide6 import QtWidgets, QtCore, QtGui

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget
from bookkeeper.view.expenses_table import ExpensesTable
from bookkeeper.view.budget_widget import BudgetWidget
from bookkeeper.view.expenses_edit_panel import AmountEdit, CommentEdit, CategoryChoice
from bookkeeper.view.category_edit_window import EditCategoryWidget
from bookkeeper.view.budget_edit_window import EditBudgetWidget


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
        self.vertical_layout = QtWidgets.QVBoxLayout()

        self.create_menu()

        self.vertical_layout.addWidget(QtWidgets.QLabel("Последние расходы"))
        self.expenses_table_layout = QtWidgets.QStackedLayout()
        self.expenses_table = ExpensesTable([])
        self.expenses_table_layout.addWidget(self.expenses_table.create_table())
        self.vertical_layout.addLayout(self.expenses_table_layout)
        self.delete_expense_button = QtWidgets.QPushButton("Удалить последнюю запись")
        self.vertical_layout.addWidget(self.delete_expense_button)

        self.budget_layout = QtWidgets.QVBoxLayout()
        self.budget_layout.addWidget(QtWidgets.QLabel("Бюджет"))
        self.vertical_layout.addLayout(self.budget_layout)

        self.amount_edit = AmountEdit()
        self.comment_edit = CommentEdit()

        self.central_widget.setLayout(self.vertical_layout)

    def create_menu(self) -> None:
        """
        Создание панели меню в верхнем левом углу. Описаны
        кнопки закрытия приложения, редактирования списка
        категорий и таблицы бюджета. Само редактирование
        осуществляется в отдельных диалоговых окнах.
        """
        self.file_menu = self.menuBar().addMenu("Файл")
        self.edit_menu = self.menuBar().addMenu("Редактировать")

        self.edit_category_action = QtGui.QAction("Правка категорий", self)
        self.edit_category_action.setObjectName("edit_cats_action")
        self.edit_category_action.triggered.connect(self.edit_category_button_clicked)
        self.edit_menu.addAction(self.edit_category_action)

        self.edit_budget_action = QtGui.QAction("Правка бюджета", self)
        self.edit_budget_action.triggered.connect(self.edit_budget_button_clicked)
        self.edit_menu.addAction(self.edit_budget_action)

        self.exit_action = QtGui.QAction("Закрыть", self)
        self.exit_action.setObjectName("exit_action")
        self.exit_action.triggered.connect(self.exit_app)
        self.file_menu.addAction(self.exit_action)

        self.update_action = QtGui.QAction("Обновить", self)
        self.update_action.triggered.connect(self.update_app)
        self.file_menu.addAction(self.update_action)

    @QtCore.Slot()
    def edit_category_button_clicked(self) -> None:
        """
        Обработчик нажатия на кнопку "Правка категорий".
        Открывает диалоговое окно.
        """
        EditCategoryWidget(self.cat_list,
                           self.add_category_button_clicked,
                           self.delete_category_button_clicked).exec()

    @QtCore.Slot()
    def edit_budget_button_clicked(self) -> None:
        """
        Обработчик нажатия на кнопку "Правка категорий".
        Открывает диалоговое окно.
        """
        EditBudgetWidget(self.cat_list,
                         self.add_budget_button_clicked,
                         self.delete_budget_button_clicked).exec()

    def refresh_expenses_table(self, exp_list: list[list[str]]) -> None:
        """
        Принимает список расходов для перерисовки таблицы.
        """
        self.expenses_table = ExpensesTable(exp_list)
        self.expenses_table_layout.addWidget(
                            self.expenses_table.create_table())
        index = self.expenses_table_layout.currentIndex() + 1
        self.expenses_table_layout.setCurrentIndex(
                    index % self.expenses_table_layout.count())

    def create_delete_expense_button(self) -> None:
        self.delete_expense_button.clicked.connect(
                                                self.delete_expense_button_clicked)

    def create_budget_table(self) -> None:
        """
        Отрисовка таблицы с бюджетом.
        """
        self.budget_wid = BudgetWidget(self.cat_list, self.exp_list, self.bud_list)
        self.budget_layout.addLayout(self.budget_wid.create_cat_choice())
        self.stacked_bud_table = QtWidgets.QStackedLayout(parent=self.budget_layout)
        self.stacked_bud_table.addWidget(self.budget_wid.create_table())
        self.budget_layout.addLayout(self.stacked_bud_table)
        self.show_budget_button = QtWidgets.QPushButton("Показать бюджет")
        self.budget_layout.addWidget(self.show_budget_button)
        self.show_budget_button.clicked.connect(
                                self.show_budget_button_clicked)

    def show_budget_button_clicked(self) -> None:
        chosen_cat = self.budget_wid.cat_choice.get_category()
        self.budget_wid.fill_columns(chosen_cat)
        self.stacked_bud_table.addWidget(self.budget_wid.create_table())
        index = self.expenses_table_layout.currentIndex() + 1
        self.expenses_table_layout.setCurrentIndex(
                    index % self.expenses_table_layout.count())
        self.stacked_bud_table.setCurrentIndex(index)

    def create_expense_edit_panel(self) -> None:
        """
        Создание панели добавления записи о расходах.
        """
        self.vertical_layout.addLayout(self.amount_edit.create_edit())
        self.vertical_layout.addLayout(self.comment_edit.create_edit())
        self.cat_choice_panel = self.cat_choice.create_choice()
        self.vertical_layout.addLayout(self.cat_choice_panel)
        self.add_expense_button = QtWidgets.QPushButton("Добавить")
        self.vertical_layout.addWidget(self.add_expense_button)
        self.add_expense_button.clicked.connect(
                                    self.add_expense_button_clicked)

    def create_window(self) -> QtWidgets.QMainWindow:
        return self

    @QtCore.Slot()
    def update_app(self) -> None:
        """
        Кнопка меню для обновления главного окна приложения.
        После установки категорий и бюджета в отдельных
        диалоговых окнах нужно обновить главное окно для
        отображения внесенных данных.
        """
        for i in reversed(range(self.budget_layout.count())):
            try:
                self.budget_layout.itemAt(i).widget().deleteLater()
            except AttributeError:
                self.budget_layout.itemAt(i).layout().deleteLater()
        self.create_budget_table()

        self.vertical_layout.removeWidget(self.add_expense_button)
        self.vertical_layout.removeItem(self.cat_choice_panel)
        self.cat_choice_panel = self.cat_choice.create_choice()
        self.vertical_layout.addLayout(self.cat_choice_panel)
        self.vertical_layout.addWidget(self.add_expense_button)

    @QtCore.Slot()
    def exit_app(self) -> None:
        self.close()

    def set_category_list(self, cat_list: list[Category]) -> None:
        """
        Установка переданного списка категорий.
        """
        self.cat_list = [repr(cat) for cat in cat_list]
        self.cat_choice = CategoryChoice(self.cat_list)

    def set_expense_list(self, exp_list: list[Expense]) -> None:
        """
        Установка переданного списка расходов.
        """
        self.exp_list = [repr(exp).split(',') for exp in reversed(exp_list)]
        self.refresh_expenses_table(self.exp_list)

    def set_budget_list(self, bud_list: list[Budget]) -> None:
        """
        Установка переданного списка бюджета.
        """
        self.bud_list = [repr(bud) for bud in bud_list]
        for i in reversed(range(self.budget_layout.count())):
            try:
                self.budget_layout.itemAt(i).widget().deleteLater()
            except AttributeError:
                self.budget_layout.itemAt(i).layout().deleteLater()
        self.create_budget_table()

    @QtCore.Slot()
    def register_cat_adder(self,
                           handler: Callable[[str, str], None]) -> None:
        """
        Регистрация действий при нажатии
        на кнопку добавления категории. Принимает
        функцию из класса Bookkeeper.
        """
        self.add_category_button_clicked = handler

    @QtCore.Slot()
    def register_cat_deleter(self,
                             handler: Callable[[str], None]) -> None:
        """
        Регистрация действий при нажатии
        на кнопку удаления категории.
        """
        self.delete_category_button_clicked = handler

    @QtCore.Slot()
    def register_bud_adder(self,
                           handler: Callable[[str, str, str], None]) -> None:
        """
        Регистрация действий при нажатии
        на кнопку добавления бюджета.
        """
        self.add_budget_button_clicked = handler

    @QtCore.Slot()
    def register_bud_deleter(self,
                             handler: Callable[[str], None]) -> None:
        """
        Регистрация действий при нажатии
        на кнопку удаления категории.
        """
        self.delete_budget_button_clicked = handler

    @QtCore.Slot()
    def register_expense_adder(self,
                               handler: Callable[[int, str, str], None]) -> None:
        """
        Регистрация действий при нажатии
        на кнопку добавления записи о расходах.
        """
        def add_expense_button_clicked() -> None:
            handler(self.amount_edit.get_amount(),
                    self.cat_choice.get_category(),
                    self.comment_edit.get_comment())
        self.add_expense_button_clicked = add_expense_button_clicked

    @QtCore.Slot()
    def register_expense_deleter(self,
                                 handler: Callable[[None], None]) -> None:
        """
        Регистрация действий при нажатии
        на кнопку удаления записи о расходах.
        """
        def delete_expense_button_clicked() -> None:
            try:
                handler()
            except IndexError as ex:
                QtWidgets.QMessageBox.critical(self, 'Ошибка', str(ex))
        self.delete_expense_button_clicked = delete_expense_button_clicked
