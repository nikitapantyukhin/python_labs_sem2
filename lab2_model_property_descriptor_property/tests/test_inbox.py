import unittest
from src.inbox.core import TaskInbox
from src.sources.generator_source import GeneratorTaskSource

class TestInbox(unittest.TestCase):
    def test_collect_from_multiple(self):
        sources = [GeneratorTaskSource(2), GeneratorTaskSource(3)]
        inbox = TaskInbox(sources)
        tasks = list(inbox.iter_tasks())
        self.assertEqual(len(tasks), 5)