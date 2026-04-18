import os
from src.contracts.task import Task
from src.inbox.core import TaskInbox
from src.sources.generator_source import GeneratorTaskSource
from src.sources.json_source import JsonTaskSource

def main():
    db_file = "tasks.jsonl"

    sources = [
        GeneratorTaskSource(count=5),
        JsonTaskSource(db_file)
    ]

    inbox = TaskInbox(sources)

    for task in inbox.iter_tasks():
        print(f"ID: {task.id} | Priority: {task.priority} | Description: {task.description}")


    test_task = Task(task_id=999, description="Check protection", priority=10)

    # 1. Проверяем валидацию приоритета (IntegerRange)
    try:
        print("\nТест 1. Пробуем поставить приоритет 500.")
        test_task.priority = 500
    except ValueError as e:
        print(f"Результат: Система заблокировала изменение! Ошибка: {e}")

    # 2. Проверяем защиту ID (Property Read-Only)
    try:
        print("\nТест 2. Пробуем изменить защищенный ID.")
        test_task.id = 123
    except AttributeError as e:
        print(f"Результат: ID изменить нельзя!")

    # 3. Проверяем валидацию статуса (Choice)
    try:
        print("\nТест 3. Пробуем поставить несуществующий статус 'Archive'.")
        test_task.status = "Archive"
    except ValueError as e:
        print(f"Результат: Ошибка валидации статуса: {e}")


if __name__ == "__main__":
    main()