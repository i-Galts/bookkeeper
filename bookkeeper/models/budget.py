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
    amount: int
    category: int
    period: int = 30
    comment: str = ''
    pk: int = 0