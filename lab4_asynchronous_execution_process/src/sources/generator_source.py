import random
from typing import Iterable
from src.contracts.task import Task

class GeneratorTaskSource:
    def __init__(self, count: int):
        self._count = count

    def get_tasks(self) -> Iterable[Task]:
        for i in range(self._count):
            yield Task(
                task_id=i + 1,
                description = f"Generated Task №{random.randint(100, 999)}",
                priority = random.randint(0, 100)
            )