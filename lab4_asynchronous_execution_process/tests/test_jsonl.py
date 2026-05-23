import unittest
import os
from src.sources.json_source import JsonTaskSource

class TestJsonSource(unittest.TestCase):
    def test_read_jsonl(self):
        with open("test_tmp.jsonl", "w") as f:
            f.write('{"id": 10, "description": "Test", "priority": 30}\n')
        
        source = JsonTaskSource("test_tmp.jsonl")
        tasks = list(source.get_tasks())
        self.assertEqual(tasks[0].id, 10)
        self.assertEqual(tasks[0].priority, 30)
        
        os.remove("test_tmp.jsonl")