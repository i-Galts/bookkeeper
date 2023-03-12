"""
Модель бюджета
"""
from dataclasses import dataclass


@dataclass
class Budget:
    """
    Бюджет. Хранит срок, на который установлен, в днях
    в атрибуте period. По умолчанию равен 30.
    amount - сумма ограничения,
    category - категория расходов.
    """
    category: str = ''
    period: str = '1'
    amount: str = '100'
    comment: str = ''
    pk: int = 0

    def __repr__(self) -> str:
        return f'{self.category}, {self.period},' \
                f' {self.amount}, {self.comment}'
