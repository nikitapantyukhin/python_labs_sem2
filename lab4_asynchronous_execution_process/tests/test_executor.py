import asyncio
import unittest

from src.contracts.handler import TaskHandler
from src.contracts.task import Task
from src.execution.executor import AsyncTaskExecutor
from src.handlers.default import DefaultTaskHandler
from src.handlers.urgent import UrgentTaskHandler


class BrokenHandler:
    def can_handle(self, task: Task) -> bool:
        return True

    async def handle(self, task: Task) -> None:
        raise RuntimeError("processing failed")


class NoopHandler:
    def can_handle(self, task: Task) -> bool:
        return False

    async def handle(self, task: Task) -> None:
        raise AssertionError("Should not be called")


class InvalidHandler:
    pass


class TestAsyncTaskExecutor(unittest.TestCase):
    def test_handler_protocol_runtime_check(self):
        self.assertTrue(isinstance(DefaultTaskHandler(), TaskHandler))
        self.assertFalse(isinstance(InvalidHandler(), TaskHandler))

    def test_processes_tasks_with_matching_handlers(self):
        async def scenario():
            urgent = Task(1, "Urgent", 95)
            regular = Task(2, "Regular", 20)
            urgent_handler = UrgentTaskHandler(delay=0)
            default_handler = DefaultTaskHandler(delay=0)

            async with AsyncTaskExecutor(
                [urgent_handler, default_handler], worker_count=2
            ) as executor:
                report = await executor.run([urgent, regular])

            return report, urgent, regular, urgent_handler, default_handler

        report, urgent, regular, urgent_handler, default_handler = asyncio.run(
            scenario()
        )

        self.assertEqual(report.loaded, 2)
        self.assertEqual(report.processed, 2)
        self.assertEqual(report.failed, 0)
        self.assertEqual(urgent.status, "Done")
        self.assertEqual(regular.status, "Done")
        self.assertEqual(urgent_handler.processed, [1])
        self.assertEqual(default_handler.processed, [2])

    def test_failed_task_is_logged_in_report(self):
        async def scenario():
            task = Task(1, "Broken", 50)

            async with AsyncTaskExecutor([BrokenHandler()], worker_count=1) as executor:
                report = await executor.run([task])

            return report, task

        report, task = asyncio.run(scenario())

        self.assertEqual(report.loaded, 1)
        self.assertEqual(report.processed, 0)
        self.assertEqual(report.failed, 1)
        self.assertEqual(task.status, "Failed")

    def test_task_without_handler_is_skipped(self):
        async def scenario():
            task = Task(1, "No handler", 10)

            async with AsyncTaskExecutor([NoopHandler()], worker_count=1) as executor:
                report = await executor.run([task])

            return report, task

        report, task = asyncio.run(scenario())

        self.assertEqual(report.loaded, 1)
        self.assertEqual(report.processed, 0)
        self.assertEqual(report.skipped, 1)
        self.assertEqual(task.status, "New")

    def test_invalid_handler_fails_fast(self):
        with self.assertRaises(TypeError):
            AsyncTaskExecutor([InvalidHandler()])
