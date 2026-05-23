import asyncio
from collections.abc import Iterable
from typing import Final

from src.contracts.task import Task


_STOP: Final = object()


class AsyncTaskQueue:
    """Асинхронная очередь задач поверх asyncio.Queue."""

    def __init__(self, maxsize: int = 0) -> None:
        self._queue: asyncio.Queue[Task | object] = asyncio.Queue(maxsize=maxsize)

    async def put(self, task: Task) -> None:
        await self._queue.put(task)

    async def get(self) -> Task | None:
        item = await self._queue.get()
        if item is _STOP:
            return None
        return item

    def task_done(self) -> None:
        self._queue.task_done()

    async def join(self) -> None:
        await self._queue.join()

    async def close(self, worker_count: int) -> None:
        for _ in range(worker_count):
            await self._queue.put(_STOP)

    async def load_from_iterable(self, tasks: Iterable[Task]) -> int:
        """Загружает задачи из синхронного iterable, не блокируя event loop."""
        loaded = 0
        iterator = iter(tasks)

        while True:
            item = await asyncio.to_thread(next, iterator, _STOP)
            if item is _STOP:
                return loaded

            await self.put(item)
            loaded += 1
