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
    added_date: datetime = field(default_factory=datetime.now)
    expense_date: datetime = field(default_factory=datetime.now)
    amount: float = 1
    category: str = ''
    comment: str = ''
    pk: int = 0

    def __repr__(self):
        return f'{str(self.added_date.date())}, {str(self.expense_date.date()).strip()},' \
                f' {self.amount}, {self.category}, {self.comment}'

    # def __repr__(self):
    #     return f'{"{:%B %d %Y}".format(self.added_date.date()).strip()}, \
    #                       {"{:%B %d %Y}".format(self.expense_date.date()).strip()}, \
    #                         {self.amount}, {self.category}, {self.comment}'

if __name__ == "__main__":
    exp = Expense(amount=100, category='Milk', comment='lalala')
    print(exp)
    