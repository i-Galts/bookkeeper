"""
Репозиторий для работы с базой данных.
"""
from typing import Any
from inspect import get_annotations

import sqlite3

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
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled `pk` attribute')
        names = ', '.join(self.fields.keys())
        qm_line = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file,
                             detect_types=sqlite3.PARSE_DECLTYPES) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'INSERT INTO {self.table_name} ({names}) VALUES ({qm_line})',
                values
            )
            obj.pk = cur.lastrowid
        con.close()
        return obj.pk

    def get(self, pk: int) -> T | None:
        obj = None
        names = ', '.join(self.fields.keys())
        with sqlite3.connect(self.db_file,
                             detect_types=sqlite3.PARSE_DECLTYPES) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                    f'SELECT {names} from {self.table_name} WHERE ROWID={pk}'
                )
            record = cur.fetchone()
            if record:
                obj = self.cls(pk=pk)
                for field, item in zip(self.fields, record):
                    setattr(obj, field, item)
        con.close()
        return obj

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        records = []
        if where is None:
            with sqlite3.connect(self.db_file,
                                 detect_types=sqlite3.PARSE_DECLTYPES) as con:
                cur = con.cursor()
                cur.execute('PRAGMA foreign_keys = ON')
                cur.execute(
                    f'SELECT * FROM {self.table_name}')
                all_records = cur.fetchall()
                for i, record in enumerate(all_records):
                    obj = self.cls(pk=i+1)
                    for field, item in zip(self.fields, record):
                        setattr(obj, field, item)
                    records.append(obj)
            con.close()
        else:
            pass
        return records

    def update(self, obj: T) -> None:
        pk = obj.pk
        if not pk:
            raise ValueError('attempt to update object with unknown primary key')
        names = '=?, '.join(self.fields.keys()) + '=?'
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file,
                             detect_types=sqlite3.PARSE_DECLTYPES) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'UPDATE {self.table_name} SET {names} WHERE ROWID={pk}',
                values
            )
        con.close()

    def delete(self, pk: int) -> None:
        with sqlite3.connect(self.db_file,
                             detect_types=sqlite3.PARSE_DECLTYPES) as con:
            cur = con.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(
                f'SELECT Count(*) FROM {self.table_name}'
            )
            rows_num, = cur.fetchone()
            if not rows_num:
                raise KeyError('the table is empty')
            elif pk not in range(1, rows_num):
                raise KeyError('no object with given primary key')
            else:
                cur.execute(
                    f'DELETE from {self.table_name} WHERE ROWID={pk}'
                    )
        con.close()

# if __name__ == "__main__":
    # sqlrepo_exp = SQLiteRepository('expense_repo.db', Expense)
    # print(sqlrepo_exp.table_name)
    # print(sqlrepo_exp.fields)

    # exp = Expense(amount=100, category='Хлеб', comment='Какой-то расход')
    # sqlrepo_exp.add(exp)

    # other_exp = Expense(amount=8, category='Книги', comment='Пакет на кассе')
    # one_more_exp = Expense(amount=105, category='Продукты',
    #                                   comment='Длинное-предлинное сообщение')
    # sqlrepo_exp.add(other_exp)
    # sqlrepo_exp.add(one_more_exp)

    # sqlrepo_cat = SQLiteRepository('category_repo.db', Category)
    # print(sqlrepo_cat.table_name)
    # print(sqlrepo_cat.fields)

    # cat = Category(name='Фрукты')
    # sqlrepo_cat.add(cat)

    # other_cat = Category(name='Яблоки', parent='Фрукты')
    # sqlrepo_cat.add(other_cat)

    # sqlrepo_bud = SQLiteRepository('budget_repo.db', Budget)
    # print(sqlrepo_bud.table_name)
    # print(sqlrepo_bud.fields)

    # bud = Budget(category='Фрукты', amount=500, period=7)
    # sqlrepo_bud.add(bud)

    # other_bud = Budget(category='Яблоки', amount=600, period=30)
    # sqlrepo_bud.add(other_bud)
