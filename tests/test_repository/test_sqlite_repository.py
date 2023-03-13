"""
Тесты для класса репозитория, работающего
с базой данных
"""
import os
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.models.category import Category

import sqlite3

import pytest

category_db = 'category_repo.db'

@pytest.fixture
def clear_db():
    os.remove(category_db)

@pytest.fixture
def set_db(clear_db):
    with sqlite3.connect(category_db,
                         detect_types=sqlite3.PARSE_DECLTYPES) as con:
        cur = con.cursor()
        cur.execute('PRAGMA foreign_keys = ON')
        cur.execute(
            f'CREATE TABLE category (name text, parent text)')
    con.close()

@pytest.fixture
def repo():
    return SQLiteRepository('category_repo.db', Category)

def test_crud(repo, set_db, clear_db):
    obj = Category('Apples')
    assert obj.pk == 0
    pk = repo.add(obj)
    assert obj.pk == pk
    assert repo.get(pk) == obj
    obj2 = Category('Bananas')
    obj2.pk = pk
    repo.update(obj2)
    assert repo.get(pk) == obj2
    obj3 = Category('Fruits')
    repo.add(obj3)
    repo.delete(pk)
    assert repo.get(pk) is None

def test_cannot_add_with_pk(repo, set_db, clear_db):
    obj = Category('Apples')
    obj.pk = 1
    with pytest.raises(ValueError):
        repo.add(obj)

def test_cannot_add_without_pk(repo, set_db, clear_db):
    with pytest.raises(ValueError):
        repo.add(0)

def test_cannot_delete_unexistent(repo, set_db, clear_db):
    with pytest.raises(KeyError):
        repo.delete(1)

def test_cannot_update_without_pk(repo, set_db, clear_db):
    obj = Category('Apples')
    with pytest.raises(ValueError):
        repo.update(obj)

def test_get_all(repo, set_db, clear_db):
    objects = [Category() for i in range(5)]
    for o in objects:
        repo.add(o)
    assert repo.get_all() == objects