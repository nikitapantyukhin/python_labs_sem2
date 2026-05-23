import unittest
from src.queue.core import TaskQueue
from src.sources.generator_source import GeneratorTaskSource
from src.contracts.task import Task

class TestTaskQueue(unittest.TestCase):
    def setUp(self):
        self.source1 = GeneratorTaskSource(2)
        self.source2 = GeneratorTaskSource(3)
        self.queue = TaskQueue([self.source1, self.source2])

    def test_iteration_protocol(self):
        """Проверка протокола итерации и сбора из нескольких источников"""
        tasks = list(self.queue)
        self.assertEqual(len(tasks), 5)
        self.assertIsInstance(tasks[0], Task)

    def test_repeated_iteration(self):
        """Проверка поддержки повторного обхода очереди"""
        run1 = list(self.queue)
        run2 = list(self.queue)
        self.assertEqual(len(run1), 5)
        self.assertEqual(len(run2), 5)

    def test_filter_by_status(self):
        """Проверка ленивой фильтрации по статусу"""
        # Искусственно зададим статус первой задаче для теста
        tasks = list(self.queue)
        tasks[0].status = "In Progress"
        
        # Мокаем источник, чтобы он возвращал наши измененные задачи
        class MockSource:
            def get_tasks(self):
                yield from tasks
                
        test_queue = TaskQueue([MockSource()])
        filtered = list(test_queue.filter_by_status("In Progress"))
        
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].status, "In Progress")