from typing import Sequence, Iterator, Callable
from src.contracts.task import Task
from src.contracts.source import TaskSource

class TaskQueue:
    """
    Очередь задач, поддерживающая ленивую загрузку и итерацию.
    Данные не хранятся в памяти, а генерируются на лету из источников.
    """
    def __init__(self, sources: Sequence[TaskSource] = None):
        self._sources = sources or []

    def __iter__(self) -> Iterator[Task]:
        """
        Реализация протокола итерации.
        Позволяет обходить очередь несколько раз. При каждом вызове источники заново генерируют или считывают данные.
        """
        for src in self._sources:
            if not isinstance(src, TaskSource):
                raise TypeError(
                    f"Объект {type(src).__name__} не реализует протокол TaskSource"
                )
            yield from src.get_tasks()

    def filter(self, predicate: Callable[[Task], bool]) -> Iterator[Task]:
        """Универсальный ленивый фильтр на основе предиката (конвейер)."""
        for task in self:
            if predicate(task):
                yield task

    def filter_by_status(self, status: str) -> Iterator[Task]:
        """Ленивая фильтрация задач по статусу."""
        yield from self.filter(lambda t: t.status == status)

    def get_urgent_tasks(self) -> Iterator[Task]:
        """Ленивое получение только срочных задач."""
        yield from self.filter(lambda t: t.is_urgent)