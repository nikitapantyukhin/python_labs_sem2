import asyncio
import unittest

from src.contracts.task import Task
from src.execution.async_queue import AsyncTaskQueue


class TestAsyncTaskQueue(unittest.TestCase):
    def test_load_from_iterable(self):
        async def scenario():
            queue = AsyncTaskQueue()
            tasks = [Task(1, "First", 10), Task(2, "Second", 90)]

            loaded = await queue.load_from_iterable(tasks)

            first = await queue.get()
            second = await queue.get()
            queue.task_done()
            queue.task_done()

            return loaded, first, second

        loaded, first, second = asyncio.run(scenario())

        self.assertEqual(loaded, 2)
        self.assertEqual(first.id, 1)
        self.assertEqual(second.id, 2)

    def test_close_sends_stop_signal(self):
        async def scenario():
            queue = AsyncTaskQueue()
            await queue.close(worker_count=1)
            item = await queue.get()
            queue.task_done()
            await queue.join()
            return item

        self.assertIsNone(asyncio.run(scenario()))
