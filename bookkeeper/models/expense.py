"""
Описан класс, представляющий расходную операцию
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Expense:
    """
    Расходная операция.
    amount - сумма
    category - id категории расходов
    expense_date - дата расхода
    added_date - дата добавления в бд
    comment - комментарий
    pk - id записи в базе данных
    """
    amount: int = 1
    category: int = 1
    expense_date: datetime = field(default_factory=datetime.now)
    added_date: datetime = field(default_factory=datetime.now)
    comment: str = ''
    pk: int = 0

    def __repr__(self):
        return f'{"{:%B %d %Y}".format(self.expense_date.date())}, \
                             {self.amount}, {self.category}, {self.comment}'

    
def convert_expense(s: bytes):
    sp = s.split(",")
    pk, amount, cat, exp_date, add_date, comment = \
            int(sp[0]), int(sp[1]), int(sp[2]), \
                datetime(sp[3]), datetime(sp[4]), str(sp[5])
    return Expense(amount, cat, exp_date, exp_date, add_date, comment, pk)

if __name__ == "__main__":
    exp = Expense(100, 1)
    print(exp)
    