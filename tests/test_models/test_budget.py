import pytest

from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.models.budget import Budget

@pytest.fixture
def repo():
    return MemoryRepository()

def test_create_with_full_args_list():
    b = Budget(amount=1000, category='Молоко', period=7,
               comment='временно', pk=1)
    assert b.period == 7
    assert b.amount == 1000

def test_default_pk_is_zero():
    b = Budget(amount=100, period=1)
    assert b.pk == 0

