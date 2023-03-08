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
    amount: int = 1
    category: int = 1
    period: int = 1
    comment: str = ''
    pk: int = 0

def convert_budget(s: bytes):
    sp = s.split(b",")
    pk, amount, cat, period, comment = \
            int(sp[0]), int(sp[1]), int(sp[2]), int(sp[3]), str(sp[4])
    return Budget(amount, cat, period, comment, pk)