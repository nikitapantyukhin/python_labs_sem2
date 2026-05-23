import asyncio

from src.contracts.task import Task


class DefaultTaskHandler:
    """Базовый обработчик для любых задач."""

    def __init__(self, delay: float = 0.01) -> None:
        self.delay = delay
        self.processed: list[int] = []

    def can_handle(self, task: Task) -> bool:
        return True

    async def handle(self, task: Task) -> None:
        await asyncio.sleep(self.delay)
        self.processed.append(task.id)
