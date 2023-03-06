import sys

from bookkeeper.models.category import Category
# from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget

from PySide6 import QtWidgets, QtCore

from bookkeeper.view.main_window import BookkeeperMainWindow

from typing import Protocol

# У MainView должны быть реализованы эти методы!
class AbstractView(Protocol):
    def set_category_list(lst: list[Category]) -> None:
        pass

    def show_budget_widget() -> None:
        pass

    def show_amount_edit_widget() -> None:
        pass

    def show_category_choice_widget() -> None:
        pass

class BookkeeperMainView:
    def __init__(self, 
                 window: BookkeeperMainWindow):
        self.window = window

    def set_category_list(self, lst: list[Category]) -> None:
        #cat_to_str = [str(cat) for cat in lst.split()]
        self.window.create_expenses_table(lst)

    def show_budget_widget(self) -> None:
        self.window.create_budget_table()

    def show_amount_edit_widget(self) -> None:
        self.window.create_amount_edit_widget()

    def show_category_choice_widget(self) -> None:
        self.window.create_category_choice_widget()

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
    def __init__(self, 
                 view: AbstractView): # с каким отображением будем работать
                 #repo_factory) -> None: # repo - идея, чтобы не передавать какой-то конкретный репо

        self.view = view
        # self.category_repository = \
        #         repo_factory.get(Category) # т.е. нужен спец. метод этого класса repo_factory
        # self.cats = self.category_repository.get_all()
        self.cats = [
            ['2023-01-09 15:09:00', '7.49', 'Хозтовары', 'Пакет на кассе'],
            ['2023-01-09 15:09:00', '104.99', 'Кефир', 'Длинное-предлинное сообщение']
        ]
        self.view.set_category_list(self.cats)
        self.view.show_budget_widget()
        self.view.show_amount_edit_widget()
        self.view.show_category_choice_widget()

    # def provide_with_category_list(self):
    #     # take from repo...
    #     # self.category_repository = \
    #     #         repo_factory.get(Category) # т.е. нужен спец. метод этого класса repo_factory
    #     # self.cats = self.category_repository.get_all()
    #     self.cats = [
    #         ['2023-01-09 15:09:00', '7.49', 'Хозтовары', 'Пакет на кассе'],
    #         ['2023-01-09 15:09:00', '104.99', 'Кефир', 'Длинное-предлинное сообщение']
    #     ]
    #     self.view.set_category_list(self.cats)

        
        # main_window.some_method(...)

    # def register_cat_modifier(
    #          self,
    #          handler: Callable[[Category], None]) -> None:
    #     self.cat_modifier = handle_error(self, handler)

    # def register_cat_adder(
    #         self,
    #         handler: Callable[[Category], None]) -> None:
    #     self.cat_adder = handle_error(self, handler)

    # def add_category(self):
    #     # получение данных из формочки
    #     # name = 
    #     # parent = 
    #     pass

    # def delete_category(self):
    #     # cat = ... определить выбранную категорию
    #     # тут может быть отдельное окно, галочки, контекстное меню
    #     del_subcats, del_expenses = self.ask_del_cat()
    #     self.cat_deleter(cat, del_subcats,del_expenses)

    # def add_expense_updater(self, callback):
    #     self.table.itemChanged.connect(self.on_table_change)
    #     self.expense_updater = callback

    # def on_table_change(self, item):
    #     self.expense_updater(expense_from_item(item))

if __name__ == "__main__":

    # 1. Надо создать объект класса MainView - он изначально пустой
    # 2. Надо построить на нем Bookkeeper
    # 3. Надо получить список категорий у репо из bookkeeper
    # 4. Надо передать этот список MainWindow из bookkeeper/MainView
    # 5. так делать со всем остальным, пока MainWindow не заполнится
    # 6. По итогу отрисовать окно

    app = QtWidgets.QApplication(sys.argv)

    window = BookkeeperMainWindow()
    view = BookkeeperMainView(window)
    bookkeeper = Bookkeeper(view)
    #bookkeeper.provide_with_category_list()
    window.show()
    sys.exit(app.exec())


    # app = QtWidgets.QApplication(sys.argv)
    # window = MainWindow()
    # bookkeeper = Bookkeeper(window)
    # bookkeeper.provide_with_category_list()
    # window.show()
    # sys.exit(app.exec())