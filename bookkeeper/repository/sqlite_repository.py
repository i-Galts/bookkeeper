from inspect import get_annotations
import sqlite3

from typing import Any

from bookkeeper.models.expense import Expense

from bookkeeper.repository.abstract_repository import AbstractRepository, T

class SQLiteRepository(AbstractRepository[T]):
    """
    Репозиторий, работающий с базой данных.
    """
    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
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
        if where is None:
            with sqlite3.connect(self.db_file, 
                             detect_types=sqlite3.PARSE_DECLTYPES) as con:
                cur = con.cursor()
                cur.execute('PRAGMA foreign_keys = ON')
                cur.execute(
                    f'SELECT * FROM {self.table_name}')
                self.records = cur.fetchall()
                for row in self.records:
                    print(row)
            con.close()
            return self.records
        else:
            pass

    def update(self, obj: T) -> None:
        pass

    def delete(self, pk: int) -> None:
        pass
    
if __name__ == "__main__":
    sqlrepo = SQLiteRepository('expenses_repo.db', Expense)
    print(sqlrepo.table_name)
    print(sqlrepo.fields)

    exp = Expense(100, 1, comment='Какой-то расход')
    sqlrepo.add(exp)

    other_exp = Expense(8, 2, comment='Пакет на кассе')
    one_more_exp = Expense(105, 4, comment='Длинное-предлинное сообщение')
    sqlrepo.add(other_exp)
    sqlrepo.add(one_more_exp)