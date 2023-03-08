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
    amount: int
    category: int
    expense_date: datetime = field(default_factory=datetime.now)
    added_date: datetime = field(default_factory=datetime.now)
    comment: str = ''
    pk: int = 0

    def __repr__(self):
        # #return (["{:%B %d, %Y}".format(self.expense_date.date()), str(self.amount),
        #             str(self.category), self.comment])
        return f'{"{:%B %d %Y}".format(self.expense_date.date())}, {self.amount}, {self.category}, {self.comment}'

if __name__ == "__main__":
    exp = Expense(100, 1)
    print(exp)