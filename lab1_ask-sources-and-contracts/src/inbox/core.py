from typing import Sequence, Iterable
from src.contracts.task import Task
from src.contracts.source import TaskSource

class TaskInbox:
    def __init__(self, sources: Sequence[TaskSource] = None):
        self._sources = sources or []

    def iter_tasks(self) -> Iterable[Task]:
        for src in self._sources:
            # Обязательная проверка контракта по заданию
            if not isinstance(src, TaskSource):
                raise TypeError(
                    f"Object {type(src).__name__} does not implement TaskSource protocol"
                )
            yield from src.get_tasks()