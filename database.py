import sys
from methods import ALL_METHODS, RECIEVE_METHODS


class Transaction:
    
    def __init__(self):
        self.commands = []

    def add_action(self, action, *args):
        self.commands.append(
            {
                'action': action,
                'args': args,
            }
        )

    def execute(self):
        for command in self.commands:
            result = command['action'](*command['args'])
            if result is not None:
                print(result)


class DataBase:

    def __init__(self):
        self.data = {}
    
    def set(self, *args) -> None:
        """Создаем значение в БД по ключу."""
        key, value = args
        self.data[key] = value

    def get(self, *args):
        """
        Получаем значение в БД по ключу,
        если нет совпадений, то NULL.
        """
        key = args[0]
        try:
            return self.data[key]
        except KeyError:
            return 'NULL'

    def get_amount_values(self, *args) -> int|None:
        """Получим сколько раз встречается переданное значение в БД."""
        count = 0
        value = args[0]
        for el in self.data.values():
            if value == el:
                count += 1
        return count

    def unset(self, *args) -> None:
        """Удаляет запись из БД."""
        value = args[0]
        if value in self.data:
            del self.data[value]
    
    def find(self, *args) -> str|None:
        """Получим ключи, в которых содержится указанное значение."""
        sended_value = args[0]
        keys = [key for key, value in self.data.items() if value==sended_value]
        return " ".join(keys)


def run_transaction(transaction, database, actions):
    """
    Управление транзакциями. В цикле получаем команду, которые добавляем в транзакцию
    Если команда BEGIN, то рекурсивно вызываем нашу функцию.
    """
    while True:
        data = input()
        data = data.split()
        try:
            # Пропускаем пустую строку
            command = data[0]
        except IndexError:
            continue
        if command.upper() not in ALL_METHODS:
            continue
        elif command.upper() == 'BREAK':
            sys.exit()
        elif command.upper() in RECIEVE_METHODS:
            # Если действие на получение значения, то исполняем
            argue = data[1:]
            action = actions[command]
            result = action(*argue)
            if result is not None:
                print(result)
            continue
        elif command == 'BEGIN':
            # Создание вложенной транзакции
            new_transaction = Transaction()
            run_transaction(
                transaction=new_transaction,
                database=database,
                actions=actions,
            )
            continue
        elif command == 'COMMIT':
            # Завершение и исполнение транзакции
            transaction.execute()
            break
        # Если действие на создание, то добавляем в транзакцию
        argue = data[1:]
        action = actions[command]
        transaction.add_action(
            action,
            *argue,
        )


def main():
    database = DataBase()
    actions = {
        'GET': getattr(database, 'get'),
        'SET': getattr(database, 'set'),
        'COUNTS': getattr(database, 'get_amount_values'),
        'UNSET': getattr(database, 'unset'),
        'FIND': getattr(database, 'find'),
    }
    while True:
        data = input()
        data = data.split()
        try:
            # Пропускаем пустую строку
            command = data[0]
        except IndexError:
            continue
        if command.upper() not in ALL_METHODS:
            continue
        elif command.upper() == 'BREAK':
            break
        elif command.upper() == 'BEGIN':
            transaction = Transaction()
            run_transaction(
                transaction=transaction,
                database=database,
                actions=actions,
            )
            continue
        argue = data[1:]
        action = actions[command]
        result = action(*argue)
        if result is not None:
            print(result)


if __name__ == '__main__':
    main()
