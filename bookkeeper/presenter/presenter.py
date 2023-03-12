"""Главный модуль проекта по разработке приложения личных финансов"""
import sys
from typing import Protocol, Callable
from PySide6 import QtWidgets

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.view.main_window import BookkeeperMainWindow


class RepositoryFactory:
    """
    Фабрика репозиториев. При создании передается
    тип репозитория repo_type.
    """
    def __init__(self, repo_type):
        if repo_type == SQLiteRepository:
            self.repo_dict = {
                Category: repo_type('./repos/category_repo.db', Category),
                Expense:  repo_type('./repos/expense_repo.db', Expense),
                Budget:   repo_type('./repos/budget_repo.db', Budget)
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
    """
    Класс абстрактного View. Класс Bookkeeper не
    зависит от конкретной реализации.
    """
    def set_category_list(self, lst: list[Category]) -> None:
        """
        Устанавливает список категорий расходов.
        """

    def register_cat_adder(
            self,
            handler: Callable[[str, str], None]) -> None:
        """
        Регистратор добавления категории расходов.
        """

    def register_cat_deleter(
            self,
            handler: Callable[[None], None]) -> None:
        """
        Регистратор удаления категории расходов.
        """

    def set_expense_list(self, exp_list: list[Expense]) -> None:
        """
        Устанавливает список расходов.
        """

    def register_expense_adder(
            self,
            handler: Callable[[int, str, str], None]) -> None:
        """
        Регистратор добавления записи о расходах.
        """

    def register_expense_deleter(
            self,
            handler: Callable[[None], None]) -> None:
        """
        Регистратор удаления записи о расходах.
        """

    def create_delete_expense_button(self) -> None:
        """
        Регистратор кнопки удаления записи о расходах.
        """

    def set_budget_list(self, exp_list: list[Budget]) -> None:
        """
        Устанавливает данные о бюджете.
        """

    def create_expense_edit_panel(self) -> None:
        """
        Добавляет панель редактирования записей о расходах.
        """


class Bookkeeper:
    """
    Класс для взаимодействия главного окна с bookkeeper.
    Детали интерфейса описаны в классе MainWindow.
    Определены обработчики при работе с моделями.
    """
    def __init__(self,
                 view: AbstractView,
                 repository_factory: RepositoryFactory) -> None:

        self.view = view
        # self.view.register_cat_modifier(self.modify_category)
        self.view.register_cat_adder(self.add_category)
        self.view.register_cat_deleter(self.delete_category)
        self.category_repository = repository_factory.get(Category)
        self.cats = self.category_repository.get_all()
        self.cat_names = [cat.name.capitalize() for cat in self.cats]
        self.view.set_category_list(self.cats)

        self.view.register_expense_adder(self.add_expense)
        self.view.register_expense_deleter(self.delete_expense)
        self.expense_repository = repository_factory.get(Expense)
        self.exps = self.expense_repository.get_all()
        self.view.set_expense_list(self.exps)
        self.view.create_delete_expense_button()

        self.budget_repository = repository_factory.get(Budget)
        self.buds = self.budget_repository.get_all()
        self.view.set_budget_list(self.buds)

        self.view.create_expense_edit_panel()

    def add_expense(self, amount: int,
                    category: str, comment: str) -> None:
        """
        Добавляет запись о расходах. Указывается потраченная
        сумма amount, категория расхода category и
        комментарий comment.
        """
        exp = Expense(amount=amount, category=category, comment=comment)
        self.expense_repository.add(exp)
        self.exps.append(exp)
        self.view.set_expense_list(self.exps)

    def delete_expense(self) -> None:
        """
        Удаляет последнюю запись о расходах.
        """
        if not self.exps:
            raise IndexError('Нет записей о расходах!')
        last_pk = len(self.exps)
        self.exps.pop()
        self.view.set_expense_list(self.exps)
        self.expense_repository.delete(last_pk)

    def add_category(self, name: str, parent: str) -> None:
        """
        Добавляет новую категорию после ввода
        названия name и выбора родительсокй категории parent.
        """
        if name.capitalize() in self.cat_names:
            raise IndexError('Категория с таким именем уже добавлена!')
        cat = Category(name=name, parent=parent)
        self.category_repository.add(cat)
        self.cats.append(cat)
        self.cat_names = [cat.name.capitalize() for cat in self.cats]
        self.view.set_category_list(self.cats)

    def delete_category(self, cat: str) -> None:
        """
        Удаляет выбранную категорию.
        """
        if not self.cats:
            raise IndexError('Нет категорий!')
        cur_pk = self.cat_names.index(cat.capitalize())
        self.category_repository.delete(cur_pk + 1)
        self.cats.pop(cur_pk)
        self.cat_names = [cat.name.capitalize() for cat in self.cats]
        self.view.set_category_list(self.cats)
        # self.cats = self.category_repository.get_all()


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = BookkeeperMainWindow()
    repo_factory = RepositoryFactory(SQLiteRepository)
    bookkeeper = Bookkeeper(window, repo_factory)
    window.show()
    sys.exit(app.exec())
