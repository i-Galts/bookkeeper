import pytest

from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.models.budget import Budget

@pytest.fixture
def repo():
    return MemoryRepository()

def test_create_with_full_args_list():
    b = Budget(amount=1000, category=1, period=7,
               comment='временно', pk=1)
    assert b.period == 7
    assert b.amount == 1000

def test_create_brief():
    b = Budget(100, 1)
    assert b.category == 1
    assert b.amount == 100

def test_default_pk_is_zero():
    b = Budget(100, 1)
    assert b.pk == 0

