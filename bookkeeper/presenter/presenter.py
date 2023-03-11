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
    def __init__(self, repo_type):
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

class AbstractView(Protocol):
    def set_category_list(lst: list[Category]) -> None:
        pass

    def register_cat_adder(
            self,
            handler: Callable[[str, int], None]) -> None:
        pass

    def register_cat_deleter(
            self,
            handler: Callable[[None], None]):
        pass

    def set_expense_list(self, exp_list: list[Expense]) -> None:
        pass

    def register_expense_adder(
            self,
            handler: Callable[[int, str], None]) -> None:
        pass

    def register_expense_deleter(
            self,
            handler: Callable[[None], None]) -> None:
        pass

    def create_delete_expense_button(self) -> None:
        pass

    def set_budget_list(self, exp_list: list[Budget]) -> None:
        pass

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
        self.view.register_cat_deleter(self.delete_category)
        self.category_repository = repo_factory.get(Category)
        self.cats = self.category_repository.get_all()
        self.cat_names = [cat.name.capitalize() for cat in self.cats]
        self.view.set_category_list(self.cats)

        self.view.register_expense_adder(self.add_expense)
        self.view.register_expense_deleter(self.delete_expense)
        self.expense_repository = repo_factory.get(Expense)
        self.exps = self.expense_repository.get_all()
        self.view.set_expense_list(self.exps)
        self.view.create_delete_expense_button()

        # self.budget_repository = repo_factory.get(Budget)
        # self.buds = self.budget_repository.get_all()
        # self.view.set_budget_list(self.buds)

        self.view.create_expense_edit_panel()

    def add_expense(self, amount: int, category: str, comment: str) -> None:
        exp = Expense(amount=amount, category=category, comment=comment)
        # (handle error if smth wrong in input)
        self.expense_repository.add(exp)
        self.exps.append(exp)
        self.view.set_expense_list(self.exps)

    def delete_expense(self):
       if (len(self.exps) == 0):
            raise IndexError('Нет записей о расходах!')
       last_pk = len(self.exps)
       self.exps.pop()
       self.view.set_expense_list(self.exps)
       self.expense_repository.delete(last_pk)

    def add_category(self, name: str, parent: int):
        if (name.capitalize() in self.cat_names):
            raise IndexError('Категория с таким именем уже добавлена!')
        cat = Category(name=name, parent=parent)
        self.category_repository.add(cat)
        self.cats.append(cat)
        self.view.set_category_list(self.cats)

    def delete_category(self) -> None:
        if (len(self.cats) == 0):
            raise IndexError('Нет категорий!')
        last_pk = len(self.cats)
        self.cats.pop()
        self.view.set_category_list(self.cats)
        self.category_repository.delete(last_pk)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = BookkeeperMainWindow()
    repo_factory = RepositoryFactory(SQLiteRepository)
    bookkeeper = Bookkeeper(window, repo_factory)
    window.show()
    sys.exit(app.exec())