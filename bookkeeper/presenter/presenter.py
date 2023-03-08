import sys

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget

from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.repository.memory_repository import MemoryRepository

from PySide6 import QtWidgets, QtCore

from bookkeeper.view.main_window import BookkeeperMainWindow

from typing import Protocol, Callable

class RepositoryFactory:
    """
    Класс, предоставляющий фабрику репозиториев.
    При создании фабрики указывается тип repo_type:
    либо MemoryRepository, либо SQLiteRepository.
    """
    def __init__(self, repo_type: type):
        # self.repo_dict = {}
        if (repo_type == SQLiteRepository):
            self.repo_dict = {
                Category: SQLiteRepository('category_repo.db', Category),
                Expense:  SQLiteRepository('expense_repo.db', Expense),
                Budget:   SQLiteRepository('budget_repo.db', Budget)
            }
            # self.repo_dict[Category] = SQLiteRepository('category_repo.db', Category)
            # self.repo_dict[Expense]  = SQLiteRepository('expense_repo.db', Expense)
            # self.repo_dict[Budget]   = SQLiteRepository('budget_repo.db', Budget)
        else:
            self.repo_dict = {
                Category: MemoryRepository(),
                Expense:  MemoryRepository(),
                Budget:   MemoryRepository()   
            }
            # self.repo_dict[Category] = MemoryRepository()
            # self.repo_dict[Expense]  = MemoryRepository()
            # self.repo_dict[Budget]   = MemoryRepository()
        
    def get(self, model_cls: type):
        """
        Возвращает репозиторий для каждой
        конкретной модели.
        """
        return self.repo_dict[model_cls]

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

    def register_cat_modifier(
             self,
             handler: Callable[[Category], None]) -> None:
        pass

    def register_cat_adder(
            self,
            handler: Callable[[Category], None]) -> None:
        pass

# class BookkeeperMainView:
#     def __init__(self, 
#                  window: BookkeeperMainWindow):
#         self.window = window

#     # def set_category_list(self, cat_list: list[Category]) -> None:
#     #     #cat_to_str = [str(cat) for cat in lst.split()]

#     def set_expense_list(self, exp_list: list[Expense]) -> None:
#         #exp_to_str = [str(exp) for cat in exp_list.split()]
#         self.window.create_expenses_table(exp_list)

#     def show_budget_widget(self) -> None:
#         self.window.create_budget_table()

#     def show_expense_edit_panel(self) -> None:
#         self.window.create_expense_edit_panel()

    # def show_category_choice_widget(self) -> None:
    #     self.window.create_category_choice_widget()

    # def register_expense_adder(
    #         self,
    #         handler: Callable[[Category], None]) -> None:
    #     pass


    # def register_cat_modifier(
    #          self,
    #          handler: Callable[[Category], None]) -> None:
    #     self.cat_modifier = handle_error(self, handler)

    # def register_cat_adder(
    #         self,
    #         handler: Callable[[Category], None]) -> None:
    #     self.cat_adder = handle_error(self, handler)

class Bookkeeper:
    """
    Класс для взаимодействия главного окна с bookkeeper. 
    Детали интерфейса описаны в классе MainWindow.
    Определены обработчики при работе с моделями.
    """
    def __init__(self, 
                 view: AbstractView, # с каким отображением будем работать
                 repo_factory: RepositoryFactory) -> None: # repo - идея, чтобы не передавать какой-то конкретный репо

        self.view = view
        self.view.register_expense_adder(self.add_expense)
        self.expense_repository = repo_factory.get(Expense)
        self.exps = self.expense_repository.get_all()
        # self.exps = [
        #     Expense(8, 2, comment='Пакет на кассе'),
        #     Expense(105, 4, comment='Длинное-предлинное сообщение')
        # ]
        # self.exps = [
        #     ['2023-01-09 15:09:00', '7.49', 'Хозтовары', 'Пакет на кассе'],
        #     ['2023-01-09 15:09:00', '104.99', 'Кефир', 'Длинное-предлинное сообщение']
        # ]
        self.view.set_expense_list(self.exps)
        self.view.show_budget_widget()
        self.view.show_expense_edit_panel()

    def add_expense(self, amount: int, comment: str) -> None:
        print(amount, comment)
        exp = Expense(amount, 10, comment=comment)
        # (handle error if smth wrong in input)
        # save to exp_repository
        self.exps.append(exp)
        print(self.exps)
        self.view.set_expense_list(self.exps)

    # def modify_cat(self, cat: Category) -> None:
    #     # self.category_repository.update(cat)
    #     # self.cats = self.category_repository.get_all()
    #     self.cats.append(['2023-01-09 15:09:00', '43.67', 'Бублик'])
    #     self.view.set_category_list(self.cats)

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
    repo_factory = RepositoryFactory(SQLiteRepository)
    # view = BookkeeperMainView(window)
    bookkeeper = Bookkeeper(window, repo_factory)
    #bookkeeper.provide_with_category_list()
    window.show()
    sys.exit(app.exec())


    # app = QtWidgets.QApplication(sys.argv)
    # window = MainWindow()
    # bookkeeper = Bookkeeper(window)
    # bookkeeper.provide_with_category_list()
    # window.show()
    # sys.exit(app.exec())