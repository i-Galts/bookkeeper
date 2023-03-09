from inspect import get_annotations
import sqlite3

from typing import Any

from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.models.budget import Budget

from bookkeeper.repository.abstract_repository import AbstractRepository, T

class SQLiteRepository(AbstractRepository[T]):
    """
    Репозиторий, работающий с базой данных.
    """
    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.cls = cls
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
        self.fields.pop('pk')

    def add(self, obj: T) -> int:
        names = ', '.join(self.fields.keys())
        p = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file, 
                             detect_types=sqlite3.PARSE_DECLTYPES) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'INSERT INTO {self.table_name} ({names}) VALUES ({p})',
                values
            )
            obj.pk = cur.lastrowid
        con.close()
        return obj.pk
    
    def get(self, pk: int) -> T | None:
        pass

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        self.records = []
        if where is None:
            with sqlite3.connect(self.db_file,
                             detect_types=sqlite3.PARSE_DECLTYPES) as con:
                cur = con.cursor()
                cur.execute('PRAGMA foreign_keys = ON')
                cur.execute(
                    f'SELECT * FROM {self.table_name}')
                records = cur.fetchall()
                for i, record in enumerate(records):
                    obj = self.cls(pk=i+1)
                    for field, item in zip(self.fields, record):
                        setattr(obj, field, item)
                    self.records.append(obj)
            con.close()
            return self.records
        else:
            pass

    def update(self, obj: T) -> None:
        pass

    def delete(self, pk: int) -> None:
        with sqlite3.connect(self.db_file,
                             detect_types=sqlite3.PARSE_DECLTYPES) as con:
                cur = con.cursor()
                cur.execute('PRAGMA foreign_keys = ON')
                cur.execute(
                    f'DELETE from {self.table_name} WHERE ROWID={pk}'
                )
        con.close()
    
if __name__ == "__main__":
    sqlrepo_exp = SQLiteRepository('expense_repo.db', Expense)
    print(sqlrepo_exp.table_name)
    print(sqlrepo_exp.fields)

    exp = Expense(amount=100, category='Хлеб', comment='Какой-то расход')
    sqlrepo_exp.add(exp)

    other_exp = Expense(amount=8, category='Книги', comment='Пакет на кассе')
    one_more_exp = Expense(amount=105, category='Продукты', comment='Длинное-предлинное сообщение')
    sqlrepo_exp.add(other_exp)
    sqlrepo_exp.add(one_more_exp)


    # sqlrepo_cat = SQLiteRepository('category_repo.db', Category)
    # print(sqlrepo_cat.table_name)
    # print(sqlrepo_cat.fields)

    # cat = Category(name='Продукты')
    # sqlrepo_cat.add(cat)

    # other_cat = Category(name='Молоко', parent=1)
    # one_more_cat = Category(name='Хлеб', parent=1)
    # sqlrepo_cat.add(other_cat)
    # sqlrepo_cat.add(one_more_cat)

    # again = Category(name='Книги', parent=2)
    # sqlrepo_cat.add(again)