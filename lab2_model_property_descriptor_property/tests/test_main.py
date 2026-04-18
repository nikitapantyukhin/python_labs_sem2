import unittest
from src.main import main

class TestMain(unittest.TestCase):
    def test_main_execution(self):
        try:
            main()
        except Exception as e:
            self.fail(f"main() raised {type(e).__name__} unexpectedly!")