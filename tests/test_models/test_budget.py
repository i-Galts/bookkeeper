"""
Тесты для модели бюджета
"""
import pytest

from bookkeeper.models.budget import Budget


def test_create_with_full_args_list():
    b = Budget(amount='1000', category='Молоко', period='7',
               comment='временно', pk=1)
    assert b.period == '7'
    assert b.amount == '1000'

def test_default_pk_is_zero():
    b = Budget(amount='100', period='1')
    assert b.pk == 0

def test_eq():
    """
    class should implement __eq__ method
    """
    c1 = Budget(amount='100', period='30', comment='text')
    c2 = Budget(amount='100', period='30', comment='text')
    assert c1 == c2

def test_reassign():
    """
    class should not be frozen
    """
    c = Budget('cat_name')
    c.name = 'other_name'
    c.pk = 1
    assert c.name == 'other_name'
    assert c.pk == 1
