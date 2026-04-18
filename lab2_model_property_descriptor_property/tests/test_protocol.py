import unittest
from src.contracts.source import TaskSource
from src.sources.generator_source import GeneratorTaskSource
from src.sources.json_source import JsonTaskSource

class TestProtocol(unittest.TestCase):
    def test_is_instance_of_protocol(self):
        self.assertTrue(isinstance(GeneratorTaskSource(1), TaskSource))
        self.assertTrue(isinstance(JsonTaskSource("fake.jsonl"), TaskSource))