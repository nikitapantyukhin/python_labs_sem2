import os
from src.queue.core import TaskQueue
from src.sources.generator_source import GeneratorTaskSource
from src.sources.json_source import JsonTaskSource

def main():
    db_file = "tasks.jsonl"
    
    sources = [
        GeneratorTaskSource(count=3),
        JsonTaskSource(db_file)
    ]

    queue = TaskQueue(sources)

    print("1. Обычная итерация по всей очереди")
    for task in queue:
        print(task)

    print("\n2. Ленивая фильтрация (только срочные)")
    # Генератор не вычисляет ничего, пока мы не начнем по нему итерироваться
    urgent_generator = queue.get_urgent_tasks()
    for task in urgent_generator:
        print(f"Срочная задача: {task.id} (Приоритет: {task.priority})")

    print("\n3. Проверка повторного обхода")
    # Доказываем, что очередь не исчерпалась после первой итерации
    total_tasks = sum(1 for _ in queue)
    print(f"Очередь успешно пройдена заново. Всего задач: {total_tasks}")

if __name__ == "__main__":
    main()