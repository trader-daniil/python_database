from database import DataBase, Transaction
import pytest


@pytest.fixture()
def database():
    """Создадим объект БД."""
    database = DataBase()
    print(database)
    return database

@pytest.fixture()
def transaction():
    """Создадим объект БД."""
    database = DataBase()
    print(database)
    return database

def test_create(database):
    """Проверяем создание объекта"""
    database.set(*('A', 10))
    assert database.get(*('A',)) ==  10

def test_delete(database):
    """Проверка удаления объекта."""
    database.set(*('A', 10))
    database.unset(('A',))
    assert database.get(('A',)) == 'NULL'

def test_search(database):
    """Прверка поиска значения."""
    database.set(*('A', 10))
    database.set(*('B', 10))
    assert database.get_amount_values(*(10,)) == 2

def test_search_keys(database):
    """Ищет ключи с переданным значением."""
    database.set(*('A', 10))
    database.set(*('B', 10))
    assert database.find(*(10,)) == 'A B'


