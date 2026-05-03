import unittest
from src.contracts.task import Task

class TestTask(unittest.TestCase):
    def test_creation(self):
        t = Task(1, "Desc", 50)
        self.assertEqual(t.id, 1)
        self.assertEqual(t.priority, 50)

    def test_priority_validation(self):
        t = Task(1, "Desc", 50)
        with self.assertRaises(ValueError):
            t.priority = 101

    def test_readonly_id(self):
        t = Task(1, "Desc", 50)
        with self.assertRaises(AttributeError):
            t.id = 2