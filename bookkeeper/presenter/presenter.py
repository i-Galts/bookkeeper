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
        if (repo_type == SQLiteRepository):
            self.repo_dict = {
                Category: SQLiteRepository('./repos/category_repo.db', Category),
                Expense:  SQLiteRepository('./repos/expense_repo.db', Expense),
                Budget:   SQLiteRepository('./repos/budget_repo.db', Budget)
            }
        else:
            self.repo_dict = {
                Category: MemoryRepository(),
                Expense:  MemoryRepository(),
                Budget:   MemoryRepository()   
            }
        
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
                 view: AbstractView,
                 repo_factory: RepositoryFactory) -> None:

        self.view = view
        # self.view.register_cat_modifier(self.modify_category)
        self.view.register_cat_adder(self.add_category)
        # self.view.register_cat_deleter(self.delete_category)
        self.category_repository = repo_factory.get(Category)
        self.cats = self.category_repository.get_all()
        self.view.set_category_list(self.cats)

        self.view.register_expense_adder(self.add_expense)
        self.view.register_expense_deleter(self.delete_expense)
        self.expense_repository = repo_factory.get(Expense)
        self.exps = self.expense_repository.get_all()
        self.view.set_expense_list(self.exps)
        self.view.create_delete_expense_button()

        self.view.show_budget_widget()
        self.view.create_expense_edit_panel()

    def add_expense(self, amount: int, category: str, comment: str) -> None:
        exp = Expense(amount=amount, category=category, comment=comment)
        # (handle error if smth wrong in input)
        self.expense_repository.add(exp)
        self.exps.append(exp)
        self.view.set_expense_list(self.exps)

    def delete_expense(self):
       last_pk = len(self.exps)
       self.exps.pop()
       self.view.set_expense_list(self.exps)
       self.expense_repository.delete(last_pk)

    # def modify_cat(self, cat: Category) -> None:
    #     # self.category_repository.update(cat)
    #     # self.cats = self.category_repository.get_all()
    #     self.cats.append(['2023-01-09 15:09:00', '43.67', 'Бублик'])
    #     self.view.set_category_list(self.cats)

    def add_category(self, name: str, parent: int):
        print(name, parent)

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