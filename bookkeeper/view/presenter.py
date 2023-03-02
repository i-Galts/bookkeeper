from typing import Protocol

from bookkeeper.models.category import Category

class AbstractView(Protocol):
    def set_category_list(lst: list[Category]) -> None:
        pass

class Bookkeeper:
    def __init__(self,
                 view: AbstractView,
                 repository_factory) -> None:
        self.view = view
        self.category_repository = \
                    repository_factory.get(Category)
        
        self.cats = self.category_repository.get_all()
        self.view.set_category_list(self.cats)
        