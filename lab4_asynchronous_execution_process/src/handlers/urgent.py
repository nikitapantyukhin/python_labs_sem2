import asyncio

from src.contracts.task import Task


class UrgentTaskHandler:
    """Обработчик срочных задач."""

    def __init__(self, delay: float = 0.005) -> None:
        self.delay = delay
        self.processed: list[int] = []

    def can_handle(self, task: Task) -> bool:
        return task.is_urgent

    async def handle(self, task: Task) -> None:
        await asyncio.sleep(self.delay)
        self.processed.append(task.id)
