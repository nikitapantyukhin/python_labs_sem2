import unittest
from src.sources.generator_source import GeneratorTaskSource

class TestGenerator(unittest.TestCase):
    def test_generate_count(self):
        count = 5
        source = GeneratorTaskSource(count)
        tasks = list(source.get_tasks())
        self.assertEqual(len(tasks), count)
        for t in tasks:
            self.assertTrue(0 <= t.priority <= 100)