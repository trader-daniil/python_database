from database import DataBase, Transaction
import pytest


@pytest.fixture()
def database():
    """Создадим объект БД."""
    database = DataBase()
    return database

@pytest.fixture()
def transaction():
    """Создадим объект Транзакции."""
    transaction = Transaction()
    return transaction

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

def test_create_transaction(database, transaction):
    """Проверим создание транзакции без применения."""
    set_action = getattr(database, 'set')
    transaction.add_action(set_action, *('A', 10))
    transaction.add_action(set_action, *('B', 20))
    assert database.get(*('A',)) ==  'NULL'

def test_apply_transaction(database, transaction):
    """Проверим создание траназакции с применением."""
    set_action = getattr(database, 'set')
    transaction.add_action(set_action, *('A', 10))
    transaction.add_action(set_action, *('B', 20))
    transaction.execute()
    assert database.get(*('A',)) ==  10
    assert database.get(*('B',)) ==  20

def test_nested_transaction(database, transaction):
    """Проверим создание внутренней транзакции."""
    set_action = getattr(database, 'set')
    transaction.add_action(set_action, *('A', 10))
    transaction.add_action(set_action, *('B', 20))
    nested_transaction = Transaction()
    nested_transaction.add_action(set_action, *('F', 30))
    nested_transaction.execute()
    assert database.get(*('A',)) ==  'NULL'
    assert database.get(*('F',)) == 30

