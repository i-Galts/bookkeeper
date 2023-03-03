from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget

from typing import Protocol

class AbstractView(Protocol):
    def set_category_list(lst: list[Category]) -> None:
        pass

    def register_cat_modifier(
            handler: Callable[[Category], None]) -> None:
        pass

    def register_cat_adder(
            handler: Callable[[Category], None]) -> None:
        pass

class Bookkeeper:
    def __init__(self,
                 view: AbstractView,
                 repository_factory) -> None:
        self.view = view
        self.category_repository = \
                    repository_factory.get(Category)
        self.expense_repository = \
                    repository_factory.get(Expense)
        self.budget_repository = \
                    repository_factory.get(Budget)
        
        self.cats = self.category_repository.get_all()
        self.view.set_category_list(self.cats)

        self.view.register_cat_modifier(self.modify_cat)
        self.view.register_cat_adder(self.add_cat)

    def modify_cat(self, cat: Category) -> None:
        # Проверка ошибок
        self.category_repository.update(cat)
        self.view.set_category_list(self.cats)

    def add_category(self, name, parent):
        if name in [c.name for c in self.cats]:
            raise ValidationError(
                f'Категория {name} уже существует')
        
        cat = Category(name, parent)
        self.category_repository.add(cat)
        self.cats.append(cat)
        self.view.set_category_list(self.cats)
        