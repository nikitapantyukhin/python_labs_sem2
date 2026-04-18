import random
from typing import Iterable
from src.contracts.task import Task

class GeneratorTaskSource:
    def __init__(self, count: int):
        self._count = count

    def get_tasks(self) -> Iterable[Task]:
        for i in range(self._count):
            yield Task(
                id=i + 1,
                payload=f"Generated Data: {random.randint(100, 999)}"
            )