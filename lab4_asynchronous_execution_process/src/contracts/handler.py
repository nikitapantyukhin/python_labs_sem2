from typing import Protocol, runtime_checkable

from src.contracts.task import Task


@runtime_checkable
class TaskHandler(Protocol):
    """Контракт асинхронного обработчика задач."""

    def can_handle(self, task: Task) -> bool:
        """Возвращает True, если обработчик умеет обработать задачу."""
        ...

    async def handle(self, task: Task) -> None:
        """Асинхронно обрабатывает задачу."""
        ...
