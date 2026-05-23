import asyncio
import logging
from collections.abc import Iterable, Sequence
from dataclasses import dataclass

from src.contracts.handler import TaskHandler
from src.contracts.task import Task
from src.execution.async_queue import AsyncTaskQueue


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ExecutionReport:
    """Итог асинхронной обработки очереди."""

    loaded: int = 0
    processed: int = 0
    failed: int = 0
    skipped: int = 0


class AsyncTaskExecutor:
    """Асинхронный исполнитель задач с расширяемыми обработчиками."""

    def __init__(
        self,
        handlers: Sequence[TaskHandler],
        worker_count: int = 2,
        queue_maxsize: int = 0,
        log: logging.Logger | None = None,
    ) -> None:
        if worker_count < 1:
            raise ValueError("worker_count должен быть больше 0")

        self._handlers = list(handlers)
        self._worker_count = worker_count
        self._queue_maxsize = queue_maxsize
        self._logger = log or logger
        self._workers: list[asyncio.Task[None]] = []
        self._processed = 0
        self._failed = 0
        self._skipped = 0

        for handler in self._handlers:
            if not isinstance(handler, TaskHandler):
                raise TypeError(
                    f"Обработчик {type(handler).__name__} не соответствует TaskHandler"
                )

    async def __aenter__(self) -> "AsyncTaskExecutor":
        self._logger.info("Асинхронный исполнитель задач запущен")
        return self

    async def __aexit__(self, exc_type, exc, traceback) -> None:
        for worker in self._workers:
            if not worker.done():
                worker.cancel()

        if self._workers:
            await asyncio.gather(*self._workers, return_exceptions=True)

        self._workers.clear()
        self._logger.info("Асинхронный исполнитель задач остановлен")

    async def run(self, tasks: Iterable[Task]) -> ExecutionReport:
        """Обрабатывает iterable задач через асинхронных воркеров."""
        self._processed = 0
        self._failed = 0
        self._skipped = 0

        queue = AsyncTaskQueue(maxsize=self._queue_maxsize)
        self._workers = [
            asyncio.create_task(self._worker(queue), name=f"task-worker-{index + 1}")
            for index in range(self._worker_count)
        ]

        loaded = 0
        try:
            loaded = await queue.load_from_iterable(tasks)
        finally:
            await queue.close(self._worker_count)

        await queue.join()
        await asyncio.gather(*self._workers)
        self._workers.clear()

        return ExecutionReport(
            loaded=loaded,
            processed=self._processed,
            failed=self._failed,
            skipped=self._skipped,
        )

    async def _worker(self, queue: AsyncTaskQueue) -> None:
        while True:
            task = await queue.get()
            try:
                if task is None:
                    return

                await self._process(task)
            finally:
                queue.task_done()

    async def _process(self, task: Task) -> None:
        handler = self._select_handler(task)
        if handler is None:
            self._skipped += 1
            self._logger.error("Для задачи %s не найден подходящий обработчик", task.id)
            return

        task.status = "In Progress"

        try:
            await handler.handle(task)
        except Exception:
            self._failed += 1
            task.status = "Failed"
            self._logger.exception("Ошибка при обработке задачи %s", task.id)
            return

        self._processed += 1
        task.status = "Done"
        self._logger.info("Задача %s успешно обработана", task.id)

    def _select_handler(self, task: Task) -> TaskHandler | None:
        for handler in self._handlers:
            if handler.can_handle(task):
                return handler
        return None
